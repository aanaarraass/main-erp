{
    'name': 'OpenEduCat LMS Quiz match the following',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'website': 'http://www.openeducat.org',
    'summary': 'OpenEduCat LMS Quiz match the following',
    'author': 'OpenEduCat Inc',
    'depends': ['openeducat_quiz', 'openeducat_quiz_match_following', 'openeducat_lms'],
    'data': [
        'views/website_lms_match_following.xml'
        ],

    'demo': [],
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
