# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class RegisterFee(models.Model):
    _name = 'register.fee'
    _rec_name = 'name'
    _description = 'Transport Agreement Account'

    batch_number = fields.Char('Batch')
    name = fields.Char('Name')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Student Name", domain=[("is_student", "=", True)])
    fee_year = fields.Selection(
        selection='years_selection',
        string="Year", default='2023'
    )
    academic_year = fields.Many2one(comodel_name='op.academic.year', string='Academic Year')
    semester_fee = fields.Float('Semester fee')
    no_of_semester = fields.Integer('No. of Semesters')
    admission_fee = fields.Float('Admission fee')
    total_amount = fields.Float('Total fee', compute='_compute_total_amount', store=True)
    total_other_fee = fields.Float('Total other fees', compute='_compute_other_fees')
    total_fee = fields.Float('Total payable fee', compute='_compute_total_fee')
    late_fine = fields.Float('Late Fine')
    batch_id = fields.Many2one('op.batch', 'Batch', required=True, tracking=True)
    roll_number = fields.Char('Roll Number', tracking=True)
    notes = fields.Text()
    course_id = fields.Many2one(comodel_name='op.course', string='Course', ondelet='cascade')
    fee_register_line = fields.One2many(comodel_name='register.fee.line', inverse_name='register_fee_id')

    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year, datetime.now().year + 10):
            year_list.append((str(y), str(y)))
        return year_list

    @api.depends('no_of_semester', 'semester_fee', 'admission_fee', 'late_fine')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = max([0, (rec.no_of_semester * rec.semester_fee) + rec.admission_fee - rec.late_fine])

    @api.depends('fee_register_line.amount')
    def _compute_other_fees(self):
        for rec in self:
            rec.total_other_fee = max([0, sum(rec.fee_register_line.mapped('amount'))])

    @api.depends('total_amount', 'total_other_fee')
    def _compute_total_fee(self):
        for rec in self:
            rec.total_fee = max([0, rec.total_amount + rec.total_other_fee])


class RegisterFeeLine(models.Model):
    _name = 'register.fee.line'

    name = fields.Char('Description')
    amount = fields.Float('Amount')
    register_fee_id = fields.Many2one(comodel_name='register.fee', ondelete="cascade")
