# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields


class EntryTestFee(models.Model):
    _name = 'entry.test.fee'
    _description = 'Transport Agreement Account'

    batch_number = fields.Char('Batch')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Student Name", domain=[("is_student", "=", True)])
    year_of_fee = fields.Selection(
        selection='years_selection',
        string="Year",
    )
    semester_fee = fields.Float('Semester fee')
    admission_fee = fields.Float('admission fee')
    late_fine = fields.Float('Late Fine')

    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year, datetime.now().year + 10):
            year_list.append((str(y), str(y)))
        return year_list
