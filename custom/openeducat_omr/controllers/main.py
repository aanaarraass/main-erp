# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import io
import base64
from werkzeug.utils import redirect
from odoo import http
from odoo import _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal,\
    pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.addons.website.controllers.main import QueryURL
from odoo.tools import consteq
from odoo.osv import expression
from collections import OrderedDict

PPG = 12  # Products Per Page
PPR = 4  # Products Per Row


class OMRScanner(CustomerPortal):

    def _document_check_access(self, model_name, document_id, access_token=None):
        document = request.env[model_name].browse([document_id])
        document_sudo = document.with_user(SUPERUSER_ID).exists()
        if not document_sudo:
            raise MissingError(_("This document does not exist."))
        try:
            document.check_access_rights('read')
            document.check_access_rule('read')
        except AccessError:
            if not access_token or not document_sudo.access_token or not consteq(
                    document_sudo.access_token, access_token):
                raise
        return document_sudo

    @http.route(['/openeducat-omr/exam/result/<int:order_id>',
                 '/openeducat-omr/exam/result/<int:student_id>/<int:order_id>'],
                type='http', auth="user", website=True)
    def portal_omr_exam_result_download(self, order_id, mimetype=None,
                                        access_token=None, download=False, **post):
        try:
            order_sudo = self._document_check_access('op.answer.sheets', order_id,
                                                     access_token=access_token)
            image_attachment = order_sudo.image_id
            return self.download_attachment(image_attachment)

        except (AccessError, MissingError):
            return request.redirect('/openeducat-omr/exam')

    def download_attachment(self, attachment_id):
        attachment = request.env['op.omr.image'].sudo().search_read(
            [('id', '=', int(attachment_id))]
        )
        if attachment:
            attachment = attachment[0]
        else:
            return redirect(self.orders_page)

        if attachment["image"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["image"]))
            filename = 'result'
            return http.send_file(data, filename=filename, as_attachment=True)

        else:
            return request.not_found()

    @http.route(['/openeducat-omr/exam',
                 '/openeducat-omr/exam/<int:student_id>',
                 '/openeducat-omr/exam/<int:page>',
                 '/openeducat-omr/exam/<int:student_id>/page/<int:page>'], type='http',
                auth="user", website=True, csrf=False)
    def openeducat_omr_exam(self, date_begin=None, student_id=None,
                            date_end=None, page=1, search=None,
                            ppg=False, sortby=None, filterby=None,
                            search_in='all', groupby='none', **post):

        user = request.env.user
        student_id = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        omr_result_count = request.env['op.answer.sheets'].sudo()\
            .search_count([('student_id', '=', student_id.id),
                           ('omr_exam_id.state', '=', 'done')])
        values = {}
        values['omr_result_count'] = omr_result_count

        domain = [('student_id', '=', student_id.id),
                  ('omr_exam_id.state', '=', 'done')]
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sorting = {
            'id': {'label': _('Newest'), 'order': 'id desc'},
            'omr_exam_id': {'label': _('Exam'), 'order': 'omr_exam_id'},
            'right_answer': {'label': _('Right Answer'), 'order': 'right_answer'},
            'score': {'label': _('Total Score'), 'order': 'score'},
        }

        if not sortby:
            sortby = 'id'
        order = searchbar_sorting[sortby]['order']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")]
                         for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_inputs = {
            'all': {'input': 'all',
                    'label': _('Search in All')},
            'omr_exam_id.name': {'input': 'omr_exam_id.name',
                                 'label': _('OMR Exam')},
            'roll_number': {'input': 'roll_number',
                            'label': _('Roll Number')},
            'key_type': {'input': 'key_type',
                         'label': _('Paper Set')},
            'score': {'input': 'score',
                      'label': _('Score')},
            'right_answer': {'input': 'right_answer',
                             'label': _('Right Answer')},
            'wrong_answer': {'input': 'wrong_answer',
                             'label': _('Wrong Answer')},
            'not_attampted': {'input': 'not_attampted',
                              'label': _('Not Attempted')},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'wrong_answer'):
                search_domain = expression.OR(
                    [search_domain, [('wrong_answer', 'ilike', search)]])
            if search_in in ('all', 'omr_exam_id'):
                search_domain = expression.OR(
                    [search_domain, [('omr_exam_id.name', 'ilike', search)]])
            if search_in in ('all', 'roll_number'):
                search_domain = expression.OR(
                    [search_domain, [('roll_number', 'ilike', search)]])
            if search_in in ('all', 'score'):
                search_domain = expression.OR(
                    [search_domain, [('score', 'ilike', search)]])
            if search_in in ('all', 'not_attampted'):
                search_domain = expression.OR(
                    [search_domain, [('not_attampted', 'ilike', search)]])
            domain += search_domain

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        if student_id:
            keep = QueryURL('/openeducat-omr/exam/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            omr_result_count = request.env['op.answer.sheets']. \
                sudo().search_count([('student_id', '=', student_id.id),
                                     ('omr_exam_id.state', '=', 'done')])
            pager = portal_pager(
                url="/openeducat-omr/exam/%s" % student_id,
                url_args={
                    'sortby': sortby,
                    'filterby': filterby,
                    'search': search,
                    'search_in': search_in
                },
                total=omr_result_count,
                page=page,
                step=ppg
            )

        if student_id:
            omr_result = request.env['op.answer.sheets'].sudo()\
                .search(domain, order=order, limit=ppg, offset=pager['offset'])

            data = []
            for res in omr_result:
                data.append({
                    'id': res,
                    'omr_image': res.get_portal_url(report_type='pdf', download=True),
                })
            post['result_data'] = data

            values.update({
                'user': request.env.user,
                'page_name': 'OMR Exam Result',
                'default_url': '/openeducat-omr/exam',
                'pager': pager,
                'keep': keep,
                'result_data': data,
                'searchbar_sorting': searchbar_sorting,
                'sortby': sortby,
                'searchbar_inputs': searchbar_inputs,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'search_in': search_in,
            })
            return request.render('openeducat_omr.'
                                  'omr_exam_result', values)


class CustomerPortal(CustomerPortal):

    @http.route()
    def home(self, **kw):
        """ Add sales documents to main account page """
        response = super(CustomerPortal, self).home(**kw)
        user = request.env.user
        student_id = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        omr_result_count = request.env['op.answer.sheets']. \
            sudo().search_count([('student_id', '=', student_id.id),
                                 ('omr_exam_id.state', '=', 'done')])
        response.qcontext.update({
            'omr_result_count': omr_result_count
        })
        return response
