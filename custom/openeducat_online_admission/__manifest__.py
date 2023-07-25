# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Online Admission',
    'version': '15.0.1.0',
    'description': """This module allows you to get online application
    using web page.""",
    'category': 'Education',
    "sequence": 3,
    'summary': 'Online Admission',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'website_sale',
        'website_payment',
        'openeducat_admission',
        'openeducat_core_enterprise'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/admission_view.xml',
        'views/course_view.xml',
        'views/admission_website_view.xml',
        'views/admission_registration_other.xml',
        'views/student_registration_details_portal.xml',
        'views/uoj_application.xml',
        'views/report_menu.xml',
        'data/admission_portal_menu.xml',
        'data/mail_data.xml',
        'data/quotation_&_saleorder_portal_menu.xml',
    ],
    'images': [
        'static/description/openeducat_online_admission_banner.jpg',
    ],
    'demo': ['demo/product_demo.xml',
             'demo/op_course_demo.xml',
             'demo/subject_demo.xml',
             'demo/admission_register_demo.xml',
             'demo/batch_demo.xml',
             'demo/student_course_demo.xml', ],
    'css': [],
    'qweb': [],
    'js': [
        'static/src/js/custome.js'
    ],
    'assets': {
        'web.assets_tests': [
            '/openeducat_online_admission/'
            'static/tests/tours/test_admission_registration.js'
        ],
        'web.assets_frontend': [
            '/openeducat_online_admission/static/src/js/custome.js',
            '/openeducat_online_admission/static/src/js/datepicker.js'
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
