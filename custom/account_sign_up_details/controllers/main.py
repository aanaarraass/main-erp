# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
import logging
from odoo.http import request,route
from odoo.exceptions import UserError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.main import SIGN_UP_REQUEST_PARAMS

import werkzeug

from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.base_setup.controllers.main import BaseSetup


_logger = logging.getLogger(__name__)






class AuthSignupHome(Home):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'mobile') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        # lang = request.context.get('lang', '').split('_')[0]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()
    
class AuthSighup(AuthSignupHome):

    def get_auth_signup_qcontext(self):
        SIGN_UP_REQUEST_PARAMS.update({'mobile'})
        return super().get_auth_signup_qcontext()


    #
    # @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    # def web_auth_signup(self, *args, **kw):
    #     res = super(AuthSighup, self).web_auth_signup(*args, **kw)
    #     User = request.env['res.users']
    #     user_sudo = User.sudo().search(
    #              User._get_login_domain(kw.get('login')), order=User._get_login_order(), limit=1
    #          )
    #
    #     http.request.env['op.student'].sudo().create({
    #         'first_name': user_sudo.name,
    #         'middle_name': user_sudo.name,
    #         'last_name': user_sudo.name,
    #         'mobile': user_sudo.partner_id.mobile,
    #         'email': user_sudo.partner_id.email,
    #         'birth_date': '08/13/2022',
    #         'user_id': user_sudo.id,
    #         'partner_id': user_sudo.partner_id.id,
    #         'gender': 'm',
    #         # 'groups_id': [
    #         #     (6, 0,
    #         #      [self.env.ref('base.group_portal').id])]
    #
    #     })
    #
    #     user_sudo.sudo().write({'groups_id': [
    #              (6, 0,
    #               [request.env.ref('base.group_portal').id])]})

        # def create_student_user(self):
        #     user_group = self.env.ref("base.group_portal") or False
        #     users_res = self.env['res.users']
        #     for record in self:
        #         if not record.user_id:
        #             user_id = users_res.create({
        #                 'name': record.name,
        #                 'partner_id': record.partner_id.id,
        #                 'login': record.email,
        #                 'groups_id': user_group,
        #                 'is_student': True,
        #                 'tz': self._context.get('tz'),
        #             })
        #             record.user_id = user_id


        # return res

    # def _signup_with_values(self, token, values):
    #     res = super()._signup_with_values(token, values)
    #     print(res)
    #     return res

    # def do_signup(self, qcontext):
    #     """ Shared helper that creates a res.partner out of a token """
    #     res = super().do_signup(qcontext)
    #     User = request.env['res.users']
    #     user_sudo = User.sudo().search(
    #         User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
    #     )
    #     return res