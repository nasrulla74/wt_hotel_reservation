# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'utm.mixin']

    #bk_order_ids = fields.One2many('sale.order', 'hotel_id', string="Room Categories")

    # def unlink(self):
    #     downpayment_lines = self.mapped('line_ids.booking_line_ids').filtered(lambda line: line.is_downpayment and line.invoice_lines <= self.mapped('line_ids'))
    #     res = super(AccountMove, self).unlink()
    #     if downpayment_lines:
    #         downpayment_lines.unlink()
    #     return res
    #
    # def _post(self, soft=True):
    #     # OVERRIDE
    #     # Auto-reconcile the invoice with payments coming from transactions.
    #     # It's useful when you have a "paid" sale order (using a payment transaction) and you invoice it later.
    #     posted = super()._post(soft)
    #
    #     for invoice in posted.filtered(lambda move: move.is_invoice()):
    #         payments = invoice.mapped('transaction_ids.payment_id')
    #         move_lines = payments.line_ids.filtered(lambda line: line.account_internal_type in ('receivable', 'payable') and not line.reconciled)
    #         for line in move_lines:
    #             invoice.js_assign_outstanding_line(line.id)
    #     return posted
    #
    # def action_post(self):
    #     #inherit of the function from account.move to validate a new tax and the priceunit of a downpayment
    #     res = super(AccountMove, self).action_post()
    #     return res
        


    # def action_paid(self, vals):
    #     import pdb;pdb.set_trace()
    #     res = super(AccountMove, self).action_paid(vals)
    #     if self.payment_state == 'paid':
    #         for line in self.invoice_line_ids:
    #             line.booking_line_ids.booking_id.state = 'booked'


    def write(self, vals):
        # import pdb;pdb.set_trace()
        res = super(AccountMove, self).write(vals)
        if self.state == 'posted':
            for line in self.invoice_line_ids:
                line.sale_line_ids.order_id.bk_state = 'booked'

        if self.payment_state == 'paid':
            for line in self.invoice_line_ids:
                line.sale_line_ids.order_id.bk_state = 'booked'

        return res