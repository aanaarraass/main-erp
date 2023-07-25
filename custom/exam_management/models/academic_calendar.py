# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcademicCalendar(models.Model):
    _name = 'academic.calendar'
    _rec_name = 'name'
    _description = 'exam_management.exam_management'

    name = fields.Char('Name')
    course_name = fields.Char('Course')
    value = fields.Integer()
    date_start = fields.Date('Date Start')
    date_stop = fields.Date('Stop Date')
    description = fields.Text()
    color = fields.Integer('Color Index', default=0)
    duration = fields.Float('Duration')


