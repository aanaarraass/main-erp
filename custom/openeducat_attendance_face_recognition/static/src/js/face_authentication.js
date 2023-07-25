odoo.define('openeducat_attendance_face_recognition.face_authentication', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var Session = require('web.session');
    var QWeb = core.qweb;
    var face_control = require('openeducat_attendance_face_recognition.face_control');

    var CamDialog = AbstractAction.extend({
        title: core._t('Face Detection'),
        template: 'WebCamDialog',
        jsLibs: [
            '/openeducat_attendance_face_recognition/static/src/js/lib/webcam.js',
            '/openeducat_attendance_face_recognition/static/src/js/lib/face-api.min.js',
        ],
        events: {
            'click #canvas_back': 'back_sheet',
            'click .o_student_attendance_button_dismiss': 'back_attendance',
        },
        init: function (parent, options) {
            this._super(parent, options);
            options = options || {};
            options.dialogClass = options.dialogClass || '' + ' o_act_window';
            options.size = 'large';
            options.title = _t("Face recognition process");
            this.attendance_id = options.params.attendance_id || options.context.attendance_id;
            this.canvas_done = false;
            this.scan_state = 'attendance';
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.width = document.body.scrollWidth;
                self.height = document.body.scrollHeight;

                Webcam.set({
                    width: self.width,
                    height: self.height,
                    dest_width: self.width,
                    dest_height: self.height,
                    image_format: 'jpeg',
                    jpeg_quality: 90,
                    force_flash: false,
                    fps: 45,
                    swfURL: '/openeducat_attendance_face_recognition/static/src/libs/webcam.swf',
                    constraints: { optional: [{ minWidth: 600 }] }
                });
                Webcam.attach(self.$('#webcam')[0]);
                Webcam.on('live', function (data) {
                    $('video').css('width', '100%');
                    $('video').css('height', '100%');
                    $('#webcam').css('width', '100%');
                    $('#webcam').css('height', '100%');
                    self._setUpModels();
                    self._getdata();
                });
            });
        },

        _setUpModels: async function () {
            await face_control.load_models();
            await this.create_canvas();
        },

        back_sheet: function () {
            $('#webcam').remove();
            $('#canvas_back').hide();
            this.do_action('openeducat_attendance_face_recognition.student_attendance_action_checkin');
            Webcam.reset();

        },

        back_webcam: function () {
            this.do_action('openeducat_attendance_face_recognition.student_attendance_action_webcam');
            Webcam.reset();
        },

        back_attendance: function () {
            var self = this;

            this.do_action({
                type: 'ir.actions.client',
                tag: 'student_attendance_webcam',
                params: {
                    attendance_id: self.attendance_id,
                },
            });
            Webcam.reset();
        },

        _getdata: function () {
            var self = this;
            ajax.jsonRpc('/face-recognition/student/attendance', 'call', {
                params: {}
            }).then(function (result) {
                self.details = result.details;
                self.descriptor_ids = [];
                for (var f32base64 of result.descriptor_ids) {
                    self.descriptor_ids.push(new Float32Array(new Uint8Array([...atob(f32base64)].map(c => c.charCodeAt(0))).buffer))
                }
                self.labels_ids = result.labels_ids;
            });

        },

        _create_attendance: async function (results) {
            var self = this;
            this.student_id = this.details[results['label']]
            var def = this._rpc({
                model: 'op.student',
                method: 'search_read',
                args: [[['id', '=', this.student_id]], ['name']],
            }).then(function (stu_data) {
                self.student_data = stu_data;
                if (self.attendance_id) {
                    var def = self._rpc({
                        model: 'op.attendance.line',
                        method: 'create',
                        args: [{
                            'student_id': self.student_id,
                            'attendance_id': self.attendance_id,
                        }],
                    }).then(function (data) {
                        self.$el.html(QWeb.render("StudentAttendanceMessage", { widget: self.student_data[0] }));
                    });
                }
                return;
            });

        },

        face_detection: async function (video, canvas) {
            var self = this;
            if (this.stop)
                return;
            const displaySize = { width: video.clientWidth, height: video.clientHeight };
            faceapi.matchDimensions(canvas, displaySize);
            const detections = await face_control.getDescriptors(video, null);

            canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
            if (displaySize['width'] > 0) {
                if (detections) {
                    const resizedDetections = faceapi.resizeResults(detections, displaySize);
                    faceapi.draw.drawDetections(canvas, resizedDetections);
                    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

                    const maxDescriptorDistance = 0.5;
                    const labeledDescriptors = await Promise.all(
                        this.labels_ids.map(async (label, i) => {
                            return new faceapi.LabeledFaceDescriptors(label, [this.descriptor_ids[i]])
                        })
                    );
                    if (labeledDescriptors.length > 0) {
                        const faceMatcher = new faceapi.FaceMatcher(labeledDescriptors, maxDescriptorDistance)
                        const results = faceMatcher.findBestMatch(resizedDetections.descriptor);
                        const box = resizedDetections.detection.box;
                        const text = results.toString();
                        const drawBox = new faceapi.draw.DrawBox(box, { label: text });
                        drawBox.draw(canvas);

                        if (results['label'] != 'unknown') {
                            this._create_attendance(results);
                            this.stop = true;
                        }
                    }
                }
            }
            await this.sleep(100);
            this.face_detection(video, canvas);
        },

        sleep: function (ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },

        destroy: function () {
            this._super.apply(this, arguments);
            Webcam.reset();
            this.$el.empty();
        },

        create_canvas: async function () {
            if (!this.canvas_done) {
                this.canvas_done = true;
            } else {
                return;
            }
            const video = $('video')[0];
            if (video) {
                if ($('#webcam').find('canvas').length < 1) {
                    const canvas = faceapi.createCanvasFromMedia(video);
                    $(canvas).css('left', '16px');
                    $(canvas).css('position', 'absolute');
                    $(video).css('float', 'left');
                    let container = $('#webcam');
                    let btn = $('#canvas_back');
                    container.append(canvas);
                    this.face_detection(video, canvas);
                }
            }
            else {
                alert('Canvas not loaded yet')
            }
        },
    });

    core.action_registry.add('student_attendance_webcam', CamDialog);
    return CamDialog;

});
