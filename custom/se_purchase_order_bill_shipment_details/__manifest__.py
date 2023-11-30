# -*- coding: utf-8 -*-

{
    'name': 'Purchase Order Status',
    'category': 'Purchase',
    'version': '15.0',
    'author': 'SprintERP',
    'website': 'http://www.sprinterp.com',
    'summary': """Purchase Order Vendor Bill And Incoming shipment Details""",
    'description': """
        This plugin use for see Vendor Bill And Incoming shipment details in purchase order with new useful filters.
    """,
    'depends': ['purchase_stock','purchase', 'account'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],
    'application': True,
    'installable': True,
    'price': 12,
	'currency': 'USD',
}
