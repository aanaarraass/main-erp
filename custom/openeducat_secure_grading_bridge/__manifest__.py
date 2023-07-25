# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': "OpenEduCat Secure Grading Bridge",
    'description': """This module allows you to create secure qr code
    for grade book.""",
    'version': '15.0.1.0',
    'depends': ['web', 'base', 'openeducat_core_enterprise',
                'openeducat_grading', 'openeducat_secure'],
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',

    'data': [
        'report/student_transcript.xml',
        'report/student_grade_report.xml',
        'views/model_templates.xml'
    ],
    'demo': [
        'demo/gradebook_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'Other proprietary',
}
