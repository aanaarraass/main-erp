/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerInstancePatchModel('mail.thread', "openeducat_live/static/src/js/thread.js", {
    async toggleCall(options) {
        setTimeout(() => {
            if (this.messaging.currentPartner) {
                this.env.services.rpc(
                    {
                        route: '/mail/rtc/session/temp-host',
                        params: {
                            channel_id: this.id,
                            partner: this.messaging.currentPartner.id
                        },
                    },
                    { shadow: true }
                ).then((res) => {
                    if (res) {
                        if (this.messaging.rtc) {
                            if (this.messaging.rtc.currentRtcSession) {
                                this.messaging.rtc.currentRtcSession.update({ isHost: res })
                            }
                        }
                    }
                })
            }
            else {
                if (this.messaging.rtc) {
                    if (this.messaging.rtc.currentRtcSession) {
                        this.messaging.rtc.currentRtcSession.update({ isHost: false })
                    }
                }
            }
        }, 300);
        if (this.messaging.rtc.channel) {
            $('.o_ChannelMemberList').addClass('d-none');
            $('#messagelist').addClass('w-100');
        }
        else {
            $('.o_ChannelMemberList').removeClass('d-none');
            $('#messagelist').removeClass('w-100');
        }
        await this._super(...arguments)
    },
    async open({ expanded = false, focus } = {}) {
        const discuss = this.messaging.discuss;
        // check if thread must be opened in discuss
        const device = this.messaging.device;
        if (
            (!device.isMobile && (discuss.isOpen || expanded)) ||
            this.model === 'mail.box'
        ) {
            if (this.rtc) {
                $('.o_ChannelMemberList').removeClass('d-none');
                $('#messagelist').removeClass('w-100');
            }
            else {
                $('.o_ChannelMemberList').addClass('d-none');
                $('#messagelist').addClass('w-100');
            }
        }
        await this._super(...arguments)
    }
});
registerFieldPatchModel('mail.thread', "openeducat_live/static/src/js/thread.js", {
    isMeetStart: attr({ default: false }),
    isDisplayList: attr({ default: true }),
});