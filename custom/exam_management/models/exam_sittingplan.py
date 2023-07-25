# -*- coding: utf-8 -*-
import odoo.exceptions
from odoo import models, fields, api

#
# class OpStudents(models.Model):
#     _inherit = 'op.student'
#
#     is_seated = fields.Boolean(default=False)


class ExamSittingPlan(models.Model):
    _name = 'exam.sittingplan'
    _rec_name = 'name'
    _description = 'exam.sittingplan'

    name = fields.Char('Name')
    exam_id = fields.Many2one('exam.exam', string='For Exam', ondelete='cascade')
    date_start = fields.Date('Date Start', related='exam_id.date_start')
    date_end = fields.Date('Date End', related='exam_id.date_end')
    time_from = fields.Float(string='Time From', related='timetable_id.time_from')
    time_to = fields.Float(string='Time To', related='timetable_id.time_to')
    mark = fields.Integer(string='Mark',  related='timetable_id.mark')
    subject_id = fields.Many2one(comodel_name='op.subject', string='Course Subject')
    timetable_id = fields.Many2one(comodel_name='timetable.request', string='Course Subject')
    batch_id = fields.Many2one(comodel_name='op.batch', string='Batch', required=True)
    course_id = fields.Many2one(comodel_name='op.course', string='Course',
                                ondelet='cascade', related='exam_id.course_id')
    subjects = fields.Char('Subjects')
    room_id = fields.Many2one('exam.room', string='Room')
    date = fields.Date('Date', default=lambda self: fields.Date.today())
    company_id = fields.Many2one(comodel_name='res.company', string='Company', ondelet='cascade',
                                 default=lambda self: self.env.company)
    sittingplan_line = fields.One2many(comodel_name='exam.sittingplan.line', inverse_name='sittingplan_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Approved'),
        ('cancel', 'Rejected')
    ], string="status", default='draft', copy=False, tracking=True, )

    def sitting_plan_2nd_room(self, i, student_name):
        for rec in self:
            j = 0
            if i >= 30 and i <= 39:
                j = 1
            elif i >= 40 and i <= 49:
                j = 2
            elif i >= 50 and i <= 59:
                j = 3
            elif i >= 60 and i <= 69:
                j = 1
            elif i >= 70 and i <= 79:
                j = 2
            elif i >= 80 and i <= 89:
                j = 3

            return (0, 0, {
                'student_name': student_name.name,
                'roll_number': student_name.course_detail_ids.roll_number,
                'chair_no': i + 1,
                'row_no': j,
                'sittingplan_id': rec.id,
            })


    def action_confirm(self):
        self.state = 'confirm'
        self.sittingplan_line = False
        student_list = self.env['op.student'].search([
            ('course_detail_ids.course_id', '=', self.course_id.id),
            ('course_detail_ids.batch_id', '=', self.batch_id.id),
        ])
        students = int(len(student_list))
        # students = 70
        if students <= 0:
            raise odoo.exceptions.UserError('There is no Student Available for this Course and Batch')
        o2m_list = []
        o2m_list2 = []
        o2m_list3 = []
        for rec in self:
            for i, student_name in enumerate(student_list):
            # for i in range(students):
                j = 0
                if i >= 30 and i <= 59:
                    o2m_list2.append(rec.sitting_plan_2nd_room(i, student_name))
                elif i >=60 and i <= 89:
                    o2m_list3.append(rec.sitting_plan_2nd_room(i, student_name))
                elif i <= 9:
                    j = 1
                elif i > 9 and i <= 19:
                    j = 2
                else:
                    j = 3

                o2m_list.append((0, 0, {
                    'student_name': student_name.name,
                    'roll_number': student_name.course_detail_ids.roll_number,
                    'chair_no': i + 1,
                    'row_no': j,
                    'sittingplan_id': rec.id,
                }))
        if o2m_list:
            self.update({
                'sittingplan_line': o2m_list
            })
        if o2m_list2:
            self.create({
                'exam_id': self.exam_id.id,
                'timetable_id': self.timetable_id.id,
                'batch_id': self.batch_id.id,
                'sittingplan_line': o2m_list2
            })
        if o2m_list3:
            self.create({
                'exam_id': self.exam_id.id,
                'timetable_id': self.timetable_id.id,
                'batch_id': self.batch_id.id,
                'sittingplan_line': o2m_list3
            })

    def action_cancel(self):
        self.state = 'cancel'


    def action_draft(self):
        self.state = 'draft'


class ExamSittingPlanLine(models.Model):
    _name = 'exam.sittingplan.line'

    student_name = fields.Char('Name')
    roll_number = fields.Char('Roll Number')
    row_no = fields.Integer('Row#')
    chair_no = fields.Integer('Chair No.')
    sittingplan_id = fields.Many2one('exam.sittingplan', ondelete='cascade')
