import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EmiPayment(models.TransientModel):
    _name = 'emi.payment.wizards'
    _description = 'About Payments'

    total_amount = fields.Monetary()
    paid_amount = fields.Monetary()
    tax_amount = fields.Monetary()
    journal_id = fields.Many2one('account.journal', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    amount_installment_id = fields.Many2one('amount.installment')
    partner_id = fields.Many2one('res.partner')
    fine_on_paid_amount = fields.Monetary()

    # fields added by waqas ali to map the values in invoice qweb
    property_selling_price = fields.Monetary('Selling Price')
    discount_amount = fields.Monetary('Discount')
    total_emi_amount = fields.Monetary(string="Total Contract Amount")
    paid_installment_emi = fields.Monetary(string="Total Paid Amount", store=True)
    remaining_balance = fields.Monetary(string="Total Due Amount", store=True)
    # default=lambda self: self.env.company.account_sale_tax_id,
    contract_total_amount_with_tax = fields.Monetary(string="Contract Total Amount With Tax",store=True)

    # @api.depends('amount_installment_id.balance_amount')
    # def _onchange_balance_amount(self):
    #     if self.paid_amount>0 and self.paid_amount<= self.amount_installment_id.balance_amount:

    def create_invoice_action(self):
        print('create_invoice_action')
        active_id = self._context.get("active_id")
        line_agents = []
        if active_id:
            property_agent = self.env['property.property.contract'].browse(int(active_id))
            if property_agent:
                for agent in property_agent.agent_ids:
                    line_agents.append((0,0,{
                        'agent_id': agent.agent_id.id,
                        'commission_id': agent.commission_id.id,
                    }))

        if self.paid_amount:
            per_day_fine_percent = self._context.get("per_day_fine_percent")
            delay_in_days = self._context.get("delay_in_days")
            date = self._context.get("date")
            if date:
                if per_day_fine_percent and delay_in_days:
                    per_day_fine_percent = float(per_day_fine_percent)
                    per_day_fine = self.paid_amount * per_day_fine_percent / 100
                    total_fine = per_day_fine * int(delay_in_days)
                    self.fine_on_paid_amount = total_fine
            print("paid_amount", self.paid_amount, self.total_amount)

            if self.paid_amount > self.total_amount:
                raise ValidationError(_('Paid amount always less than Total Amount.'))
        else:
            raise ValidationError(_(' Paid amount always grater than 0.'))
        tax = False
        if self.amount_installment_id.property_contract_id.tax_ids:
            tax = [(6, 0, self.amount_installment_id.property_contract_id.tax_ids.ids)]
        if self.amount_installment_id:
            invoice_lines = [(0, 0, {
                'quantity': 1.0,
                'name': self.amount_installment_id.description,
                'price_unit': self.paid_amount,
                'tax_ids': tax,
            })]
            if self.fine_on_paid_amount:
                invoice_lines.append((0, 0, {
                    'quantity': 1.0,
                    'name': "Delay Fine Charge",
                    'price_unit': self.fine_on_paid_amount,
                    # 'tax_ids': tax,
                }))
            # if self.discount_amount > 0:
            #     discount = -1 * self.discount_amount
            #     invoice_lines.append((0, 0, {
            #         'quantity': 1.0,
            #         'name': "Discount",
            #         'price_unit': discount,
            #         # 'tax_ids': tax,
            #     }))

            invoice_due_date = self._context.get("invoice_date_due")
            invoice_due_date = fields.Date.to_date(invoice_due_date)
            if invoice_due_date <= datetime.datetime.today().date():
                invoice_due_date = datetime.datetime.today().date()
            print("invoice_lines", invoice_lines)
            vals = {
                'move_type': 'out_invoice',
                'journal_id': self.journal_id.id,
                'partner_id': self.amount_installment_id.property_contract_id.partner_id.id,
                'currency_id': self.currency_id.id,
                'invoice_date': datetime.datetime.today().date(),
                'invoice_date_due': invoice_due_date,
                'property_selling_price': self.property_selling_price,
                'property_discount_amount': self.discount_amount,
                'total_emi_amount': self.total_emi_amount,
                'contract_total_amount_with_tax': self.contract_total_amount_with_tax,
                'date': datetime.datetime.today().date(),
                'amount_installment_id': self.amount_installment_id.id,
                'property_contract_id': self.amount_installment_id.property_contract_id.id,
                'invoice_line_ids': invoice_lines}

            # self.amount_installment_id.installment_total_with_fine += self.fine_on_paid_amount
            invoice = self.env['account.move'].create(vals)
            self.amount_installment_id.invoice_date = datetime.datetime.today().date()
        else:
            invoice_line_desc = self._context.get("invoice_line_desc")
            partner_id = self._context.get("partner_id")
            invoice_lines = [(0, 0, {
                'quantity': 1.0,
                'name': invoice_line_desc,
                'price_unit': self.paid_amount,
                'tax_ids': tax,
                'agent_ids': line_agents
            })]
            # if self.discount_amount > 0:
            #     discount = -1 * self.discount_amount
            #     invoice_lines.append((0, 0, {
            #         'quantity': 1.0,
            #         'name': "Discount",
            #         'price_unit': discount,
            #         # 'tax_ids': tax,
            #     }))

            vals = {
                'move_type': 'out_invoice',
                'journal_id': self.journal_id.id,
                'partner_id': partner_id,
                'currency_id': self.currency_id.id,
                'invoice_date': datetime.datetime.today().date(),
                # 'invoice_date_due': invoice_due_date,
                'date': datetime.datetime.today().date(),
                # 'amount_installment_id': self.amount_installment_id.id,
                'invoice_line_ids': invoice_lines}
            print("vals", vals)
            # self.amount_installment_id.installment_total_with_fine += self.fine_on_paid_amount
            invoice = self.env['account.move'].create(vals)
            self.amount_installment_id.invoice_date = datetime.datetime.today().date()

            print("invoice_id", invoice)
            contract_ids = self._context.get("active_ids")
            if contract_ids:
                contract_id = self.env["property.property.contract"].search([("id", "=", contract_ids[0])])
                contract_id.invoice_id = invoice.id
