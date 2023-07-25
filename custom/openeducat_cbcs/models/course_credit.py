
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class CourseCredit(models.Model):
    _name = "course.credit"
    _inherit = ['mail.thread']
    _description = "Course Credit"
    _rec_name = "course_id"

    course_id = fields.Many2one('op.course', string="Course")
    academic_year_id = fields.Many2one('op.academic.year', string="Academic Year")
    sem_credit_line_id = fields.One2many('sem.credit', 'course_credit_id',
                                         string="Semester Credit")
    all_academic = fields.Selection([('general', 'General'),
                                     ('academic_based', 'Based On Academic')],
                                    default="academic_based",
                                    string="Credit System")
    subject_credit = fields.One2many('subject.credit', 'course_credit_id',
                                     string="Subject Credit")


class SemCredit(models.Model):
    _name = "sem.credit"
    _inherit = ['mail.thread']
    _description = "Semester Credit"
    _rec_name = "semester_id"

    semester_id = fields.Many2one('op.academic.term', string="Semester")
    course_credit_id = fields.Many2one('course.credit', string="Course Credit")
    min_credit = fields.Float(string="Minimum Credit")
    max_credit = fields.Float(string="Maximum Credit")
    subject_credit = fields.One2many('subject.credit', 'sem_credit_id',
                                     string="Subject Credit")


class SubjectCredit(models.Model):
    _name = "subject.credit"
    _description = "Subject Credit"

    subject_id = fields.Many2one('op.subject', string="Subject")
    credit = fields.Float('Credit')
    course_credit_id = fields.Many2one('course.credit', string="Course Credit")
    sem_credit_id = fields.Many2one('sem.credit', string="semester Credit")

    @api.onchange('subject_id')
    def _onchange_subject_credit(self):
        self.credit = self.subject_id.credit_point
