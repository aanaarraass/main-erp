/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('wk_pos_invoice_offline.models', function (require) {
    "use strict"
    var models = require('point_of_sale.models');
    var PosDB = require("point_of_sale.DB");
    var SuperPosModel = models.PosModel.prototype;
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');

    PosDB.include({
        init: function(options){
            this._super(options);
            this.offline_invoiced_order = []
        },
    })

    models.PosModel = models.PosModel.extend({
        _save_to_server: function (orders, options) {
            var self = this;
            return SuperPosModel._save_to_server.call(this,orders,options).then(function(return_dict){
                // Download the Order which are Invoiced,
                // If the Download invoice options is enabled in Config.
                if(self.config.invoice_journal_id && self.config.invoice_offline && self.config.download_invoice){
                    // self.db.offline_invoiced_order = []
                    if(self.db.offline_invoiced_order.length){
                        var val = []
                        _.each(self.db.offline_invoiced_order, function(invoice_order_id){
                            _.each(return_dict, function(order_data){
                                if(order_data.pos_reference == invoice_order_id.name){
                                    val.push(order_data.id)
                                }
                            })
                        })

                        if(val.length){
                            var i = 0; 
                            var interval = setInterval(function () { 
                                if (i < val.length) {
                                    self.do_action('account.account_invoices',{ additional_context:{ active_ids: [val[i]] }});
                                } else { 
                                    (interval) 
                                } 
                                i++; 
                            }, 1500) 
                            self.db.offline_invoiced_order = []
                        }
                    }
                }
                return return_dict
            });
        }
    });

    // Inherit PaymentScreen-------------
    const PosResPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen{
            async _finalizeValidation() {
                var self = this;
                if(self.env.pos.config.invoice_journal_id && self.env.pos.config.invoice_offline){
                    if (this.currentOrder.is_paid_with_cash() && this.env.pos.config.iface_cashdrawer) {
                        this.env.pos.proxy.printer.open_cashbox();
                    }
                    this.currentOrder.initialize_validation_date();
                    this.currentOrder.finalized = true;
                    let syncedOrderBackendIds = [];
                    try {
                        if (this.currentOrder.is_to_invoice()) {
                            syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                                this.currentOrder
                            );
                        } else {
                            syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                        }
                    } catch (error) {
                        if (error instanceof Error) {
                            throw error;
                        } else {
                            // await this._handlePushOrderError(error);
                            if (error.message === 'Backend Invoice') {
                                await this.showPopup('ConfirmPopup', {
                                    title: this.env._t('Please print the invoice from the backend'),
                                    body: this.env._t(
                                        'The order has been synchronized earlier. Please make the invoice from the backend for the order: '
                                    ) + error.data.order.name,
                                });
                            } else if (error.code < 0) {
                                // XmlHttpRequest Errors
                                await this.showPopup('OfflineErrorPopup', { 
                                    title:this.env._t('Unable to sync order'),
                                    body: this.env._t(
                                        'Check the internet connection then try to sync again by clicking on the red wifi button (upper right of the screen).'
                                    ),
                                });
                                if(self.env.pos.config.download_invoice && self.currentOrder &&self.currentOrder.is_to_invoice()){
                                    if(self.currentOrder && self.currentOrder.to_invoice){
                                        if(self.env.pos.db.offline_invoiced_order.length){
                                            var exist = false
                                            _.each(self.env.pos.db.offline_invoiced_order, function(order_name){
                                                if(self && self.currentOrder){
                                                    if(order_name.uid == self.currentOrder.uid){
                                                        exist = true
                                                    }
                                                }
                                            })
                                            if(!exist){
                                                self.env.pos.db.offline_invoiced_order.push(self.currentOrder)
                                            }
                                        } else {
                                            self.env.pos.db.offline_invoiced_order.push(self.currentOrder)
                                        }
                                    }
                                }
                            } else if (error.code === 200) {
                                // OpenERP Server Errors
                                await this.showPopup('ErrorTracebackPopup', {
                                    title: error.data.message || this.env._t('Server Error'),
                                    body:
                                        error.data.debug ||
                                        this.env._t('The server encountered an error while receiving your order.'),
                                });
                            } else {
                               var info = await this.showPopup('ErrorPopup', {
                                    title: this.env._t('Unknown Error'),
                                    body: this.env._t(
                                        'The order could not be sent to the server due to an unknown error'
                                    ),
                                });
                                if(self.env.pos.config.download_invoice && self.currentOrder &&self.currentOrder.is_to_invoice()){
                                    if(self.currentOrder && self.currentOrder.to_invoice){
                                        if(self.env.pos.db.offline_invoiced_order.length){
                                            var exist = false
                                            _.each(self.env.pos.db.offline_invoiced_order, function(order_name){
                                                if(self && self.currentOrder){
                                                    if(order_name.uid == self.currentOrder.uid){
                                                        exist = true
                                                    }
                                                }
                                            })
                                            if(!exist){
                                                self.env.pos.db.offline_invoiced_order.push(self.currentOrder)
                                            }
                                        } else {
                                            self.env.pos.db.offline_invoiced_order.push(self.currentOrder)
                                        }
                                    }
                                }
                            }
                        }
                    }

                    if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                        const result = await this._postPushOrderResolve(
                            this.currentOrder, syncedOrderBackendIds
                        );
                        if (!result) {
                            await this.showPopup('ErrorPopup', {
                                title: 'Error: no internet connection.',
                                body: error,
                            });
                        }
                    }
                    this.showScreen(this.nextScreen);
        
                    // If we succeeded in syncing the current order, and
                    // there are still other orders that are left unsynced,
                    // we ask the user if he is willing to wait and sync them.
                    if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                        const { confirmed } = await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Remaining unsynced orders'),
                            body: this.env._t(
                                'There are unsynced orders. Do you want to sync these orders?'
                            ),
                        });
                        if (confirmed) {
                            // NOTE: Not yet sure if this should be awaited or not.
                            // If awaited, some operations like changing screen
                            // might not work.
                            this.env.pos.push_orders();
                        }
                    }
                } else {
                    super._finalizeValidation();
                }
            }
        }
	Registries.Component.extend(PaymentScreen, PosResPaymentScreen);
});
