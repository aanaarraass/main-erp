# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from . import models
from . import wizard
from . import controllers
# from odoo.api import Environment, SUPERUSER_ID
#
#
# def post_init_hook_terminology_settings(cr, registry):
#     env = Environment(cr, SUPERUSER_ID, {})
#     models_str = env['ir.config_parameter'].sudo().get_param('terminology_template')
#     if models_str:
#         res_ids = env['terminology.configuration'].sudo().search([('id', '=', models_str)])
#         res_ids.label_name_change()
