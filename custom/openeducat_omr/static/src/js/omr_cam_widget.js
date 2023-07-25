odoo.define("openeducat_omr.omr_cam_widget", function (require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Widget = require("web.Widget");
    var Dialog = require("web.Dialog");
    var ajax = require("web.ajax");
    var widget_registry = require('web.widget_registry');
    var qweb = core.qweb;
    var _t = core._t;


    var OMRCamWidget = Widget.extend({
        tagName: 'button',
        className: 'btn oe_stat_button',

        xmlDependencies: ['/openeducat_omr/static/src/xml/web_widget_image_webcam.xml'],
        jsLibs: [
            '/openeducat_omr/static/src/lib/webcam.js',
        ],
        events: {
            'click': 'web_cam'
        },

        init: function (parent, record) {
            this._super.apply(this, arguments);
            this.record = record;
            console.log(this, 'this')
        },

        start: function () {
            this._super();
            this.$el.text(' OMR Scanner');
            this.$el.prepend('<i class="fa fa-camera o_button_icon"/>');
        },
        sleep: function (ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },

        destroy: function () {
            Webcam.reset();
            this._super.apply(this, arguments);
        },

        remove_image: function () {
            var self = this;
            return this._rpc({
                model: 'op.omr.image',
                method: 'unlink',
                args: [self.image_ids]
            })
        },

        upload_image: function (image) {
            var self = this;
            console.log("iiiiiiiiiiiiiiijhhihoihoih")
            this._rpc({
                model: 'op.omr.image',
                method: 'create',
                args: [{ 'omr_exam_id': this.record.data.id, 'image': image }],
            }).then((res) => {
                console.log(res)
                this.image_ids = res
                console.log(this.image_ids, "fdsfsdgfsgb")
                return res
            })
        },

        prev_image: function () {
            var self = this;
            console.log("In Prev Image Data")
            this._rpc({
                model: 'op.omr.exam',
                method: 'action_prev_omr_sheet',
                args: [this.record.data.id],
            }).then((res) => {
                $("#webcam").addClass("d-none")
                if(this.dialog){
                    var $table = $('<table></table>')
                    var $h1 = $('<h1 style="align:center;">Last Student Record</h1>')
                    Object.entries(res).forEach(([k, v]) => {
                        console.log("The key: ", k)
                        console.log("The value: ", v)
                        var $tr = $('<tr/>');
                        $tr.append($('<td/>',
                            {
                            }).append($('<input/>', {
                                'disabled': 'disabled',
                                'value': k,
                            })));
                        $tr.append($('<td/>',
                            {
                            }).append($('<input/>', {
                                'disabled': 'disabled',
                                'value': v,
                            })));
                        $table.append($tr);
                    });
                    this.$el.append($h1)
                    this.$el.append($table)

                    $('#prev_result').append($h1);
                    $('#prev_result').append($table);
                }

            })
        },

        scan_image: function (image_id) {
            var self = this;
            console.log("SCAN IMAGE function..........")
            return this._rpc({
                model: 'op.omr.exam',
                method: 'action_check_omr_sheet',
                args: [this.record.data.id],
            }).then(function (flag) {
                if (flag == false) {
                    self.displayNotification({message: _t("Not Valid Image..!!!")});
                    self.remove_image()
                } else if (flag == 2) {
                    self.displayNotification({message: _t("Paper Key Not Found..!!!")});
                    self.remove_image()
                } else if (flag == 3) {
                    self.displayNotification({message: _t("Student Id Not Found..!!!")});
                    self.remove_image()
                } else {
                    self.displayNotification({message: _t("Successfully Scanned OMR "+ flag + "..!!!")});
                }
            });
        },

        web_cam: function () {
            console.log("In WEB CAM FUNCTION")
            var image_id
            this.stop = false;
            console.log("On WEBCAM function")
            var self = this;
            var CamDialog = $(qweb.render('CamDialog', {
                widget: this
            }));
            var dialog = new Dialog(self, {
                size: 'large',
                dialogClass: 'o_act_window',
                title: _t("OMR Scanner"),
                $content: CamDialog,

                buttons: [{
                    text: _t("Prev"), classes: 'btn-secondary prev_record_btn',
                    click: function () {
                        Webcam.reset();
                        self.prev_image();
                        $(".prev_record_btn").addClass("d-none")
                    }
                },
                {
                    text: _t("Next"), classes: 'btn-primary take_snap_btn',
                    click: function () {
                        console.log($("#webcam").length)
                        if($("#webcam").hasClass("d-none")){
                        $("#webcam").removeClass("d-none")
                        $("#prev_result").addClass("d-none")
                        console.log("aave 6666")
                        dialog.close();
                        self.web_cam()
                        }
                        else{
                        Webcam.snap(function (data) {
                            self.img_data = data;
                            self.stop = true;
                            Webcam.reset();
                            self.img_data_base64 = self.img_data.split(',')[1];

                            $.when(self.upload_image(self.img_data_base64)).then(function () {
                                setTimeout(() => {
                                    if (self.img_data_base64) {
                                        self.scan_image();
                                    }
                                }, 1000)
                            })
                            dialog.close();

                            self.web_cam()

                        });
                        }
                    }
                },
                {
                    text: _t("Close"),
                    click: function () {
                        Webcam.reset();
                        dialog.close();
                        self.stop = true;
                    }
                }]

            }).open();
            this.dialog = dialog;
            Webcam.set({
                width: 320,
                height: 480,
                dest_width: 320,
                dest_height: 480,
                image_format: 'jpeg',
                jpeg_quality: 90,
                force_flash: false,
                fps: 45,
            });

            Webcam.attach(CamDialog.find('#webcam')[0]),
                Webcam.on('live', function (data) {
                    console.log($('video'), 'video')
                    $('video').css('width', '100%');
                    $('video').css('height', '100%');
                    $('#webcam').css('width', '100%');
                    $('#webcam').css('height', '100%');

                });
            Dialog.include({
                destroy: function () {
                    Webcam.reset();
                    this._super.apply(this, arguments);
                },
            });
        },
    });

    widget_registry.add('omr_cam_widget', OMRCamWidget);
});
