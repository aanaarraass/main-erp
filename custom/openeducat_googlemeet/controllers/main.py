from odoo import http
from odoo.http import request
import werkzeug
import os
from google_auth_oauthlib.flow import Flow

dir_path = os.path.dirname(os.path.realpath(__file__))


class AuthController(http.Controller):
    @http.route('/get_auth_url/<int:current_id>/<string:tag>',
                type='http', method=['POST'], auth='public')
    def get_auth_url(self, current_id=None, tag=None, **post):
        self.tag = tag
        self.current_id = current_id
        user = None
        res_config = None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar',
                       'https://www.googleapis.com/auth/userinfo.profile',
                       'openid',
                       'https://www.googleapis.com/auth/userinfo.email',
                       ]
        if tag == 'user':
            user = request.env['res.users'].sudo().search(
                [('id', '=', request.env.user.id)])
        if tag == 'settings':
            res_config = request.env['res.config.settings'].sudo().search(
                [('id', '=', int(current_id))])

        if user:
            self.api_dict = {
                "web": {
                    "client_id": user.client_id,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url":
                        "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": user.client_secret
                }
            }

        if res_config:
            self.api_dict = {
                "web": {
                    "client_id": res_config.client_id,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url":
                        "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": res_config.client_secret
                }
            }

        flow = Flow.from_client_config(
            self.api_dict, scopes=self.SCOPES)
        flow.redirect_uri = str(
            request.httprequest.host_url) + 'google_auth_token'
        self.authorization_url, self.state = flow.authorization_url(
            access_type='offline', include_granted_scopes='true')

        return werkzeug.utils.redirect(self.authorization_url)

    @http.route('/google_auth_token', type='http',
                methods=['GET'], auth='public', website=True)
    def google_auth_token(self):

        user = None
        res_config = None

        if self.tag == 'user':
            user = request.env['res.users'].sudo().search(
                [('id', '=', request.env.user.id)])
        if self.tag == 'settings':
            res_config = request.env['res.config.settings'].sudo().search(
                [('id', '=', int(self.current_id))])

        flow = Flow.from_client_config(
            self.api_dict, scopes=self.SCOPES, state=self.state)
        flow.redirect_uri = str(
            request.httprequest.host_url) + 'google_auth_token'
        authorization_response = request.httprequest.url
        flow.fetch_token(authorization_response=authorization_response)
        access_token = self.credentials_to_dict(flow.credentials)

        if user:
            for record in user:
                record.update(
                    {
                        'access_token': access_token['token'],
                        'refresh_token': access_token['refresh_token']
                    }
                )
            return request.render('openeducat_googlemeet.token_confirmed')
        if res_config:
            for res in res_config:
                res.update(
                    {
                        "access_token": access_token['token'],
                        "refresh_token": access_token['refresh_token']
                    }
                )
                res.get_values()
                res.set_values()
            return request.render('openeducat_googlemeet.token_confirmed')

        if not user and res_config:
            return request.render('openeducat_googlemeet.token_refused')

    def credentials_to_dict(self, credentials):
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}
