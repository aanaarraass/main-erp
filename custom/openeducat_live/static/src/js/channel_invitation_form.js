/** @odoo-module **/
import { registerInstancePatchModel } from '@mail/model/model_core';

registerInstancePatchModel('mail.channel_invitation_form', "openeducat_live/static/src/js/channel_invitation_form.js", {
    _created() {
        this._super(...arguments)
        this._password = this._password.bind(this);
    },
    _password(e){
        this.messaging.rtc.currentRtcSession.togglepassword()
        this.env.services.rpc(
            {
                route: '/mail/rtc/session/get-password',
                params: {
                    channel_id : this.thread.id,
                },
            },
            { shadow: true }
        ).then((res)=> {
            if (this.messaging) {
                if (this.messaging.rtc) {
                    if (this.messaging.rtc.currentRtcSession) {
                        this.messaging.rtc.currentRtcSession.update({iscreatedpassword:res})
                    }
                }
            }
        })
    },

});
