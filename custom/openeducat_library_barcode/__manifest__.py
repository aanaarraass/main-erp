# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'Library Barcode Scanning System',
    'description': """This module adds the feature of library management to OpenEduCat.
    You can print media barcode & library id card.""",
    'version': '15.0.1.0',
    'category': 'Education',
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'barcodes',
        'openeducat_library',
        'openeducat_core_enterprise',
    ],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/library_barcode.xml',
        'views/barcode_view.xml',
    ],
    'qweb': [],
    'images': [
        'static/description/openeducat_library_barcode_banner.jpg',
    ],
    'assets': {
        'web.assets_backend': [
            '/openeducat_library_barcode/static/src/js/'
            'library_barcode.js',
            '/openeducat_library_barcode/static/src/scss/'
            'library_barcode.scss'
        ],
        'web.assets_qweb': [
            "/openeducat_library_barcode/static/src/xml/"
            "openeducat_library_barcode_template.xml"
        ],
    },
    'application': True,
    "sequence": 3,
    'price': 298,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
