# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Skype Meet Integration',
    'description': """This module allows you to manage and
    create calender online meeting using session on Skype meeting.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Skype Meet Integration with OpenEduCat',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_web',
        'openeducat_online_tools_enterprise',
    ],
    'data': [
        'security/ir.model.access.csv',
        "wizard/meeting_view.xml",
        "views/online_meeting_timetable_template.xml",
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
