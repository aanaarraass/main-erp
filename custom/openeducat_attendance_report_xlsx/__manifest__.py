# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    "name": "Openeducat Attendance Report Xlsx",
    'description': """This module allows you to manage the student attendance.
    You can print absent report in xlsx format for student.""",
    "summary": "Openeducat Attendance Report Xlsx module to create xlsx report",
    "author": "OpenEduCat Inc",
    "website": "http://www.openeducat.org",
    "category": "Education",
    "version": "15.0.1.0",
    "license": "Other proprietary",
    "external_dependencies": {"python": ["xlsxwriter", "xlrd"]},
    "depends": ["base", "web"],
    "data": [
        "menu/report.xml"
    ],
    'assets': {
        'web.assets_backend': [
            '/openeducat_attendance_report_xlsx/'
            'static/src/js/report/action_manager_report.js'
        ]
    },
    "demo": [],
    "installable": True,
}
