# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################

from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def write(self, values):
        result = super(SaleOrderLine, self).write(values)
        status = ''
        if values.get('qty_delivered'):
            service_lines = self.order_id.order_line.filtered(lambda x:x.product_id.type=='service')
            for service_line in service_lines:
                if service_line.product_uom_qty==service_line.qty_delivered:
                    status = 'ship_status'
                else:
                    status = ''
            rest_lines = self.order_id.order_line - service_lines
            for l in rest_lines:
                if l.product_uom_qty==l.qty_delivered:
                    status = 'ship_status'
                else:
                    status = ''
            if status!='':
                self.order_id.temp_ship_status = True
        return result

class sale_order(models.Model):
    _inherit = "sale.order"

    temp_ship_status = fields.Boolean(copy=False,store=True)

    def _compute_invoiced(self):
        for sale in self:
            sale.invoice_status_new = False
            if sale.invoice_ids:
                a=0
                inv_len = len(sale.invoice_ids)
                for invoice in sale.invoice_ids:
                    if invoice.payment_state == 'paid':
                        a += 1
                if inv_len == a:
                    sale.invoice_status_new = True
                    sale.temp_invoice_status_new = True
    def _compute_invoiced_open(self):
        for sale in self:
            sale.invoice_open = False
            for invoice in sale.invoice_ids:
                if invoice.state == 'draft':
                    sale.invoice_open = True
                    
    def _compute_shiped(self):
        for sale in self:
            sale.ship_partial = False
            if sale.temp_ship_status:
                sale.ship_status = True
            else:
                sale.ship_status = False
            if sale.picking_ids:
                a=0
                picking_len = len(sale.picking_ids)
                for picking in sale.picking_ids:
                    if picking.state == 'done':
                        a += 1
                if picking_len == a:
                    service_lines = sale.order_line.filtered(lambda x: x.product_id.type == 'service' and x.product_uom_qty!=x.qty_delivered)
                    if service_lines:
                        sale.ship_status = False
                        sale.ship_partial = True
                        sale.temp_ship_partial = True
                    else:
                        sale.ship_status = True
                if a != 0 and not picking_len == a:
                    sale.ship_partial = True
                    sale.temp_ship_partial = True

    @api.depends('invoice_ids')
    def _compute_invoiced_partial(self):
        for sale in self:
            p_paid = False
            inv_paid = False
            inv_open = False
            for inv in sale.invoice_ids:
                if inv.payment_state == 'paid':
                    inv_paid = True
                if inv.state == 'draft':
                    inv_open = True
                if inv.amount_residual > 0 and inv.amount_residual < inv.amount_total: 
                    p_paid = True
            
            if inv_open and inv_paid and not p_paid:
                p_paid = True
            sale.invoice_partial = p_paid
            sale.temp_invoice_partial = p_paid
        return True
    
    invoice_open = fields.Boolean(string='Invoiced', compute='_compute_invoiced_open',search='_search_open_invoice')
    invoice_status_new = fields.Boolean(string='Paid', compute='_compute_invoiced', search='_search_full_paid_invoice')
    temp_invoice_status_new = fields.Boolean(string='Paid',store=True,copy=False)
    invoice_partial = fields.Boolean(string='Partial Paid', compute='_compute_invoiced_partial',search='_search_partial_paid_invoice',copy=False)
    temp_invoice_partial = fields.Boolean(string='Partial Paid', copy=False, store=True)
    ship_status = fields.Boolean(string='Shiped',compute='_compute_shiped',copy=False, search='_search_full_shipment')
    ship_partial = fields.Boolean(string='Partial Delivered',compute='_compute_shiped',copy=False, search='_search_partial_shipment')
    temp_ship_partial = fields.Boolean(string='Partial Delivered',copy=False,store=True)
    not_ship_status = fields.Boolean(string='Not Shiped', compute='_compute_not_shiped', copy=False, search='_search_full_shipment')
    not_temp_ship_status = fields.Boolean(copy=False, store=True)
    not_paid_status = fields.Boolean(string='Not Paid', compute='_compute_not_shiped', copy=False, search='_search_full_shipment')
    not_temp_paid_status = fields.Boolean(copy=False, store=True)


    def _compute_not_shiped(self):
        for order in self:
            order.not_ship_status = True
            order.not_temp_ship_status = True
            order.not_paid_status = True
            order.not_temp_paid_status = True
            for inv in order.invoice_ids:
                if inv.payment_state !='not_paid':
                    order.not_paid_status = False
                    order.not_temp_paid_status = False
            for line in order.order_line:
                if line.qty_delivered > 0:
                    order.not_ship_status = False
                    order.not_temp_ship_status = False
    def _search_full_shipment(self, operator, value):
        done_picking =  []
        if operator == '=':
            done_picking = open_picking = []
            query = """ select distinct sol.order_id from stock_move as sm \
                    JOIN sale_order_line as sol ON sol.id = sm.sale_line_id \
                    JOIN stock_picking as sp ON sp.id = sm.picking_id \
                    where sm.state = %s """
            params = ('done',)
            self.env.cr.execute(query, params)
            result = self.env.cr.dictfetchall()
            done_picking = [order.get('order_id') for order in result]
            
            state = ['done','cancel']
            query = """ select distinct sol.order_id from stock_move as sm \
                    JOIN sale_order_line as sol ON sol.id = sm.sale_line_id \
                    JOIN stock_picking as sp ON sp.id = sm.picking_id \
                    where sm.state not in %s """
            params = (tuple(state),)
            self.env.cr.execute(query, params)
            result = self.env.cr.dictfetchall()
            open_picking = [order.get('order_id') for order in result]
            if open_picking:
                done_picking = list(set(done_picking) - set(open_picking))
        
        return [('id', 'in', done_picking)]
            
    
    def _search_full_shipment1(self, operator, value):
        sale_order = self.env['sale.order'].search([])
        sale_ids = []
        for sale in sale_order:
            if operator == '=':
                if sale.picking_ids:
                    a=0
                    picking_len = len(sale.picking_ids)
                    for picking in sale.picking_ids:
                        if picking.state == 'done':
                            a += 1
                    if picking_len == a:
                        sale_ids.append(sale.id)
            else:
                if sale.picking_ids:
                    a=0
                    picking_len = len(sale.picking_ids)
                    for picking in sale.picking_ids:
                        if picking.state != 'done':
                            a += 1
                    if picking_len == a:
                        sale_ids.append(sale.id)
                if not sale.picking_ids:
                    sale_ids.append(sale.id)
        return [('id', 'in', sale_ids)]
        
    def _search_partial_shipment(self, operator, value):
        sale_order = self.env['sale.order'].search([])
        sale_ids = []
        for sale in sale_order:
            if operator == '=':
                if sale.picking_ids:
                    a=0
                    picking_len = len(sale.picking_ids)
                    for picking in sale.picking_ids:
                        if picking.state == 'done':
                            a += 1
                    if a != 0 and picking_len != a:
                        sale_ids.append(sale.id)
            else:
                if sale.picking_ids:
                    a=0
                    picking_len = len(sale.picking_ids)
                    for picking in sale.picking_ids:
                        if picking.state != 'done':
                            a += 1
                    if picking_len == a:
                        sale_ids.append(sale.id)
                if not sale.picking_ids:
                    sale_ids.append(sale.id)
    
        return [('id', 'in', sale_ids)]
        
        
    
    def _search_partial_paid_invoice(self, operator, value):
        sale_order = self.env['sale.order'].search([])
        sale_ids = []
        for sale in sale_order:
            if operator == '=':
                if sale.invoice_ids:
                    a=0
                    inv_len = len(sale.invoice_ids)
                    for invoice in sale.invoice_ids:
                        if invoice.state == 'posted' and invoice.amount_residual > 0 and  invoice.amount_residual < invoice.amount_total:
                            a += 1
                    if a != 0:
                        sale_ids.append(sale.id)
            else:
                if sale.invoice_ids:
                    a=0
                    for invoice in sale.invoice_ids:
                        if invoice.state != 'open':
                            sale_ids.append(sale.id)
                if not sale.invoice_ids:
                    sale_ids.append(sale.id)
        return [('id', 'in', sale_ids)]
        
        
    def _search_full_paid_invoice(self, operator, value):
        open_sale_ids = []
        paid_sale_ids = []
        if operator == '=':
            query = """ select sol.order_id,ai.state from sale_order_line_invoice_rel as solr \
                    JOIN account_move_line as ail ON ail.id = solr.invoice_line_id \
                    JOIN account_move as ai ON ai.id = ail.move_id \
                    JOIN sale_order_line as sol ON sol.id = solr.order_line_id \
                    where ai.state = %s """
            params = ('open',)
            self.env.cr.execute(query, params)
            result = self.env.cr.dictfetchall()
            open_sale_ids = [order.get('order_id') for order in result]
            
            query = """ select sol.order_id,ai.state from sale_order_line_invoice_rel as solr \
                    JOIN account_move_line as ail ON ail.id = solr.invoice_line_id \
                    JOIN account_move as ai ON ai.id = ail.move_id \
                    JOIN sale_order_line as sol ON sol.id = solr.order_line_id \
                    where ai.payment_state = %s """
            params = ('paid',)
            self.env.cr.execute(query, params)
            result = self.env.cr.dictfetchall()
            paid_sale_ids = [order.get('order_id') for order in result]
            
            if open_sale_ids:
                lst3 = [value for value in paid_sale_ids if value in open_sale_ids] 
                paid_sale_ids= list(set(paid_sale_ids) - set(open_sale_ids))
        return [('id', 'in', paid_sale_ids)]
        

    def _search_open_invoice(self, operator, value):
        open_sale_ids = []
        paid_sale_ids = []
        if operator == '=':
            query = """ select sol.order_id,ai.state from sale_order_line_invoice_rel as solr \
                    JOIN account_move_line as ail ON ail.id = solr.invoice_line_id \
                    JOIN account_move as ai ON ai.id = ail.move_id \
                    JOIN sale_order_line as sol ON sol.id = solr.order_line_id \
                    where ai.state = %s """
            params = ('draft',)
            self.env.cr.execute(query, params)
            result = self.env.cr.dictfetchall()
            open_sale_ids = [order.get('order_id') for order in result]
            
            
        return [('id', 'in', open_sale_ids)]
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
