 
{
    'name': 'POS restaurant depend',
    'category': 'Website',
    'version': '15.0.1.0.0',
    'author': 'Terabits Technolab ',
    'website': 'https://www.terabits.xyz',
    'summary': 'This module contains pos restaurant-related customizations depending on delight_pos_theme_bits',
    'description': """ This module contains pos restaurant-related customizations depending on delight_pos_theme_bits """,
    'depends': [
        'pos_restaurant',   
    ],
    'assets': {
        
        'point_of_sale.assets': [   
            'pos_restaurant_depends_bits/static/src/xml/FloorScreen.xml',
            'pos_restaurant_depends_bits/static/src/js/FloorScreen.js',
            'pos_restaurant_depends_bits/static/src/js/TableWidget.js',
            'pos_restaurant_depends_bits/static/src/js/FloorScreenMenu.js',            
        ],
        'web.assets_qweb': [  
            'pos_restaurant_depends_bits/static/src/xml/FloorScreenMenu.xml', 
            'pos_restaurant_depends_bits/static/src/xml/Chrome.xml'
        ],
        
    },
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1', 
}
