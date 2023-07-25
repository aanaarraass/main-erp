# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from werkzeug.utils import redirect
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date
from odoo.osv import expression
from odoo.addons.website.controllers.main import QueryURL

from collections import OrderedDict

PPG = 3


class RequestAssetController(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(RequestAssetController, self). \
            _prepare_home_portal_values(counters)
        user = request.env.user.id
        request_count = request.env['account.asset.request'].sudo().search_count(
            ['|', ('student_id.user_id', '=', user), ('faculty_id.user_id', '=', user)])
        values['asset_request_count'] = request_count
        return values

    def _prepare_portal_layout_values(self):
        values = super(RequestAssetController, self)._prepare_portal_layout_values()
        user = request.env.user.id
        request_count = request.env['account.asset.request'].sudo().search_count(
            ['|', ('student_id.user_id', '=', user), ('faculty_id.user_id', '=', user)])
        values['asset_request_count'] = request_count
        return values

    def _parent_prepare_portal_layout_values(self, student_id=None):
        val = super(RequestAssetController, self)._parent_prepare_portal_layout_values(
            student_id)
        request_count = request.env['account.asset.request'].sudo().search_count(
            [('student_id.id', '=', student_id)])
        val['asset_request_count'] = request_count
        return val

    @http.route(['/my/asset/asset-request',
                 '/my/asset/asset-request/<int:asset_id>'],
                auth='user', website=True, csrf=False)
    def request_asset_form(self, asset_id=None, **post):
        student = request.env['op.student'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        faculty = request.env['op.faculty'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        data = request.env['account.asset.request'].sudo(). \
            search([('id', '=', asset_id)])
        reasons = request.env['asset.request.reason'].sudo().search([])
        values = {
            'student': student,
            'faculty': faculty,
            'reasons': reasons,
            'requests': data,
        }
        if not asset_id:
            if post:
                request.env['account.asset.request'].sudo().create({
                    'request_for': post.get('request_for'),
                    'student_id': student.id,
                    'faculty_id': faculty.id,
                    'request_date': date.today(),
                    'request_reason_id': post.get('request_reason_id'),
                    'requested_asset': post.get('assets')
                })
                return redirect('/my/asset-request')
            return request.render('openeducat_asset_request_enterprise.'
                                  'request_assets_form', values)
        else:
            if post:
                data.write({
                    'request_for': post.get('request_for'),
                    'student_id': student.id,
                    'faculty_id': faculty.id,
                    'request_date': date.today(),
                    'request_reason_id': post.get('request_reason_id'),
                    'requested_asset': post.get('assets')
                })
                return redirect('/my/asset-request')
            return request.render('openeducat_asset_request_enterprise.'
                                  'request_assets_form_edit', values)

    def get_search_domain_asset(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|',
                    ('asset_id', 'ilike', srch),
                    ('requested_asset', 'ilike', srch),
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

    @http.route(['/my/asset-request',
                 '/my/asset-request/<int:student_id>',
                 '/my/asset-request/page/<int:page>',
                 '/my/asset-request/<int:student_id>/page/<int:page>'],
                auth='user', website=True, csrf=False)
    def all_request_assets(self, student_id=None, page=0, sortby=None,
                           filterby=None, groupby=None, search='',
                           search_in='all', ppg=False, **kw):
        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()
        user = request.env.user.id
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            kw["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sorting = {
            'id': {'label': _('Newest'), 'order': 'id desc'},
            'asset_id': {'label': _('Asset Name'), 'order': 'asset_id asc'}
        }

        searchbar_filters = {
            'all': {'label': _('All'),
                    'domain': []},
            'draft': {'label': _('Approve'),
                      'domain': [('state', '=', 'approved')]},
            'allocate': {'label': _('Allocate'),
                         'domain': [('state', '=', 'allocate')]},
            'reject': {'label': _('Reject'),
                       'domain': [('state', '=', 'rejected')]},
            'return': {'label': _('Return'),
                       'domain': [('state', '=', 'returned')]},
        }

        searchbar_inputs = {
            'all': {'input': 'all',
                    'label': _('Search in All')},
            'asset_id': {'input': 'asset_id',
                         'label': _('Search in allocated asset')},
            'requested_asset': {'input': 'requested_asset',
                                'label': _('Search in requested asset')},
        }

        searchbar_groupby = {
            'none': {'input': 'none',
                     'label': _('None')},
            'date': {'input': 'request_date',
                     'label': _('By Date')},
        }

        if not sortby:
            sortby = 'id'
        if not filterby:
            filterby = 'all'

        order = searchbar_sorting[sortby]['order']

        if not groupby:
            groupby = 'none'

        if groupby == 'date':
            order = "request_date, %s" % order

        if student_id:
            domain = [('student_id.id', '=', student_id)]
        else:
            domain = ['|', ('student_id.user_id', '=', user),
                      ('faculty_id.user_id', '=', user)]

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'asset_id'):
                search_domain = expression.OR(
                    [search_domain, [('asset_id', 'ilike', search)]])
            if search_in in ('all', 'requested_asset'):
                search_domain = expression.OR(
                    [search_domain, [('requested_asset', 'ilike', search)]])

            domain += search_domain

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        domain += self.get_search_domain_asset(search, attrib_values)
        domain += searchbar_filters[filterby]['domain']
        requests = request.env['account.asset.request']. \
            sudo().search(domain, order=order)

        if student_id:
            keep = QueryURL('/my/asset-request/%s' % student_id,
                            search=search, attrib=attrib_list,
                            sortby=sortby, filterby=filterby, groupby=groupby,
                            search_in=search_in, order=kw.get('order'))
            asset_count = requests.sudo().search_count(domain)
            pager = portal_pager(
                url="/my/asset-request/%s" % student_id,
                url_args={'sortby': sortby, 'filterby': filterby, 'groupby': groupby,
                          'search_in': search_in,
                          'search': search},
                total=asset_count,
                page=page,
                step=ppg
            )
            offset = pager['offset']
            requests = requests[offset: offset + 3]
        else:
            keep = QueryURL('/my/asset-request',
                            search=search, attrib=attrib_list, sortby=sortby,
                            filterby=filterby, groupby=groupby,
                            search_in=search_in, order=kw.get('order'))
            asset_count = requests.sudo().search_count(domain)
            pager = portal_pager(
                url="/my/asset-request",
                url_args={'sortby': sortby, 'filterby': filterby,
                          'groupby': groupby, 'search_in': search_in,
                          'search': search},
                total=asset_count,
                page=page,
                step=ppg
            )
            offset = pager['offset']
            requests = requests[offset: offset + 3]

        if student_id:
            val.update({
                'user': request.env.user,
                'page_name': 'request_asset',
                'default_url': '/my/asset-request/%s' % student_id,
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'requests': requests,
                'searchbar_sorting': searchbar_sorting,
                'search_in': search_in,
                'search': search,
                'sortby': sortby,
                'groupby': groupby,
                'searchbar_inputs': searchbar_inputs,
                'searchbar_groupby': searchbar_groupby,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'st_id': student_id
            })
            return request.render('openeducat_asset_request_enterprise.'
                                  'all_asset_request', val)

        else:
            values.update({
                'user': request.env.user,
                'page_name': 'request_asset',
                'default_url': '/my/asset-request',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'requests': requests,
                'searchbar_sorting': searchbar_sorting,
                'search_in': search_in,
                'search': search,
                'sortby': sortby,
                'groupby': groupby,
                'searchbar_inputs': searchbar_inputs,
                'searchbar_groupby': searchbar_groupby,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
            })
            return request.render('openeducat_asset_request_enterprise.'
                                  'all_asset_request', values)

    @http.route(['/my/asset/asset-detail/<int:asset_request_id>'],
                auth='user', website=True, csrf=False)
    def approve_asset_detail(self, asset_request_id=None):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        domain = [('id', '=', asset_request_id)]
        assign = request.env['account.asset.request'].sudo().search(domain)
        values.update({
            'page_name': 'my_asset',
            'assets': assign,
            'user_id': user
        })
        return request.render('openeducat_asset_request_enterprise.'
                              'asset_detail', values)

    @http.route('/my/asset/delete-request/<int:asset_id>',
                auth='user', website=True, csrf=False)
    def delete_request(self, asset_id=None):
        requests = request.env['account.asset.request'].sudo().browse(asset_id)
        requests.unlink()
        return redirect('/my/asset-request')
