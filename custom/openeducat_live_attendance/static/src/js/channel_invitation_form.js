/** @odoo-module **/
import { registerInstancePatchModel } from '@mail/model/model_core';

registerInstancePatchModel('mail.channel_invitation_form', "openeducat_live_attendance/static/src/js/channel_invitation_form.js", {
    _created() {
        this._super(...arguments)
        this._attendance = this._attendance.bind(this);
        this.onclickSave = this.onclickSave.bind(this);
        this.onclickregister = this.onclickregister.bind(this);
        this.updateshhetdata = this.updateshhetdata.bind(this);
    },
    _attendance(e) {
        this.messaging.rtc.currentRtcSession.toggleAttendance()
        setTimeout(() => {
            var regitervalue = document.getElementById("Registermember").value
            if (regitervalue) {
                this.updateshhetdata(regitervalue)
            }
        }, 100);
    },
    onclickregister() {
        var self = this
        var regitervalue = document.getElementById("Registermember").value
        this.updateshhetdata(regitervalue)
    },
    updateshhetdata(regitervalue) {
        var self = this
        this.env.services.rpc(
            {
                route: '/mail/rtc/session/get-sheetdata',
                params: {
                    values: {
                        "registerid": regitervalue
                    },
                },
            },
            { shadow: true }
        ).then(function (res) {
            self.messaging.rtc.currentRtcSession.update({ issheetdata: res })
        })
    },
    onclickSave(e) {
        var self = this
        var regitervalue = document.getElementById("Registermember").value
        if (document.getElementById("sheetdata").value) {
            var sheetvalue = document.getElementById("sheetdata").value
            self.messaging.rtc.currentRtcSession.update({ issheetid: parseInt(sheetvalue) })
            this.env.services.rpc(
                {
                    route: '/mail/rtc/session/add-sheetid',
                    params: {
                        channel_id: this.thread.id,
                        values: {
                            "sheetid": parseInt(sheetvalue)
                        },
                    },
                },
                { shadow: true }
            );
        }
        this.messaging.rtc.currentRtcSession.update({ isAttendance: false, isonclickradio: false })
        this.delete();
    }
});
