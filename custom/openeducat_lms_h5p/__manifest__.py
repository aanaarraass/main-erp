{
    'name': 'OpenEduCat LMS H5P',
    'description': """This module allows you to add videos, quizzes, and presentations
    directly via the H5p platform.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'summary': 'OpenEduCat LMS H5P',
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_lms',
    ],
    'data': [
        'views/course_material_view.xml',
        'views/material_view_details.xml',
        'views/course_detail.xml',

    ],
    'demo': [
        'demo/op_course_demo.xml',
    ],
    'images': [
        'static/description/h5p_icon.png',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_frontend': ['/openeducat_lms_h5p/static/src/js/material_upload.js',
                                '/openeducat_lms_h5p/static/src/scss/lms_h5p.scss',
                                ],
        'web.assets_qweb': [
            '/openeducat_lms_h5p/static/src/xml/*.xml'
        ],
    },
    'license': 'Other proprietary',
    'price': 150,
}
