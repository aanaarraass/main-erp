# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Backmate Configuration Base",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Extra Tools",
    "summary": "Backmate Backend Theme, fully functional Backend Theme, flexible Backend Theme, fast Backend Theme, lightweight Backend Theme, animated Backend Theme, modern multipurpose theme Odoo",
    "description": """Are you bored with your standard odoo backend theme? Are You are looking for modern, creative, clean, clear, materialize Odoo theme for your backend? So you are at right place, We have made sure that this theme is highly customizable and it comes with a premium look and feel. Our theme is not only beautifully designed but also fully functional, flexible, fast, lightweight, animated and modern multipurpose theme. Our backend theme is suitable for almost every purpose.""",
    "version": "15.0.3",
    "depends": [
        "base", "base_setup"

    ],
    "application": True,
    "data": [
        "security/base_security.xml",
        "security/ir.model.access.csv",
        "data/theme_config_data.xml",
        "views/back_theme_config_view.xml",
        "views/assets_backend.xml",
        "views/global_search_view.xml",
        "wizard/theme_preview_wizard.xml",

    ],
     'assets': {
       
        'web.assets_backend': [
            'sh_back_theme_config/static/src/scss/fonts.scss',
            
        ],
        
         'web.assets_frontend': [
             'sh_back_theme_config/static/src/scss/fonts.scss',
           
        ],
         'web._assets_primary_variables': [
          ('after', 'web/static/src/legacy/scss/primary_variables.scss', '/sh_back_theme_config/static/src/scss/back_theme_config_main_scss.scss'),        
        ],
    },
     
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 1,
    "currency": "EUR"
}
