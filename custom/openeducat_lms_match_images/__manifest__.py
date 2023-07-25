{
    'name': 'OpenEduCat LMS Quiz match the images',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure to
    a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'website': 'http://www.openeducat.org',
    'summary': 'OpenEduCat LMS Quiz match the images',
    'depends': ['openeducat_quiz', 'openeducat_quiz_match_images',
                'openeducat_lms'],
    'data': [
        'security/ir.model.access.csv',
        'views/website_lms_match_following_images.xml'
        ],

    'demo': [],
    'installable': True,
    'qweb': [
    ],
    'auto_install': True,
    'application': True,
    'price': 199,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
