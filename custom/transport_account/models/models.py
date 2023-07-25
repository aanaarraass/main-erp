# -*- coding: utf-8 -*-
import odoo.exceptions
from odoo import models, fields, api, _, exceptions


class TransportAgreementAccount(models.Model):
    _name = 'agreement.account'
    _description = 'Transport Agreement Account'

    account_id = fields.Many2one(comodel_name='account.account', string="Account For Fee",
                                 domain="[('user_type_id', '=', 'Income')]")
    description = fields.Text(default="Set Account for Transport fee")

    @api.model
    def create(self, vals):
        agreement = self.env['agreement.account'].search([])
        if len(agreement) == 1:
            raise exceptions.UserError(_('You cannot Create Account more than 1'))
        res = super(TransportAgreementAccount, self).create(vals)
        return res


class OpPartnerTransportationFeesDetails(models.Model):
    _inherit = "op.partner.transportation.fees.details"

    def get_invoice(self):
        """ Create invoice for fee payment process of student """
        account_id = self.env['agreement.account'].search([]).mapped('account_id')[0]
        if not account_id:
            raise exceptions.UserError('Please set the account first in Transport Agreement Account model'
                                       ' You may have to install a chart of account from Accounting')
        inv_obj = self.env['account.move']
        partner_id = self.agreement_id.partner_id
        if self.amount <= 0.00:
            raise odoo.exceptions.UserError(
                _('The value of the deposit amount must be positive.'))
        for record in self:
            invoice = inv_obj.create({
                'partner_id': partner_id.name,
                'move_type': 'out_invoice',
                'invoice_date': record.date,
                'partner_id': partner_id.id,
            })
        line_values = {'name': 'Transport Fee',
                       'account_id': account_id.id,
                       'price_unit': self.amount,
                       'quantity': 1.0,
                       'discount': 0.0,
                       }
        invoice.write({'invoice_line_ids': [(0, 0, line_values)]})

        invoice._compute_always_tax_exigible()
        self.state = 'invoiced'
        self.invoice_id = invoice.id
        return True




