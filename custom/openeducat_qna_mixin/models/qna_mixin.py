from odoo import fields, models


class QnaMixin(models.AbstractModel):
    _name = 'qna.mixin'
    _description = 'QNA Mixin'

    question_ids = fields.One2many('question.single', 'qna_id',
                                   string="Questions", help='Ask question to user')
