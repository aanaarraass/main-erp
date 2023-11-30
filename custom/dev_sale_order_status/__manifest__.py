# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################

{
    'name': 'Sale Order Status',
    'version': '15.0.0.0',
    'category': 'Sales',
    'summary': 'odoo app will show Partial Ship, Delivery, Partial Invoice and Invoice Status on Sale OrderSale order status , sale status , Partial delivered, Partial Ship, Delivered, Partial Invoice, Partial paid, Invoiced, sale delivery,sale invoice, Sale partial',
    'description': """
       odoo app will show Partial Ship, Delivery, Partial Invoice and Invoice Status on Sale Order
Sale order status , sale status , Partial delivered, Partial Ship, Delivered, Partial Invoice, Partial paid, Invoiced, sale delivery, sale invoice, Sale partial , Sale Invoice Status, sale Delivery Status

Sale Order Status
Odoo sale order status
Sale order status odoo app
Sale order status odoo apps
Partial Ship, Delivery, Partial Invoice and Invoice Status on Sale Order
Odoo Partial Ship, Delivery, Partial Invoice and Invoice Status on Sale Order
Print order status
Odoo print order status
Print order status odoo app
Print order status odoo apps
    """,
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale_management', 'sale_stock'],
    'data': [
        'view/sale_view.xml',
        ],
    'demo': [],
    'test': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'css': [],
    'js': [],
    'qweb': [],
    'price':12.00,
    'currency':'EUR',  
    'live_test_url':'https://youtu.be/2Eg_3lzy6oc',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
