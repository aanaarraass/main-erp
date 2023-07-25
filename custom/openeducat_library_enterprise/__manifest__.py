
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Library Enterprise',
    'description': """This module adds the feature of library management to OpenEduCat.
    You can print media barcode & library id card.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Library',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_library',
        'openeducat_core_enterprise',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'wizards/barcode_issue_media_view.xml',
        'views/media_view.xml',
        'views/media_unit_view.xml',
        'views/media_movement_view.xml',
        'views/library_view.xml',
        'views/publisher_view.xml',
        'views/author_view.xml',
        'views/media_type_view.xml',
        'views/library_dashboard_view.xml',
        'views/openeducat_library_portal.xml',
        'views/library_onboard.xml',
        'views/media_queue_request.xml',
        'views/media_purchase_request.xml',
        'views/openeducat_student_library_portal.xml',
        'menu/library_portal_menu.xml'
    ],
    'demo': [
    ],
    'images': [
        'static/description/openeducat_library_enterprise_banner.jpg',
    ],
    'qweb': [],
    'assets': {
        'web.assets_tests': [
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_queue_request_submit_test.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_test.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_queue_request.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/queue_list_test.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_purchase_request_test.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_purchase_list_test.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_movement_list_test.js',
            '/openeducat_library_enterprise/'
            'static/tests/tours/media_movement_information_test.js',
        ],
        'web.assets_frontend': [
            '/openeducat_library_enterprise/static/src/js/datepicker.js'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 208,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
