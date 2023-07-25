
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpStudent(models.Model):
    _inherit = "op.student"

    health_lines = fields.One2many('op.health', 'student_id',
                                   string='Health Detail')

    health_count = fields.Integer(compute='_compute_count_health')

    def get_health(self):
        action = self.env.ref('openeducat_health_enterprise.'
                              'act_open_op_health_view').read()[0]
        action['domain'] = [('student_id', 'in', self.ids)]
        return action

    def _compute_count_health(self):
        for record in self:
            record.health_count = self.env['op.health'].search_count(
                [('student_id', 'in', self.ids)])
