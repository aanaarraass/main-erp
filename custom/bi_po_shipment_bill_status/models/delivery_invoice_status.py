# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare

class inherit_purchase(models.Model):
	_inherit = "purchase.order"
	
	check_partially_delivery = fields.Boolean(string="Partially Shipped",readonly=1,copy=False)
	check_fully_delivery = fields.Boolean(string="Fully Shipped",readonly=1,copy=False)
	check_partially_paid = fields.Boolean(string="Partially Paid",readonly=1,copy=False)
	check_fully_paid = fields.Boolean(string="Fully Paid",default=False,readonly=1,copy=False)



class inherit_stock_picking(models.Model):
	_inherit = "stock.picking"

	pick_bool = fields.Boolean(string="demo bool",compute="_compute_purchase_fully_picking",store=True)

	@api.depends("move_ids_without_package.quantity_done")
	def _compute_purchase_fully_picking(self):
		
		for i in self:
			purchase_order = i.env['purchase.order'].search([])
			for j in purchase_order:
				if j.name == i.origin:
					counter_qty = 0.0
					main_qty = 0.0

					for ids in j.picking_ids:
						for lines in ids.move_ids_without_package:
							counter_qty += lines.quantity_done

					for main in j.order_line:
						main_qty += main.product_qty

					if counter_qty >= 0.0:

						if counter_qty < main_qty:
							j.write({
								"check_partially_delivery":True
									})

						if counter_qty == 0:
							j.write({
								"check_fully_delivery":False,
								"check_partially_delivery":False
									})

						if counter_qty == main_qty:
							j.write({
								"check_fully_delivery":True,
								"check_partially_delivery":False
									})

					i.pick_bool = True


class inherit_invoicing(models.Model):
	_inherit = "account.move"

	def _compute_amount(self):
		for move in self:

			if move.payment_state == 'invoicing_legacy':
				move.payment_state = move.payment_state
				continue

			total_untaxed = 0.0
			total_untaxed_currency = 0.0
			total_tax = 0.0
			total_tax_currency = 0.0
			total_to_pay = 0.0
			total_residual = 0.0
			total_residual_currency = 0.0
			total = 0.0
			total_currency = 0.0
			currencies = set()

			for line in move.line_ids:
				if line.currency_id:
					currencies.add(line.currency_id)

				if move.is_invoice(include_receipts=True):
					# === Invoices ===

					if not line.exclude_from_invoice_tab:
						# Untaxed amount.
						total_untaxed += line.balance
						total_untaxed_currency += line.amount_currency
						total += line.balance
						total_currency += line.amount_currency
					elif line.tax_line_id:
						# Tax amount.
						total_tax += line.balance
						total_tax_currency += line.amount_currency
						total += line.balance
						total_currency += line.amount_currency
					elif line.account_id.user_type_id.type in ('receivable', 'payable'):
						# Residual amount.
						total_to_pay += line.balance
						total_residual += line.amount_residual
						total_residual_currency += line.amount_residual_currency
				else:
					# === Miscellaneous journal entry ===
					if line.debit:
						total += line.balance
						total_currency += line.amount_currency

			if move.move_type == 'entry' or move.is_outbound():
				sign = 1
			else:
				sign = -1
			move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
			move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
			move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
			move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
			move.amount_untaxed_signed = -total_untaxed
			move.amount_tax_signed = -total_tax
			move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
			move.amount_residual_signed = total_residual

			currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id

			# Compute 'payment_state'.
			new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

			if move.is_invoice(include_receipts=True) and move.state == 'posted':

				if currency.is_zero(move.amount_residual):
					if all(payment.is_matched for payment in move._get_reconciled_payments()):
						new_pmt_state = 'paid'
					else:
						new_pmt_state = move._get_invoice_in_payment_state()
				elif currency.compare_amounts(total_to_pay, total_residual) != 0:
					new_pmt_state = 'partial'

			if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
				reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
				reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

				# We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
				reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
				if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
					new_pmt_state = 'reversed'

			move.payment_state = new_pmt_state
			if move.payment_state == 'paid':
				move.invoice_line_ids[0].purchase_order_id.write({
					"check_partially_paid": False,
					"check_fully_paid": True
				})

			elif move.payment_state == 'partial':
				if move.invoice_line_ids.purchase_order_id:
					move.invoice_line_ids[0].purchase_order_id.write({
						"check_partially_paid": True
					})
			else:
				if move.invoice_line_ids.purchase_order_id:
					move.invoice_line_ids[0].purchase_order_id.write({
					"check_partially_paid": False,
					"check_fully_paid": False
				})

		res = super(inherit_invoicing, self)._compute_amount()
		return res









