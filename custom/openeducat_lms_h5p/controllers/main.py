import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, UserError
from odoo.addons.openeducat_lms_website.controllers.main import \
    OpenEduCatLms

_logger = logging.getLogger(__name__)


class OpenEduCatLmsH5p(OpenEduCatLms):

    @http.route()
    def create_slide(self, *args, **post):
        if post.get('datas'):
            file_size = len(post['datas']) * 3 / 4  # base64
            if (file_size / 1024.0 / 1024.0) > 25:
                return {'error': _('File is too big. File size cannot exceed 25MB')}

        values = dict((fname, post[fname]) for fname in self.
                      _get_valid_slide_post_values() if post.get(fname))

        try:
            channel = request.env['op.course'].browse(values['course_id'])
            can_upload = channel.can_upload
            can_publish = channel.can_publish
        except (UserError, AccessError) as e:
            _logger.error(e)
            return {'error': e.name}
        else:
            if not can_upload:
                return {'error': _('You cannot upload on this channel.')}

        if post.get('document_url'):
            values['document_url'] = post.get('document_url')
        if post.get('iframe_video_data'):
            values['iframe_video_data'] = post.get('iframe_video_data')
        if post.get('duration'):
            values['total_time'] = int(post['duration']) / 60
        if post.get('material_type') == 'video':
            document_type, document_id = request.env['op.material'].\
                _find_document_data_from_url(post['url'])
            values['document_id'] = document_id
        if post.get('category_id'):
            category_id = post['category_id'][0]

        try:
            values['user_id'] = request.env.uid
            values['is_published'] = values.get('is_published', False) and can_publish
            slide = request.env['op.material'].sudo().create(values)
            slide._compute_get_embed_code()
        except (UserError, AccessError) as e:
            _logger.error(e)
            return {'error': e.name}
        except Exception as e:
            _logger.error(e)
            return {'error': _(
                'Internal server error, please try again later or '
                'contact administrator.\nHere is the error message: %s') % e}

        material_seq = request.env['op.course.section'].search([
            ('id', 'in', post['category_id'])])
        material_seq.seq = material_seq.seq + 1
        section_material = request.env['op.course.material'].create({
            'sequence': material_seq.seq,
            'section_id': category_id,
            'material_id': slide.id

        })

        redirect_url = "%s" % (channel.id)
        if slide.material_type == "quiz":
            action_id = request.env.ref('openeducat_lms.'
                                        'act_open_op_course_material_view').id
            redirect_url = '/web#id=%s&action=%s&model=op.material&view_type=form' \
                           % (slide.id, action_id)
        return {
            'section_material_ids': section_material,
            'url': redirect_url,
            'slide_id': slide.id,
            'category_id': slide.category_id
        }
