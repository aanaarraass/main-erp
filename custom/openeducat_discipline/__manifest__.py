# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Discipline',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Discipline Rules',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'account',
        'product',
        'openeducat_core_enterprise',
        'openeducat_student_progress_enterprise',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/fine_product_demo.xml',
        'data/discipline_mail_template_data.xml',
        'wizard/take_action_wizard_view.xml',
        'wizard/progression_discipline_wizard_view.xml',
        'views/misbehaviour_category_view.xml',
        'wizard/take_action_wizard_view.xml',
        'views/discipline_record_view.xml',
        'views/suspended_student_view.xml',
        'views/student_view.xml',
        'views/school_offences_view.xml',
        'views/elearning_rules_view.xml',
        'views/openeducat_discipline_portal.xml',
        'views/openeducat_progression_discipline.xml',
        'views/student_progression_discipline_portal.xml',
        'wizard/misbehaviour_type_wizard_view.xml',
        'wizard/student_wise_wizard_view.xml',
        'report/misbehaviour_type_report.xml',
        'report/student_wise_report.xml',
        'report/report_menu.xml',
        'report/discipline_progression_report.xml',
        'menus/op_menu.xml',
        'views/assets.xml',
    ],
    'demo': [
        'demo/misbehave_category_demo.xml',
        'demo/discipline_record_demo.xml',
        'demo/suspended_students_demo.xml',
        'demo/progression_discipline_demo.xml'
    ],
    'images': [
        'static/description/openeducat_discipline_banner.jpg',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_discipline/static/js/load_editore.js'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 298,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
