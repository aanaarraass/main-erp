# -*- coding: utf-8 -*-
# Copyright (C) Cybat.

import json
import logging
import traceback
from datetime import timedelta

import psycopg2
import requests

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_id = fields.Char("POSID",required=1)
    auth_header = fields.Char("FBR Header Authorization",required=1)
    post_data = fields.Boolean()
    fbr_url = fields.Char('FBR Url',required=1)
    allow_fbr_charges = fields.Boolean('Allow FBR Charges')
    service_product_id = fields.Many2one('product.product', string='FBR FEE',
                                         domain="[('available_in_pos', '=', True),"
                                                "('sale_ok', '=', True), ('type', '=', 'service'),('is_fbr_fee','=',True)]")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    prod_pct_code = fields.Char("PCT Code", required=True)
    is_fbr_fee = fields.Boolean('Is FBR FEE?')

    @api.constrains('is_fbr_fee')
    def check_is_fbr_fee(self):
        product = self.env['product.template'].search([('is_fbr_fee','=',True)])
        if product.__len__()> 1:
            raise ValidationError('FBR FEE product already exists!')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    invoice_no = fields.Char("FBR Invoice Number")
    response = fields.Text("FBR Response")
    is_registered = fields.Boolean("Post Successfully ?")
    reference = fields.Char(string='Receipt Reference', readonly=True)
    is_returned = fields.Boolean("Is Returned ?")
    return_invoice_number = fields.Char("FBR Return Invoice Number")

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
        print(today, 'currnet time')
        print(previous_time, 'within time')
        if session.config_id.post_data:
            if pos_order :
                try:
                    if pos_order['amount_total']<0:

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

                    header.update({'Authorization': 'Bearer '+session.config_id.auth_header})
                    order_dict.update({'POSID':session.config_id.pos_id})
                    if pos_order.get('partner_id'):
                        partner = self.env['res.partner'].sudo().search([('id','=',pos_order.get('partner_id'))])
                        order_dict.update({
                              "BuyerName": partner.name,
                              "BuyerPhoneNumber": partner.mobile,
                              "BuyerNTN":partner.vat,
                            })
                    items_list = []
                    total_qty = 0.0
                    for line in pos_order.get('lines'):
                        product_dic = line[2]
                        total_qty += product_dic.get('qty')
                        if 'product_id' in product_dic:
                            product = self.env['product.product'].sudo().search([('id','=',product_dic.get('product_id'))])
                            if product:
                                tax_rate = 0.0
                                if product_dic.get('tax_ids'):
                                    for i in product_dic['tax_ids'][0][2]:
                                        tax = self.env['account.tax'].sudo().search([('id','=',i)])
                                        tax_rate+=tax.amount
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
                                        "TaxCharged": round(product_dic.get('price_subtotal_incl') - product_dic.get('price_subtotal'),4),
                                        "InvoiceType": 1,
                                        "RefUSIN": ""
                                    }
                                items_list.append(line_dic)
                    order_dict.update({'Items':items_list,'TotalQuantity':abs(total_qty)})

                    payment_response = requests.post(url,data=json.dumps(order_dict), headers=header, verify=False, timeout=20)
                    r_json=payment_response.json()
                    invoice_no = r_json.get('InvoiceNumber')

                except Exception as e:
                    values = dict(
                                exception=e,
                                traceback=traceback.format_exc(),
                            )

            return [invoice_no]
        return [invoice_no]


    def cron_to_post_data(self):
        pending_orders = self.search([('is_registered','=',False),('invoice','=',False)])
        self.pending_order_post(pending_orders)

    def action_to_post_data_to_fbr(self):
        orders = []
        for order in self:
            if not order.is_registered and not order.invoice_no:
                orders.append(order.id)
        pending_orders = self.browse(orders)
        self.pending_order_post(pending_orders)

    def pending_order_post(self,pending_orders):
        header = {"Content-Type": "application/json"}
        for order in pending_orders:
            try:
                url = order.session_id.config_id.fbr_url
                if order and order.session_id and order.session_id.config_id and order.session_id.config_id.auth_header:
                    header.update({'Authorization': 'Bearer ' + order.session_id.config_id.auth_header})
                    bill_amount = order.amount_total
                    tax_amount = order.amount_tax
                    sale_amount = order.amount_total - order.amount_tax
                    if bill_amount < 0:
                        order_dict = {
                            "InvoiceNumber": "",
                            "POSID": order.session_id.config_id.pos_id,
                            "USIN": "USIN0",
                            "DateTime": order.date_order.strftime("%Y-%m-%d %H:%M:%S"),
                            "TotalBillAmount": abs(bill_amount),
                            "TotalSaleValue": abs(sale_amount),
                            "TotalTaxCharged": abs(tax_amount),
                            "PaymentMode": 1,
                            "InvoiceType": 3,
                        }
                    else:
                        order_dict = {
                            "InvoiceNumber": "",
                            "POSID": order.session_id.config_id.pos_id,
                            "USIN": "USIN0",
                            "DateTime": order.date_order.strftime("%Y-%m-%d %H:%M:%S"),
                            "TotalBillAmount": bill_amount,
                            "TotalSaleValue": sale_amount,
                            "TotalTaxCharged": tax_amount,
                            "PaymentMode": 1,
                            "InvoiceType": 1,
                        }
                    if order.partner_id:
                        order_dict.update({
                            "BuyerName": order.partner_id.name,
                            "BuyerPhoneNumber": order.partner_id.mobile,
                            "BuyerNTN": order.partner_id.vat,
                        })
                    if order.lines:
                        items_list = []
                        total_qty = 0.0
                        for line in order.lines:
                            if line.product_id:
                                tax_rate = 0.0
                                if line.tax_ids_after_fiscal_position:
                                    for tax in line.tax_ids_after_fiscal_position:
                                        tax_rate += tax.amount
                                total_qty += line.qty
                                if line.price_subtotal < 0:
                                    line_dic = {
                                        "ItemCode": line.product_id.default_code,
                                        "ItemName": line.product_id.name,
                                        "Quantity": abs(line.qty),
                                        "PCTCode": line.product_id.prod_pct_code,
                                        "TaxRate": tax_rate,
                                        "SaleValue": abs(line.price_unit),
                                        "TotalAmount": abs(line.price_subtotal),
                                        "TaxCharged": abs(line.price_subtotal_incl) - abs(line.price_subtotal),
                                        "InvoiceType": 3,
                                        "RefUSIN": ""
                                    }
                                else:
                                    line_dic = {
                                        "ItemCode": line.product_id.default_code,
                                        "ItemName": line.product_id.name,
                                        "Quantity": line.qty,
                                        "PCTCode": line.product_id.prod_pct_code,
                                        "TaxRate": tax_rate,
                                        "SaleValue": line.price_unit,
                                        "TotalAmount": line.price_subtotal,
                                        "TaxCharged": line.price_subtotal_incl - line.price_subtotal,
                                        "InvoiceType": 1,
                                        "RefUSIN": ""
                                    }
                                items_list.append(line_dic)
                        order_dict.update({
                            "Items": items_list,
                            'TotalQuantity': abs(total_qty)
                        })
                    payment_response = requests.post(url, data=json.dumps(order_dict), headers=header, verify=False,
                                                     timeout=20)
                    r_json = payment_response.json()
                    invoice_no = r_json.get('InvoiceNumber')
                    order.sudo().write({'response': r_json, 'is_registered': True, 'invoice_no': invoice_no})

            except Exception as e:
                values = dict(
                    exception=e,
                    traceback=traceback.format_exc(),
                )
                order.write({'response': values})


    def return_order_to_fbr_action(self):
        header = {"Content-Type": "application/json"}
        for order in self:
            fbr_url = order.session_id.config_id.fbr_url
            if order.is_registered and order.invoice_no:
                if not order.is_returned and not order.return_invoice_number:
                    try:
                        if order and order.session_id and order.session_id.config_id and order.session_id.config_id.auth_header:
                            header.update({'Authorization': 'Bearer ' + order.session_id.config_id.auth_header})
                            bill_amount = order.amount_total
                            tax_amount = order.amount_tax
                            sale_amount = order.amount_total - order.amount_tax
                            order_dict = {
                                "InvoiceNumber": "",
                                "POSID": order.session_id.config_id.pos_id,
                                "USIN": order.name,
                                "DateTime": order.date_order.strftime("%Y-%m-%d %H:%M:%S"),
                                "TotalBillAmount": abs(bill_amount),
                                "TotalSaleValue": abs(sale_amount),
                                "TotalTaxCharged": abs(tax_amount),
                                "PaymentMode": 1,
                                "InvoiceType": 3,
                            }
                            if order.partner_id:
                                order_dict.update({
                                    "BuyerName": order.partner_id.name,
                                    "BuyerPhoneNumber": order.partner_id.mobile,
                                    "BuyerNTN": order.partner_id.vat,
                                })
                            if order.lines:
                                items_list = []
                                total_qty = 0.0
                                for line in order.lines:
                                    tax_rate = 0.0
                                    if line.tax_ids_after_fiscal_position:
                                        for i in line.tax_ids_after_fiscal_position:
                                            tax = self.env['account.tax'].sudo().search([('id', '=', i.id)])
                                            tax_rate += tax.amount
                                    total_qty += line.qty
                                    line_dic = {
                                        "ItemCode": line.product_id.default_code,
                                        "ItemName": line.product_id.name,
                                        "Quantity": line.qty,
                                        "PCTCode": line.product_id.prod_pct_code,
                                        "TaxRate": tax_rate,
                                        "SaleValue": line.price_unit,
                                        "TotalAmount": line.price_subtotal,
                                        "TaxCharged": line.price_subtotal_incl - line.price_subtotal,
                                        "InvoiceType": 3,
                                        "RefUSIN": ""
                                    }
                                    items_list.append(line_dic)
                                order_dict.update({
                                    "Items": items_list, 'TotalQuantity': total_qty
                                })
                            payment_response = requests.post(fbr_url, data=json.dumps(order_dict), headers=header, verify=False,
                                                             timeout=50)
                            r_json = payment_response.json()
                            _logger.info(payment_response.text)
                            invoice_no = r_json.get('InvoiceNumber')

                            order.sudo().write({'return_invoice_number': invoice_no,'is_returned':True})
                            return
                    except Exception as e:
                        _logger.info(e)
                        raise ValidationError(e)
                raise ValidationError('This order is already returned to FBR.')
            else:
                raise ValidationError('This order '+order.name+' is not posted yet to FBR.')


    @api.model
    def _order_fields(self, order):
        res = super(PosOrder, self)._order_fields(order)
        res['invoice_no'] = order.get('invoice_no', False)
        res['is_registered'] = order.get('is_registered', False)
        return res


