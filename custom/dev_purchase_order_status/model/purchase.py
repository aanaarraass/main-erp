# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################

from odoo import api, fields, models, _

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def write(self, values):
        result = super(PurchaseOrderLine, self).write(values)
        status = ''
        if values.get('qty_received_manual'):
            service_lines = self.order_id.order_line.filtered(lambda x:x.product_id.type=='service')
            for service_line in service_lines:
                if service_line.product_qty==service_line.qty_received:
                    status = 'ship_status'
                else:
                    status = ''
            rest_lines = self.order_id.order_line - service_lines
            for l in rest_lines:
                if l.product_uom_qty==l.qty_received:
                    status = 'ship_status'
                else:
                    status = ''
            if status!='':
                self.order_id.temp_ship_status = True
        return result

class purchase_order(models.Model):
    _inherit = "purchase.order"
    temp_ship_status = fields.Boolean(copy=False, store=True)
#    check partial paid flag after complet
    
    def _compute_invoiced(self):
        for purchase in self:
            invoice_partial_flag = False
            invoice_status_new_flag = False
            if purchase.invoice_ids:
                a=0
                inv_len = len(purchase.invoice_ids)
                for invoice in purchase.invoice_ids:
                    if invoice.payment_state == 'paid':
                        a += 1
                if inv_len == a:
                    invoice_status_new_flag = True
                else:
                    count = 0
                    for invoice in purchase.invoice_ids:
                        if invoice.state == 'posted' and invoice.amount_residual < invoice.amount_total: 
                            invoice_partial_flag = True
            purchase.invoice_partial = invoice_partial_flag
            purchase.temp_invoice_partial = invoice_partial_flag
            purchase.invoice_status_new = invoice_status_new_flag
            purchase.temp_invoice_status_new = invoice_status_new_flag

    def _compute_invoiced_open(self):
        for purchase in self:
            purchase.invoice_open = False
            if purchase.invoice_ids:
                a=0
                inv_len = len(purchase.invoice_ids)
                for invoice in purchase.invoice_ids:
                    if invoice.state == 'draft':
                        a += 1
                if inv_len == a:
                    purchase.invoice_open = True
#                    
#                
    def _compute_shiped(self):
        for purchase in self:
            ship_status_flag = False
            ship_partial_flag = False
            if purchase.temp_ship_status:
                ship_status_flag = True
            else:
                ship_status_flag = False
            if purchase.picking_ids:
                a=0
                picking_len = len(purchase.picking_ids)
                for picking in purchase.picking_ids:
                    if picking.state == 'done':
                        a += 1
                if picking_len == a:
                    service_lines = purchase.order_line.filtered(
                        lambda x: x.product_id.type == 'service' and x.product_uom_qty != x.qty_received)
                    if service_lines:
                        ship_partial_flag = True
                        ship_status_flag = False
                    else:
                        ship_status_flag = True
                if a != 0 and not picking_len == a:
                    ship_partial_flag = True
            purchase.ship_status = ship_status_flag
            purchase.temp_ship_status = ship_status_flag
            purchase.ship_partial = ship_partial_flag
            purchase.temp_ship_partial = ship_partial_flag

    invoice_open = fields.Boolean(string='Invoiced', compute='_compute_invoiced_open',search='_search_open_invoice')
    invoice_status_new = fields.Boolean(string='Paid', compute='_compute_invoiced', search='_search_full_paid_invoice')
    temp_invoice_status_new = fields.Boolean(string='Paid', store=True, copy=False)
    invoice_partial = fields.Boolean(string='Partial Paid', compute='_compute_invoiced', search='_search_partial_paid_invoice',copy=False)
    temp_invoice_partial = fields.Boolean(string='Partial Paid', copy=False, store=True)
    ship_status = fields.Boolean(string='Received',compute='_compute_shiped',copy=False, search='_search_full_shipment')
    ship_partial = fields.Boolean(string='Partial Received',compute='_compute_shiped',copy=False, search='_search_partial_shipment')
    temp_ship_partial = fields.Boolean(string='Partial Delivered', copy=False, store=True)
    not_ship_status = fields.Boolean(string='Not Received', compute='_compute_not_shiped', copy=False,
                                     search='_search_full_shipment')
    not_temp_ship_status = fields.Boolean(copy=False, store=True)
    not_paid_status = fields.Boolean(string='Not Paid', compute='_compute_not_shiped', copy=False,
                                     search='_search_full_shipment')
    not_temp_paid_status = fields.Boolean(copy=False, store=True)

    def _compute_not_shiped(self):
        for order in self:
            order.not_ship_status = True
            order.not_temp_ship_status = True
            order.not_paid_status = True
            order.not_temp_paid_status = True
            for inv in order.invoice_ids:
                if inv.payment_state != 'not_paid':
                    order.not_paid_status = False
                    order.not_temp_paid_status = False
            for line in order.order_line:
                if line.qty_received > 0:
                    order.not_ship_status = False
                    order.not_temp_ship_status = False
    
    def _search_full_shipment(self, operator, value):
        purchase_order = self.env['purchase.order'].search([])
        purchase_ids = []
        for purchase in purchase_order:
            if operator == '=':
                if purchase.picking_ids:
                    a=0
                    picking_len = len(purchase.picking_ids)
                    for picking in purchase.picking_ids:
                        if picking.state == 'done':
                            a += 1
                    if picking_len == a:
                        purchase_ids.append(purchase.id)
            else:
                if purchase.picking_ids:
                    a=0
                    picking_len = len(purchase.picking_ids)
                    for picking in purchase.picking_ids:
                        if picking.state != 'done':
                            a += 1
                    if picking_len == a:
                        purchase_ids.append(purchase.id)
                if not purchase.picking_ids:
                    purchase_ids.append(purchase.id)
        return [('id', 'in', purchase_ids)]
        
    def _search_partial_shipment(self, operator, value):
        purchase_order = self.env['purchase.order'].search([])
        purchase_ids = []
        for purchase in purchase_order:
            if operator == '=':
                if purchase.picking_ids:
                    a=0
                    picking_len = len(purchase.picking_ids)
                    for picking in purchase.picking_ids:
                        if picking.state == 'done':
                            a += 1
                    if a != 0 and picking_len != a:
                        purchase_ids.append(purchase.id)
            else:
                if purchase.picking_ids:
                    a=0
                    picking_len = len(purchase.picking_ids)
                    for picking in purchase.picking_ids:
                        if picking.state != 'done':
                            a += 1
                    if picking_len == a:
                        purchase_ids.append(purchase.id)
                if not purchase.picking_ids:
                    purchase_ids.append(purchase.id)
    
        return [('id', 'in', purchase_ids)]
#        
#        
#    
    def _search_partial_paid_invoice(self, operator, value):
        purchase_order = self.env['purchase.order'].search([])
        purchase_ids = []
        for purchase in purchase_order:
            if operator == '=':
                if purchase.invoice_ids:
                    a=0
                    inv_len = len(purchase.invoice_ids)
                    for invoice in purchase.invoice_ids:
                        if invoice.state == 'posted' and invoice.payment_state != 'paid' and invoice.amount_residual < invoice.amount_total:
                            a += 1
                    if a != 0:
                        purchase_ids.append(purchase.id)
            else:
                if purchase.invoice_ids:
                    a=0
                    for invoice in purchase.invoice_ids:
                        if invoice.state != 'posted':
                            purchase_ids.append(purchase.id)
                if not purchase.invoice_ids:
                    purchase_ids.append(purchase.id)
                
        return [('id', 'in', purchase_ids)]
#        
#        
    def _search_full_paid_invoice(self, operator, value):
        purchase_order = self.env['purchase.order'].search([])
        purchase_ids = []
        for purchase in purchase_order:
            if operator == '=':
                if purchase.invoice_ids:
                    a=0
                    inv_len = len(purchase.invoice_ids)
                    for invoice in purchase.invoice_ids:
                        if invoice.payment_state == 'paid':
                            a += 1
                    if inv_len == a:
                        purchase_ids.append(purchase.id)
            else:
                if purchase.invoice_ids:
                    for invoice in purchase.invoice_ids:
                        if invoice.payment_state != 'paid':
                            purchase_ids.append(purchase.id)
                if not purchase.invoice_ids:
                    purchase_ids.append(purchase.id)
        return [('id', 'in', purchase_ids)]
#        

    @api.depends('invoice_ids','state')
    def _search_open_invoice(self, operator, value):
        purchase_order = self.env['purchase.order'].search([])
        purchase_ids = []
        if operator == '=':
            for purchase in purchase_order:
                if purchase.invoice_ids:
                    a=0
                    inv_len = len(purchase.invoice_ids)
                    for invoice in purchase.invoice_ids:
                        if invoice.state == 'draft':
                            a += 1
                    if inv_len == a:
                        purchase_ids.append(purchase.id)
        else:
            for purchase in purchase_order:
                if purchase.invoice_ids:
                    a=0
                    inv_len = len(purchase.invoice_ids)
                    for invoice in purchase.invoice_ids:
                        if invoice.state != 'draft':
                            purchase_ids.append(purchase.id)
                if not purchase.invoice_ids:
                    purchase_ids.append(purchase.id)
        return [('id', 'in', purchase_ids)]
#    
#    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
