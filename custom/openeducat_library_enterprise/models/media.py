
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpMedia(models.Model):
    _inherit = "op.media"

    def _compute_total_units(self):
        for record in self:
            record.total_units = self.env['op.media.unit'].search_count(
                [('media_id', '=', record.id)])

    total_units = fields.Integer('Total Units', compute='_compute_total_units')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
