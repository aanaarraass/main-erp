# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, _
from odoo.exceptions import UserError


class FeeInstallmentLine(models.Model):
    _name = 'fee.installment.line'
    _rec_name = 'name'
    _description = 'installment lines'

    date = fields.Date('Date')
    name = fields.Char('Description')
    student_name = fields.Char('Student', related='register_fee_id.name')
    installment_amount = fields.Float('Amount')
    state = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('invoiced', 'Invoiced'),
        ('paid', 'paid'),
    ], default='unpaid', string='Status')
    register_fee_id = fields.Many2one(comodel_name='register.fee', string='Parent Id', ondelete='cascade')
    student_contract_id = fields.Many2one(comodel_name='student.contract', string='Parent Id', ondelete='cascade')
    sequence = fields.Integer()
    invoice_id = fields.Many2one(comodel_name='account.move', string='Invoice_id', ondelete='cascade')
    invoice_status = fields.Selection(related='invoice_id.state')
    payment_status = fields.Selection(related='invoice_id.payment_state')

    def action_create_invoice(self):
        inv_obj = self.env['account.move']
        partner_id = self.register_fee_id.partner_id

        if self.installment_amount <= 0.00:
            raise UserError(
                _('The value of the deposit amount must be positive.'))
        check_installment = self.check_previous_installment()
        if check_installment:
            raise UserError('Please first make the full payment of previous installment')
        o2m_list = []
        for rec in self:
            o2m_list.append((0, 0, {
                'name': self.name,
                'price_unit': rec.installment_amount,
                'quantity': 1.0,
                'discount': 0.0,
            }))
        invoice = inv_obj.create({
            'partner_id': partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': self.date,
            'student_contract_id': self.student_contract_id.id,
            'invoice_line_ids': o2m_list,
        })
        self.state = 'invoiced'
        self.invoice_id = invoice.id
        return True

    def action_view_invoice(self):
        view_id = self.register_fee_id.id
        return {
            "name": "Created Invoices",
            "type": "ir.actions.act_window",
            "views": [[False, "list"], [False, "form"]],
            "res_model": "account.move",
            "domain": [("register_fee_id", "=", view_id)],
        }

    def check_previous_installment(self):
        for rec in self:
            all_installments = rec.student_contract_id.installment_lines.filtered(lambda ls: ls.sequence < rec.sequence)
            if any(x.payment_status != "paid" for x in all_installments):
                return True
        return False


class AccountMOve(models.Model):
    _inherit = 'account.move'

    student_contract_id = fields.Many2one(comodel_name='register.fee', ondelete='cascade')
