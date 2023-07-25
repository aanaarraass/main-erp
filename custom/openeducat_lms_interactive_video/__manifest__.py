{
    'name': 'OpenEduCat lms interactive video',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'website': 'http://www.openeducat.org',
    'summary': 'OpenEduCat lms interactive video',
    'author': 'OpenEduCat Inc',
    'depends': ['openeducat_lms', 'openeducat_quiz'],
    'data': [
        'security/ir.model.access.csv',
        'views/course_view.xml',
        'views/material_detail_view_inherit.xml',
        ],
    'demo': [
        'demo/iv-demo.xml',
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_lms_interactive_video/static/src/js/index.js',
            '/openeducat_lms_interactive_video/static/src/css/style.css'
        ],
        'web._assets_primary_variables': [
        ],
        'web.assets_tests': [
        ]
    },
    'installable': True,
    'qweb': [],
    'auto_install': False,
    'application': True,
    'price': 199,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
