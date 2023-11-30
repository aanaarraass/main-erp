# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    inv_status = fields.Selection([('draft', 'Draft'),
                                   ('posted', 'Posted'),
                                   ('paid', 'Paid'),
                                   ('cancel', 'Cancelled'),
                                   ('partial_paid', 'Partial Paid')], string="Invoice State",
                                  compute='calculate_invoice_amount_state', store=True)
    inv_amount_due = fields.Float(string="Amount Due", compute='calculate_invoice_amount_state', store=True)
    inv_amount_paid = fields.Float(string="Amount Paid", compute='calculate_invoice_amount_state', store=True)
    inv_paid_in_per = fields.Float(string="Amount Paid (%)", compute='calculate_invoice_amount_state', store=True)

    @api.depends('invoice_ids', 'invoice_ids.state', 'invoice_ids.amount_residual')
    def calculate_invoice_amount_state(self):
        for order in self:
            amount_due_total = 0
            inv_paid_in_per = 0
            inv_total = 0
            for invoice in order.invoice_ids.filtered(lambda l: l.state != 'cancel'):
                if invoice.state == 'draft':
                    amount_due_total += invoice.amount_total
                else:
                    amount_due_total += invoice.amount_residual
                inv_total += invoice.amount_total
            inv_amount_paid = inv_total - amount_due_total
            if inv_total:
                inv_paid_in_per = (inv_amount_paid * 100) / inv_total
            # Show invoice status
            invoice_status_lst = set(order.invoice_ids.mapped('state'))
            if not invoice_status_lst:
                continue
            do_status = ''
            if 'cancel' in invoice_status_lst and len(set(invoice_status_lst)) != 1:
                invoice_status_lst.remove('cancel')
            if all(l in ('posted', 'draft') for l in invoice_status_lst):
                do_status = 'draft'
            if all(l == 'posted' for l in invoice_status_lst):
                do_status = 'posted'
                if inv_amount_paid > 0:
                    do_status = 'partial_paid'
                if amount_due_total == 0:
                    do_status = 'paid'
            if all(l == 'cancel' for l in invoice_status_lst):
                do_status = 'cancel'
            order.update({'inv_status': do_status,
                          'inv_amount_due': amount_due_total,
                          'inv_amount_paid': inv_amount_paid,
                          'inv_paid_in_per': inv_paid_in_per})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
