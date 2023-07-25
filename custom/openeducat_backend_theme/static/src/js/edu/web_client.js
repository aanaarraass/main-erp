/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { useService } from "@web/core/utils/hooks";
import { hasTouch } from "@web/core/browser/feature_detection";
const { HomeMenu } = require('@openeducat_backend_theme/js/edu/home_menu');
const { hooks } = owl;
import { bus } from 'web.core';

export class WebClientTheme extends WebClient {
    setup() {
        super.setup(...arguments);
        this.previous_url = false;
        hooks.onMounted(() => {
            this.env.bus.on("home_menu_toggled", this, (toggle) => {
                this.toggleHomeMenu(toggle)
            });
            bus.on("home_menu_selected", this, (menu) => {
                this.homeMenuSelected(menu)
            });
        });
    }

    toggleHomeMenu(toggle) {
        this.previous_url = $.bbq.getState();
        bus.trigger('set_prev_url', $.bbq.getState());
        this.trigger('do-action', {
            action: 'apps_menu',
            options: {},
        });
    }

    homeMenuSelected(menu) {
        return this.menuService.selectMenu(menu);
    }

    _loadDefaultApp() {
        this.trigger('do-action', {
            action: 'apps_menu',
            options: {},
        });
    }
}
WebClientTheme.components = { ...WebClient.components, HomeMenu };