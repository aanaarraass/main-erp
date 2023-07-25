# Copyright 2020 Lorenzo Battistini @ TAKOBI
# Copyright 2020 Tecnativa - Alexandre D. Díaz
# Copyright 2020 Tecnativa - João Marques
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Progressive web application",
    "summary": "Make Odoo a PWA",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Website",
    "website": "https://github.com/OCA/web",
    "author": "TAKOBI, Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "depends": ["web", "mail"],
    "assets": {
            'web.assets_backend': [
                'web_pwa_oca/static/src/pwa_manager.js',
                'web_pwa_oca/static/src/webclient.js',
                # ("remove", "web_cohort/static/src/legacy/**/*"),
            ],
        },
    "data": ["templates/assets.xml", "views/res_config_settings_views.xml"],
    "images": ["static/description/pwa.png"],
}
