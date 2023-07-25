
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class StudentProgression(models.Model):
    _inherit = ["op.student.progression"]

    @api.depends("achievement_lines")
    def _compute_total_achievemenet(self):
        self.total_achievement = len(self.achievement_lines)

    achievement_lines = fields.One2many('op.achievement',
                                        'progression_id',
                                        string='Progression Achivement')
    total_achievement = fields.Integer('Total Achievement',
                                       compute="_compute_total_achievemenet",
                                       store=True)
