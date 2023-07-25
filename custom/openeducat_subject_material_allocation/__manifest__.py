
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Subject Material Allocation',
    'description': """This module provides the facility of the
    specific subject material allocation which help the admin and faculty
    to add material to the subject so that the student has
    can download the material and see their study material
    by logging into their account.""",
    'version': '15.0.1.0',
    'category': 'Education',
    "sequence": 4,
    'summary': 'Manage Subject Matterial',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_core_enterprise',

    ],
    'data': [
        'menus/study_material_portal_menu.xml',
        'views/openeducat_subject_material.xml',
    ],
    'demo': ['demo/demo_subject_material1.xml',
             'demo/demo_subject_registration.xml'],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_tests': [
            'openeducat_subject_material_allocation/static/tests/tours/**/*'],
    },
    'price': 50,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
