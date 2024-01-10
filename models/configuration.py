# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelType(models.Model):
    _name = 'hotel.type'
    _description = 'name'

    name = fields.Char(string="Name", required="True")


class HotelRoomType(models.Model):
    #_name = 'hotel.room.type'
    _inherit = 'product.product'
    _description = 'Room Types '

    is_room_type = fields.Boolean(string="Is Room Type")
    #image_128 = fields.Image(required=True)
    image_128 = fields.Image()
    room_type_name = fields.Char('Room Type Name', required=True)
    description = fields.Text(string="Description")
    room_type_state = fields.Selection([('available', 'available'), ('reserve', 'Reserve')], default='available')
    hotel_id = fields.Many2one('hotel.hotel', string='Hotel', required=True)
    meal_id = fields.Many2one('hotel.meal', string="Meal Plan", required=True)
    room_category_id = fields.Many2one('room.category', string="Room Category", required=True)
    adults = fields.Integer('Adults')
    childs = fields.Integer('Childs')
    infants = fields.Integer('Infants')
    room_amenities_ids = fields.Many2many('room.amenities', string="Amenities")
    room_image_ids = fields.One2many('room.image', 'product_variant_id', string="Room Images")
    is_package = fields.Boolean(string="Is Package", default=False)
    bed_nights = fields.Integer('Bed Nights', default=7)
    valid_from = fields.Date(string="Valid From")
    valid_to = fields.Date(string="Valid To")
    book_before = fields.Date(string="Book Before")
    package_details = fields.Html("Package Details")
    package_price = fields.Integer('Package Price', default=0)

    @api.onchange('room_type_name', 'room_category_id', 'meal_id', 'adults', 'childs', 'infants')
    def _onchange_set_roomtpe_name(self):
        if self.room_type_name and self.room_category_id and self.meal_id:
            name_text = self.room_type_name + "/" + self.room_category_id.name + "/" + self.meal_id.name + " | " + str(
                 self.adults) + " Adults + (" + str(self.childs) + " Child, " + str(self.infants) + " Infants)"
            self.name = name_text

    @api.onchange('hotel_id')
    def _onchange_filetr_room_cat(self):
        if self.hotel_id:
            for rec in self:
                return {'domain': {'room_category_id': [('hotel_id', '=', rec.hotel_id.id)]}}


    @api.model_create_multi
    def create(self, vals_list):

        for val in vals_list:
            if 'room_type_name' in val:
                search_name = val['name']
                #rec_count = self.env['product.product'].sudo().search_count(
                #[('room_category_id', '=', rcat_id), ('meal_id', '=', mealid), ('room_type_name', '=', r_name), ('adults', '=', adlt), ('childs', '=', chd), ('infants', '=', inf)])

                rec_count = self.env['product.product'].sudo().search_count([('name', '=', search_name)])
                print('roomcount', rec_count)
                if (rec_count > 0):
                    raise ValidationError(_('Record Exists with same room type'))
        return super().create(vals_list)


class HotelAmenities(models.Model):
    _name = 'hotel.amenities'
    _description = 'name'

    name = fields.Char(string="Name", required="True")
    fa_icon = fields.Char('Fa-Icon')
    icon = fields.Image(string="SVG Icon")
    category_id = fields.Many2one('amenity.category', string='Category', required="True")


class RoomAmenities(models.Model):
    _name = 'room.amenities'
    _description = 'name'

    name= fields.Char(string='Name', required="True")
    fa_icon = fields.Char('Fa-Icon')
    icon = fields.Image(string="SVG Icon")

class FeauturedAmenities(models.Model):
    _name = 'feat.amenities'
    _description = 'name'

    name= fields.Char(string='Name', required="True")
    fa_icon = fields.Char('Fa-Icon')
    icon = fields.Image(string="SVG Icon")


class GhMeals(models.Model):
    _name = "hotel.meal"
    _description = "Meals"

    name = fields.Char(string="Meal Name", required=True)


class ApIslands(models.Model):
    _name = "appeul.island"
    _description = "Islands"

    name = fields.Char(string="Island", required=True)

class AppeulPaymentMethods(models.Model):
    _name = "payment.methods"
    _description = "name"

    name = fields.Char(string="Card Name", required=True)
    image = fields.Image(string="Image")


class AppeulAtolls(models.Model):
    _name = "appeul.atoll"
    _description = "name"

    name = fields.Char(string="Atoll", required=True)
    island_ids = fields.Many2many('appeul.island', string="Islands")



class AmenityCategory(models.Model):
    _name = "amenity.category"
    _description = "Amenity category"

    name = fields.Char(string="Amenity Category", required=True)
    amenity_ids = fields.Many2many('hotel.amenities', string="Amenities")