/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerInstancePatchModel('mail.rtc_session', "openeducat_live/static/src/js/rtc_session.js", {
    _created() {
        this._super(...arguments)
        this.selectemoji = this.selectemoji.bind(this);
        if (this.channel) {
            this.env.services.rpc(
                {
                    route: '/mail/rtc/session/get-password',
                    params: {
                        channel_id: this.channel.id,
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
        }
    },
    async togglescreen(e) {
        if (!this.rtc) {
            return;
        }
        this.updateAndBroadcast({
            isScreenShow: !this.isScreenShow,
        });
        for (const session of this.messaging.models['mail.rtc_session'].all()) {
            if (!session.audioElement) {
                continue;
            }
            session.audioElement.isScreenShow = this.isScreenShow;
        }
        if (this.channel.rtc) {
            await this.async(() => this.channel.rtc.toggleScreenDiseble());
        }
    },
    async toggleHandraised(e) {
        if (!this.rtc) {
            return;
        }
        this.updateAndBroadcast({
            isHandRaised: !this.isHandRaised,
        });
    },
    
    async togglepassword(e) {
        if (!this.rtc) {
            return;
        }
        this.updateAndBroadcast({
            isPassword: !this.isPassword,
            is_lockpassword: !this.is_lockpassword,
        });
        this.env.services.rpc(
            {
                route: '/mail/rtc/session/lock-password',
                params: {
                    channel_id: this.channel.id,
                    values: {
                        is_lockpassword: this.isPassword,
                    },
                },
            },
            { shadow: true }
        )
    },
    async toggleEmoji(e) {
        this.update({ isEmoji: e })
        this.updateAndBroadcast({
            isEmoji: e,
            isFeedbackEmoji: e,
        });
    },
    async toggleMeeting(e) {
        if (!this.rtc) {
            return;
        }
        this.update({
            isMeetingLock: !this.isMeetingLock,

        });
        this.env.services.rpc(
            {
                route: '/mail/rtc/session/lock-meeting',
                params: {
                    channel_id: this.channel.id,
                    values: {
                        is_lockmeet: this.isMeetingLock,
                    },
                },
            },
            { shadow: true }
        )
    },
    async selectemoji(member, as){
        this.env.services.rpc(
            {
                route: '/mail/rtc/session/update-and-emoji',
                params: {
                    session_id: member.rtcSession.id,
                    values: {
                        is_badgeemoji: as.detail.unicode,
                    },
                },
            },
            { shadow: true }
        );
    },

    updateAndBroadcast(data) {
        if (!this.rtc) {
            return;
        }
        this.update(data);
        this._debounce(async () => {
            if (!this.exists()) {
                return;
            }
            await this.async(() => {
                this.env.services.rpc(
                    {
                        route: '/mail/rtc/session/update_and_broadcast',
                        params: {
                            session_id: this.id,
                            values: {
                                is_camera_on: this.isCameraOn,
                                is_deaf: this.isDeaf,
                                is_muted: this.isMuted,
                                is_screen_sharing_on: this.isScreenSharingOn,
                                is_screen_show: this.isScreenShow,
                                is_hand_raised: this.isHandRaised,
                                is_host: this.isHost,
                                is_Emoji: this.isEmoji,
                            },
                        },
                    },
                    { shadow: true }
                );
            });
        }, 3000);
    },
});
registerFieldPatchModel('mail.rtc_session', "openeducat_live/static/src/js/rtc_session.js", {
    isScreenShow: attr({ default: true }),
    isMeetingLock: attr({ default: false }),
    isHandRaised: attr({ default: false }),
    isPassword: attr({ default: true }),
    isbadgeemoji: attr(),
    iscreatedpassword: attr(),
    isEmoji: attr(),
    isFeedbackEmoji: attr(),
    isHost: attr({ default: false }),
    is_lockpassword: attr({ default: true }),
    iscalendarid: attr({ default: "" }),
});
