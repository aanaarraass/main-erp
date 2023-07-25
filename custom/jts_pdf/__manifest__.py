# -*- coding: utf-8 -*-
{
    'name': "JTS Pdf",

    'summary': """
        pdf report for invoice
       
        """,

    'description': """
        
    """,

    'author': "My Company",
    'website': "http://www.jtstorm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/pos_pdf_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
