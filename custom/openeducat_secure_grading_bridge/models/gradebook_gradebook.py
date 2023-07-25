# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class GradebookGradebook(models.Model):

    _name = 'gradebook.gradebook'
    _inherit = ['gradebook.gradebook', 'secure.hash']

    student_id = fields.Many2one(
        'op.student', string="Student", required=True, secure=True)
    gradebook_line_id = fields.One2many('gradebook.line', 'gradebook_id',
                                        string='Gradebook Line', secure=True)
    percentage = fields.Float(string="Percentage", secure=True)
    grade = fields.Char(string="Grade", store=True, secure=True)
    course_id = fields.Many2one('op.course', string='Course',
                                tracking=True, required=True, secure=True)
    academic_year_id = fields.Many2many('op.academic.year', string='Year',
                                        required=True, tracking=True, secure=True)
