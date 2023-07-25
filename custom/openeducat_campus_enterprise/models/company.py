
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

    campus_enterprise_onboard_panel = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the campus onboarding step",
        default='not_done')
    onboarding_facilities_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding facilities layout step",
        default='not_done')
    onboarding_facilities_type_layout_state = fields.Selection(
        [('not_done', "Not done"),
         ('just_done', "Just done"),
         ('done', "Done"),
         ('closed', "Closed")],
        string="State of the onboarding facilities type layout  step",
        default='not_done')

    @api.model
    def action_close_campus_panel_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.user.company_id.campus_enterprise_onboard_panel = 'closed'

    # facility record layout starts##

    @api.model
    def action_onboarding_facilities_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_campus_enterprise.'
            'action_onboarding_facilities_layout').read()[0]
        return action

    def action_done_onboarding_facilities_layout(self):
        """ Set the onboarding step as done """
        if bool(self.logo) and self.logo != self._get_logo():
            self.set_onboarding_step_done('onboarding_facilities_layout_state')

    # facility type record layout starts##

    @api.model
    def action_onboarding_facilities_type_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_campus_enterprise.'
            'action_onboarding_facilities_type_layout').read()[0]
        return action

    def update_campus_onboarding_state(self):
        """ This method is called on the controller
         rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'onboarding_facilities_layout_state',
            'onboarding_facilities_type_layout_state'
        ]
        return self.get_and_update_onbarding_state(
            'campus_enterprise_onboard_panel', steps)
