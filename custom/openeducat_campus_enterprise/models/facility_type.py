
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpFacilityType(models.Model):
    _name = "op.facility.type"
    _description = "Facility Type"

    name = fields.Char('Name', size=64, required=True)
    code = fields.Char('Code', size=64, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)

    def action_onboarding_facilities_type_layout(self):
        self.env.user.company_id.onboarding_facilities_type_layout_state =\
            'done'
