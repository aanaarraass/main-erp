# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
{
    'name': 'OpenEduCat Assets Management',
    'description': """This module adds the feature of accounting management system to
     OpenEduCat. You can create online course and publish it.""",
    'version': '15.0.1.0',
    'category': 'Accounting',
    'sequence': 12,
    'summary': 'Assets Management',
    'complexity': 'easy',
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['account'],
    'data': [
        'security/account_asset_security.xml',
        'security/ir.model.access.csv',
        'wizard/asset_depreciation_confirmation_wizard_views.xml',
        'wizard/asset_modify_views.xml',
        'views/account_asset_views.xml',
        'views/account_invoice_views.xml',
        'views/product_views.xml',
        'report/account_asset_report_views.xml',
        'data/account_asset_data.xml',
    ],

    'demo': ['demo/account_account_demo.xml'],
    'images': ['static/description/assets.gif'],

    'qweb': [],
    'assets': {
        'web.assets_backend': [
            "/openeducat_account_asset/static/src/js/account_asset.js",
            "/openeducat_account_asset/static/src/scss/account_asset.scss"
        ],
        'web.qunit_suite': [
            "/openeducat_account_asset/static/tests/account_asset_tests.js"
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
