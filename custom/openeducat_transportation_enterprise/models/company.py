
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

    transportation_enterprise_onboard_panel = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the transportation onboarding step",
        default='not_done')
    onboarding_route_layout_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the onboarding route layout  step",
        default='not_done')
    onboarding_stop_layout_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the onboarding stops layout  step",
        default='not_done')
    onboarding_trip_layout_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the onboarding trip layout  step",
        default='not_done')
    onboarding_vehicle_layout_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the onboarding vehicle layout  step",
        default='not_done')

    @api.model
    def action_close_transportation_panel_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.user.company_id.transportation_enterprise_onboard_panel =\
            'closed'

    # route layout starts##

    @api.model
    def action_onboarding_route_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_transportation_enterprise.'
            'action_onboarding_route_layout').read()[0]
        return action

    # stops layout starts##

    @api.model
    def action_onboarding_stop_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_transportation_enterprise.'
            'action_onboarding_stop_layout').read()[0]
        return action

    # trip layout starts##

    @api.model
    def action_onboarding_trip_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_transportation_enterprise.'
            'action_onboarding_trip_layout').read()[0]
        return action

    # vehicle type layout starts##

    @api.model
    def action_onboarding_vehicle_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_transportation_enterprise.'
            'action_onboarding_vehicle_layout').read()[0]
        return action

    def update_transportation_onboarding_state(self):
        """ This method is called on the controller rendering method and
            ensures that the animations
            are displayed only one time. """
        steps = [
            'onboarding_route_layout_state',
            'onboarding_stop_layout_state',
            'onboarding_trip_layout_state',
            'onboarding_vehicle_layout_state'
        ]
        return self.get_and_update_onbarding_state(
            'transportation_enterprise_onboard_panel', steps)
