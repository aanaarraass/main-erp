# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class OpTransportationAgreement(models.Model):
    _name = "op.transportation.agreement"
    _rec_name = "partner_id"
    _description = "Transportation Agreement"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string='Student/Faculty', required=True)
    route_register_id = fields.Many2one(
        'op.route.register', string='Route Register', required=True)
    route_id = fields.Many2one('op.route', 'Route')
    # route_id = fields.Many2one('op.route', 'Route', required=True)
    stop_id = fields.Many2one('op.stop', 'Stop', required=True)
    plan_id = fields.Many2one('cost.plan', string="Plan")
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'),
         ('confirm', 'Confirmed'), ('agreement', 'Agreement Confirm'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', default='draft', tracking=True)
    date = fields.Date('Agreement Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", tracking=True)
    invoice_count = fields.Integer(
        compute="_compute_invoice", string='Bill Count', copy=False, default=0,
        store=True)
    transportation_fees_detail_ids = fields.One2many(
        'op.partner.transportation.fees.details',
        'agreement_id',
        string='Transportation Fees Collection Details',
        tracking=True)
    next_invoice_date = fields.Date(string="Next Invoice Date",
                                    help='The next invoice'
                                         ' will be created on this date then the'
                                         ' period will be extended')
    prev_invoice_date = fields.Date(string="Previous Invoice Date",
                                    help='This date will show previously created '
                                         'invoice')
    bill = fields.Integer(string="Bill Every")
    bill_selection = fields.Selection([('days', 'Day(s)'),
                                       ('weeks', 'Week(s)'),
                                       ('months', 'Month(s)'), ('years', 'Year(s)')],
                                      string="Bill Type",
                                      help='Repeat every (Days/Week/Month/Year)')
    expires_after = fields.Integer(help="Expires after number of billing cycles")

    @api.depends('route_register_id.product_id')
    def _compute_invoice(self):
        for order in self:
            invoices = order.mapped('route_register_id.product_id')
            order.invoice_count = len(invoices)

    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        self.bill = self.plan_id.bill
        self.bill_selection = self.plan_id.bill_selection
        for record in self:
            record.expires_after = record.plan_id.expires_after
            if record.date:
                if record.bill_selection == 'days':
                    days_count = record.expires_after
                    end_date_day = (record.date + timedelta(days=days_count))
                    next_date = (record.date + timedelta(days=1))
                    if not record.next_invoice_date and not record.end_date:
                        record.update({
                            'end_date': end_date_day,
                            'next_invoice_date': next_date
                        })
                elif record.bill_selection == 'weeks':
                    week_count = record.expires_after
                    end_date_week = (record.date + relativedelta(weeks=week_count))
                    next_week = (record.date + relativedelta(weeks=1))
                    if not record.next_invoice_date and not record.end_date:
                        record.update({
                            'end_date': end_date_week,
                            'next_invoice_date': next_week
                        })
                elif record.bill_selection == 'months':
                    month_count = record.expires_after
                    end_date_month = (record.date + relativedelta(
                        months=month_count))
                    next_month = (record.date + relativedelta(months=1))
                    if not record.next_invoice_date and not record.end_date:
                        record.update({
                            'end_date': end_date_month,
                            'next_invoice_date': next_month
                        })
                elif record.bill_selection == 'years':
                    year_count = record.expires_after
                    end_date_year = (record.date + relativedelta(years=year_count))
                    next_year = (record.date + relativedelta(years=1))
                    if not record.next_invoice_date and not record.end_date:
                        record.update({
                            'end_date': end_date_year,
                            'next_invoice_date': next_year
                        })

    @api.onchange('route_register_id')
    def _onchange_route_register_id(self):
        self.plan_id = self.route_register_id.plan_id

    @api.onchange('route_register_id')
    def onchange_route(self):
        self.route_id = self.route_register_id.route_id

    def submit_form(self):
        self.state = 'submit'

    def agreement_confirm(self):
        self.state = 'agreement'

    def confirm_in_progress(self):
        for record in self:
            record.state = 'confirm'

    def enroll_partner(self):
        for record in self:
            record.stop_id.write({
                'partner_ids': [[4, (self.partner_id.id)]],
            })
        self.state = 'done'

    def confirm_rejected(self):
        self.state = 'reject'

    def confirm_pending(self):
        self.state = 'pending'

    def confirm_to_draft(self):
        self.state = 'draft'

    def confirm_cancel(self):
        self.state = 'cancel'

    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_move_out_invoice_type')
        fees = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(fees).read()[0]
        inv_ids = []
        for agreement in self:
            inv_ids += [invoice.id for invoice in agreement.invoice_ids]
            result['context'] = {'default_partner_id': agreement.partner_id.id}
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.view_move_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

    @api.model
    def create_partner_transportation_fees(self):
        dict_val = {}
        agreement = self.env['op.transportation.agreement'].search([(
            'state', '=', 'done')])
        for record in agreement:
            if record.next_invoice_date:
                dict_val.update({
                    'amount': record.route_id.cost,
                    'date': record.next_invoice_date,
                    'product_id': record.route_id.product_id.id,
                    'state': 'draft'
                })
            if record.next_invoice_date <= record.end_date:
                record.update({
                    'prev_invoice_date': record.next_invoice_date
                })
                if record.bill_selection == 'days':
                    next_inv_date = record.bill
                    next_date = (record.next_invoice_date + timedelta(
                        days=next_inv_date))
                    record.update({
                        'next_invoice_date': next_date
                    })
                elif record.bill_selection == 'weeks':
                    next_inv_date = record.bill
                    next_date = (record.next_invoice_date + relativedelta(
                        weeks=next_inv_date))
                    record.update({
                        'next_invoice_date': next_date
                    })
                elif record.bill_selection == 'months':
                    next_inv_date = record.bill
                    next_date = (record.next_invoice_date + relativedelta(
                        months=next_inv_date))
                    record.update({
                        'next_invoice_date': next_date
                    })
                elif record.bill_selection == 'years':
                    next_inv_date = record.bill
                    next_date = (record.next_invoice_date + relativedelta(
                        years=next_inv_date))
                    record.update({
                        'next_invoice_date': next_date
                    })
                record.write({
                    'transportation_fees_detail_ids': [(0, 0, dict_val)]}
                )


class OpPartnerTransportationFeesDetails(models.Model):
    _name = "op.partner.transportation.fees.details"
    _description = "Partner Transportation Fees Details"

    invoice_id = fields.Many2one('account.move', 'Invoice ID')
    # amount = fields.Monetary('Fees Amount', currency_field='currency_id')
    amount = fields.Float('Fee Amount', related="agreement_id.route_id.transport_fee", store=True)
    date = fields.Date('Submit Date')
    # date = fields.Date('Submit Date', related="agreement_id.date", store=True)
    product_id = fields.Many2one('product.product', string='Amount For')
    agreement_id = fields.Many2one('op.transportation.agreement',
                                   'Transport Agreement', ondelete="cascade")
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'),
                              ('confirm', 'Confirmed'), ('agreement', 'Agreement Confirm'),
                              ('reject', 'Rejected'), ('pending', 'Pending'), ('invoiced', 'Invoiced'),
                              ('cancel', 'Cancelled'), ('done', 'Done')], default='draft',
                             string='State', copy=False)
    invoice_state = fields.Selection(string='Invoice',
                                     related="invoice_id.state", readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = template.company_id.sudo(
            ).currency_id.id or main_company.currency_id.id

    currency_id = fields.Many2one(
        'res.currency', string='Currency', compute='_compute_currency_id',
        default=lambda self: self.env.user.company_id.currency_id.id)

    def get_invoice(self):
        """ Create invoice for fee payment process of student """
        inv_obj = self.env['account.move']
        partner_id = self.agreement_id.partner_id
        account_id = False
        # product = self.agreement_id.route_id.product_id
        product = self.product_id

        if product.property_account_income_id:
            account_id = product.property_account_income_id.id
        if not account_id:
            account_id = product.categ_id.property_account_income_categ_id.id
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s".'
                  'You may have to install a chart of account from Accounting'
                  ' app, settings menu.') % product.name)
        if self.amount <= 0.00:
            raise UserError(
                _('The value of the deposit amount must be positive.'))
        else:
            amount = self.amount
            name = product.name

        for record in self:
            invoice = inv_obj.create({
                'partner_id': partner_id.name,
                'move_type': 'out_invoice',
                'invoice_date': record.date,
                'partner_id': partner_id.id,
            })
        line_values = {'name': name,
                       'account_id': account_id,
                       'price_unit': amount,
                       'quantity': 1.0,
                       'discount': 0.0,
                       'product_uom_id': product.uom_id.id,
                       'product_id': product.id}
        invoice.write({'invoice_line_ids': [(0, 0, line_values)]})

        invoice._compute_always_tax_exigible()
        self.state = 'invoiced'
        self.invoice_id = invoice.id
        return True

    def action_get_invoice(self):
        value = True
        if self.invoice_id:
            form_view = self.env.ref('account.view_move_form')
            tree_view = self.env.ref('account.view_invoice_tree')
            value = {
                'domain': str([('id', '=', self.invoice_id.id)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.move',
                'view_id': False,
                'views': [(form_view and form_view.id or False, 'form'),
                          (tree_view and tree_view.id or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': self.invoice_id.id,
                'target': 'current',
                'nodestroy': True
            }
        return value
