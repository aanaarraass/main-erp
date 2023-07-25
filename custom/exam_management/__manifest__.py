# -*- coding: utf-8 -*-
{
    'name': "Exam Management",

    'summary': """
       
        """,

    'description': """
       
    """,

    'author': "JTS",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/academic_calendar.xml',
        'views/exam_exam.xml',
        'views/exam_room.xml',
        'views/timetable_request.xml',
        'views/exam_sittingplan.xml',
        'views/exam_result.xml',
        'views/exam_timeslots.xml',
        'views/templates.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
