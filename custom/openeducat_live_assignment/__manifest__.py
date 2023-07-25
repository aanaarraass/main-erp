{
    'name': 'OpenEduCat Live Assignment',
    'description': """This module allows you to manage the assignments easily. Faculty
    can create and allocate assignment,it & student can make submission for that.""",
    'version': '15.0.1.0',
    'category': 'Productivity/Discuss',
    'sequence': 145,
    'author': 'OpenEduCat Inc',
    'company': 'OpenEduCat Inc.',
    'summary': 'Manage Attendance Sheet',
    'depends': ['mail', 'openeducat_assignment_enterprise', 'openeducat_live'],
    'website': 'http://www.openeducat.org',
    'data': [
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_qweb': [
            'openeducat_live_assignment/static/src/xml/*.xml',
        ],
        'web.assets_backend': [
            'openeducat_live_assignment/static/src/js/*.js',
            'openeducat_live_assignment/static/src/xml/*.xml',
            'openeducat_live_assignment/static/src/css/*.css',
        ],
        'mail.assets_discuss_public': [
            'openeducat_live_assignment/static/src/js/*.js',
            'openeducat_live_assignment/static/src/xml/*.xml',
            'openeducat_live_assignment/static/src/css/*.css',
        ],
    },
    'price': 199,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
