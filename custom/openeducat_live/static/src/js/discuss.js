/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerInstancePatchModel('mail.discuss', "openeducat_live/static/src/js/discuss.js", {
    async onClickStartAMeetingButton(ev) {
        var self = this
        await this._super(...arguments).then(() => {
            self.update({ isstart: true })
            setTimeout(() => {
                self.forceUpdateHost()
                this.env.services.rpc(
                    {
                        route: '/mail/rtc/session/create-password',
                        params: {
                            channel_id: this.thread.id,
                        },
                    },
                    { shadow: true }
                ).then((res) => {
                    if (this.messaging) {
                        if (this.messaging.rtc) {
                            if (this.messaging.rtc.currentRtcSession) {
                                this.messaging.rtc.currentRtcSession.update({ iscreatedpassword: res.password })
                                this.messaging.rtc.currentRtcSession.update({
                                    iscalendarid: res.calendar
                                });
                            }
                        }
                    }
                    if (this.thread) {
                        this.thread.update({ isMeetStart: true })
                    }
                })
            }, 500)
        });
        if (this.isstart) {
            var changeView = setInterval(() => {
                $('.o_DiscussSidebar').addClass('d-none');
                $('.o_ThreadView_channelMemberList').removeClass('d-none');
                $('.o_ChannelMemberList').removeClass('d-none');
                $('#messagelist').removeClass('w-100');
                $('#messagelist').addClass('col-md-3');
                if (!$('#messagelist').hasClass('w-100')) {
                    if ($('#messagelist').hasClass('col-md-3')) {
                        clearInterval(changeView)
                        self.update({ isstart: false })
                    }
                }
            }, 200)
        }
        if (this.threadView) {
            this.threadView.update({ isMemberListOpened: true })
        }
        return window.requestAnimationFrame ||
            window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame ||
            window.oRequestAnimationFrame ||
            window.msRequestAnimationFrame ||
            function (callback) {
                return window.setTimeout(callback, 1000 / 60);
            };
    },

    forceUpdateHost() {
        if (this.messaging && this.messaging.rtc && this.messaging.rtc.currentRtcSession && !this.messaging.rtc.currentRtcSession.isHost) {
            this.messaging.rtc.currentRtcSession.update({
                isHost: true
            });
            return;
        } else {
            setTimeout(this.forceUpdateHost.bind(this), 100);
        }
    }
});
registerFieldPatchModel('mail.discuss', "openeducat_live/static/src/js/discuss.js", {
    isstart: attr({ default: true }),
});