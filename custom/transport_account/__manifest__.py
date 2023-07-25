# -*- coding: utf-8 -*-
{
    'name': "Transport Account",

    'summary': """
        this modules sets the journal and account  for transport fee
       
        """,

    'description': """
       
    """,

    'author': "My Company",
    'website': "http://www.jtstorm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'openeducat_transportation_enterprise'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/agreement_account.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
