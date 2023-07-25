{
    'name': 'OpenEduCat Online Appointments',
    'description': """This module allows you to create appointment with assigned
    timezone, location and duration. Also allocate staff based on random,
    customer selection and direct appointment link with particular staff.
    Add slots,message and all types of questions to the appointment.""",
    'version': '15.0.1.0',
    'category': 'Website',
    "sequence": 3,
    'summary': 'Online appointments',
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['calendar', 'hr', 'website',
                'openeducat_core_enterprise', 'openeducat_qna_mixin'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'data/menu.xml',
        'views/calendar_online_appointment_view.xml',
        'views/calendar_view.xml',
        'views/appointment_template.xml',
    ],
    'demo': [
        'demo/slot.xml',
        'demo/appointment.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/openeducat_online_appointment/static/src/'
            'scss/custom.scss',
            '/openeducat_online_appointment/static/src/'
            'scss/simple-calendar.scss',
            '/openeducat_online_appointment/static/src/'
            'css/rangecalendar.css',
            '/openeducat_online_appointment/static/src/'
            'css/style.css',
            '/openeducat_online_appointment/static/src/'
            'tests/tours/booking_test.js',
            '/openeducat_online_appointment/static/src/'
            'tests/tours/booking_cancel_test.js',
            '/openeducat_online_appointment/static/src/'
            'js/jquery.simple-calendar.js',
            '/openeducat_online_appointment/static/src/'
            'js/jquery.rangecalendar.js',
            '/openeducat_online_appointment/static/src/'
            'js/custom.js'
        ],
        'web.assets_backend': [
            '/openeducat_online_appointment/static/src/js/appointment_access_url.js'
        ],
        'web.assets_qweb': [
            '/openeducat_online_appointment/static/src/xml/*.xml'
        ],
    },
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 298,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
