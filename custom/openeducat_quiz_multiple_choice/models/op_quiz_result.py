from odoo import fields, models, api


class QuizResulMultipleChoice(models.Model):
    _inherit = "op.quiz.result.line"

    que_type = fields.Selection(
        selection_add=[('multiple_choice', 'Match Following Images')],
        default='optional')
    multiple_choice_que_type = fields.Selection([
        ('text', 'Text'), ('image', 'Image')], 'multiple choice Question Type')
    multiple_choice_line_ids = fields.One2many(
        'op.quiz.result.line.multiple.choice',
        'multiple_choice_line_id', 'Following Images')


class QuizResultLineMultipleChoice(models.Model):
    _name = "op.quiz.result.line.multiple.choice"
    _description = "quiz multiple choice result"

    que_type = fields.Selection([
        ('text', 'Text'), ('image', 'Image')], 'Question Type')
    que_image = fields.Binary("Image")
    que_text = fields.Char('Text Question')
    given_answer = fields.Boolean('Given Answer')
    default_answer = fields.Boolean('default Answer')
    multiple_choice_line_id = fields.Many2one(
        'op.quiz.result.line', 'Question line')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)


class QuizResultMatchFollowingimages(models.Model):
    _inherit = "op.quiz.result"

    @api.depends('line_ids.multiple_choice_line_ids',
                 'line_ids.multiple_choice_line_ids.given_answer',
                 'line_ids', )
    def _compute_get_result(self):
        res = super(QuizResultMatchFollowingimages, self)._compute_get_result()
        for obj in self:
            obj.total_question = len(obj.line_ids.ids)
        total_correct = obj.total_correct
        total_incorrect = obj.total_incorrect
        total_not_attempt = obj.total_not_attempt
        total_marks = 0
        received_marks = obj.received_marks
        for line in obj.line_ids:
            total_marks += line.question_mark or 0.0
            if not line.name or line.name == '':
                total_not_attempt += 1
                continue
            if line.que_type == 'multiple_choice':
                line.mark = 0
                temp_total_correct = 0
                total_question_line = len(line.multiple_choice_line_ids)

                for data in line.multiple_choice_line_ids:
                    if data.default_answer == data.given_answer:
                        temp_total_correct += 1
                if(temp_total_correct == total_question_line):
                    total_correct += 1
                    received_marks += (line.question_mark *
                                       line.grade_true_id.value)/100
                    line.mark = (line.question_mark *
                                 line.grade_true_id.value)/100
                else:
                    total_incorrect += 1
                    received_marks += (line.question_mark *
                                       line.grade_false_id.value)/100
                    line.mark = (line.question_mark *
                                 line.grade_false_id.value)/100
        obj.total_marks = total_marks or 0.0
        obj.total_not_attempt = total_not_attempt or 0.0
        obj.total_incorrect = total_incorrect or 0.0
        obj.total_correct = total_correct or 0.0
        obj.received_marks = received_marks or 0.0
        obj.score = (received_marks * 100) / total_marks
        return res

    def get_answer_data(self):

        res = super(QuizResultMatchFollowingimages, self).get_answer_data()
        datafilter = list(filter(
            lambda i: i['que_type'] != 'multiple_choice',
            res['not_attempt_answer']))
        res['not_attempt_answer'] = datafilter
        for line in self.line_ids:
            if line.que_type == 'multiple_choice':
                temp_total_correct = 0
                total_attemp = 0
                total_question_line = len(line.multiple_choice_line_ids)
                for data in line.multiple_choice_line_ids:
                    if data.default_answer == data.given_answer:
                        temp_total_correct += 1
                if len(line.multiple_choice_line_ids) == total_attemp:
                    questiondata = []
                    for temp in line.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'que_image': temp.que_image,
                            'que_text': temp.que_text,
                            'que_type': line.multiple_choice_que_type,
                            'default_answer': temp.default_answer,
                            'id': temp.id
                        })
                    res['not_attempt_answer'].append(
                        {'que_type': line.que_type,
                         'question': line.name,
                         'answer': line.answer or '',
                         'line_data': questiondata})
                elif(temp_total_correct == total_question_line):
                    questiondata = []
                    for temp in line.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'que_image': temp.que_image,
                            'que_text': temp.que_text,
                            'que_type': line.multiple_choice_que_type,
                            'default_answer': temp.default_answer,
                            'id': temp.id
                        })
                    res['right_answers'].append(
                        {'que_type': line.que_type, 'question': line.name,
                         'answer': line.answer, 'line_data': questiondata})
                else:
                    questiondata = []
                    for temp in line.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'que_image': temp.que_image,
                            'que_text': temp.que_text,
                            'que_type': line.multiple_choice_que_type,
                            'default_answer': temp.default_answer,
                            'id': temp.id
                        })
                    res['wrong_answer'].append(
                        {'que_type': line.que_type, 'question': line.name,
                         'given_answer': line.given_answer,
                         'answer': line.answer, 'line_data': questiondata})
        quiz = self.quiz_id
        if quiz.wrong_ans and res['wrong_answer']:
            res['display_wrong_ans'] = 1
        if quiz.right_ans and res['right_answers']:
            res['display_true_ans'] = 1
        if quiz.not_attempt_ans and res['not_attempt_answer']:
            res['not_attempt_ans'] = 1
        return res

    def get_quiz_grid_data(self, current_line):

        res = super(QuizResultMatchFollowingimages,
                    self).get_quiz_grid_data(current_line)
        quiz = self.quiz_id
        que_no = 1
        temp = True
        number = 0
        for line in self.line_ids:
            if line.que_type == 'multiple_choice':
                is_ans_given = 0
                is_readonly = 0
                current_id = 0
                if line.id == current_line.id:
                    current_id = 1
                    temp = False
                for result in line.multiple_choice_line_ids:
                    if result.given_answer:
                        is_ans_given = 1
                if line.id == current_line.id:
                    current_id = 1
                    temp = False
                if not quiz.prev_allow:
                    is_readonly = 1
                if quiz.que_required:
                    if not temp and is_ans_given == 0:
                        is_readonly = 1
                res[number].update({
                    'is_ans_given': is_ans_given,
                    'is_readonly': is_readonly,
                    'line': line,
                    'quiz': self,
                    'que_no': que_no,
                    'current_id': current_id
                })
                que_no += 1
            number = number + 1
        return res
