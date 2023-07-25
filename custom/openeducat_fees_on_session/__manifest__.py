# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Fees On Sesion',
    'description': """This module allows you to set fee duration on session based,
    set subject cost, based on these elements system will create
    an invoice for fees collection""",
    'version': '15.0.1.0',
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'license': 'Other proprietary',
    'depends': ['openeducat_attendance_enterprise',
                'openeducat_fees_enterprise',
                'openeducat_admission_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'views/fees_session_based_view.xml'
    ],
    'demo': [
        'demo/product_demo.xml',
        'demo/fees_element_line_demo.xml',
        'demo/fees_terms_line_demo.xml',
        'demo/fees_terms_demo.xml',
        'demo/faculty_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
