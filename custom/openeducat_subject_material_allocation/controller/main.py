
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.osv import expression
from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
import base64
import io

PPG = 10  # record per page


class SubjectMaterialAllocation(CustomerPortal):

    def _prepare_portal_layout_values(self):

        values = super(SubjectMaterialAllocation, self)._prepare_portal_layout_values()
        user = request.env.user
        student = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        sub_id = []
        attachemnts_ids = []
        for course in student.course_detail_ids:
            for record in course.subject_ids:
                sub_id.append(record.id)
                for j in record.attachment_ids:
                    attachemnts_ids.append(j.id)
        domain = [('id', 'in', sub_id)]

        domain += [('attachment_ids', 'in', attachemnts_ids)]
        material_count = request.env['op.subject'].sudo().search_count(domain)
        values['material_count'] = material_count
        return values

    def _parent_prepare_portal_layout_values(self, student_id=None):

        val = super(SubjectMaterialAllocation, self). \
            _parent_prepare_portal_layout_values(student_id)
        student = request.env["op.student"].sudo().search(
            [('id', '=', student_id)])
        sub_id = []
        attachemnts_ids = []
        for course in student.course_detail_ids:
            for record in course.subject_ids:
                sub_id.append(record.id)
                for j in record.attachment_ids:
                    attachemnts_ids.append(j.id)
        domain = [('id', 'in', sub_id)]
        domain += [('attachment_ids', 'in', attachemnts_ids)]
        material_count = request.env['op.subject'].sudo().search_count(domain)
        val['material_count'] = material_count
        return val

    def get_search_domain_study_material(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', ('course_id', 'ilike', search),
                    ('name', 'ilike', srch),
                ]
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

    @http.route(['/subject/details/',
                 '/subject/details/<int:student_id>/',
                 '/subject/details/page/<int:page>',
                 '/subject/details/<int:student_id>/page/<int:page>'],
                type='http', auth='user', website=True)
    def portal_student_subject_detail(
            self, student_id=None, date_begin=None, date_end=None, page=0,
            search='', ppg=False, sortby=None, filterby=None,
            search_in='name', groupby='course_id', **post):
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
            'name': {'label': _('Subject'), 'order': 'name'},
            'course_id': {'label': _('Course'),
                          'order': 'course_id'},
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
            'name': {'input': 'name',
                     'label': _('Search in Subject')},
            'course_id': {'input': 'course_id',
                          'label': _('Search in Course')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        if not filterby:
            filterby = 'all'

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'course_id': {'input': 'course_id', 'label': _('Course')},
        }

        domain = searchbar_filters[filterby]['domain']

        domain += self.get_search_domain_study_material(search, attrib_values)

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        if student_id:
            student = request.env['op.student'].sudo().search(
                [('id', '=', student_id)])
            sub_id = []
            attach_id = []
            for course in student.course_detail_ids:
                for record in course.subject_ids:
                    sub_id.append(record.id)
                    for attach in record.attachment_ids:
                        attach_id.append(attach.id)
            domain += [('id', 'in', sub_id), ('attachment_ids', 'in', attach_id)]

            keep = QueryURL('/subject/details/%s' % student_id,
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            total = request.env["op.subject"].sudo().search_count(domain)

            pager = portal_pager(
                url="/subject/details/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )
            if search and search_in:
                search_domain = []
                if search_in in ('all', 'name'):
                    search_domain = expression.OR(
                        [search_domain, [('name', 'ilike', search)]])
                if search_in in ('all', 'course_id'):
                    search_domain = expression.OR(
                        [search_domain, [('course_id', 'ilike', search)]])
                    domain += search_domain
            for course in student.course_detail_ids:
                for record in course.subject_ids:
                    sub_id.append(record.id)

            if groupby == 'course_id':
                order = "course_id, %s" % order

            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')

            subject_id = request.env[
                'op.subject'].sudo().search(domain, order=order,
                                            limit=ppg, offset=pager['offset'])

            if groupby == 'course_id':
                grouped_tasks = [
                    request.env['op.subject'].sudo().concat(*g)
                    for k, g in groupbyelem(
                        subject_id, itemgetter('course_id'))]
            else:
                grouped_tasks = [subject_id]

            val.update({
                'date': date_begin,
                'subject_id': subject_id,
                'page_name': 'subject_detail',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'stud_id': student_id,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/subject/details/%s' % student_id,
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
                "openeducat_subject_material_allocation.portal_student_subject_details",
                val)
        else:
            user = request.env.user
            student = request.env['op.student'].sudo().search(
                [('user_id', '=', user.id)])
            sub_id = []
            attach_id = []
            for course in student.course_detail_ids:
                for record in course.subject_ids:
                    sub_id.append(record.id)
                    for attach in record.attachment_ids:
                        attach_id.append(attach.id)

            domain += [('id', 'in', sub_id), ('attachment_ids', 'in', attach_id)]

            keep = QueryURL('/subject/details/',
                            search=search, attrib=attrib_list,
                            order=post.get('order'))

            total = request.env['op.subject'].sudo().search_count(
                domain)

            pager = portal_pager(
                url="/subject/details/",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )
            if search and search_in:
                search_domain = []
                if search_in in ('all', 'name'):
                    search_domain = expression.OR(
                        [search_domain, [('name', 'ilike', search)]])
                if search_in in ('all', 'course_id'):
                    search_domain = expression.OR(
                        [search_domain, [('course_id', 'ilike', search)]])
                    domain += search_domain
            for course in student.course_detail_ids:
                for record in course.subject_ids:
                    sub_id.append(record.id)

            if groupby == 'course_id':
                order = "course_id, %s" % order

            subject_id = request.env[
                'op.subject'].sudo().search(domain, order=order,
                                            limit=ppg, offset=pager['offset'])

            if groupby == 'course_id':
                grouped_tasks = [
                    request.env['op.subject'].sudo().concat(*g)
                    for k, g in groupbyelem(
                        subject_id, itemgetter('course_id'))]
            else:
                grouped_tasks = [subject_id]

            values.update({
                'date': date_begin,
                'subject_id': subject_id,
                'page_name': 'subject_detail',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/subject/details/',
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
                "openeducat_subject_material_allocation.portal_student_subject_details",
                values)

    @http.route(['/subject/material/detail/<int:subject_id>',
                 '/subject/material/detail/<int:student_id>/<int:subject_id>'],
                type='http', auth='user', website=True)
    def portal_student_subject_material_detail(
            self, student_id=None, subject_id=None):

        subject = request.env[
            'op.subject'].sudo().search(
            [('id', '=', subject_id)])

        return request.render(
            "openeducat_subject_material_allocation."
            "portal_student_subject_material_details",
            {'subject': subject,
             'page_name': 'subject_material_detail',
             'student': student_id,
             })

    @http.route(['/study/material/download/<int:attachment_id>'],
                type='http', auth='user', website=True)
    def download_study_material(self, attachment_id):
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "res_model", "res_id", "type", "url"])
        if attachment:
            attachment = attachment[0]
        res_id = attachment['res_id']
        subject_id = request.env['op.subject'].sudo().search(
            [('id', '=', res_id)])

        if subject_id:
            if attachment["type"] == "url":
                if attachment["url"]:
                    return http.redirect_with_hash(attachment["url"])
                else:
                    return request.not_found()
            elif attachment["datas"]:
                data = io.BytesIO(base64.standard_b64decode(
                    attachment["datas"]))
                return http.send_file(
                    data, filename=attachment['name'], as_attachment=True)
            else:
                return request.not_found()
