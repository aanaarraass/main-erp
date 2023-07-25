odoo.define('openeducat_attendance_face_recognition.face_mode', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var face_control = require('openeducat_attendance_face_recognition.face_control');

    var AuthMode = AbstractAction.extend({
        title: core._t('Face Detection'),
        template: 'StudentAttendanceSheet',
        events: {
            "click .submit_attendance ": '_onClickSubmit',
        },

        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.action_manager = parent;
        },

        start: function () {
            var self = this;
            self._get_data();
            return this._super.apply(this, arguments);
        },

        _get_data: function () {
            var self = this;
            ajax.jsonRpc('/face-recognition/get/sheetdata', 'call', {
                'value': ''
            }).then(function (result) {
                for (let i = 0; i < result.length; i++) {
                    $('#select_sheet').append($('<option>', {
                        value: result[i]['id'],
                        text: result[i]['name']
                    }));
                }
            });
        },

        _onClickSubmit: function () {
            var self = this;
            if (window.location.protocol == "http:") {
                self.action_manager.notifications.add(
                    _t('Camera Can Not Be Opened on Http Protocol'), {
                    type: 'warning',
                    title: _t("Protocol")
                });
                return;
            }
            var sel_value = parseInt($('#select_sheet :selected').val());
            self.do_action({
                type: 'ir.actions.client',
                tag: 'student_attendance_webcam',
                params: {
                    attendance_id: sel_value,
                },
                attendance_id: sel_value,
            });
        },
    });

    core.action_registry.add('student_attendance_face_mode', AuthMode);
    return AuthMode;

});
