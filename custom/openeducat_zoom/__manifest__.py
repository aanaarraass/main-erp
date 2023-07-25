
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Zoom Integration',
    'description': """This module allows you to manage
    and create calender online meeting using session on Zoom.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Zoom',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_web',
        'openeducat_online_tools_enterprise',
    ],
    'data': [
        'security/ir.model.access.csv',
        "data/parameter_data.xml",
        "wizard/meeting_view.xml",
        "views/online_meeting_timetable_template.xml",
        "views/res_config_setting_view.xml",
        'views/res_users_views.xml',
        "views/calender_event.xml",
        "menus/op_menu.xml",

    ],
    'images': [
        'static/description/icon.jpg',
    ],
    'demo': [],
    'css': [],
    'qweb': [],
    'js': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 298,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
