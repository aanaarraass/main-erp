/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerInstancePatchModel('mail.rtc_controller', "openeducat_live_attentiveness/static/src/js/rtc_controller.js", {
    _created() {
        this._super(...arguments)
        this.onClickToggleAudioCall = this.onClickToggleAudioCall.bind(this);

    },
    async onClickToggleAudioCall(ev) {
        this._super(...arguments)
        if (this.messaging) {
            if (this.messaging.rtc) {
                if (this.messaging.rtc.currentRtcSession) {
                    this.env.services.rpc(
                        {
                            route: '/mail/rtc/session/start-end-meeting',
                            params: {
                                channel_id: this.messaging.rtc.currentRtcSession.channel.id,
                                meeting: 'end',
                                host: this.messaging.rtc.currentRtcSession.isHost
                            },
                        },
                        { shadow: true }
                    )
                }
            }
        }
    },
});
