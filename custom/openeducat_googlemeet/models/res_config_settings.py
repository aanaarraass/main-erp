
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import api, fields, models
import os
from odoo.http import request
import requests


class GoogleMeetConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    access_token = fields.Char("")
    refresh_token = fields.Char("Refresh Token")

    @api.model
    def get_values(self):
        res = super(GoogleMeetConfig, self).get_values()
        res.update(
            client_id=self.env['ir.config_parameter'].sudo(
            ).get_param('google.meet.client.id'),
            client_secret=self.env['ir.config_parameter'].sudo(
            ).get_param('google.meet.client.secret'),
            access_token=self.env['ir.config_parameter'].sudo(
            ).get_param('google.meet.access.token'),
            refresh_token=self.env['ir.config_parameter'].sudo(
            ).get_param('google.meet.refresh.token'),
        )
        return res

    def set_values(self):
        super(GoogleMeetConfig, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('google.meet.client.id',
                        self.client_id)
        param.set_param('google.meet.client.secret', self.client_secret)
        param.set_param('google.meet.access.token', self.access_token)
        param.set_param('google.meet.refresh.token', self.refresh_token)

    def auth_google(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        callback = str(request.httprequest.host_url) + \
            'get_auth_url/%s/settings' % self.id
        return {
            'type': 'ir.actions.act_url',
            'url': callback,
            'target': 'new',
            'res_id': self.id,
        }

    def refreshToken(self):

        res_config = self.env['ir.config_parameter'].sudo()

        client_id_key = res_config.search(
            [('key', '=', 'google.meet.client.id')])
        client_secret_key = res_config.search(
            [('key', '=', 'google.meet.client.secret')])

        refresh_token_key = res_config.search(
            [('key', '=', 'google.meet.refresh.token')])

        client_id = client_id_key.value
        client_secret = client_secret_key.value
        refresh_token = refresh_token_key.value

        params = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)
        if r.ok:
            self.env['ir.config_parameter'].sudo().set_param(
                'google.meet.access.token', r.json()['access_token'])
