odoo.define("openeducat_attendance_face_recognition.cam_widget", function (require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Widget = require("web.Widget");
    var Dialog = require("web.Dialog");
    var ajax = require("web.ajax");
    var widget_registry = require('web.widget_registry');
    var face_control = require("openeducat_attendance_face_recognition.face_control");
    var qweb = core.qweb;
    var _t = core._t;

    var WebcamWidget = Widget.extend({
        tagName: 'button',
        className: 'btn btn oe_stat_button',
        xmlDependencies: ['/openeducat_attendance_face_recognition/static/src/xml/attendance.xml'],
        jsLibs: [
            '/openeducat_attendance_face_recognition/static/src/js/lib/webcam.js',
            '/openeducat_attendance_face_recognition/static/src/js/lib/face-api.min.js',
        ],
        events: {
            'click': 'web_cam'
        },

        init: function (parent, record, state) {
            this._super.apply(this, arguments);
            this.record = record;
            this.scan_state = 'student';
        },

        start: function () {
            this._super();
            this.$el.html('<span>Capture Live Photo</span>');
            this.$el.prepend('<i class="fa fa-fw fa-camera o_button_icon"/>');
        },

        sleep: function (ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },

        destroy: function () {
            Webcam.reset();
            this._super.apply(this, arguments);
        },

        create_canvas: async function () {
            var self = this;
            const video = $('video')[0];
            if (video) {
                const canvas = faceapi.createCanvasFromMedia(video);

                $(canvas).css('left', '16px');
                $(canvas).css('position', 'absolute');
                $(video).css('float', 'left');
                let container = $('#webcam');
                container.append(canvas);

                this.face_detection(video, canvas)
            } else {
                alert('Canvas not loaded yet')
            }
        },

        face_detection: async function (video, canvas) {

            const displaySize = { width: video.clientWidth, height: video.clientHeight };
            faceapi.matchDimensions(canvas, displaySize);
            const detections = await face_control.getDescriptors(video, null);

            if (detections) {
                const resizedDetections = faceapi.resizeResults(detections, displaySize);
                faceapi.draw.drawDetections(canvas, resizedDetections, { withScore: true });
                faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
            }
            if (this.stop)
                return;
            await this.sleep(1000);
            this.face_detection(video, canvas);
        },

        upload_image: function (image) {
            var self = this;
            return this._rpc({
                model: 'op.student',
                method: 'write',
                args: [[this.record.data.id], {
                    ['image_detect']: image,
                }],
            }).then(function () {
                self.generate_descriptor(image, 'image_detect');
            });
        },

        validation: async function (image) {
            var self = this;
            var img = $('<img id="cam_snap">');
            img.attr('src', 'data:image/png;base64,' + image);
            var src = $('#cam_snap').attr('src');
            let red_img = document.querySelector("#red_tick");
            let green_img = document.querySelector("#green_tick");
            const detections = await face_control.getDescriptors(null, img[0]);

            if (detections) {
                if (detections.detection._score > 0.5) {
                    $(green_img).show();
                    self.final_image = img[0].src;
                    $(red_img).hide();
                }
                else {
                    $(green_img).hide();
                    $(red_img).show();
                }
            }
            else {
                $(green_img).hide();
                $(red_img).show();
            }
        },

        write_descriptor: function (data) {
            return this._rpc({
                model: this.record.model,
                method: 'write',
                args: [[this.record.data.id], {
                    ['descriptor']: data,
                }],
            });
        },

        generate_descriptor: async function (image, field) {
            var image = await faceapi.fetchImage(`${window.location.origin}/web/image?model=op.student&field=${field}&id=${this.record.data.id}`);
            const detections = await face_control.getDescriptors(null, image);
            if (detections) {
                var data = face_control._f32base64(detections.descriptor);
                this.write_descriptor(data);
            }
            window.location.reload();
            this.stop = true;
            return;
        },

        web_cam: async function () {
            var self = this;
            this.stop = false;
            await face_control.load_models();
            if (window.location.protocol == "http:") {
                this.displayNotification({
                    title: _t("Protocol"),
                    message: _t("Camera Can Not Be Opened on Http Protocol"),
                    type: 'warning',
                });
                return;
            }
            var CamDialog = $(qweb.render('WebCamDialog', {
                widget: this
            }));
            CamDialog.find(".fa").children('img').hide();

            var dialog = new Dialog(self, {
                size: 'large',
                dialogClass: 'o_act_window',
                title: _t("WebCam Booth"),
                $content: CamDialog,

                buttons: [{
                    text: _t("Take Snapshot"), classes: 'btn-primary take_snap_btn',
                    click: function () {
                        Webcam.snap(function (data) {
                            self.img_data = data;
                            CamDialog.find("#webcam_result").html('<img class="" src="' + self.img_data + '"/>');
                            var img_data_base64 = self.img_data.split(',')[1];
                            self.validation(img_data_base64);
                        });
                    }
                }, {
                    text: _t("Image Descriptor"), classes: 'btn-primary save_close_btn', close: true,
                    click: function () {
                        self.generate_descriptor(null, 'image_1920');
                        Webcam.reset();
                    }
                }, {
                    text: _t("Save & Close"), classes: 'btn-primary save_close_btn', close: true,
                    click: function () {
                        if (self.final_image) {
                            self.final_image = self.final_image.split(',')[1];
                            self.upload_image(self.final_image);
                            Webcam.reset();
                        }
                    }
                }, {
                    text: _t("Close"),
                    click: function () {
                        Webcam.reset();
                        dialog.close();
                        self.stop = true;
                    }
                }]
            }).open();

            Webcam.set({
                width: 640,
                height: 480,
                dest_width: 640,
                dest_height: 480,
                image_format: 'jpeg',
                jpeg_quality: 90,
                force_flash: false,
                fps: 45,
                swfURL: '/openeducat_attendance_face_recognition/static/src/js/webcam.swf',
            });

            Webcam.attach(CamDialog.find('#webcam')[0]),
                Webcam.on('live', function (data) {
                    $('video').css('width', '100%');
                    $('video').css('height', '100%');
                    $('#webcam').css('width', '100%');
                    $('#webcam').css('height', '100%');
                    self.create_canvas();
                });
            Dialog.include({
                destroy: function () {
                    Webcam.reset();
                    this._super.apply(this, arguments);
                },
            });
        },
    });

    widget_registry.add('cam_widget', WebcamWidget);
});
