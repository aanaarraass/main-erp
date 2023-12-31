
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

    meeting_enterprise_onboard_panel = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the meeting onboarding step", default='not_done')
    onboarding_meeting_layout_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"),
         ('done', "Done"), ('closed', "Closed")],
        string="State of the onboarding meeting layout  step",
        default='not_done')

    @api.model
    def action_close_meeting_panel_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.user.company_id.meeting_enterprise_onboard_panel = 'closed'

    @api.model
    def action_onboarding_meeting_layout(self):
        """ Onboarding step for the quotation layout. """
        action = self.env.ref(
            'openeducat_meeting_enterprise.'
            'action_onboarding_meeting_layout').read()[0]
        return action

    def update_meeting_onboarding_state(self):
        """ This method is called on the controller rendering
            method andensures that the animations
            are displayed only one time. """
        steps = [
            'onboarding_meeting_layout_state',
        ]
        return self.get_and_update_onbarding_state(
            'meeting_enterprise_onboard_panel', steps)
