# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).


{
    "name": "Custom Dashboard",
    "version": "15.0.1.0",
    "summary": """
        Custom Dashboard.
    """,
    'description': """
    Custom Dashboard

    """,
    "category": "Extra Tools",
    'license': 'OPL-1',
    "author": "Kanak Infosystems LLP.",
    "website": "https://www.kanakinfosystems.com",
    "depends": ['base_accounting_kit'],

    'assets': {
        'web.assets_backend': [
            'custom_dashboard_knk/static/src/scss/style.scss',
        ],
        'web.assets_qweb': [
            'custom_dashboard_knk/static/src/xml/template.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
