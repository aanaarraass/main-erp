# -*- coding: utf-8 -*-


from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpAdmissionQuota(models.Model):
    _name = "op.program"
    _inherit = "mail.thread"
    _description = "Admission Quota"
    _order = 'id DESC'

    name = fields.Char(
        'Name')

    code = fields.Char(
        'Code')


    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    department_id = fields.Many2one(
        'op.department', string='Department')


