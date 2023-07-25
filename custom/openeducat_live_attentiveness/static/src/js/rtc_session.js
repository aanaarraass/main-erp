/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';
import { clear, insert, insertAndReplace, link, unlink } from '@mail/model/model_field_command';

registerInstancePatchModel('mail.rtc_session', "openeducat_live_attentiveness/static/src/js/rtc_session.js", {
    _created() {
        this._super(...arguments)
        var self = this
        window.addEventListener('blur', function () {
            self.toggleTab(true);
        });
        window.addEventListener('focus', function () {
            self.toggleTab(false);
        });
        document.addEventListener('visibilitychange', function (event) {
            if (document.hidden) {
                self.toggleTab(true);

            } else {
                self.toggleTab(false);

            }
        });
    },
    toggleTab(e) {
        var self = this
        this.updateAndBroadcast({ isAttentiveness: e });
        if (!this.rtc) {
            return;
        }
        if (!this.exists()) {
            return;
        }
        if (e == true) {
            if (self.partner) {
                self.env.services.rpc(
                    {
                        route: '/mail/rtc/session/is-start-time',
                        params: {
                            channel_id: self.channel.id,
                            partner_id: self.partner.id,
                            calendar_id: self.iscalendarid
                        },
                    },
                    { shadow: true }
                ).then(function (res) {
                    self.update({ islogid: res })
                });
            }
        }
        if (e == false) {
            if (self.partner) {
                self.env.services.rpc(
                    {
                        route: '/mail/rtc/session/is-end-time',
                        params: {
                            log_id: self.islogid,
                            channel_id: self.channel.id,
                        },
                    },
                    { shadow: true }
                );
            }
        }
    },
    async toggleHandraised() {
        var self = this
        this._super(...arguments).then(() => {
            if (self.isHandRaised) {
                if (self.partner) {
                    self.env.services.rpc(
                        {
                            route: '/mail/rtc/session/raisedhand',
                            params: {
                                channel_id: self.channel.id,
                                partner_id: self.partner.id,
                                calendar_id: self.iscalendarid
                            },
                        },
                        { shadow: true }
                    );
                }
            }
        })
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
                                is_MeetingLock: this.isMeetingLock,
                                is_Emoji: this.isEmoji,
                                is_Attentiveness: this.isAttentiveness,
                            },
                        },
                    },
                    { shadow: true }
                );
            });
        }, 3000);
    },
    _computenumber() {
        if (!this.rtc) {
            return;
        }
        if (!this.exists()) {
            return;
        }
        if (this.messaging.discuss) {
            if (this.messaging.discuss.threadView) {
                if (this.messaging.discuss.threadView.rtcCallViewer) {
                    if (this.messaging.discuss.threadView.rtcCallViewer.tileParticipantCards) {
                        var guest = []
                        this.messaging.discuss.threadView.rtcCallViewer.tileParticipantCards.forEach(function (value) {
                            if (value.rtcSession) {
                                if (!value.rtcSession.partner) {
                                    guest.push(value.name)
                                }
                            }
                        });
                        this.env.services.rpc(
                            {
                                route: '/mail/rtc/session/add-guest',
                                params: {
                                    guest: guest,
                                    calendar_id: this.iscalendarid
                                },
                            },
                            { shadow: true }
                        )
                        guest = []
                        return guest
                    }
                }
            }
        }
    },
});
registerFieldPatchModel('mail.rtc_session', "openeducat_live_attentiveness/static/src/js/rtc_session.js", {
    isAttentiveness: attr({ default: false }),
    islogid: attr({ default: "" }),
    number: attr({
        compute: '_computenumber',
    }),
});
