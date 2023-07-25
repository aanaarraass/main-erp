from odoo import fields, models, api
from odoo.tools.translate import html_translate


class OpCourseMaterialInteractiveVideo(models.Model):
    _inherit = "op.material"

    material_type = fields.Selection(
        selection_add=[('interactive_video', 'Interactive Video')],
        ondelete={'interactive_video': 'set default'}
    )
    data_interactive_video = fields.Binary('Video')
    interactive_video_line_ids = fields.One2many('op.material.interactive.video',
                                                 'interactive_video_line_id',
                                                 'Question')

    @api.depends('data_interactive_video', 'material_type')
    def _compute_get_embed_code(self):
        res = super(OpCourseMaterialInteractiveVideo, self)._compute_get_embed_code()
        for record in self:
            if record.material_type == 'interactive_video':
                temp = record.data_interactive_video
                record.embed_code = '<video id="v"  .\
                    poster="/openeducat_lms_interactive_video/static/src/img/openeducat.jpg".\
                        oncontextmenu="return false;" class="player__video viewer" .\
                            src="data:video/mp4;base64, %s"></video>.\
                                ' % temp.decode("utf-8")
        return res


class QuizSortParagraphs(models.Model):
    _name = "op.material.interactive.video"
    _description = "openeducat lms interactive video"

    interactive_video_type = fields.Selection([
        ('description', 'Description'), ('quiz', 'Quiz')],
        string="Question Type")
    full_description = fields.Html('Full Description',
                                   translate=html_translate,
                                   sanitize_attributes=False)
    question = fields.Char('Question')
    time = fields.Float('time')
    interactive_video_line_id = fields.Many2one('op.material', 'question' ,
                                                invisible=True)
    quiz_id = fields.Many2one('op.quiz', 'Quiz')
