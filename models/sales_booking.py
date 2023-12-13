from odoo.exceptions import ValidationError
from odoo import models, fields, api, _



class SaleOrderBooking(models.Model):
    _inherit = 'sale.order'

    booking_name = fields.Char('Booking Name', default='')
    booking_ref = fields.Char('Booking Ref')
    booking_no = fields.Char('Booking No')
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel")
    check_in_date = fields.Date(string="Check In")
    check_out_date = fields.Date(string="Check Out")
    #room_type_id = fields.Many2one('product.product', string="Room Type", required=True)
    ## --------------Depricated - start!!
    room_type_id = fields.Many2one('product.product', string="Room Type")
    adults = fields.Integer(string="Adults", required=True, default="2", related="room_type_id.adults")
    childs = fields.Integer(string="Child", required=True, default="0", related="room_type_id.childs")
    infants = fields.Integer(string="Infants", required=True, default="0", related="room_type_id.infants")
    meal_id = fields.Many2one('hotel.meal', string="Meal", related="room_type_id.meal_id")
    ## --------------Depricated - end!!
    bk_method = fields.Selection(
        [('foreign-operator', 'Foreign tour operator'), ('local-operator', 'Local tour operator'),
         ('direct-fit', 'Direct booking/(FIT)'), ('ota', 'Online travel agent')],
        default='ota', string="Booking Method")
    bed_nights = fields.Integer('Bed Nights', compute="_compute_bed_nights")
    is_booking = fields.Boolean(string='Is Booking')
    bk_state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('verified', 'Verified'),
        ('booked', 'Booked'),
        ('check_in', 'Check-In'),
        ('check_out', 'Check-Out'),
        ('cancelled', 'Cancelled'),
    ], string='State', readonly=True, copy=False, index=True, tracking=3, default='draft')

    @api.onchange('check_out_date', 'check_in_date')
    def _compute_bed_nights(self):
        for rec in self:

            if (rec.check_in_date and rec.check_out_date):
                rec.bed_nights = (rec.check_out_date - rec.check_in_date).days
                self.is_booking = True

    @api.model_create_multi
    def create(self, vals_list):
        # default_hotel_id = self.env['ir.config_parameter'].sudo().get_param(
        #     'wt_hotel_reservation.default_booking_default_hotel_id')
        for vals in vals_list:
            if vals['is_booking']:
                vals['booking_no'] = (self.env['ir.sequence'].next_by_code('hotel.booking') or 'New')

                return super().create(vals_list)
            else:
                return super().create(vals_list)


