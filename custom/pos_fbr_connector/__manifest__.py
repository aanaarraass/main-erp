# -*- coding: utf-8 -*-
{
    'name': "Odoo POS FBR Cnnector",

    'summary': """
        Send POS Order detail to FBR to pay sales tax""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cybat",
    'website': "https://www.cybat.net",

    'category': 'POS',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'views/pos_config.xml',
        'views/pos_order.xml',
        'views/product.xml',
        'views/cron.xml',
        'views/templates.xml',
        'views/ir_action_server.xml'
    ],
    # 'pos_fbr_connector/static/src/css/pos.css'
    'assets': {
        'point_of_sale.assets': [
            'pos_fbr_connector/static/src/css/pos.css',
            'pos_fbr_connector/static/src/js/pos.js'
        ],
        'web.assets_qweb': [
            'pos_fbr_connector/static/src/xml/**/*',
        ],
    },

    "qweb":["static/src/xml/pos.xml"],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    # 'images': ['static/description/background.png',],
    "price": 100,
    "currency": "EUR"
}
