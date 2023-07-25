# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class GradebookLine(models.Model):
    _name = 'gradebook.line'
    _inherit = 'gradebook.line'

    academic_term_id = fields.Many2one('op.academic.term', string='Term',
                                       required=True, tracking=True, secure=True)
    subject_id = fields.Many2one('op.subject', string="Subject",
                                 tracking=True, secure=True)
    grade_assigment_id = fields.Many2one('grading.assignment', 'Assignment',
                                         required=True, tracking=True, secure=True)
    marks = fields.Float('Marks', tracking=True, secure=True)
