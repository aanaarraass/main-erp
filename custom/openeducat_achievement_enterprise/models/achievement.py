
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class OpAchievement(models.Model):
    _name = "op.achievement"
    _inherit = ["mail.thread"]
    _rec_name = "student_id"
    _description = "Achievement"

    progression_id = fields.Many2one('op.student.progression',
                                     'Progression No')
    student_id = fields.Many2one('op.student', 'Student',
                                 required=True, tracking=True)
    faculty_id = fields.Many2one(
        'op.faculty', 'Faculty', required=True, tracking=True)
    achievement_type_id = fields.Many2one(
        'op.achievement.type', 'Achievement Type',
        required=True, tracking=True)
    description = fields.Text(
        'Description', required=True, tracking=True)
    achievement_date = fields.Date(
        'Date', required=True,
        default=fields.Date.today(), tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id,
        tracking=True)
    active = fields.Boolean(default=True)

    @api.onchange('student_id')
    def onchange_student_achievement_progrssion(self):
        if self.student_id:
            student = self.env['op.student.progression'].search(
                [('student_id', '=', self.student_id.id)])
            self.progression_id = student.id
            sequence = student.name
            student.write({'name': sequence})


class OpStudent(models.Model):
    _inherit = "op.student"

    achievement_line_ids = fields.One2many(
        'op.achievement', 'student_id', 'Achievement Details')
