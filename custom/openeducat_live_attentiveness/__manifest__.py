{
    'name': 'OpenEduCat Live Attentiveness',
    'description': """OpenEduCat Live Attentiveness is very important part of
    any educational institute.During an event, the host can use the attention tracking
    feature to monitor if attendees are focused on the presentation.
    The attention indicator shows in sidebar.""",
    'category': 'Productivity/Discuss',
    'sequence': 145,
    'author': 'OpenEduCat Inc',
    'company': 'OpenEduCat Inc.',
    'summary': 'Manage Attentiveness',
    'depends': ['mail', 'calendar', 'openeducat_live'],
    'website': 'http://www.openeducat.org',
    'data': [
        'views/calendar_event.xml',
        'views/op_logs_attentive_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_qweb': [
            'openeducat_live_attentiveness/static/src/xml/*.xml',
        ],
        'web.assets_backend': [
            'openeducat_live_attentiveness/static/src/js/*.js',
            'openeducat_live_attentiveness/static/src/xml/*.xml',
        ],
        'mail.assets_discuss_public': [
            'openeducat_live_attentiveness/static/src/js/*.js',
            'openeducat_live_attentiveness/static/src/xml/*.xml',
        ],
    },
    'price': 99,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
