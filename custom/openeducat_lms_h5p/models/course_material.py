from odoo import fields, models


class CourseMaterial(models.Model):
    _inherit = "op.material"

    material_type = fields.Selection(
        selection_add=[
            ('h5p_url', 'H5p URL'),
            ('h5p_iframe', 'H5p Iframe')],
        required=False, default='video'
    )
    iframe_video_data = fields.Text('H5p Iframe')

    def _compute_get_embed_code(self):
        super(CourseMaterial, self)._compute_get_embed_code()
        for record in self:
            if record.material_type == 'h5p_url' and \
                    record.document_url:
                url = str(record.document_url) + \
                         ('' if record.document_url.split('/')[-1] ==
                          'embed' else '/embed')
                record.embed_code = '<iframe  src="%s"\
                            width="1088" height="637" \
                            frameborder="0" allowfullscreen="allowfullscreen" \
                            allow="geolocation *; microphone *; camera *; midi *;' \
                                    ' encrypted-media *"></iframe> \
                    <script src="https://ebz.h5p.com/js/h5p-resizer.js"' \
                                    ' charset="UTF-8"></script>' % (url)
            if record.material_type == 'h5p_iframe' and \
                    record.iframe_video_data:
                record.embed_code = record.iframe_video_data
