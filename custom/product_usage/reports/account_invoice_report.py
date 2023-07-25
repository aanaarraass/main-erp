# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_usage_id = fields.Many2one(comodel_name="product.usage", string="usage")

    @api.model
    def _select(self):
        select_str = super()._select()
        select_str += """
            , template.product_usage_id as product_usage_id
            """
        return select_str

    @api.model
    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", template.product_usage_id"
        return group_by_str
