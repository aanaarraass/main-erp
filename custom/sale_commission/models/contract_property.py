# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProperyPropertyContract(models.Model):
    _inherit = ["property.property.contract","sale.commission.mixin"]
    _name = 'property.property.contract'

    agent_ids = fields.One2many(comodel_name="property.contract.line.agent",inverse_name="object_id",)
    commission_total = fields.Float(
        string="Commissions",
        compute="_compute_commission_total",
        store=True,
    )

    def _compute_agent_ids(self):
        self.agent_ids = False  # for resetting previous agents
        for record in self.filtered(lambda x: x.partner_id):
            if not record.commission_free:
                record.agent_ids = record._prepare_agents_vals_partner(
                    record.partner_id
                )

    def _prepare_invoice_line(self, **optional_values):
        vals = super(ProperyPropertyContract, self)._prepare_invoice_line(**optional_values)
        vals["agent_ids"] = [
            (0, 0, {"agent_id": x.agent_id.id, "commission_id": x.commission_id.id})
            for x in self.agent_ids
        ]
        return vals

    @api.depends("agent_ids.amount")
    def _compute_commission_total(self):
        for record in self:
            record.commission_total = sum(record.mapped("agent_ids.amount"))




class SaleOrderLineAgent(models.Model):
    _inherit = "sale.commission.line.mixin"
    _name = "property.contract.line.agent"
    _description = "Agent detail of commission line in property contract lines"

    object_id = fields.Many2one(comodel_name="property.property.contract")
    # currency_id = fields.Many2one(related="object_id.currency_id")

    @api.depends(
        "commission_id",
        "object_id.property_selling_price",
    )
    def _compute_amount(self):
        for line in self:
            property_id = line.object_id
            line.amount = line._get_commission_amount(
                line.commission_id,
                property_id.property_selling_price,
                property_id,
                1,
            )

