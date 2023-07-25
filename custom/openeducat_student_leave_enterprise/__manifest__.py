# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat Student Leave Enterprise",
    'description': """This module aims to manage student's leave requests
    and keeps account of the leaves of the students.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'sequence': 3,
    'summary': "Manage Student Leave""",
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'mail',
        'openeducat_core_enterprise',
        'openeducat_web'],
    'data': [
        'security/ir.model.access.csv',
        'data/leave_request_number.xml',
        'security/op_security.xml',
        'views/leave_type_view.xml',
        'views/student_leave_request_view.xml',
        'views/student_leave_portal.xml',
        'menu/op_menus.xml',
        'menu/portal_menu_data.xml'
    ],
    'demo': ['demo/leave_type_demo.xml',
             'demo/student_leave_request_demo.xml'],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_student_leave_enterprise/static/src/js/date_validation.js',
            '/openeducat_student_leave_enterprise/static/src/js/datepicker.js'
        ],
        'web.assets_tests': [
            'openeducat_student_leave_enterprise/'
            'static/tests/tours/student_leave_test.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 75,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
