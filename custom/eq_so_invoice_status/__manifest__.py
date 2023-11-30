# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################
{
    'name': "Invoice details on Sale order",
    'category': 'Sales',
    'version': '15.0.1.0',
    'author': 'Equick ERP',
    'description': """
        * This module allows to user to see the Invoice state on Sale order.
        * User can see invoice Due amount, Paid amount, Paid amount in Percentage on sale order.
        * User can also search the sale order by Invoice state, Paid amount, Due amount, Paid amount in Percentage.
    """,
    'summary': """Invoice state on Sale order invoice details on sale order invoice state invoice status on sale order invoice status on Sale Order Invoiced Details sales invoice details sale order due amount sale order paid amount Sale order Invoiced Sale Order Status""",
    'depends':['base', 'sale_management'],
    'price': 10,
    'currency': 'EUR',
    'license': 'OPL-1',
    'website': "",
    'data':[
        'views/sale_view.xml',
    ],
    'demo': [],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: