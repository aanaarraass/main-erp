
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Google Meet',
    'description': """This module allows you to manage and
    create calender online meeting using session on Google Meet.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Meetings using Google Meet',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',

    'depends': ['openeducat_core_enterprise',
                'openeducat_online_tools_enterprise',
                ],

    'data': [
        'security/ir.model.access.csv',
        'data/refresh_ir_cron.xml',
        'data/parameter_data.xml',
        'views/token_view.xml',
        'views/res_config_settings.xml',
        'views/res_users.xml',
        'wizard/google_meet_view.xml',
        'views/google_meeting_view.xml',
        'views/online_meeting_template.xml',
    ],
    'demo': [],

    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 298,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'external_dependencies': {'python': ['google-api-python-client',
                                         'google-auth-httplib2',
                                         'google-auth-oauthlib']},
    'live_test_url': 'https://www.openeducat.org/plans'

}
