/** @odoo-module **/
import { patch } from "@web/core/utils/patch";  
const TableWidget = require("pos_restaurant.TableWidget")

patch(TableWidget.prototype,"point_of_sale.TableWidget",{
    onMounted() {
        const table = this.props.table;
        function unit(val) {
            return `${val}px`;
        } 
        function shadow(color) {
            return '0px 3px 6px ' + color;
        }   
        const style = {
            'box-shadow': shadow(this.props.table.color),
            width: unit(table.width),
            height: unit(table.height),
            'line-height': unit(table.height),
            top: unit(table.position_v),
            left: unit(table.position_h),
            'border-radius': table.shape === 'round' ? unit(1000) : '3px',
        };
        if (table.color) {
            style.background = table.color;
        }
        if (table.height >= 150 && table.width >= 150) {
            style['font-size'] = '32px';
        }
        Object.assign(this.el.style, style);

        const tableCover = this.el.querySelector('.table-cover');
        Object.assign(tableCover.style, { height: `${Math.ceil(this.fill * 100)}%` });
    } 
}); 
 
