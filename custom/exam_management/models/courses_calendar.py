# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api


class CoursesCalendar(models.Model):
    _name = 'courses.calendar'
    _rec_name = 'name'
    _description = 'exam_management.exam_management'

    name = fields.Char('Name')
    course_name = fields.Char('Course')
    date_start = fields.Date('Date Start')
    date_time_start = fields.Datetime('Date Start')
    date_stop = fields.Date('Stop Date')
    duration = fields.Float('Duration')

# access_courses_calendar,courses_calendar,model_courses_calendar,base.group_user,1,1,1,1


