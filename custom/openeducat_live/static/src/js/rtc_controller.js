/** @odoo-module **/
import { registerInstancePatchModel,registerFieldPatchModel} from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerInstancePatchModel('mail.rtc_controller', "openeducat_live/static/src/js/rtc_controller.js", {
    _created() {
        this._super(...arguments)
        this.onClickRiseHand = this.onClickRiseHand.bind(this);
        this._onEmojiSelections = this._onEmojiSelections.bind(this);
        this.onClicklockMeeting = this.onClicklockMeeting.bind(this);
    },

    async onClickRiseHand(ev) {
        await this.messaging.rtc.currentRtcSession.toggleHandraised();
        this.update({isRaiseHandMessege:!this.isRaiseHandMessege})
    },
    async onClicklockMeeting(ev) {
        await this.messaging.rtc.currentRtcSession.toggleMeeting();
       
    },
    async _onEmojiSelections(ev) {
        await this.messaging.rtc.currentRtcSession.toggleEmoji(ev.detail.unicode);
    },
});
registerFieldPatchModel('mail.rtc_controller', "openeducat_live/static/src/js/rtc_controller.js", {
    isRaiseHandMessege:attr({ default:true}),
});
