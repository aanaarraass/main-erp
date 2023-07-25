# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api


class ExamExam(models.Model):
    _name = 'exam.exam'
    _rec_name = 'name'

    name = fields.Char('Title')
    department_id = fields.Many2one('op.department', 'Department', tracking=True)
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')
    academic_year = fields.Many2one(comodel_name='op.academic.year', string='Academic Year')
    state = fields.Selection([
        ('draft', 'draft'),
        ('ongoing', 'Ongoing'),
        ('cancel', 'Cancelled'),
        ('close', 'Closed'),
    ], string="status", default='draft')
    course_id = fields.Many2one(comodel_name='op.course', string='Course', ondelet='cascade')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', ondelet='cascade',
                                 default=lambda self: self.env.company)
    exam_subject_line = fields.One2many('exam.subject.line', 'exam_id', string='Subjects')
    timetable_request_line = fields.One2many('timetable.request', 'exam_id', string='Time Table')

# access_courses_calendar,courses_calendar,model_courses_calendar,base.group_user,1,1,1,1
    def action_draft(self):
        self.state = 'draft'

    def action_ongoing(self):
        self.state = 'ongoing'

    def action_cancel(self):
        self.state = 'cancel'

    def action_close(self):
        self.state = 'close'


class ExamExamLine(models.Model):
    _name = 'exam.subject.line'
    _rec_name = 'name'

    exam_id = fields.Many2one('exam.exam', ondelete='cascade')
    name = fields.Char('Subject')
    subject_id = fields.Many2one(comodel_name='op.subject', string='Course Subject')
    time_from = fields.Float(string='Time From', required=True)
    time_to = fields.Float(string='Time To', required=True)
    mark = fields.Integer(string='Mark')
    date = fields.Date()

    @api.onchange('exam_id.course_id', 'subject_id')
    def subjects_of_course(self):
        print('same subjects of the course'.center(100, '='))
        domain = {'subject_id': [('course_id', '=', self.exam_id.course_id)]}
        return {'domain': domain}
