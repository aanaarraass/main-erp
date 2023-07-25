from odoo import models, fields


class OpQuestionBankdeagIntoText(models.Model):
    _inherit = "op.question.bank.line"

    que_type = fields.Selection(
        selection_add=[('drag_into_text', 'Drag Into Text')],
        ondelete={'drag_into_text': 'set default'})
