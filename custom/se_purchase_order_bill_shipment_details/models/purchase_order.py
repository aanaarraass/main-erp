# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    invoiced_amount = fields.Float(String='Billed Amount', compute='_compute_invoice_detail')
    amount_due = fields.Float(String='Amount Due', compute='_compute_invoice_detail')
    paid_amount = fields.Float(String='Paid Amount', compute='_compute_invoice_detail')
    invoiced = fields.Boolean(String='Billed', compute='_compute_invoice_detail', search='_search_invoice_detail')
    invoice_paid = fields.Boolean(String='Paid', compute='_compute_invoice_detail',
                                  search='_search_invoice_paid_detail')

    def _search_invoice_paid_detail(self, operator, value):
        if self.env.context and self.env.context.get('invoice_paid') == False:
            recs = self.search([]).filtered(lambda x: x.invoice_paid is False)
            if recs:
                return [('id', 'in', [x.id for x in recs])]
        recs = self.search([]).filtered(lambda x: x.invoice_paid is True)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    def _search_invoice_detail(self, operator, value):
        if self.env.context and self.env.context.get('invoiced') == False:
            recs = self.search([]).filtered(lambda x: x.invoiced is False)
            if recs:
                return [('id', 'in', [x.id for x in recs])]
        recs = self.search([]).filtered(lambda x: x.invoiced is True)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    # @api.multi
    def _compute_invoice_detail(self):
        inv_obj = self.env['account.move'].sudo()
        for one_so in self:
            one_so.invoiced = False
            one_so.invoice_paid = False
            invoices = inv_obj.search([('invoice_origin', '=', one_so.name), ('state', 'in', ['posted'])])
            invoiced_amount = 0
            amount_due = 0
            for one_invoice in invoices:
                invoiced_amount += one_invoice.amount_total
                amount_due += one_invoice.amount_residual
            one_so.invoiced_amount = invoiced_amount
            one_so.amount_due = amount_due
            one_so.paid_amount = invoiced_amount - amount_due
            if invoices:
                one_so.invoiced = True
            # if inv_obj.search([('origin', '=', one_so.name), ('state', 'in', ['paid'])]):
            #     one_so.invoiced = True
            invoices_delivered = inv_obj.search([('invoice_origin', '=', one_so.name)])
            for one_inv in invoices_delivered:
                if one_inv.payment_state == 'paid':
                    one_so.invoice_paid = True

    delivered = fields.Boolean(String='Received', compute='_compute_delivery_detail', search='_search_delivery_detail')

    def _search_delivery_detail(self, operator, value):
        if self.env.context and self.env.context.get('delivered') == False:
            recs = self.search([]).filtered(lambda x: x.delivered is False)
            if recs:
                return [('id', 'in', [x.id for x in recs])]
        recs = self.search([]).filtered(lambda x: x.delivered is True)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    # @api.multi
    def _compute_delivery_detail(self):
        # picking_obj = self.env['stock.picking'].sudo()
        for one_so in self:
            # pickings = picking_obj.search([('origin', '=', one_so.name), ('state', 'in', ['confirmed', 'assigned', 'waiting', 'done'])])
            pickings = one_so.picking_ids
            if pickings and len(pickings) == 1:
                if pickings.state == 'done':
                    one_so.delivered = True
                else:
                    one_so.delivered = False
            elif not pickings:
                one_so.delivered = False
            else:
                # not_done_pickings = picking_obj.search([('origin', '=', one_so.name), ('state', 'in', ['confirmed', 'assigned', 'waiting'])])
                not_done_pickings = pickings.filtered(lambda pick: pick.state in ['confirmed', 'assigned', 'waiting'])
                if not_done_pickings:
                    one_so.delivered = False
                else:
                    one_so.delivered = True
