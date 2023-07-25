# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Student Attendance Face Recognition',
    'description': """This module aims to manage student's attendances.
    Keeps account of the attendances of the students .""",
    'version': '15.0.1.0',
    'category': 'Tools',
    "sequence": 3,
    'summary': 'Track student attendance from a '
               'image or a video frame',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_core',
        'openeducat_attendance_enterprise',
        'openeducat_student_attendance_enterprise'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/student_attendance_view.xml',
        'menus/op_student_face_recognition_menus.xml',
    ],
    'images': [
        'static/description/img/green_mark.png'
        'static/description/img/red-tick.png'
    ],
    'assets': {
        'web.assets_backend': [
            'openeducat_attendance_face_recognition/static/src/css/webcam.css',
            'openeducat_attendance_face_recognition/static/src/js/face_control.js',
            'openeducat_attendance_face_recognition/static/src/js/face_mode.js',
            'openeducat_attendance_face_recognition/'
            'static/src/js/face_authentication.js',
            'openeducat_attendance_face_recognition/static/src/js/cam_widget.js',
        ],
        'web.assets_qweb': [
            'openeducat_attendance_face_recognition/static/src/xml/attendance.xml',
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
