# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat Admission subject",
    'description': """This module allows you to manage admission
    process via subjects.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'sequence': 3,
    'summary': "Manage Admissions Subject""",
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_admission',
        'openeducat_admission_enterprise',
        'openeducat_core_enterprise',
        'openeducat_cbcs',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/subject_view_inherit.xml',
    ],
    'assets': {
        'web.assets_frontend': [],
    },
    'demo': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 75,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
