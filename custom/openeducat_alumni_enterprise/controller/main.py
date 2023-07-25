
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import http, modules
from odoo.http import request
import werkzeug.wrappers
import base64


class AlumniWeb(http.Controller):

    @http.route('/alumni', type='http', auth='public', website=True)
    def alumni_group(self, **kwargs):
        alumni_id = request.env['op.alumni.group'].sudo().search([])

        return request.render('openeducat_alumni_enterprise.alumni_page', {
            'alumni_id': alumni_id
        })

    @http.route([
        '/alumni/detail/<model("op.alumni.group"):alumni>'],
        type='http', auth='public', website=True)
    def alumni_detail(self, alumni, **kwargs):
        alumni_id = alumni.sudo().alumni_student_line
        return http.request.render('openeducat_alumni_enterprise.alumni_group',
                                   {'alumni': alumni,
                                    'alumni_id': alumni_id})

    # @http.route([
    #     '/alumni/detail/<model("op.alumni.group"):alumni>/<int:student>'],
    #     type='http', auth="public",sitemap=False, website=True)
    # def jobpost_detail(self, student, alumni, **kwargs):
    #     student_obj = request.env['op.student']
    #     student_id = student_obj.sudo().search([('id', '=', student)])
    #     return request.render("openeducat_alumni_enterprise.student_detail", {
    #         'student': student_id,
    #     })

    @http.route(['/alumni/user/<int:user_id>/avatar'],
                type='http', auth="public", website=True, sitemap=False)
    def user_avatar(self, user_id=0, **post):
        status, headers, content = request.env['ir.http'].\
            sudo().binary_content(model='op.student',
                                  id=user_id, field='image_1920',
                                  default_mimetype='image/png')
        if not content:
            img_path = modules.get_module_resource('web', 'static/src/img',
                                                   'placeholder.png')
            with open(img_path, 'rb') as f:
                image = f.read()
            content = base64.b64encode(image)
        if status == 304:
            return werkzeug.wrappers.Response(status=304)
        image_base64 = base64.b64decode(content)
        headers.append(('Content-Length', len(image_base64)))
        response = request.make_response(image_base64, headers)
        response.status = str(status)
        return response
