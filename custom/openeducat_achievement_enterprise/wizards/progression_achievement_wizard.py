
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class ProgressAchievement(models.TransientModel):
    """ Progression Achievement """
    _name = "achievement.progress.wizard"
    _description = "Achievement Progress Wizard"

    @api.model
    def _get_default_student(self):
        ctx = self._context
        if ctx.get('active_model') == 'op.student.progression':
            obj = self.env['op.student.progression']. \
                browse(ctx.get('active_ids')[0])
            return obj.student_id

    student_id = fields.Many2one('op.student',
                                 string="Student Name",
                                 default=_get_default_student)
    achievement_ids = fields.Many2many('op.achievement',
                                       string='Achievement')

    def Add_achievement(self):
        core = self.env['op.student.progression']. \
            browse(self.env.context['active_ids'])
        for i in core:
            i.achievement_lines = self.achievement_ids
