{
    'name': 'OpenEduCat Live Attendance',
    'description': """OpenEduCat Live Attendance is very important part of
    any educational institute. OpenEduCat Live Attendance module from OpenEduCat
    helps you manage attendance of student in meeting.""",
    'version': '15.0.1.0',
    'category': 'Productivity/Discuss',
    'sequence': 145,
    'author': 'OpenEduCat Inc',
    'company': 'OpenEduCat Inc.',
    'summary': 'Manage Attendance Sheet',
    'depends': ['mail', 'openeducat_attendance', 'openeducat_live'],
    'website': 'http://www.openeducat.org',
    'data': [
        'views/calendar_event.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_qweb': [
            'openeducat_live_attendance/static/src/xml/*.xml',
        ],
        'web.assets_backend': [
            'openeducat_live_attendance/static/src/js/*.js',
            'openeducat_live_attendance/static/src/xml/*.xml',
        ],
        'mail.assets_discuss_public': [
            'openeducat_live_attendance/static/src/js/*.js',
            'openeducat_live_attendance/static/src/xml/*.xml',
        ],
    },
    'price': 199,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
