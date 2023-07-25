
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat CRM Enterprise',
    'description': """Based on best of class enterprise level architecture,
    OpenEduCat is ready to be used from local infrastructure
    to a highly scalable cloud environment.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Convert Lead to Student',
    'complexity': "easy",

    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'crm',
        'openeducat_admission_enterprise',
    ],
    'data': ['security/ir.model.access.csv',
             'wizard/crm_lead_to_student.xml',
             'views/crm_lead_view_inherit.xml',
             'views/student_view_inherit.xml'],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 50,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
