# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat Jitsi Integration",
    'description': """This module use calendar for online meetings.
    This module adds feature to Enable video conferencing with a single click.""",
    'version': '15.0.1.0',
    'summary': 'Jitsi Integration',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'category': 'Education',
    'depends': [
        'calendar',
        'website',
        'openeducat_online_tools_enterprise',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/jitsi_server_data.xml',
        'wizard/meeting_view.xml',
        'views/views.xml',
        'views/res_config_setting_view.xml',
        'views/templates.xml',
        'views/online_meeting_timetable_template.xml',
        'menus/op_menu.xml'
    ],
    'demo': [],
    'qweb': [],
    'css': [],
    'images': ['static/description/module-banner.png', ],
    'assets': {
        'web.assets_frontend': [
            "https://meet.jit.si/external_api.js",
            "/openeducat_jitsi_enterprise/static/src/js/jitsi_room_widget.js",
            "/openeducat_jitsi_enterprise/static/src/js/jitsi_room.js",
        ],
        'web.assets_qweb': [
            '/openeducat_jitsi_enterprise/static/src/xml/templates.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 298,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
