from odoo import api, fields, models, _


class BookingPartner(models.Model):
    _inherit = 'res.partner'

    is_booking_agent = fields.Boolean(string='Is Booking Agent')
    is_booking_client = fields.Boolean(string='Is Booking Client')


