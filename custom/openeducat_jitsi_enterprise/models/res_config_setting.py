
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    openeducat_jitsi_url_key = fields.Char(
        "OpenEducat Jitsi Url", readonly=False)
    record_meeting_jitsi = fields.Boolean(config_parameter='jitsi.recordmeeting')
    auto_start_recording_jitsi = fields.Boolean(config_parameter='jitsi.autostartrecording') # noqa
    dial_number_jitsi = fields.Char(config_parameter='jitsi.dial_number')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            openeducat_jitsi_url_key=self.env['ir.config_parameter'].sudo().get_param(
                'jitsi.server'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('jitsi.server', self.openeducat_jitsi_url_key)
