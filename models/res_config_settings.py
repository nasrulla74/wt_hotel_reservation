from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_booking_default_product_id = fields.Many2one(
        'product.product',
        'Deposit Product',
        domain="[('type', '=', 'service')]",
        config_parameter='wt_hotel_reservation.default_booking_deposit_product_id',
        help='Default product used for payment advances')

    booking_default_pricelist_id = fields.Many2one(
        'product.pricelist',
        'Default Price List',
        config_parameter='wt_hotel_reservation.default_booking_default_pricelist_id',
        help='Default price list used for bookings')

    booking_default_hotel_id = fields.Many2one(
        'hotel.hotel',
        'Default Hotel',
        config_parameter='wt_hotel_reservation.default_booking_default_hotel_id',
        help='Default Hotel')