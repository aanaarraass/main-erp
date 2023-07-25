# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class StudentTransportFee(models.Model):
    _name = "student.transport.fee"


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_driver = fields.Boolean("Is a Driver", help="Get driver info. page")
    license_number = fields.Char('License Number')
    roll_number = fields.Char('Roll Number')
    father_name = fields.Char('Father name')
    studetn_cnic_number = fields.Char('Student CNIC')
    license_district = fields.Char('License District')
    license_date = fields.Date('License Expiry Date')
    license_type = fields.Selection([('ltv', 'LTV'), ('htv', 'HTV')], string='License Type')
    # op_student_course_id = fields.Many2one('op.student.course',)
