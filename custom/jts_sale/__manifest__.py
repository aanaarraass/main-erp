# -*- coding: utf-8 -*-
{
    'name': "jts_sale",

    'summary': """
        this modules hides the price unit and subtotal in sale order
       
        """,

    'description': """
        this modules hides the price unit and subtotal in sale order and invoice 
        only group (Sale Lines Prices/Sale Unit Price) members can see those fields.
        more over it changes the sale menu name as inventory request
    """,

    'author': "My Company",
    'website': "http://www.jtstorm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/account_invoice.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
