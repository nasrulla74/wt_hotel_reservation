# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.translate import html_translate
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import json
from odoo.http import request
import base64



class AppeulExtraBedPolicy(models.Model):
    _name = "extrabed.policy"
    _description = "Extra Bed Policy"

    name = fields.Char(string="Period", required=True)
    description = fields.Char(string="Description")
    price = fields.Char(string="Price")
    ap_hotel_id = fields.Many2one('hotel.hotel', string="Hotel")







class AppeulSurroundingLines(models.Model):
    _name = "surrounding.lines"
    _description = "Surrounding Lines"

    name = fields.Char(string="Name")
    type = fields.Selection([('restaurant', 'Restaurant'), ('beach', 'Beach'), ('airport', 'Airport')], string="Surroundings", default='beach')
    description = fields.Char(string="Description")
    distance = fields.Char(string="Distance")
    ap_hotel_id = fields.Many2one('hotel.hotel', string="Hotel")
class AppeulRestaurantLines(models.Model):
    _name = "restaurant.lines"
    _description = "Restaurants Lines"

    name = fields.Char(string="Name")
    cuisine = fields.Char(string="Cuisine")
    open_for = fields.Char(string="Open For")
    ambiance = fields.Char(string="Ambiance")
    ap_hotel_id = fields.Many2one('hotel.hotel', string="Hotel")
class AppeulFAQLines(models.Model):
    _name = "faqs.lines"
    _description = "FAQs Lines"

    name = fields.Char(string="Question")
    answer = fields.Html("Answer")
    ap_hotel_id = fields.Many2one('hotel.hotel', string="Hotel")

class Hotel(models.Model):
    _name = 'hotel.hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin', 'rating.mixin']
    _rec_name = 'name'
    _description = 'name'
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying a Hotel list')
    owner_id = fields.Many2one('res.users', string="Owner")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the Hotel without removing it.")
    hotel_type = fields.Many2one('hotel.type', string="Type")
    description = fields.Char(string="Description")
    hotel_policy = fields.Html(string="Policies")
    #location = fields.Text(string="Location")
    #room_ids = fields.One2many('product.product', 'hotel_id', string="Rooms", domain="[('is_room', '=', True)]")
    room_type_ids = fields.One2many('product.product', 'hotel_id', string="Room Type", domain="[('is_room_type', '=', True)]")
    room_category_ids = fields.One2many('room.category', 'hotel_id', string="Room Categories")
    amenities_ids = fields.Many2many('hotel.amenities', string="Amenities")
    featured_amenity_ids = fields.Many2many('feat.amenities', string="Featured Amenities", index=True)
    payment_method_ids = fields.Many2many('payment.methods', string="Payment Methods")
    # Address
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    # Contact Info
    email = fields.Char('Email', required=True)
    phone_number = fields.Char('Phone Number', required=True)
    hotel_image_ids = fields.One2many('hotel.image', 'hotel_id', string="Hotel Images")
    #is_couple_friendly = fields.Boolean('Couple Friendly')
    #facility = fields.Html(string="Facility")
    check_in_time = fields.Float(string="Check In Time")
    check_out_time = fields.Float(string="Check Out Time")
    selected_room_ids = fields.Many2many('product.product')
    lattitude = fields.Float()
    longitude = fields.Float()
    about = fields.Html(string="About")
    company_info = fields.Html(string="Company Information")
    property_info = fields.Html(string="Property Information")
    neighbourhood_info = fields.Html(string="Neighbourhood Information")
    the_fine_print = fields.Html(string="The Fine Print")
    cancellation_prepayment = fields.Text(string="Cancellation/Prepayment")
    child_policies = fields.Text(string="Child policies")
    age_restriction = fields.Char(string="Age restriction")
    smoking = fields.Char(string="Smoking")
    pets = fields.Char(string="Pets")
    extra_bed_policy_ids = fields.One2many('extrabed.policy', 'ap_hotel_id', string="Extra Bed Policy")
    surrounding_lines_ids = fields.One2many('surrounding.lines', 'ap_hotel_id', string="Surroundings")
    restaurant_lines_ids = fields.One2many('restaurant.lines', 'ap_hotel_id', string="Restaurants")
    faqs_lines_ids = fields.One2many('faqs.lines', 'ap_hotel_id', string="FAQs")
    featured_image = fields.Binary("Featured Image")
    island_id = fields.Many2one('appeul.island', string="Island")
    cover_image = fields.Image(string="Cover Image 1920x500")
    star_rate = fields.Selection([
        ('1', 'Normal'),
        ('2', 'Low'),
        ('3', 'High'),
        ('4', 'High'),
        ('5', 'Very High')], string="Star Rate")


    def success_popup(self, data):
        return {
            "name": "Message",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "pop.message",
            "target": "new",
            "context": {
                "default_name": "%s"%data
            },
        }

    @api.model
    def get_hotel_address(self, is_state=None, is_country=None):
        address = []
        address.append(self.street) if self.street else None
        address.append(self.street2) if self.street2 else None
        address.append(self.city) if self.city else None
        address.append(self.state_id.name) if self.state_id and is_state else None
        address.append(self.country_id.name) if self.country_id and is_country else None
        address_join = ", ". join(address)
        return address_join

    @api.model
    def get_check_in_time(self):
        time = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(self.check_in_time) * 60, 60))
        return datetime.strptime(time, "%H:%M").strftime('%I:%M %p')

    @api.model
    def get_check_out_time(self):
        time = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(self.check_out_time) * 60, 60))
        return datetime.strptime(time, "%H:%M").strftime('%I:%M %p')
        

    @api.model
    def get_room_by_capacity(self, rooms, room_cap):
        total = 0
        a_rooms = []
        for rm in rooms:
            total = total + (rm.adults + rm.childs)
            if total <= room_cap:
                a_rooms.append(rm.id)
                if total == room_cap or total >= room_cap:
                    break
                continue
            else:
                a_rooms.append(rm.id)
                break
        return a_rooms



    @api.model
    def get_room_type_data(self, r_types):
        rooms_datas = []

        for rm_type in r_types:
            amenities = r_types.room_category_id.mapped('room_amenities_ids')
            room_types_datas = {
                'room_type': rm_type,
                'type_name': rm_type.name,
                'room_id': rm_type.id,
                'room_cat_id': rm_type.room_category_id,
                'amenities': amenities or [],
                'list_price': rm_type.list_price,
                'per_night_price': rm_type.list_price,
                'price': rm_type.list_price,
                }
            rooms_datas.append(room_types_datas)

        return rooms_datas

    @api.model
    def get_room_type_data_old(self, r_types, room_capacity, avalible_rooms, b_days, pricelist=None):
        rooms_datas = []
        context = dict(self.env.context, quantity=b_days, pricelist=pricelist.id if pricelist else False)
        for rm_type in r_types:
            rooms = avalible_rooms.filtered(lambda x: x.room_type and x.room_type.id == rm_type.id)
            a_rooms = self.get_room_by_capacity(rooms, room_capacity)
            room_bws = self.env['product.product'].sudo().browse(a_rooms)
            if room_bws:
                price, list_price = self.env['product.product'].sudo().with_context(
                    context).get_booking_combination_info(room_bws)
                amenities = room_bws.mapped('room_amenities_ids')
                room_types_datas = {
                    'room_type': rm_type,
                    'type_name': rm_type.name,
                    'room_id': room_bws[0] or False,
                    'b_room_ids': a_rooms,
                    'amenities': amenities or [],
                    'room_count': len(room_bws),
                    'price': (price * b_days),
                    'list_price': list_price,
                    'has_discount': True if price < list_price else False,
                    'room_info': str(room_capacity) + ' Guest, ' + str(len(room_bws)) + ' ' + str(
                        rm_type.name) + ' Rooms, ' + str(b_days) + ' Night',
                    'nights': b_days or 1,
                    'per_night_price': price,
                    'booked_room': json.dumps({
                        'room_ids': a_rooms,
                        'nights': b_days or 1
                    })
                }
                if a_rooms:
                    rooms_datas.append(room_types_datas)
        return rooms_datas



    @api.model
    def get_selected_rooms(self, rooms_datas, b_days, eagle_booking_rooms):
        selected_datas = None
        booked_room = {}
        if rooms_datas:
            for datas in rooms_datas:
                if datas.get('room_count') == int(eagle_booking_rooms):
                    selected_datas = datas
                    booked_room = {
                        'room_ids': selected_datas['b_room_ids'],
                        'nights': b_days or 1
                    }
                    break
        if not selected_datas and rooms_datas:
            selected_datas = rooms_datas[:1][0]
            booked_room = {
                'room_ids': selected_datas['b_room_ids'],
                'nights': b_days or 1
            }
        return (selected_datas, booked_room)

    @api.model
    def get_booking_types(self, avalible_rooms, room_capacity):
        a_types = []
        def _keys_in_sorted(ml):
            return ((ml.room_type.adults + ml.room_type.childs) ,ml.room_type.id)
        for k, g in groupby(sorted(avalible_rooms, key=_keys_in_sorted), key=itemgetter('room_type')):
            total = sum((ml.adults + ml.childs) for ml in g)
            if total >= room_capacity:
                a_types.append(k.id)
        return a_types

    @api.model
    def get_hotel_room_info(self, check_in, check_out, guest, rooms, pricelist=None):
        s_check_in_date = datetime.strptime(check_in, '%m-%d-%Y').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        s_check_out_date = datetime.strptime(check_out, '%m-%d-%Y').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        dalta = datetime.strptime(check_out, '%m-%d-%Y') - datetime.strptime(check_in, '%m-%d-%Y')
        b_days = dalta.days
        s_books = self.env['hotel.booking'].search([('check_out_date', '>', s_check_in_date), ('hotel_id', '=', self.id), ('state', 'not in', ['draft', 'cancelled'])])
        s_books = s_books.filtered(lambda x: str(x.check_in_date) <= s_check_out_date)
        book_rooms = s_books.mapped('booking_line').mapped('room_id')
        avalible_rooms = self.room_ids.filtered(lambda x: x.id not in book_rooms.ids)
        avalible_rooms = avalible_rooms.sorted(lambda x: x.list_price)
        a_types = self.get_booking_types(avalible_rooms, guest)
        r_types = self.env['hotel.room.type'].browse(a_types)
        rooms_datas = self.get_room_type_data(r_types, guest, avalible_rooms, b_days, pricelist)
        selected_datas, booking_datas = self.get_selected_rooms(rooms_datas, b_days, rooms)
        if selected_datas and booking_datas:
            return selected_datas
        return False


class HotelImage(models.Model):
    _name = 'hotel.image'
    _description = "Hotel Image"

    image_1920 = fields.Image(required=True)
    hotel_id = fields.Many2one('hotel.hotel', "Hotel", index=True)





