# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'Openeducat Terminology',
    'description': """This module allows you to Configure the terminology.""",
    'version': "15.0.1.0",
    'summary': 'Manage Terminology',
    "sequence": 3,
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': ['web', 'openeducat_core_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'data/college_subject_data.xml',
        'wizard/wizard_terminology_view.xml',
        'views/res_config_setting_view.xml',
        'views/terminology_configuration_views.xml',
        'menu/menu.xml',
    ],

    'images': [],
    'installable': True,
    'auto_install': True,
    # 'post_init_hook': 'post_init_hook_terminology_settings',
    'license': 'LGPL-3',
    'application': True,
    'live_test_url': 'https://www.openeducat.org/plans'
}
