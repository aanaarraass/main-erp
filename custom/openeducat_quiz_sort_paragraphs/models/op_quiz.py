from odoo import fields, models


class QuizmatchSortParagraphs(models.Model):
    _inherit = "op.quiz.line"

    que_type = fields.Selection(
        selection_add=[('sort_paragraphs', 'Sort the Paragraphs')],
        ondelete={'sort_paragraphs': 'set default'})
    sort_paragraphs_line_ids = fields.One2many(
        'op.quiz.answer.sort.paragraphs',
        'sort_paragraphs_line_id', 'Sort the Paragraphs Answers')


class QuizSortParagraphs(models.Model):
    _name = "op.quiz.answer.sort.paragraphs"
    _description = "Quiz Answers sort paragraphs"

    question = fields.Char('Question')
    answer = fields.Char('Answer')
    sort_paragraphs_line_id = fields.Many2one('op.quiz.line', 'question Line')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self : self.env.user.company_id)


class QuizResultSortParagraphs(models.Model):
    _inherit = "op.quiz"

    def get_result_id(self):
        res = super(QuizResultSortParagraphs, self).get_result_id()
        for data in res.line_ids:
            if data.bank_line.que_type == 'sort_paragraphs':
                if data.que_type != 'sort_paragraphs':
                    for temp in data.bank_line.sort_paragraphs_line_ids:
                        self.env['op.quiz.result.line.sort.paragraphs'].sudo().create({
                            'line_id' : data.id,
                            'given_answer' : '',
                            'default_answer' : temp.question,
                        })
                data.que_type = data.bank_line.que_type
                data.grade_true_id = data.bank_line.grade_true_id
                data.grade_false_id = data.bank_line.grade_false_id
        return res
