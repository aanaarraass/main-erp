
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Campus Enterprise',
    'description': """This module allows you to manage campus.
    You can define the facility capacity.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Campus',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'account',
        'openeducat_core_enterprise',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'wizard/facility_create_invoice_view.xml',
        'views/facility_type_view.xml',
        'views/facility_allocation_view.xml',
        'views/facility_view.xml',
        'views/onboard.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
        'demo/facility_type_demo.xml',
        'demo/facility_demo.xml',
        'demo/facility_allocation_demo.xml',
    ],
    'test': [],
    'images': [
        'static/description/openeducat_campus_enterprise_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 238,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
