{
    'name': 'OpenEduCat Live',
    'description': """OpenEduCat Live is very important part of
    any educational institute. OpenEduCat Live module from OpenEduCat helps you managing
    all type of the Meeting.""",
    'version': '15.0.1.0',
    'category': 'Productivity/Discuss',
    'sequence': 145,
    'author': 'OpenEduCat Inc',
    'company': 'OpenEduCat Inc.',
    'summary': 'Manage Password Protected Meeting',
    'depends': ['base', 'mail', 'openeducat_core_enterprise',
                'openeducat_meeting_enterprise',
                'openeducat_online_tools_enterprise'],
    'website': 'http://www.openeducat.org',
    'data': [
        'security/ir.model.access.csv',
        'security/openeducat_live_security.xml',
        'views/calendar_event.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_qweb': [
            'openeducat_live/static/src/xml/*.xml',
        ],
        'web.assets_backend': [
            'openeducat_live/static/src/js/*.js',
            'openeducat_live/static/src/widgets/*.js',
            'openeducat_live/static/src/css/*.css',
            'openeducat_live/static/src/scss/*.scss',
            'openeducat_live/static/src/create_meet_calendar/create_meet_calendar.js',
        ],
        'mail.assets_discuss_public': [
            'openeducat_live/static/src/js/*.js',
            'openeducat_live/static/src/xml/*.xml',
            'openeducat_live/static/src/css/*.css',
            'openeducat_live/static/src/scss/*.scss',
        ],
    },
    'price': 598,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
