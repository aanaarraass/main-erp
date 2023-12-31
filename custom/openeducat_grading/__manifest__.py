# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Grading',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Grading',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core_enterprise',
                'openeducat_student_progress_enterprise',
                'openeducat_assignment_enterprise',
                'openeducat_attendance_enterprise'],

    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/gradebook_sequence.xml',
        'data/report_paperformat.xml',
        'data/op_grade_table_line_data.xml',
        'data/op_grade_table_data.xml',
        'data/gradebook_portal_menu.xml',
        'wizard/assignment_wizard_view.xml',
        'wizard/grading_wizard.xml',
        'views/op_grade_type_view.xml',
        'views/op_grade_scale_view.xml',
        'views/op_grade_table_line_view.xml',
        'views/op_grade_table_view.xml',
        'views/op_grade_template_line_view.xml',
        'views/op_grade_template_view.xml',
        'views/subterm_weight_line_view.xml',
        'views/assignment_type_weight_line_view.xml',
        'views/attendance_type_line_view.xml',
        'views/op_batch_view.xml',
        'views/op_student_view.xml',
        'views/op_course_view.xml',
        'views/op_subject_view.xml',
        'views/gradebook_gradebook_view.xml',
        'views/gradebook_line_view.xml',
        'views/grading_assignment_view.xml',
        'views/student_grade_progress_view.xml',
        'views/op_grade_override_line_view.xml',
        'views/grade_book_portal_view.xml',
        'views/statistics_view.xml',
        'views/student_statistics_view.xml',
        'views/op_honorroll.xml',
        'views/op_honorroll_line_view.xml',
        'menus/op_menu.xml',
        'report/report_menu.xml',
        'report/student_grade_report.xml',
        'report/student_transcript.xml',
        'report/honour_roll_report.xml',
        'report/honor_roll_list.xml',
    ],
    'demo': [
        'demo/op_grade_type_demo.xml',
        'demo/op_grade_scale_demo.xml',
        'demo/assignment_type_weight_line_demo.xml',
        'demo/op_grade_template_demo.xml',
        'demo/op_grade_template_line_demo.xml',
        'demo/grading_assignment_demo.xml',
        'demo/gradebook_line_demo.xml',
        'demo/op_course_demo.xml',
        'demo/gradebook_demo.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            '/openeducat_grading/static/src/js/grade_book_grid_view.js',
            '/openeducat_grading/static/src/js/gradebook_by_course.js',
            '/openeducat_grading/static/src/js/gradebook_by_batch.js',
            '/openeducat_grading/static/src/js/grade_book_by_subject.js',
            '/openeducat_grading/static/src/css/handsontable.full.min.css',
            '/openeducat_grading/static/src/css/grid_view.css'
        ],
        'web.assets_frontend': [
            '/openeducat_grading/static/src/js/grade_book_portal.js',
            '/openeducat_grading/static/src/css/handsontable.full.min.css',
            '/openeducat_grading/static/src/css/grid_view.css', ],
        'web.assets_qweb': [
            'openeducat_grading/static/src/xml/**/*',
        ],
    },
    'application': True,
    'price': 748,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
