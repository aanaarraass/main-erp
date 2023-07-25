# -*- coding: utf-8 -*-
{
    'name': "UOJ Fee Management",

    'summary': """
        this modules handles fee management structure
       
        """,

    'description': """
       
    """,

    'author': "JTS",
    'website': "http://www.jtstorm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['openeducat_core','openeducat_admission'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/entry_test_fee.xml',
        'views/register_fee.xml',
        'views/fee_installment_line.xml',
        'views/student_contract.xml',
        'views/register_fee_quota.xml',
        'views/templates.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
