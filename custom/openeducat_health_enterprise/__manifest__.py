
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Health Enterprise',
    'description': """This module allows you to manage health details
    for students and faculties.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Health',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_core_enterprise'
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/health_view.xml',
        'views/openeducat_health_portal.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/health_line_demo.xml',
        'demo/health_demo.xml',
    ],
    'images': [
        'static/description/openeducat_health_enterprise_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 87,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
