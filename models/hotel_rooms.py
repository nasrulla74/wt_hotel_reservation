# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class roomcategory(models.Model):
    _name = "room.category"
    _description = "room category"

    name = fields.Char(string="Room Category", required=True)
    size = fields.Char(string="Room Size")
    featured_image = fields.Image(string="Room Featured Image")
    room_type_ids = fields.One2many('product.product', 'hotel_id', string="Room Type", domain="[('is_room_type', '=', True)]")
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel", ondelete='cascade', required=True)
    room_amenities_ids = fields.Many2many('room.amenities', string="Amenities")
    room_image_ids = fields.One2many('room.cat.image', 'room_cat_id', string="Room Images")
    description = fields.Html(string="Description")



class HotelRooms(models.Model):
    _name = "hotel.rooms"
    _description = "Rooms"

    name = fields.Char(string="Room No", required=True)
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel", ondelete='cascade')
    room_category_id = fields.Many2one('room.category', string="Room Category", ondelete='cascade')
    room_state = fields.Selection([
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
    ], string='Room State', copy=False, default='vacant')

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_allow_on_booking = fields.Boolean(string="Is Allow On Booking")

# class HotelRoom(models.Model):
#     _inherit = 'product.product'
#
#     is_room = fields.Boolean(string="Is Room")
#     state = fields.Selection([('available', 'available'), ('reserve', 'Reserve')], default='available')
#     hotel_id = fields.Many2one('hotel.hotel', string="Hotel", ondelete='cascade')
#     room_category_id = fields.Many2one('room.category', string='Room Category')
#     #room_type = fields.Many2one('hotel.room.type', string="Room Type")
#     room_amenities_ids = fields.Many2many('room.amenities', string="Amenities")
#     room_image_ids = fields.One2many('room.image', 'product_variant_id', string="Room Images")
#     #adults = fields.Integer(related="room_type.adults", string='Adults')
#     #childs = fields.Integer(related="room_type.childs", string='Childs')
#     #infants = fields.Integer(related="room_type.infants", string='Infants')
#
#
#     def _get_booking_contextual_price_tax_selection(self):
#         self.ensure_one()
#         price = self._get_contextual_price()
#         line_tax_type = self.env['ir.config_parameter'].sudo().get_param('account.show_line_subtotals_tax_selection')
#         if line_tax_type == "tax_included" and self.taxes_id:
#             price = self.taxes_id.compute_all(price, product=self, partner=self.env['res.partner'])['total_included']
#         return price
#
#     def get_booking_combination_info(self, products=None):
#         arr_lists = []
#         context = self.env.context
#         pricelist_id = context.get('pricelist', False)
#         pricelist = None
#         if pricelist_id:
#             pricelist = self.env['product.pricelist'].sudo().browse(pricelist_id)
#         for product in products:
#             list_price = product.list_price
#             if pricelist and pricelist.currency_id != product.currency_id:
#                 list_price = product.currency_id._convert(
#                     list_price, pricelist.currency_id, product.product_tmpl_id._get_current_company(pricelist=pricelist),
#                     fields.Date.today()
#                 )
#             price = product.with_context(context)._get_booking_contextual_price_tax_selection()
#             arr_lists.append({'price': price, 'list_price': list_price})
#         if arr_lists:
#             price_sum = sum(map(lambda x: x.get('price'), list(arr_lists)))
#             list_price = sum(map(lambda x: x.get('list_price'), list(arr_lists)))
#             return (price_sum, list_price)
#         return (False, False)

class RoomImage(models.Model):
    _name = 'room.image'
    _description = "Room Image"

    image_1920 = fields.Image(required=True)
    product_variant_id = fields.Many2one('product.product', "Product Variant", index=True)



class RoomCatImage(models.Model):
    _name = 'room.cat.image'
    _description = "Room Category Image"

    image_1920 = fields.Image(required=True)
    room_cat_id = fields.Many2one('room.category', "Room Category", index=True)

