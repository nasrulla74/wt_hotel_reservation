# -*- coding: utf-8 -*-

{
    "name": "Hotel Reservation 1.6.3",
    "version": "1.6.3",
    "category": "Hotel Reservation",
    "summary": "Hotel Reservation",
    "description": """
        Hotel Reservation for Hotels, Guest Houses
    """,
    "author": "Appeul - Solutions",
    "website": "http://appeul.com",
    "support": "info@appeul.com",
    "depends": ['base', 'account', 'utm', 'rating', 'sale', 'web_timeline'],
    "data": [
        'security/ir.model.access.csv',
        'data/booking_number.xml',
        'views/configuration_view.xml',
        'views/hotel_room_type.xml',
        'views/hotel_room_view.xml',
        'views/room_category.xml',
        'views/hotel_view.xml',
        'views/sale_booking_view.xml',
        'views/menus.xml',
        'views/pricelist.xml',
        'views/res_config.xml',
        'views/sales_order_inherit.xml',
        'views/booking_timeline.xml',

    ],
    'assets': {},
    'qweb': [],
    "price": 250,
    'currency': 'USD',
    "images": ['static/images/appeul_logo.png'],
    "license": "OPL-1",
    "installable": True,
    "application": True,
    "auto_install": False,
    'external_dependencies': {},
}
