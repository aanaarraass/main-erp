# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TimeTableRequest(models.Model):
    _name = 'timetable.request'
    _rec_name = 'subject_id'
    # _rec_name = 'name'
    _description = 'timetable.request'

    name = fields.Char('Name')
    exam_id = fields.Many2one('exam.exam', string='For Exam', ondelete='cascade')
    date_start = fields.Date('Date Start', related='exam_id.date_start')
    date_end = fields.Date('Date End', related='exam_id.date_end')
    time_from = fields.Float(string='Time From')
    time_to = fields.Float(string='Time To')
    mark = fields.Integer(string='Mark')
    course_id = fields.Many2one(comodel_name='op.course', string='Course', ondelet='cascade')
    # subjects = fields.Char('Subjects')
    subject_id = fields.Many2one(comodel_name='op.subject', string='Course Subject')
    date = fields.Date('Date')
    exam_time = fields.Float('Time')
    academic_year = fields.Many2one(comodel_name='op.academic.year',
                                    string='Academic Year', related='exam_id.academic_year')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', ondelet='cascade',
                                 default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request', 'Requested'),
        ('confirm', 'Approved'),
        ('cancel', 'Rejected')
    ], string="status", default='draft', copy=False, tracking=True, )

    @api.onchange('course_id')
    def subjects_of_course(self):
        print('same subjects of the course'.center(100, '='))
        for rec in self:
            return {'domain': {'subject_id': [('course_id', '=', rec.course_id.id)]}}

    def action_request(self):
        self.state = 'request'

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

