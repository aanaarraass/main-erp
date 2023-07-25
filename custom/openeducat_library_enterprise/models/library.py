
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpLibraryCardType(models.Model):
    _inherit = "op.library.card.type"

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    def action_onboarding_library_card_type_layout(self):
        self.env.user.company_id.onboarding_library_card_type_layout_state =\
            'done'


class OpLibraryCard(models.Model):
    _inherit = "op.library.card"

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    def action_onboarding_library_card_layout(self):
        self.env.user.company_id.onboarding_library_card_layout_state =\
            'done'
