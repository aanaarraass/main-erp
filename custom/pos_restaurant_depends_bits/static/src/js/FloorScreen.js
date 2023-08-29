/** @odoo-module **/
import { patch } from "@web/core/utils/patch";  
const FloorScreen = require("pos_restaurant.FloorScreen");

patch(FloorScreen.prototype,'pos_restaurant.FloorScreen',{
    onPatched() { 
        var img = '/web/image/pos.config/'+String(this.env.pos.config_id)+'/floor_Background'
        this.floorMapRef.el.style.background = 'url('+img+')';
        this.state.floorMapScrollTop = this.floorMapRef.el.getBoundingClientRect().top;
    }
});