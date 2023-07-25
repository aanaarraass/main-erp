# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo import http
from odoo.http import request


class SecureQRCode(http.Controller):

    @http.route(['/verify'], type='http', auth="public", website=True, csrf=False)
    def scanner(self, **kwargs):
        return request.render('openeducat_secure.qr_code_scanner')

    @http.route('/verify/binary', type="json", auth="public", website=True, csrf=False)
    def binary_data(self, **post):
        if post:
            secure_qr_code = request.env['ir.config_parameter'].sudo(). \
                get_param('secure_qr_code')
            data = request.env['ir.attachment'].sudo(). \
                search([('res_field', '!=', False)])
            if data:
                for m in data:
                    model = request.env[m.res_model].sudo() \
                        .search([('id', '=', m.res_id)])
                    qr_binary = post.get('binary')
                    res = ''.join(format(ord(i), '08b') for i in m.res_field)
                    if res == qr_binary:
                        fields = []
                        multiple_records = []
                        for name, field in model._fields.items():
                            if getattr(field, 'secure', None):
                                if field.type in ['one2many', 'many2one', 'many2many']:
                                    multiple_records.append(name)
                                else:
                                    fields.append(name)
                        for thread in model:
                            field_value = {}
                            singular_fields = {}
                            multiple_fields = {}
                            for field in fields:
                                field_value[field] = thread[field]
                                singular_fields[field] = thread[field]
                            for obj in multiple_records:
                                sorted_obj = {}
                                obj_records = {}
                                for rec in thread[obj]:
                                    multiple_rec = {}
                                    for f_name, f_type in rec._fields.items():
                                        if getattr(f_type, 'secure', None):
                                            if f_type.type in ['one2many', 'many2one',
                                                               'many2many']:
                                                for sub_fname, sub_ftype in \
                                                        rec[f_name]._fields.items():
                                                    if getattr(sub_ftype,
                                                               'secure', None):
                                                        key = str(rec.id)
                                                        multiple_rec[f_name] = \
                                                            rec[f_name][sub_fname]
                                                        obj_records[key] = multiple_rec
                                                        sorted_obj = \
                                                            sorted(obj_records.items(),
                                                                   key=lambda k_v: k_v
                                                                   [0])
                                            else:
                                                key = str(rec.id)
                                                multiple_rec[f_name] = rec[f_name]
                                                obj_records[key] = multiple_rec
                                                sorted_obj = \
                                                    sorted(obj_records.items(),
                                                           key=lambda k_v: k_v[1]
                                                           [f_name])

                                obj_string = \
                                    request.env[m.res_model]._fields[obj].string
                                multiple_fields[obj_string] = sorted_obj
                                field_value[obj_string] = sorted_obj
                        model_name = m.res_model.replace(".", "_")
                        key = "qr_hash_template" + "_" + model_name
                        view = request.env['ir.ui.view'].sudo(). \
                            search([('key', 'ilike', key), ('type', '=', 'qweb')])
                        v_model = 'ir.ui.view'
                        return request.env[v_model].sudo()._render_template(
                            view.id, {'single': singular_fields,
                                      'multiple': multiple_fields,
                                      'type': secure_qr_code, })

        return request.env['ir.ui.view'].sudo(). \
            _render_template('openeducat_secure.error_page', {'type': secure_qr_code})

    @http.route('/verify/<string:hash_key>', auth="public", website=True)
    def general_data(self, hash_key=None, **kwargs):

        data = request.env['ir.attachment'].sudo(). \
            search([('res_field', '=', hash_key)])
        secure_qr_code = request.env['ir.config_parameter']. \
            sudo().get_param('secure_qr_code')
        if data:
            model = request.env[data.res_model].sudo(). \
                search([('id', '=', data.res_id)])
            if model:
                fields = []
                multiple_records = []
                for name, field in model._fields.items():
                    if getattr(field, 'secure', None):
                        if field.type in ['one2many', 'many2one', 'many2many']:
                            multiple_records.append(name)
                        else:
                            fields.append(name)
                singular_fields = {}
                multiple_fields = {}
                for field in fields:
                    singular_fields[field] = model[field]
                for obj in multiple_records:
                    sorted_obj = {}
                    obj_records = {}
                    for rec in model[obj]:
                        multiple_rec = {}
                        for f_name, f_type in rec._fields.items():
                            if getattr(f_type, 'secure', None):
                                if f_type.type in ['one2many', 'many2one', 'many2many']:
                                    for sub_fname, sub_ftype in \
                                            rec[f_name]._fields.items():
                                        if getattr(sub_ftype, 'secure', None):
                                            key = str(rec.id)
                                            multiple_rec[f_name] = \
                                                rec[f_name][sub_fname]
                                            obj_records[key] = multiple_rec
                                            sorted_obj = \
                                                sorted(obj_records.items(),
                                                       key=lambda k_v: k_v[0])
                                else:
                                    key = str(rec.id)
                                    multiple_rec[f_name] = rec[f_name]
                                    obj_records[key] = multiple_rec
                                    sorted_obj = \
                                        sorted(obj_records.items(),
                                               key=lambda k_v: k_v[1][f_name])

                        obj_string = request.env[
                            data.res_model].sudo()._fields[obj].string
                        multiple_fields[obj_string] = sorted_obj

                model_name = data.res_model.replace(".", "_")
                key = "qr_hash_template" + "_" + model_name
                view = request.env['ir.ui.view'].sudo(). \
                    search([('key', 'ilike', key), ('type', '=', 'qweb')])
                return request.render(view.id, {
                    'single': singular_fields,
                    'multiple': multiple_fields,
                    'type': secure_qr_code,
                })
        return request.render('openeducat_secure.error_page', {'type': secure_qr_code})
