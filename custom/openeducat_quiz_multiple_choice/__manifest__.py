{
    'name': 'OpenEduCat Quiz match images',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'website': 'http://www.openeducat.org',
    'summary': 'OpenEduCat Quiz match the images',
    'depends': ['openeducat_quiz'],
    'data': [
        'security/ir.model.access.csv',
        'views/quiz_website_match_following.xml',
        'views/quiz_website_inherit.xml',
        'views/quiz_bank_view.xml',
    ],
    'demo': [
        'demo/demo_quiz_multiple_choice.xml',
        'demo/question_bank_demo.xml'
    ],
    'assets': {
        'web._assets_primary_variables': [
        ],
        'web.assets_backend': [
        ],
        'web.assets_frontend': [
            '/openeducat_quiz_multiple_choice/static/src/js/index.js',
            '/openeducat_quiz_multiple_choice/static/src/css/style.css',
        ],
        'web.assets_tests': [
        ],
        'web.qunit_suite_tests': [
        ],
        'web.assets_qweb': [
        ],
    },
    'installable': True,
    'qweb': [
    ],
    'auto_install': False,
    'application': True,
    'price': 199,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
