{
    'name': 'OpenEduCat Quiz dran into text',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'website': 'http://www.openeducat.org',
    'summary': 'OpenEduCat Quiz dran into text',
    'author': 'OpenEduCat Inc',
    'depends': ['openeducat_quiz'],
    'data': [
        'views/quiz.xml',
        'views/quiz_bank_view.xml',
        ],
    'demo': [
        'demo/question_bank_drag_into_text.xml',
        'demo/demo_quiz.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_quiz_drag_into_text/static/src/js/index.js',
            '/openeducat_quiz_drag_into_text/static/src/css/style.css'
        ],
        'web._assets_primary_variables': [
        ],
        'web.assets_tests': [
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 199,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
