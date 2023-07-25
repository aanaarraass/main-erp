# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
import json
import logging
import traceback

import psycopg2
import requests

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, values):
        session = self.env['pos.session'].browse(values['session_id'])
        values = self._complete_values_from_session(session, values)
        res =  super(PosOrder, self).create(values)
        self.env['custom.pos.order'].create({'pos_id':res.id})
        return res

    def data_to_fbr(self, pos_order):
        pos_order = pos_order[0]
        session = self.env['pos.session'].sudo().search([('id', '=', pos_order.get('pos_session_id'))])
        url = session.config_id.fbr_url
        header = {"Content-Type": "application/json"}
        invoice_no = ''
        config_time = self.env['pos.config'].sudo().search([])
        time_float = config_time.time_settlement
        today = fields.Datetime.now()
        previous_time = today + timedelta(hours=-time_float)
        existing_invoice = ''
        if session.config_id.post_data:
            if pos_order:
                try:
                    if pos_order['amount_total'] < 0:

                        order_dict = {
                            "InvoiceNumber": "",
                            "USIN": "USIN0",
                            "DateTime": fields.Datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "TotalBillAmount": abs(pos_order.get('amount_total')),
                            "TotalSaleValue": abs(pos_order.get('amount_total')) - abs(pos_order.get('amount_tax')),
                            "TotalTaxCharged": abs(pos_order.get('amount_tax')),
                            "PaymentMode": 1,
                            "InvoiceType": 3,
                        }
                    else:
                        order_dict = {
                            "InvoiceNumber": "",
                            "USIN": "USIN0",
                            "DateTime": fields.Datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "TotalBillAmount": pos_order.get('amount_total'),
                            "TotalSaleValue": pos_order.get('amount_total') - pos_order.get('amount_tax'),
                            "TotalTaxCharged": pos_order.get('amount_tax'),
                            "PaymentMode": 1,
                            "InvoiceType": 1,
                        }

                    header.update({'Authorization': 'Bearer ' + session.config_id.auth_header})
                    order_dict.update({'POSID': session.config_id.pos_id})
                    if pos_order.get('partner_id'):
                        partner = self.env['res.partner'].sudo().search([('id', '=', pos_order.get('partner_id'))])
                        order_dict.update({
                            "BuyerName": partner.name,
                            "BuyerPhoneNumber": partner.mobile,
                            "BuyerNTN": partner.vat,
                        })
                    items_list = []
                    total_qty = 0.0

                    same_order_intime = self.env['pos.order'].sudo().search([
                        ('amount_total', '=', pos_order.get('amount_total')),
                        ('date_order', '>=', previous_time)
                    ])
                    if same_order_intime:
                        print(same_order_intime, 'same order within time')
                        for rec in same_order_intime:
                            print(rec.invoice_no, 'same invoice_no ')
                            for line in pos_order.get('lines'):
                                product_dic = line[2]
                                same_order = self.env['pos.order.line'].sudo().search([
                                    ('product_id', '=', product_dic.get('product_id')),
                                    ('qty', '=', product_dic.get('qty')),
                                    ('price_unit', '=', product_dic.get('price_unit')),
                                ])
                                if same_order:
                                    if rec.invoice_no:
                                        return [rec.invoice_no]

                    for line in pos_order.get('lines'):
                        product_dic = line[2]
                        total_qty += product_dic.get('qty')
                        if 'product_id' in product_dic:
                            product = self.env['product.product'].sudo().search(
                                [('id', '=', product_dic.get('product_id'))])
                            if product:
                                tax_rate = 0.0
                                if product_dic.get('tax_ids'):
                                    for i in product_dic['tax_ids'][0][2]:
                                        tax = self.env['account.tax'].sudo().search([('id', '=', i)])
                                        tax_rate += tax.amount
                                if product_dic['price_subtotal'] < 0:
                                    line_dic = {
                                        "ItemCode": product.default_code,
                                        "ItemName": product.name,
                                        "Quantity": abs(product_dic.get('qty')),
                                        "PCTCode": product.prod_pct_code,
                                        "TaxRate": tax_rate,
                                        "SaleValue": abs(product_dic.get('price_unit')),
                                        "TotalAmount": abs(product_dic.get('price_subtotal')),
                                        "TaxCharged": abs(product_dic.get('price_subtotal_incl')) - abs(product_dic.get(
                                            'price_subtotal')),
                                        "InvoiceType": 3,
                                        "RefUSIN": ""
                                    }
                                else:
                                    line_dic = {
                                        "ItemCode": product.default_code,
                                        "ItemName": product.name,
                                        "Quantity": product_dic.get('qty'),
                                        "PCTCode": product.prod_pct_code,
                                        "TaxRate": tax_rate,
                                        "SaleValue": product_dic.get('price_unit'),
                                        "TotalAmount": product_dic.get('price_subtotal'),
                                        "TaxCharged": round(
                                            product_dic.get('price_subtotal_incl') - product_dic.get('price_subtotal'),
                                            4),
                                        "InvoiceType": 1,
                                        "RefUSIN": ""
                                    }
                                items_list.append(line_dic)
                    order_dict.update({'Items': items_list, 'TotalQuantity': abs(total_qty)})

                    payment_response = requests.post(url, data=json.dumps(order_dict), headers=header, verify=False,
                                                     timeout=20)
                    r_json = payment_response.json()
                    invoice_no = r_json.get('InvoiceNumber')
                    # invoice_no = 'zeebee234'

                except Exception as e:
                    values = dict(
                        exception=e,
                        traceback=traceback.format_exc(),
                    )

            return [invoice_no]
        return [invoice_no]


class CustomPosOrder(models.Model):
    _name = 'custom.pos.order'
    _inherits = {'pos.order': 'pos_id'}
    _description = 'custom_pos_order.custom_pos_order'

    pos_id = fields.Many2one('pos.order', string='POS id', auto_join=True, index=True, ondelete='cascade')
    # name = fields.Char()
