/** @odoo-module **/
import { RtcConfigurationMenu } from '@mail/components/rtc_configuration_menu/rtc_configuration_menu';
import { patch } from 'web.utils';

patch(RtcConfigurationMenu.prototype, "openeducat_live/static/src/js/rtc_configuration_menu.js", {
    _hidescreenshare(e) {
        this.messaging.rtc.currentRtcSession.togglescreen(true)
    },
});