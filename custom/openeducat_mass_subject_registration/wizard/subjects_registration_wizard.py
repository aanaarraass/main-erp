
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class WizardOpStudentSubjectRegistration(models.TransientModel):
    _name = 'wizard.op.student.subject.registration'
    _description = "Create Subject Registration"

    def _get_students_data(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'op.student', default=_get_students_data, string='Students')
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    subjects_ids = fields.Many2many('op.subject', string='Subjects')

    def create_student_subjects(self):
        for record in self:
            student_search = self.env['op.student']. \
                search([('id', '=', record.student_ids.ids)])
            for i in student_search:
                res = self.env['op.student.course'].create({
                    'student_id': i.id,
                    'course_id': record.course_id.id,
                    'batch_id': record.batch_id.id,
                    'subject_ids': [(6, 0, self.subjects_ids.ids)]
                })
            return res
