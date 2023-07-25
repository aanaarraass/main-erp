# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import calendar
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import dateutil.parser

from odoo.exceptions import ValidationError
from odoo.http import request

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website.controllers.main import QueryURL
from odoo.osv import expression
from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from markupsafe import Markup

PPG = 10  # record per page


class LibraryPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(LibraryPortal, self)._prepare_portal_layout_values()
        library_count = request.env['op.media'].sudo().search_count([])
        values['library_count'] = library_count

        user = request.env.user
        queue_req_count = request.env['op.media.queue'].sudo().search_count(
            [('user_id', '=', user.id)])
        values['queue_req_count'] = queue_req_count

        purchase_req_count = request.env['op.media.purchase'].sudo(). \
            search_count([('requested_id', '=', user.partner_id.id)])
        values['purchase_req_count'] = purchase_req_count

        media_movement_count = request.env['op.media.movement'].sudo(). \
            search_count([('user_id', '=', user.id)])
        values['media_movement_count'] = media_movement_count

        return values

    def _parent_prepare_portal_layout_values(self, student_id=None):

        val = super(LibraryPortal, self). \
            _parent_prepare_portal_layout_values(student_id)
        student = request.env['op.student'].sudo().search(
            [('id', '=', student_id)])

        library_count = request.env['op.media'].sudo().search_count([])
        val['library_count'] = library_count

        queue_req_count = request.env['op.media.queue'].sudo().search_count(
            [('user_id', '=', student.user_id.id)])
        val['queue_req_count'] = queue_req_count

        purchase_req_count = request.env['op.media.purchase'].sudo(). \
            search_count([('requested_id', '=', student.partner_id.id)])
        val['purchase_req_count'] = purchase_req_count

        media_movement_count = request.env['op.media.movement'].sudo(). \
            search_count([('student_id', '=', student_id)])
        val['media_movement_count'] = media_movement_count
        return val

    def get_search_domain_library_media(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('name', 'ilike', srch),
                    ('media_type_id', 'ilike', srch), ('isbn', 'ilike', srch),
                    ('internal_code', 'ilike', srch), ('edition', 'ilike', srch)]

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

    @http.route(['/library/media/',
                 '/library/media/<int:student_id>',
                 '/library/media/page/<int:page>',
                 '/library/media/<int:student_id>/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_student_library_media_list(
            self, student_id=None, date_begin=None, date_end=None,
            page=1, search='', ppg=False, sortby=None, filterby=None,
            search_in='content', groupby='media_type_id', **post):

        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sortings = {
            'name': {'label': _('Title'), 'order': 'name'},
            'edition': {'label': _('Edition'), 'order': 'edition'},
            'internal_code': {'label': _('InternalCode'),
                              'order': 'internal_code'},
            'isbn': {'label': _('ISBN'), 'order': 'isbn'}
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_inputs = {
            'content': {'input': 'content',
                        'label': Markup(_('Search <span class="nolabel"> '
                                          '(in Title)</span>'))},
            'media_type_id': {'input': 'media_type_id',
                              'label': _('Search in Media Type')},
            'isbn': {'input': 'isbn', 'label': _('Search in ISBN')},
            'internal_code': {'input': 'internal_code',
                              'label': _('Search in Internal Code')},
            'edition': {'input': 'Edition', 'label': _('Search in Edition')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'media_type_id': {'input': 'media_type_id', 'label': _('Media Type')},
        }
        media_lists = request.env['op.media'].sudo().search([])

        for media in media_lists:
            searchbar_filters.update({
                str(media.media_type_id.id):
                    {'label': media.media_type_id.name,
                     'domain': [('media_type_id', '=', media.media_type_id.id)]},
            })

        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'content'):
                search_domain = expression.OR(
                    [search_domain, [('name', 'ilike', search)]])
            if search_in in ('all', 'media_type_id'):
                search_domain = expression.OR(
                    [search_domain, [('media_type_id', 'ilike', search)]])
            if search_in in ('all', 'isbn'):
                search_domain = expression.OR(
                    [search_domain, [('isbn', 'ilike', search)]])
            if search_in in ('all', 'internal_code'):
                search_domain = expression.OR(
                    [search_domain, [('internal_code', 'ilike', search)]])
            if search_in in ('all', 'edition'):
                search_domain = expression.OR(
                    [search_domain, [('edition', 'ilike', search)]])
            domain += search_domain

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        domain += self.get_search_domain_library_media(search, attrib_values)

        if student_id:
            keep = QueryURL('/library/media/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            total = request.env['op.media'].sudo().search_count(domain)

            pager = portal_pager(
                url="/library/media/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )

        else:
            keep = QueryURL('/library/media/', search=search, attrib=attrib_list,
                            order=post.get('order'))

            total = request.env['op.media'].sudo().search_count(domain)

            pager = portal_pager(
                url="/library/media/",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )

        if groupby == 'media_type_id':
            order = "media_type_id, %s" % order

        tasks = request.env['op.media'].sudo().search(domain, order=order, limit=ppg,
                                                      offset=pager['offset'])
        if groupby == 'media_type_id':
            grouped_tasks = [request.env['op.media'].sudo().concat(*g) for k, g in
                             groupbyelem(tasks, itemgetter('media_type_id'))]
        else:
            grouped_tasks = [tasks]

        media_id = request.env["op.media"].sudo().search(
            domain, order=order, limit=ppg, offset=pager['offset'])

        if student_id:
            val.update({
                'date': date_begin,
                'library_id': media_id,
                'page_name': 'Library_media_list',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'stud_id': student_id,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/library/media/',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })
            return request.render(
                "openeducat_library_enterprise.openeducat_library_midia_portal",
                val)

        else:
            values.update({
                'date': date_begin,
                'library_id': media_id,
                'page_name': 'Library_media_list',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/library/media/',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })
            return request.render(
                "openeducat_library_enterprise.openeducat_library_midia_portal",
                values)

    @http.route(['/library/media/info/<int:library_id>',
                 '/library/media/info/<int:student_id>/<int:library_id>'],
                type='http', auth="user", website=True)
    def portal_student_library_media_form(self, student_id=None, library_id=None):

        media_all_id = request.env['op.media'].sudo().search(
            [('id', '=', library_id)])

        return request.render(
            "openeducat_library_enterprise.openeducat_library_media_data",
            {'library_ids': media_all_id,
             'student': student_id,
             'page_name': 'library_media_info', })

    @http.route(['/media/queue/request',
                 '/media/queue/request/<int:student_id>',
                 '/media/queue/request/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_library_queue_craete(self, student_id=None, **kw):

        user = request.env.user
        if student_id:
            student_queue_id = request.env['op.student'].sudo().search(
                [('user_id', '=', student_id)])
        else:
            student_queue_id = request.env['op.student'].sudo().search(
                [('user_id', '=', user.id)])

        media_data = request.env['op.media'].sudo().search([])

        return request.render(
            "openeducat_library_enterprise.openeducat_library_media_queue",
            {
                'student_ids': student_queue_id,
                'media_queue_ids': media_data,
                'date_from': datetime.today().strftime("%m/%d/%Y"),
                'page_name': 'media_queue_req_form'
            }
        )

    @http.route(['/queue/request/submit/',
                 '/queue/request/submit/<int:student_id>',
                 '/queue/request/submit/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_submit_media_queue_request(self, **kw):

        user = request.env.user

        date_to = dateutil.parser.parse(kw['date_to']).strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        date_from = dateutil.parser.parse(kw['date_from']).strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        vals = {
            'media_id': int(kw['media_ids']),
            'user_id': user.id,
            'date_to': date_to,
            'date_from': date_from,
        }
        try:
            media_id = request.env['op.media.queue'].sudo().create(vals)
            media_id.do_request_again()
        except ValidationError as e:
            raise e

        media_queue_dict = {}
        media_queue_dict.update()
        return request.render(
            "openeducat_library_enterprise.portal_submited_queue_request",
            {'media_ids': media_id,
             'page_name': 'submited_queue_req'})

    def get_search_domain_library_media_queue(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('name', 'ilike', srch),
                    ('media_id', 'ilike', srch), ('date_from', 'ilike', srch),
                    ('date_to', 'ilike', srch), ('state', 'ilike', srch)]

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

    @http.route(['/requested/queue/list/',
                 '/requested/queue/list/<int:student_id>',
                 '/requested/queue/list/page/<int:page>',
                 '/requested/queue/list/<int:student_id>/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_media_queue_requested_list(
            self, student_id=None, date_begin=None, date_end=None, page=0,
            search='', ppg=False, sortby=None, filterby=None,
            search_in='content', groupby='media_id', **post):

        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()
        user = request.env.user

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sortings = {
            'name': {'label': _('Sequence'), 'order': 'name'},
            'date_from': {'label': _('From Date'), 'order': 'date_from'},
            'date_to': {'label': _('To Date'), 'order': 'date_to'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'state accept': {'label': _('Accepted'),
                             'domain': [('state', '=', 'accept')]},
            'state reject': {'label': _('Rejected'),
                             'domain': [('state', '=', 'reject')]},
            'state request': {'label': _('Request'),
                              'domain': [('state', '=', 'request')]},
        }
        searchbar_inputs = {
            'content': {'input': 'content',
                        'label': Markup(_('Search <span class="nolabel"> '
                                          '(in Sequence)</span>'))},
            'media_id': {'input': 'Media', 'label': _('Search in Media')},
            'date_from': {'input': 'Date From', 'label': _('Search in End Date')},
            'date_to': {'input': 'Date To', 'label': _('Search in Date To')},
            'state': {'input': 'Status', 'label': _('Search in Status')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'media_id': {'media_id': 'name', 'label': _('Media')},
        }

        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'content'):
                search_domain = expression.OR(
                    [search_domain, [('name', 'ilike', search)]])
            if search_in in ('all', 'media_id'):
                search_domain = expression.OR(
                    [search_domain, [('media_id', 'ilike', search)]])
            if search_in in ('all', 'date_from'):
                search_domain = expression.OR(
                    [search_domain, [('date_from', 'ilike', search)]])
            if search_in in ('all', 'date_to'):
                search_domain = expression.OR(
                    [search_domain, [('date_to', 'ilike', search)]])
            if search_in in ('all', 'state'):
                search_domain = expression.OR(
                    [search_domain, [('state', 'ilike', search)]])
            domain += search_domain

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        domain += self.get_search_domain_library_media_queue(search, attrib_values)
        if student_id:
            keep = QueryURL('/requested/queue/list/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))
            student = request.env['op.student'].sudo().search(
                [('id', '=', student_id)])
            domain += [('user_id', '=', student.user_id.id)]
            total = request.env['op.media.queue'].sudo().search_count(
                domain)

            pager = portal_pager(
                url="/requested/queue/list/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )

        else:
            keep = QueryURL('/requested/queue/list/',
                            search=search, attrib=attrib_list,
                            order=post.get('order'))
            domain += [('user_id', '=', user.id)]
            total = request.env['op.media.queue'].sudo().search_count(
                domain)

            pager = portal_pager(
                url="/requested/queue/list/",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )

        if student_id:
            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')
            media_queue_id = request.env['op.media.queue'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])
        else:
            media_queue_id = request.env['op.media.queue'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])

        if groupby == 'media_id':
            grouped_tasks = [
                request.env['op.media.queue'].sudo().concat(*g)
                for k, g in groupbyelem(media_queue_id, itemgetter('media_id'))]
        else:
            grouped_tasks = [media_queue_id]

        if student_id:
            val.update({
                'date': date_begin,
                'media_ids': media_queue_id,
                'page_name': 'Media Queue List',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'stud_id': student_id,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/requested/queue/list/%s' % student_id,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })
            return request.render(
                "openeducat_library_enterprise.portal_submited_queue_request_list",
                val)

        else:
            values.update({
                'date': date_begin,
                'media_ids': media_queue_id,
                'page_name': 'Media Queue List',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/requested/queue/list/',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })

            return request.render(
                "openeducat_library_enterprise.portal_submited_queue_request_list",
                values)

    @http.route(['/media/purchase/request',
                 '/media/purchase/request/<int:student_id>/',
                 '/media/purchase/request/page/<int:student_id>/'],
                type='http', auth="user", website=True)
    def portal_library_media_purchase_create(self, student_id=None, **kw):

        user = request.env.user
        student_id = request.env['op.student'].sudo().search(
            [('user_id', '=', user.id)])
        media_course = request.env['op.course'].sudo().search([])
        lms_module = request.env['ir.module.module'].sudo().search(
            [('name', '=', 'openeducat_lms')])

        if lms_module.state != 'uninstalled':
            media_course = request.env['op.course'].sudo().search(
                [('online_course', '!=', True)])

        media_subject = request.env['op.subject'].sudo().search([])
        media_type = request.env['op.media.type'].sudo().search([])

        media_purchase_dict = {}
        media_purchase_dict.update()

        return request.render(
            "openeducat_library_enterprise.openeducat_library_media_purchase",
            {
                'student_ids': student_id,
                'course_ids': media_course,
                'subject_ids': media_subject,
                'media_type_ids': media_type,
                'page_name': 'media_purchase_req_form'
            }
        )

    @http.route(['/purchase/request/submit/',
                 '/purchase/request/submit/<int:student_id>',
                 '/purchase/request/submit/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_submit_media_purchase_request(self, **kw):

        partner = request.env.user.partner_id
        vals = {
            'name': kw['title'],
            'author': kw['authore'],
            'publisher': kw['publisher'],
            'edition': kw['edition'],
            'requested_id': partner.id,
            'course_ids': int(kw['media_ids']),
            'media_type_id': int(kw['media_type_ids']),
            'subject_ids': int(kw['subject_ids']),
        }
        media_id = request.env['op.media.purchase'].sudo().create(vals)
        media_id.act_requested()

        return request.render(
            "openeducat_library_enterprise.portal_submited_purchases_request",
            {'media_purchase_ids': media_id,
             'page_name': 'submited_purchase_req'})

    def get_search_domain_media_purchase(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', '|', '|', ('name', 'ilike', srch),
                    ('subject_ids', 'ilike', srch), ('author', 'ilike', srch),
                    ('edition', 'ilike', srch), ('media_type_id', 'ilike', srch),
                    ('publisher', 'ilike', srch), ('course_ids', 'ilike', srch)]

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

    @http.route(['/requested/purchase/list/',
                 '/requested/purchase/list/<int:student_id>',
                 '/requested/purchase/list/page/<int:page>',
                 '/requested/purchase/list/<int:student_id>/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_media_purchase_requested_list(
            self, student_id=None, date_begin=None, date_end=None, page=1,
            search='', ppg=False, sortby=None, filterby=None,
            search_in='content', groupby='course_ids', **post):

        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sortings = {
            'name': {'label': _('Title'), 'order': 'name'},
            'edition': {'label': _('Edition'), 'order': 'edition'},
            'author': {'label': _('Author(S)'), 'order': 'author'},
            'course_ids': {'label': _('Course'), 'order': 'course_ids'},
            'subject_ids': {'label': _('Subject'), 'order': 'subject_ids'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'state accept': {'label': _('Accepted'),
                             'domain': [('state', '=', 'accept')]},
            'state reject': {'label': _('Rejected'),
                             'domain': [('state', '=', 'reject')]},
            'state request': {'label': _('Request'),
                              'domain': [('state', '=', 'request')]},
        }
        searchbar_inputs = {
            'content': {'input': 'content',
                        'label': Markup(_('Search <span class="nolabel">'
                                          ' (in Title)</span>'))},
            'subject_ids': {'input': 'Subject',
                            'label': _('Search in Subject')},
            'course_ids': {'input': 'Course',
                           'label': _('Search in Course')},
            'media_type_id': {'input': 'Media Type',
                              'label': _('Search in Media Type')},
            'edition': {'input': 'Edition',
                        'label': _('Search in Edition')},
            'author': {'input': 'Author',
                       'label': _('Search in Author')},
            'publisher': {'input': 'Publisher',
                          'label': _('Search in Publisher')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'course_ids': {'input': 'course_ids', 'label': _('Course')},
        }

        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'content'):
                search_domain = expression.OR(
                    [search_domain, [('name', 'ilike', search)]])
            if search_in in ('all', 'subject_ids'):
                search_domain = expression.OR(
                    [search_domain, [('subject_ids', 'ilike', search)]])
            if search_in in ('all', 'course_ids'):
                search_domain = expression.OR(
                    [search_domain, [('course_ids', 'ilike', search)]])
            if search_in in ('all', 'media_type_id'):
                search_domain = expression.OR(
                    [search_domain, [('media_type_id', 'ilike', search)]])
            if search_in in ('all', 'edition'):
                search_domain = expression.OR(
                    [search_domain, [('edition', 'ilike', search)]])
            if search_in in ('all', 'author'):
                search_domain = expression.OR(
                    [search_domain, [('author', 'ilike', search)]])
            if search_in in ('all', 'publisher'):
                search_domain = expression.OR(
                    [search_domain, [('publisher', 'ilike', search)]])
            domain += search_domain

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        domain += self.get_search_domain_media_purchase(search, attrib_values)
        if student_id:
            keep = QueryURL('/requested/purchase/list/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))
            student = request.env['op.student'].sudo().search(
                [('id', '=', student_id)])

            domain += [('requested_id', '=', student.partner_id.id)]
            total = request.env['op.media.purchase'].sudo().search_count(domain)

            pager = portal_pager(
                url="/requested/purchase/list/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search},
                total=total,
                page=page,
                step=ppg
            )

        else:
            keep = QueryURL('/requested/purchase/list/',
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            partner = request.env.user.partner_id
            domain += [('requested_id', '=', partner.id)]
            total = request.env['op.media.purchase'].sudo().search_count(domain)

            pager = portal_pager(
                url="/requested/purchase/list/",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search},
                total=total,
                page=page,
                step=ppg
            )

        if groupby == 'course_ids':
            order = "course_ids, %s" % order

        if student_id:
            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')
            media_purchase_id = request.env['op.media.purchase'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])
        else:
            media_purchase_id = request.env['op.media.purchase'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])

        if groupby == 'course_ids':
            grouped_tasks = [
                request.env['op.media.purchase'].sudo().concat(*g)
                for k, g in groupbyelem(media_purchase_id, itemgetter('course_ids'))]
        else:
            grouped_tasks = [media_purchase_id]

        if student_id:
            val.update({
                'date': date_begin,
                'purchase_ids': media_purchase_id,
                'page_name': 'Media Purchase List',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'stud_id': student_id,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/requested/purchase/list/%s' % student_id,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })
            return request.render(
                "openeducat_library_enterprise."
                "portal_submited_purchase_request_list",
                val)

        else:
            values.update({
                'date': date_begin,
                'purchase_ids': media_purchase_id,
                'page_name': 'Media Purchase List',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/requested/purchase/list/',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,

            })

            return request.render(
                "openeducat_library_enterprise."
                "portal_submited_purchase_request_list",
                values)

    def get_search_domain_media_movement(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', '|', '|', ('media_id', 'ilike', srch),
                    ('state', 'ilike', srch), ('penalty', 'ilike', srch),
                    ('media_unit_id', 'ilike', srch),
                    ('return_date', 'ilike', srch), ('issued_date', 'ilike', srch),
                    ('actual_return_date', 'ilike', srch)]

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

    @http.route(['/media/movement/list',
                 '/media/movement/list/<int:student_id>',
                 '/media/movement/list/page/<int:page>',
                 '/media/movement/list/<int:student_id>/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_media_movement_list(
            self, student_id=None, date_begin=None, date_end=None, page=1,
            search='', ppg=False, sortby=None, filterby=None,
            search_in='content', groupby='media_id', **post):

        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sortings = {
            'media_id': {'label': _('Media'), 'order': 'media_id'},
            'media_unit_id': {'label': _('Media Unit'),
                              'order': 'media_unit_id'},
            'issued_date': {'label': _('Issued Date'),
                            'order': 'issued_date'},
            'return_date': {'label': _('Return Date'),
                            'order': 'return_date'},
            'actual_return_date': {'label': _('Actual Return Date'),
                                   'order': 'actual_return_date'},
            'penalty': {'label': _('Penalty'), 'order': 'penalty'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        if not sortby:
            sortby = 'media_id'
        order = searchbar_sortings[sortby]['order']
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'state available': {'label': _('Available'),
                                'domain': [('state', '=', 'available')]},
            'state isuse': {'label': _('Issued'),
                            'domain': [('state', '=', 'issue')]},
            'state return': {'label': _('Return'),
                             'domain': [('state', '=', 'return')]},
            'state return_done': {'label': _('Return Done'),
                                  'domain': [('state', '=', 'return_done')]},
        }
        searchbar_inputs = {
            'content': {'input': 'content',
                        'label': Markup(_('Search <span class="nolabel"> '
                                          '(in Media)</span>'))},
            'media_unit_id': {'input': 'media_unit_id',
                              'label': _('Search in Media Unit')},
            'penalty': {'input': 'penalty',
                        'label': _('Search in Penalty')},
            'issued_date': {'input': 'issued_date',
                            'label': _('Search in Issued Date')},
            'actual_return_date': {'input': 'actual_return_date',
                                   'label': _('Search in Actual Return Date')},
            'return_date': {'input': 'return_date',
                            'label': _('Search in Return Date')},
            'state': {'input': 'State', 'label': _('Search in State')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'media_id': {'input': 'media_id', 'label': _('Media')},
        }

        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'content'):
                search_domain = expression.OR(
                    [search_domain, [('media_id', 'ilike', search)]])
            if search_in in ('all', 'media_unit_id'):
                search_domain = expression.OR(
                    [search_domain, [('media_unit_id', 'ilike', search)]])
            if search_in in ('all', 'penalty'):
                search_domain = expression.OR(
                    [search_domain, [('penalty', 'ilike', search)]])
            if search_in in ('all', 'issued_date'):
                search_domain = expression.OR(
                    [search_domain, [('issued_date', 'ilike', search)]])
            if search_in in ('all', 'actual_return_date'):
                search_domain = expression.OR(
                    [search_domain, [('actual_return_date', 'ilike', search)]])
            if search_in in ('all', 'return_date'):
                search_domain = expression.OR(
                    [search_domain, [('return_date', 'ilike', search)]])
            if search_in in ('all', 'state'):
                search_domain = expression.OR(
                    [search_domain, [('state', 'ilike', search)]])
            domain += search_domain

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        domain += self.get_search_domain_media_movement(search, attrib_values)
        if student_id:
            keep = QueryURL('/media/movement/list/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            domain += [('student_id', '=', student_id)]
            total = request.env['op.media.movement'].sudo().search_count(domain)

            pager = portal_pager(
                url="/media/movement/list/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search},
                total=total,
                page=page,
                step=ppg
            )
        else:
            keep = QueryURL('/media/movement/list',
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            domain += [('user_id', '=', request.env.user.id)]
            total = request.env['op.media.movement'].sudo().search_count(domain)

            pager = portal_pager(
                url="/media/movement/list",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search},
                total=total,
                page=page,
                step=ppg
            )

        if groupby == 'media_id':
            order = "media_id, %s" % order

        if student_id:
            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')
            media_movement_id = request.env['op.media.movement'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])
        else:
            media_movement_id = request.env['op.media.movement'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])

        if groupby == 'media_id':
            grouped_tasks = [
                request.env['op.media.movement'].sudo().concat(*g)
                for k, g in groupbyelem(media_movement_id, itemgetter('media_id'))]
        else:
            grouped_tasks = [media_movement_id]

        if student_id:

            val.update({
                'date': date_begin,
                'media_movement_ids': media_movement_id,
                'page_name': 'Media_movement_list',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'stud_id': student_id,
                'default_url': '/media/movement/list/%s' % student_id,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })
            return request.render(
                "openeducat_library_enterprise.portal_student_media_movement_list",
                val)
        else:
            values.update({
                'date': date_begin,
                'media_movement_ids': media_movement_id,
                'page_name': 'Media_movement_list',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'stud_id': student_id,
                'default_url': '/media/movement/list',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'searchbar_inputs': searchbar_inputs,
                'search_in': search_in,
                'grouped_tasks': grouped_tasks,
                'searchbar_groupby': searchbar_groupby,
                'groupby': groupby,
            })

            return request.render(
                "openeducat_library_enterprise.portal_student_media_movement_list",
                values)

    @http.route([
        '/media/movement/information/<int:media_movement_id>',
        '/media/movement/information/<int:student_id>/<int:media_movement_id>'],
        type='http', auth="user", website=True)
    def portal_media_movement_information(
            self, student_id=None, media_movement_id=None, **kw):

        media_movement = request.env['op.media.movement'].sudo().search(
            [('id', '=', media_movement_id)])

        return request.render(
            "openeducat_library_enterprise."
            "portal_student_media_movement_information",
            {'media_movement_ids': media_movement,
             'student': student_id,
             'page_name': 'media_movement_info'})


class OpenEduCatLibraryController(http.Controller):

    @http.route('/openeducat_library_enterprise/get_library_dashboard_data',
                type='json', auth='user')
    def compute_library_dashboard_data(self):
        dbt = 0
        dbm = 0
        tpat = 0

        media = request.env['ir.model'].search(
            [('model', '=', 'op.media')])
        if media:
            last_day = date.today().replace(
                day=calendar.monthrange(date.today().year,
                                        date.today().month)[1])
            dbt = request.env['op.media.movement'].search_count(
                [('state', '=', 'issue'), ('return_date', '=', date.today())])
            dbm = request.env['op.media.movement'].search_count([
                ('state', '=', 'issue'),
                ('return_date', '>=', date.today().strftime('%Y-%m-01')),
                ('return_date', '<=', last_day)])
            movements_ids = request.env['op.media.movement'].search(
                [('state', '=', 'return'),
                 ('return_date', '>=', date.today().strftime('%Y-%m-01')),
                 ('return_date', '<=', last_day)])
            for movement in movements_ids:
                tpat += movement.penalty
        return {'dbt': dbt, 'dbm': dbm, 'tpat': tpat}
