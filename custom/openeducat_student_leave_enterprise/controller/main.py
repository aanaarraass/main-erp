# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website.controllers.main import QueryURL
from odoo.osv import expression
from collections import OrderedDict
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import dateutil.parser
import base64
from markupsafe import Markup


class StudentTimeOff(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(StudentTimeOff, self)._prepare_portal_layout_values()

        user = request.env.user
        leave_request_count = request.env['student.leave.request'].sudo().search_count(
            [('student_id.user_id.id', '=', user.id)])
        values['leave_request_count'] = leave_request_count
        return values

    def _parent_prepare_portal_layout_values(self, student_id=None):
        val = super(StudentTimeOff, self)._parent_prepare_portal_layout_values(
            student_id)

        leave_request_count = request.env['student.leave.request'].sudo().search_count(
            [('student_id', '=', student_id)])
        val['leave_request_count'] = leave_request_count
        return val

    def get_search_domain_studnet_leave_queue(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                srch = srch.lower()
                if 'requested'.__contains__(srch):
                    srch = 'conf'
                domain += [
                    '|', '|', '|', '|', '|', ('leave_type', 'ilike', srch),
                    ('description', 'ilike', srch), ('start_date', 'ilike', srch),
                    ('end_date', 'ilike', srch), ('state', 'ilike', srch),
                    ('start_date', 'ilike', srch)]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]
        return domain

    @http.route(['/my/time_off/',
                 '/my/time_off/<int:student_id>',
                 '/my/time_off/page/<int:student_id>'],
                type='http', auth="user", website=True)
    def portal_student_time_off(self, student_id=None, sortby=None, search='',
                                start_date=None, end_date=None, page=1, ppg=False,
                                filterby=None, search_in='description', **post):
        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = set([v[1] for v in attrib_values])

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        leave_type = request.env['student.leave.type'].sudo().search([])
        for leave in leave_type:
            searchbar_filters.update({
                str(leave.id):
                    {'label': leave.name,
                     'domain': [('leave_type', '=', leave.id)]},
            })

        searchbar_inputs = {
            'description': {'input': 'description',
                            'label': Markup(_('Search <span class="nolabel"> '
                                              '(Description)</span>'))},
            'leave_type': {'input': 'leave_type',
                           'label': _('Search in Leave Type')},
            'start_date': {'input': 'start_date',
                           'label': _('Search in Start Date')},
            'state': {'input': 'state',
                      'label': _('Search in Status')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        if not filterby:
            filterby = 'all'

        domain = searchbar_filters[filterby]['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'leave_type'):
                search_domain = expression.OR(
                    [search_domain, [('leave_type', 'ilike', search)]])
            if search_in in ('all', 'start_date'):
                search_domain = expression.OR(
                    [search_domain, [('start_date', 'ilike', search)]])
            if search_in in ('all', 'description'):
                search_domain = expression.OR(
                    [search_domain, [('description', 'ilike', search)]])
            if search_in in ('all', 'state'):
                search = search.lower()
                if 'requested'.__contains__(search):
                    search = 'confirm'
                search_domain = expression.OR(
                    [search_domain, [('state', 'ilike', search)]])
            domain += search_domain

        domain += self.get_search_domain_studnet_leave_queue(search, attrib_values)

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'start_date'},
            'state': {'label': _('Status'), 'order': 'state'},
            'leave_type': {'label': _('Leave Type'), 'order': 'leave_type'},
            'request_number': {'label': _('Request Number'), 'order': 'request_number'}}

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        if student_id:
            keep = QueryURL('/my/time_off/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))
            domain += [('student_id', '=', student_id)]
            total = request.env['student.leave.request'].sudo().search_count(domain)

            pager = portal_pager(
                url="/my/time_off/%s" % student_id,
                url_args={'start_date': start_date, 'end_date': end_date,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
            )
        else:
            keep = QueryURL('/my/time_off/', search=search, attrib=attrib_list,
                            order=post.get('order'))
            domain += [('student_id.user_id', '=', request.env.user.id)]
            total = request.env['student.leave.request'].sudo().search_count(domain)

            pager = portal_pager(
                url="/my/time_off/",
                url_args={'start_date': start_date, 'end_date': end_date,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
            )

        if student_id:
            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')
            time_off_request = request.env['student.leave.request'].sudo().search(
                domain, order=order, limit=ppg,
                offset=pager['offset'])
            attributes = request.env[
                'op.subject.registration'].browse(attributes_ids)

        else:
            time_off_request = request.env['student.leave.request'].sudo().search(
                domain, order=order, limit=ppg,
                offset=pager['offset'])
            attributes = request.env[
                'op.subject.registration'].browse(attributes_ids)

        if student_id:
            val.update({'leave_request_ids': time_off_request,
                        'page_name': 'student_time_off_list',
                        'keep': keep,
                        'student_id': student_id,
                        'pager': pager,
                        'default_url': '/my/time_off/%s' % student_id,
                        'attrib_values': attrib_values,
                        'attrib_set': attrib_set,
                        'searchbar_inputs': searchbar_inputs,
                        'search_in': search_in,
                        'attributes': attributes,
                        'searchbar_filters': OrderedDict(
                            sorted(searchbar_filters.items())),
                        'filterby': filterby,
                        'searchbar_sortings': searchbar_sortings,
                        'sortby': sortby,
                        })
            return request.render(
                "openeducat_student_leave_enterprise.student_time_off_portal",
                val)
        else:
            values.update(
                {'leave_request_ids': time_off_request,
                 'page_name': 'student_time_off_list',
                 'keep': keep,
                 'student_id': student_id,
                 'pager': pager,
                 'default_url': '/my/time_off/',
                 'attrib_values': attrib_values,
                 'attrib_set': attrib_set,
                 'searchbar_inputs': searchbar_inputs,
                 'search_in': search_in,
                 'attributes': attributes,
                 'searchbar_filters': OrderedDict(
                     sorted(searchbar_filters.items())),
                 'filterby': filterby,
                 'searchbar_sortings': searchbar_sortings,
                 'sortby': sortby,
                 })
            return request.render(
                "openeducat_student_leave_enterprise.student_time_off_portal", values
            )

    @http.route(['/time_off/request/',
                 '/time_off/request/<int:student_id>',
                 '/time_off/request/page/<int:student_id>'],
                type='http', auth='user', website=True)
    def portal_student_time_off_request(self, student_id=None):
        if student_id:
            student_id = request.env['op.student'].sudo().search(
                [('id', '=', student_id)])
        else:
            user = request.env.user
            student_id = request.env['op.student'].sudo().search(
                [('user_id', '=', user.id)])
        leave_type = request.env['student.leave.type'].sudo().search([])
        faculty_ids = request.env['op.faculty'].sudo().search([])

        return request.render(
            "openeducat_student_leave_enterprise.openeducat_student_time_off_request",
            {'leave_type_ids': leave_type,
             'page_name': 'leave_request_form',
             'faculty_ids': faculty_ids,
             'student_id': student_id})

    @http.route(['/time_off/request/submit/',
                 '/time_off/request/submit/<int:student_id>'],
                type='http', auth='user', website='True')
    def portal_student_time_off_submit(self, student_id=None, **kw):
        start_date = dateutil.parser.parse(kw['start_date']). \
            strftime(DEFAULT_SERVER_DATE_FORMAT)
        end_date = dateutil.parser.parse(kw['end_date']). \
            strftime(DEFAULT_SERVER_DATE_FORMAT)

        if student_id:
            vals = {
                'description': kw['description'],
                'start_date': start_date,
                'end_date': end_date,
                'leave_type': int(kw['leave_type_ids']),
                'faculty_id': kw['faculty_ids'],
                'student_id': int(student_id),
                'state': 'confirm'
            }
        else:
            student_id = request.env['op.student'].sudo().search(
                [('user_id', '=', request.env.user.id)])
            vals = {
                'description': kw['description'],
                'start_date': start_date,
                'end_date': end_date,
                'leave_type': int(kw['leave_type_ids']),
                'faculty_id': kw['faculty_ids'],
                'student_id': student_id,
                'state': 'confirm'
            }
        leave_request = request.env['student.leave.request'].sudo().create(vals)
        if 'attachments' in request.params:
            attached_files = request.httprequest.files.getlist('attachments')
            for attachment in attached_files:
                attached_file = attachment.read()
                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'student.leave.request',
                    'res_id': leave_request,
                    'type': 'binary',
                    'datas': base64.encodebytes(attached_file),
                })

        return request.render(
            "openeducat_student_leave_enterprise.student_time_off_submit",
            {'leave_request': leave_request,
             'page_name': 'leave_request_submit',
             'student_id': student_id})

    @http.route(['/check/leave/data'],
                type='json', auth='user', website='True')
    def check_leave_data(self, **kw):
        if kw.get('start_date') and kw.get('end_date'):
            start_date = dateutil.parser.parse(kw['start_date']). \
                strftime(DEFAULT_SERVER_DATE_FORMAT)
            end_date = dateutil.parser.parse(kw['end_date']). \
                strftime(DEFAULT_SERVER_DATE_FORMAT)
            if kw['student_id']:
                leave_list = request.env['student.leave.request'].sudo().search(
                    [('student_id', '=', int(kw['student_id']))])
            else:
                user = request.env.user
                student_id = request.env['op.student'].sudo().search(
                    [('user_id', '=', user.id)])
                leave_list = request.env['student.leave.request'].sudo().search(
                    [('student_id', '=', student_id.id)])
            count = 0
            for leave in leave_list:
                leave_start_date = dateutil.parser.parse(str(leave.start_date)). \
                    strftime(DEFAULT_SERVER_DATE_FORMAT)
                leave_end_date = dateutil.parser.parse(str(leave.end_date)). \
                    strftime(DEFAULT_SERVER_DATE_FORMAT)
                if leave_start_date <= start_date <= leave_end_date:
                    count += 1
                elif leave_start_date <= end_date <= leave_end_date:
                    count += 1
                elif end_date >= leave_end_date and \
                        start_date <= leave_start_date:
                    count += 1
            return count
