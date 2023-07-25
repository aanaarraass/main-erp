odoo.define('pos_fbr_connector.screens', function(require) {
    "use strict";
    var pos_models = require('point_of_sale.models');
    var web_rpc = require('web.rpc');
    pos_models.load_fields("pos.order", ['invoice_no','is_registered']);
    var pos_s_order = pos_models.Order.prototype;
    pos_models.Order = pos_models.Order.extend({
        initialize: function(attributes, options) {
            pos_s_order.initialize.apply(this, arguments);
            this.invoice_no = false;
            this.is_registered = false
        },
        set_inv_no: function(invoice_no) {
        	this.invoice_no = invoice_no || null;
        },
        get_inv_no: function() {
            return this.invoice_no
        },
        set_is_registered: function(is_registered) {
        	this.is_registered = is_registered || null;
        },
        get_is_registered: function() {
            return this.is_registered
        },
        export_as_JSON: function() {
            var vals = pos_s_order.export_as_JSON.apply(this, arguments);
            vals['invoice_no'] = this.get_inv_no();
            vals['is_registered'] = this.get_is_registered();
            return vals
        },
        export_for_printing: function () {
        var result = pos_s_order.export_for_printing.apply(this, arguments);
        result.invoice_no = this.get_inv_no();
        return result;
    },
    });
});

odoo.define('pos_fbr_connector.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const session = require('web.session');
    var web_rpc = require('web.rpc');
    const fbrPosPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
        constructor() {
            super(...arguments);
            if(this.env.pos.config.allow_fbr_charges){
                var order = this.env.pos.get_order();
                var lines    = order.get_orderlines();
                var i = 0;
                var product = this.env.pos.db.get_product_by_id(this.env.pos.config.service_product_id[0])
                while ( i < lines.length ) {
                    if (lines[i].get_product() === product) {
                        order.remove_orderline(lines[i]);
                    } else {
                        i++;
                    }
                }
                order.add_product(product, { price: product.lst_price });
            }
        }
            async validateOrder(isForceValidate) {
            self = this
            console.log(this.env.pos.get_order());
            if(this.env.pos.config.cash_rounding) {
                if(!this.env.pos.get_order().check_paymentlines_rounding()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Rounding error in payment lines'),
                        body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
                    });
                    return;
                }
            }
            if (await this._isOrderValid(isForceValidate)) {
                var pos_order = this.env.pos.get_order();
                web_rpc.query({
                    model: 'pos.order',
                    method: 'data_to_fbr',
                    args: [[pos_order.uid],[pos_order.export_as_JSON()]],
                })
                .then(function(data){
                	if(data && data[0]){
                		pos_order.set_inv_no(data[0]);
                    	pos_order.set_is_registered(true);
                	}
                	for (let line of self.paymentLines) {
                        if (!line.is_done()) self.currentOrder.remove_paymentline(line);
                    }
                    self._finalizeValidation();
                });

            }
        }
        };

    Registries.Component.extend(PaymentScreen, fbrPosPaymentScreen);

    return PaymentScreen;
});
