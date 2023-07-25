# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat OMR",
    'description': """This module adds the feature of Omr scanner to OpenEduCat.
    You can print Omr for exam & scan omr with your mobile and get result.""",
    'version': '15.0.1.0',
    'depends': ['base', 'website', 'mail',
                'portal',
                'openeducat_core',
                'openeducat_web'],
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'data': [
        'security/ir.model.access.csv',
        'wizard/template_wizard_view.xml',
        'reports/report_menu.xml',
        'reports/layout_hundred.xml',
        'views/omr_exam_view.xml',
        'views/omr_exam_portal_view.xml',
        'views/omr_template_view.xml',
        'views/answer_set_view.xml',
        'views/question_answer_view.xml',
        'views/answer_sheets_view.xml',
        'views/omr_image_view.xml',
        'views/answersheet_configuration_view.xml',
        'menus/openeducat_enterprise_omr_menu.xml',
        'data/omr_data.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [
        'demo/op_omr_answersheet_demo1.xml',
        'demo/op_omr_answersheet_demo2.xml',
        'demo/op_omr_answersheet_demo3.xml',
        'demo/op_omr_exam_demo1.xml',
        'demo/op_omr_exam_demo2.xml',
        'demo/op_omr_exam_demo3.xml',
        'demo/op_omr_student_sheet_image.xml',
        'demo/op_omr_student_result_demo1.xml',
        'demo/op_omr_student_result_demo2.xml',
        'demo/op_omr_student_result_demo3.xml',
    ],
    'images': [
        'static/src/img/cam.png',
        'static/src/img/circle2.png',
        'static/src/img/omr_marker.jpg',
        'static/src/img/square.png',
    ],
    'assets': {
        'web.assets_backend': [
            '/openeducat_omr/static/src/css/qr_template_design.css',
            '/openeducat_omr/static/src/js/omr_cam_widget.js',
            '/openeducat_omr/static/src/lib/webcam.js',
        ],
        'web.assets_qweb': [
            'openeducat_omr/static/src/xml/web_widget_image_webcam.xml',
        ],
    },
    'external_dependencies': {'python': ['opencv-python',
                                         'imutils',
                                         'numpy',
                                         'pillow',
                                         'matplotlib']},
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 448,
    'currency': 'EUR',
    'license': 'Other proprietary',

}
