from odoo import fields, models


class QuestionSingle(models.Model):
    _name = 'question.single'
    _description = 'Question Single'

    name = fields.Char('Question', translate=True, required=True)
    placeholder = fields.Char('Placeholder', translate=True)
    res_model_id = fields.Many2one('ir.model', 'Related Document Model',
                                   index=True, ondelete='cascade',
                                   help='Model of the followed resource')
    res_model = fields.Char(string='Document Model', related='res_model_id.model',
                            store=True, index=True, readonly=True)
    qna_id = fields.Integer(string='Document', required=True,
                            help="Identifier of the rated object", index=True)
    question_type = fields.Selection([
        ('char', 'Single line text'),
        ('text', 'Multi-line text'),
        ('select', 'Dropdown (one answer)'),
        ('radio', 'Radio (one answer)'),
        ('checkbox', 'Checkboxes (multiple answers)'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('file', 'File'),
        ('number', 'Number'),
        ('decimal', 'Decimal'), ], 'Question Type', default='char')
    required_answer = fields.Boolean('Answer Required')
    answer_ids = fields.Many2many('question.answer', string="Answer")


class QuestionAnswer(models.Model):
    _name = 'question.answer'
    _description = "Question Answer"
    name = fields.Char('Answer')
