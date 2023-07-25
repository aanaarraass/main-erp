# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


{'name': "OpenEduCat Asset Requests",
 'description': """This module allows you to manage the asset requests easily.
  Admin can allocate assets to students and faculties.""",
 'version': "15.0.1.0",
 'depends': ['openeducat_account_asset',
             'openeducat_core_enterprise',
             'openeducat_parent_enterprise'],
 'category': 'Education',
 "sequence": 3,
 'summary': 'Manage Asset Requests',
 'author': 'OpenEduCat Inc',
 'website': 'http://www.openeducat.org',
 'data': [
     'security/ir.model.access.csv',
     'views/request_assets_views.xml',
     'views/account_assets_views.xml',
     'views/request_reason_views.xml',
     'views/portal_menu_data.xml',
     'views/request_assets_template.xml',
     'menu/menu.xml'],
 'demo': [
     'demo/demo.xml'
 ],
 'assets': {
     'web.assets_tests': [
         "/openeducat_asset_request_enterprise/static/tests/tours/"
         "test_asset_request_detail.js",
         "/openeducat_asset_request_enterprise/static/tests/tours/"
         "test_asset_request_student.js",
         "/openeducat_asset_request_enterprise/static/tests/tours/"
         "test_asset_request.js",
         "/openeducat_asset_request_enterprise/static/tests/tours/"
         "test_request_submit.js",
     ],
 },
 'images': [],
 'installable': True,
 'auto_install': False,
 'application': True,
 'price': 208,
 'currency': 'EUR',
 'license': 'Other proprietary',
 'live_test_url': 'https://www.openeducat.org/plans'
 }
