/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerInstancePatchModel('mail.rtc_session', "openeducat_live_attendance/static/src/js/rtc_session.js", {

    async toggleAttendance() {
        var self = this
        if (!this.rtc) {
            return;
        }
        this.updateAndBroadcast({
            isAttendance: !this.isAttendance,
        });
        self.env.services.rpc(
            {
                route: '/mail/rtc/session/get-registerdata',
            },
            { shadow: true }
        ).then(function (res) {
            self.update({ isregister: res })
        })
    },

});
registerFieldPatchModel('mail.rtc_session', "openeducat_live_attendance/static/src/js/rtc_session.js", {
    isAttendance: attr({ default: false }),
    isregister: attr(),
    issheetid: attr(),
    issheetdata: attr(),
    isonclickradio: attr({ default: false }),
});
