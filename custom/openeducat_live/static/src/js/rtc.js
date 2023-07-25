/** @odoo-module **/
import { registerInstancePatchModel } from '@mail/model/model_core';

registerInstancePatchModel('mail.rtc', "openeducat_live/static/src/js/rtc.js", {
    async toggleScreenDiseble() {
        const isScreenShow = this.currentRtcSession.isScreenShow
        this.currentRtcSession.updateAndBroadcast({ isScreenShow: isScreenShow });
        await this.async(() => this._updateLocalAudioTrackEnabledState());
    },
    async _updateLocalAudioTrackEnabledState(){
        this._super(...arguments)
        await this._notifyPeers(Object.keys(this._peerConnections), {
            event: 'trackChange',
            type: 'peerToPeer',
            payload: {
                type: 'screen',
                state: {
                    isScreenShow: this.currentRtcSession.isScreenShow,
                },
            },
        });
    },
    _handleTrackChange(rtcSession, { type, state }) {
        this._super(...arguments)
        const{ isScreenShow } = state;    
        if (type === 'screen'){
            this.currentRtcSession.update({
                isScreenShow: isScreenShow
            });
        }
    },    
});
