# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    secure_qr_code = fields.Selection(
        [('secure', 'Secure'),
         ('open', 'Open'),
         ],
        config_parameter='secure_qr_code')
    parent_qrcode = fields.Boolean(
        string="QR Code")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            secure_qr_code=self.env['ir.config_parameter'].sudo().get_param(
                'secure_qr_code'),
            parent_qrcode=self.env['ir.config_parameter'].sudo().get_param(
                'parent_qrcode')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('parent_qrcode', self.parent_qrcode)
        param.set_param('secure_qr_code', self.secure_qr_code)
