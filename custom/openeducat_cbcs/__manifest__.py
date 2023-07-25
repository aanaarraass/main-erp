# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat Cbcs",
    'description': """This module allows you to give credit points based on choice.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'sequence': 3,
    'summary': "Openeducat Cbcs""",
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_admission',
        'openeducat_admission_enterprise',
        'openeducat_core_enterprise'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/course_credit_view.xml',
        'views/sem_credit_view.xml',
        'views/op_subject.xml',
        'views/subject_credit_view.xml',
        'views/op_subject_registration_portal_inherit.xml',
        'menus/op_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_cbcs/static/src/js/selection.js',
        ],
    },
    'demo': [
        'demo/course_credit.xml',
    ],
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
