
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpMediaUnit(models.Model):
    _inherit = "op.media.unit"

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
