
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Transportation Enterprise',
    'description': """This module adds feature to manage transportation
    to OpenEduCat.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Transportations',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'contacts',
        'fleet',
        'openeducat_core_enterprise',
        'account',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',

        'data/transportation_fees_cron.xml',

        'views/sequence.xml',
        'views/stop_view.xml',
        'views/route_line_view.xml',
        'views/stop_line_view.xml',
        'views/route_view.xml',
        'views/vehicle_view.xml',
        'views/route_register_view.xml',
        'views/transport_agreement_view.xml',
        'views/plan_view.xml',
        'views/onboard.xml',
        'views/transport_fee.xml',
        'menus/op_menu.xml',

        'report/transport_voucher.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
        'demo/vehicle_demo.xml',
        'demo/route_demo.xml',
        'demo/plan_demo.xml',
        'demo/route_line_demo.xml',
        'demo/route_register_demo.xml',
        'demo/stop_demo.xml',
        'demo/transportation_fees_coll_demo.xml',
        'demo/transportation_agreement_demo.xml',
        'demo/res_demo.xml'
    ],
    'images': [
        'static/description/openeducat_transportation_enterprise_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 208,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
