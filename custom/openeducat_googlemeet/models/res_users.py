
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from __future__ import print_function
import os.path
import os
from odoo import fields, models
from odoo.http import request
import requests


class GoogleMeetUsers(models.Model):
    _inherit = 'res.users'

    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    access_token = fields.Char("Access Token", readonly=True)
    refresh_token = fields.Char(readonly=True)

    def auth_google(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        callback = str(request.httprequest.host_url) + \
            'get_auth_url/%s/user' % self.id
        return {
            'type': 'ir.actions.act_url',
            'url': callback,
            'target': 'new',
            'res_id': self.id,
        }

    def refreshTokenUser(self):
        user = request.env['res.users'].sudo().search(
            [('id', '=', request.env.user.id)])
        refresh_token = user.refresh_token

        params = {
            "grant_type": "refresh_token",
            "client_id": user.client_id,
            "client_secret": user.client_secret,
            "refresh_token": refresh_token
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
            user.update({
                'access_token': r.json()['access_token']
            })
