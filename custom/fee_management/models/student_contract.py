# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class StudentContract(models.Model):
    _name = 'student.contract'
    _description = 'Contract of students'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Student Name",
                                 domain=[("is_student", "=", True)], store=True)
    register_fee_id = fields.Many2one(comodel_name='register.fee', string="Course")
    student_quota_id = fields.Many2one(comodel_name='register.fee.quota', string="Quota")
    academic_year = fields.Many2one(comodel_name='op.academic.year', string='Academic Year')
    fee_year = fields.Selection(
        selection='years_selection',
        string="Year", default='2023'
    )
    # admission_fee = fields.Float('admission fee', related='register_fee_id.total_admission_fee', store=True)
    quota_amount = fields.Float('Quota Amount', related='student_quota_id.amount', store=True)
    admission_fee = fields.Float('Total fee', compute='_compute_admission_fee', store=True)
    total_fee = fields.Float('Course fee', related='register_fee_id.total_fee', store=True)
    is_installment = fields.Boolean('Want Installments', default=False)
    no_of_installment = fields.Integer('No. of Installments', store=True)
    installment_lines = fields.One2many(comodel_name='fee.installment.line', inverse_name='student_contract_id')

    @api.depends('total_fee', 'quota_amount')
    def _compute_admission_fee(self):
        for rec in self:
            rec.admission_fee = max([0, rec.total_fee - rec.quota_amount])

    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year, datetime.now().year + 10):
            year_list.append((str(y), str(y)))
        return year_list

    def action_make_installments(self):
        amount = 0
        o2m_list = []
        self.installment_lines = False
        for rec in self:
            if rec.no_of_installment <= 0.0 or rec.admission_fee <= 0.0:
                raise ValidationError(_("Put the values correctly"))

            if rec.no_of_installment > 0:
                amount = rec.admission_fee / rec.no_of_installment
            sequence = 0
            if amount > 0:
                for line in range(rec.no_of_installment):
                    sequence += 1
                    print('action_make_installments'.center(100, '='))
                    o2m_list.append((0, 0, {
                        'date': fields.Date.today() + relativedelta(months=line),
                        'name': 'Fee Installment',
                        'sequence': sequence,
                        'installment_amount': amount,
                    }))
        self.write({
            'installment_lines': o2m_list
        })