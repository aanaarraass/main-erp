# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Attendance Enterprise',
    'description': """This module allows you to manage the student attendance.
    You can print absent report for student.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Attendances',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_attendance_report_xlsx',
        'openeducat_attendance',
        'openeducat_core_enterprise',
        'openeducat_student_progress_enterprise',
        'website'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/op_security.xml',
        'wizards/progression_attendance_wizard_view.xml',
        'data/auto_create_attendance_sheet.xml',
        'data/auto_create_attendance_sheet_if_session.xml',
        'views/attendance_sheet_view.xml',
        'views/openeducat_dashboard_view.xml',
        'views/attendance_register.xml',
        'views/onboard.xml',
        'views/openeducat_attendance_portal.xml',
        'views/attendance_line_view.xml',
        'views/openeducat_progression_attendance.xml',
        'views/student_progression_attendance_portal.xml',
        'reports/attendance_progression_report.xml',
        'menu/attendance_portal_menu.xml'
    ],
    'demo': ['demo/progression_attendance_demo.xml',
             'demo/attendance_register_demo.xml'],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [
        'static/description/openeducat_attendance_enterprise_banner.jpg',
    ],
    'assets': {
        'web.qunit_suite_tests': [
            '/openeducat_attendance_enterprise/static/tests/tours/attendance_test.js'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 238,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
