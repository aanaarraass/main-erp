
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    openeducat_library_onboard_panel = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding library layout step",
        default='not_done')
    onboarding_library_card_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding library card layout step",
        default='not_done')
    onboarding_publisher_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding publisher layout step",
        default='not_done')
    onboarding_author_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding author layout step",
        default='not_done')
    onboarding_media_type_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding media type layout step",
        default='not_done')
    onboarding_library_card_type_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding library card type layout step",
        default='not_done')

    @api.model
    def action_close_library_panel_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.user.company_id.openeducat_library_onboard_panel = 'closed'

    # library card layout start##

    @api.model
    def action_onboarding_library_card_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_library_enterprise.'
            'action_onboarding_library_card_layout').read()[0]
        return action

    # publisher layout start##

    @api.model
    def action_onboarding_publisher_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_library_enterprise.'
            'action_onboarding_publisher_layout').read()[0]
        return action

    # authors layout start##

    @api.model
    def action_onboarding_author_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_library_enterprise.'
            'action_onboarding_author_layout').read()[0]
        return action

    # media type layout start##

    @api.model
    def action_onboarding_media_type_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_library_enterprise.'
            'action_onboarding_media_type_layout').read()[0]
        return action

    # library card type layout start##

    @api.model
    def action_onboarding_library_card_type_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_library_enterprise.'
            'action_onboarding_library_card_type_layout').read()[0]
        return action

    def update_library_onboarding_state(self):
        """ This method is called on the controller
         rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'onboarding_library_card_layout_state',
            'onboarding_publisher_layout_state',
            'onboarding_author_layout_state',
            'onboarding_media_type_layout_state',
            'onboarding_library_card_type_layout_state'
        ]
        return self.get_and_update_onbarding_state(
            'openeducat_library_onboard_panel', steps)
