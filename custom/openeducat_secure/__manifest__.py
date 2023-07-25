# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat Secure",
    'description': """This module allows you to create secure qr code.""",
    'version': '15.0.1.0',
    'depends': ['web', 'base', 'openeducat_core_enterprise'],
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'data': [
        'security/ir.model.access.csv',
        'data/parameter_data.xml',
        'views/secure.xml',
        'views/res_config_setting_view.xml',
        'views/error_page.xml',
        'views/qr_code_verify.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_secure/static/src/js/qrcode.js'
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 148,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
