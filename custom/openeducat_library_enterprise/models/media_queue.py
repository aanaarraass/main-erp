
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpMediaQueue(models.Model):
    _inherit = "op.media.queue"

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        if self.date_from > self.date_to:
            raise ValidationError(
                _('To Date cannot be set before From Date.'))
