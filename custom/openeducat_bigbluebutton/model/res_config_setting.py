
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

    openeducat_big_blue_button_key = fields.Char(
        string="OpenEducat bigbluebutton Secret Key", readonly=False)
    openeducat_big_blue_url_key = fields.Char(
        "OpenEducat Bigbluebutton Url", readonly=False)
    record_meeting = fields.Boolean('Record Meeting',
                                    config_parameter='bigbluebutton.recordmeeting')
    auto_start_recording = fields.Boolean('Auto Start Recording',
                                          config_parameter='bigbluebutton.autostartrecording') # noqa
    dial_number = fields.Char('Dial Number',
                              config_parameter='bigbluebutton.dial_number')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            openeducat_big_blue_button_key=self.env['ir.config_parameter'].sudo().get_param( # noqa
                'bigbluebutton.secret'),
            openeducat_big_blue_url_key=self.env['ir.config_parameter'].sudo().get_param( # noqa
                'bigbluebutton.url'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('bigbluebutton.secret', self.openeducat_big_blue_button_key)
        param.set_param('bigbluebutton.url', self.openeducat_big_blue_url_key)
