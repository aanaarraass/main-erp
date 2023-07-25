# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class OpFaculty(models.Model):
    _inherit = "op.faculty"

    health_faculty_lines = fields.One2many('op.health', 'faculty_id',
                                           string='Health Detail')
    health_faculty_count = fields.Integer(compute='_compute_health_faculty_details')

    @api.depends('health_faculty_lines')
    def _compute_health_faculty_details(self):
        for health in self:
            health.health_faculty_count = self.env['op.health'].search_count(
                [('faculty_id', '=', self.id)])

    def count_health_faculty(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Health Details',
            'view_mode': 'tree,form',
            'res_model': 'op.health',
            'domain': [('faculty_id', '=', self.id)],
            'target': 'current',
        }
