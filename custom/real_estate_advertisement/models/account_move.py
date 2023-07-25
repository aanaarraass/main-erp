# Copyright 2014-2018 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime , date

from lxml import etree

from odoo import _, api, exceptions, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    property_selling_price = fields.Monetary('Property Selling Price')
    property_discount_amount = fields.Monetary('Discount')
    total_emi_amount = fields.Monetary(string="Total Contract Amount")
    paid_installment_emi = fields.Monetary(string="Total Paid Amount", compute='get_total_paid_emi')
    # paid_installment_emi = fields.Monetary(string="Total Paid Amount")
    remaining_balance = fields.Monetary(string="Total Remaining Amount", compute='get_total_paid_emi')
    remaining_installments = fields.Integer(string="Remaining Installments", compute='get_total_paid_emi')
    # default=lambda self: self.env.company.account_sale_tax_id,
    contract_total_amount_with_tax = fields.Monetary(string="Contract Total Amount With Tax", store=True)


    def get_total_paid_emi(self):
        if self.property_contract_id:
            for rec in self.property_contract_id:
                print(self.amount_installment_id, 'amount_installment_id', self.property_contract_id, 'contract id')
                if rec.paid_installment_emi:
                    self.paid_installment_emi = rec.paid_installment_emi
                else:
                    self.paid_installment_emi = 0.0
                if rec.remaining_balance:
                    self.remaining_balance = rec.remaining_balance
                else:
                    self.remaining_balance = 0.0
                self.remaining_installments = len(rec.amount_installment_ids.filtered(lambda r: r.state == 'unpaid'))
        else:
            self.paid_installment_emi = 0.0
            self.remaining_balance = 0.0
            self.remaining_installments = 0