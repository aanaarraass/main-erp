{
    'name': 'OpenEduCat Quiz sort the paragraphs',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'website': 'http://www.openeducat.org',
    'summary': 'OpenEduCat Quiz sort the paragraphs',
    'author': 'OpenEduCat Inc',
    'depends': ['openeducat_quiz'],
    'data': [
        'security/ir.model.access.csv',
        'views/quiz.xml',
        'views/quiz_bank_view.xml',
        'views/quiz_website.xml',
        ],
    'demo': [
        'demo/quiz.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_quiz_sort_paragraphs/static/src/js/index.js',
            '/openeducat_quiz_sort_paragraphs/static/src/css/style.css'
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
