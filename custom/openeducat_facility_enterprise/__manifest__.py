
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Facility Enterprise',
    'description': """This module adds the feature to manage facilities
    to OpenEduCat.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Facility',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_facility',
        'openeducat_core_enterprise',
    ],
    'data': [
        'security/op_security.xml',
        'views/facility_view.xml',
        'views/facility_line_view.xml',
    ],
    'demo': [
    ],
    'images': [
        'static/description/openeducat_facility_enterprise_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 50,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
