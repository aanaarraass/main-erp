
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Mass Subject Registration',
    'description': """This module allows you to manage the admission
    process via subjects selection.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage Students can Add Multiple Subjects',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_core_enterprise',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/subjects_registration_wizard_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 300,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
