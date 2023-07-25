# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import api, fields, models, tools
import hashlib
import json
import qrcode
import base64
from io import BytesIO


class SecureModel(models.AbstractModel):
    _name = 'secure.hash'
    _description = 'Secure Hash'
    hash_key = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        threads = super(SecureModel, self).create(vals_list)
        self.generate_hash_key(threads)
        return threads

    def generate_hash_key(self, record):
        fnames, multiple_records = record._get_secured_fields()
        field_value = {}
        for thread in record:
            for field in fnames:
                field_value[field] = thread[field]
            for obj in multiple_records:
                obj_records = {}
                sorted_obj = {}
                for rec in record[obj]:
                    multiple_rec = {}
                    for f_name, f_type in rec._fields.items():
                        if getattr(f_type, 'secure', None):
                            if f_type.type in ['one2many', 'many2one', 'many2many']:
                                for sub_fname, sub_ftype in rec[f_name]._fields.items():

                                    if getattr(sub_ftype, 'secure', None):
                                        key = str(rec.id)
                                        multiple_rec[f_name] = rec[f_name][sub_fname]
                                        obj_records[key] = multiple_rec
                                        sorted_obj = sorted(obj_records.items(),
                                                            key=lambda k_v: k_v[0])

                            else:
                                key = str(rec.id)
                                multiple_rec[f_name] = rec[f_name]
                                obj_records.update({key: multiple_rec})
                                sorted_obj = sorted(obj_records.items(),
                                                    key=lambda k_v: k_v[1][f_name])

                obj_string = self.env[self._name]._fields[obj].string
                field_value[obj_string] = sorted_obj

        json_data = json.dumps(field_value)
        hash_key = hashlib.md5(json_data.encode())
        record.hash_key = hash_key.hexdigest()
        is_created = self.env['ir.attachment'].search([
            ('res_field', '!=', False),
            ('res_model', '=', record._name), ('res_id', '=', record.id)])
        if is_created:
            is_created.write({'res_field': record.hash_key})
        else:
            self.env['ir.attachment'].create({
                'name': record._name + str(record.id),
                'res_model': record._name,
                'res_field': record.hash_key,
                'res_id': record.id,
                'public': True,
            })

    def write(self, values):
        hash_attachment = self.env['ir.attachment'].search([
            ('res_field', '=', self.hash_key)])
        fnames, multiple_records = self._get_secured_fields()
        field_value = {}
        secure_old_values = []
        secure_new_values = []
        for field in fnames:
            secure_old_values.append(self[field])
        for obj in multiple_records:
            sorted_obj = {}
            obj_records = {}
            for rec in self[obj]:
                multiple_rec = {}
                for f_name, f_type in rec._fields.items():
                    if getattr(f_type, 'secure', None):
                        if f_type.type in ['one2many', 'many2one', 'many2many']:
                            for sub_fname, sub_ftype in rec[f_name]._fields.items():
                                if getattr(sub_ftype, 'secure', None):
                                    key = str(rec.id)
                                    multiple_rec[f_name] = rec[f_name][sub_fname]
                                    obj_records[key] = multiple_rec
                                    sorted_obj = sorted(obj_records.items(),
                                                        key=lambda k_v: k_v[0])

                        else:
                            key = str(rec.id)
                            multiple_rec[f_name] = rec[f_name]
                            obj_records[key] = multiple_rec
                            sorted_obj = sorted(obj_records.items(),
                                                key=lambda k_v: k_v[1][f_name])

            secure_old_values.append(sorted_obj)
        threads = super(SecureModel, self).write(values)
        for field in fnames:
            field_value[field] = self[field]
            secure_new_values.append(self[field])
        for obj in multiple_records:
            sorted_obj = {}
            obj_records = {}
            for rec in self[obj]:
                multiple_rec = {}
                for f_name, f_type in rec._fields.items():
                    if getattr(f_type, 'secure', None):
                        if f_type.type in ['one2many', 'many2one', 'many2many']:
                            for sub_fname, sub_ftype in rec[f_name]._fields.items():
                                if getattr(sub_ftype, 'secure', None):
                                    key = str(rec.id)
                                    multiple_rec[f_name] = rec[f_name][sub_fname]
                                    obj_records[key] = multiple_rec
                                    sorted_obj = sorted(obj_records.items(),
                                                        key=lambda k_v: k_v[0])

                        else:
                            key = str(rec.id)
                            multiple_rec[f_name] = rec[f_name]
                            obj_records[key] = multiple_rec
                            sorted_obj = sorted(obj_records.items(),
                                                key=lambda k_v: k_v[1][f_name])

            secure_new_values.append(sorted_obj)
            obj_string = self.env[self._name]._fields[obj].string
            field_value[obj_string] = sorted_obj

        if secure_old_values != secure_new_values:
            json_data = json.dumps(field_value)
            hash_key = hashlib.md5(json_data.encode())
            self.hash_key = hash_key.hexdigest()
            hash_attachment.write({
                'res_field': self.hash_key,
            })
        return threads

    def type_qr_code(self):
        secure_qr_code = self.env['ir.config_parameter'].sudo().\
            get_param('secure_qr_code')
        return secure_qr_code

    def generate_qrcode(self):

        res = ''.join(format(ord(i), '08b') for i in self.hash_key)

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
        secure_qr_code = self.env['ir.config_parameter'].sudo().\
            get_param('secure_qr_code')

        if secure_qr_code == "open":
            res_param = self.env['ir.config_parameter'].sudo()
            base_url = res_param.search([
                ('key', '=', 'web.base.url')])

            link = base_url.value + "/verify/" + self.hash_key
            qr.add_data(link)
        else:
            qr.add_data(res)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        return qr_image

    def get_web_url(self):
        res_param = self.env['ir.config_parameter'].sudo()
        base_url = res_param.search([
            ('key', '=', 'web.base.url')])
        base_url = base_url.value + "/verify"
        return base_url

    @tools.ormcache('self.env.uid', 'self.env.su')
    def _get_secured_fields(self):
        """ Return the set of secure fields names for the current model. """
        fields = []
        multiple_records = []
        for name, field in self._fields.items():
            if getattr(field, 'secure', None):
                if field.type in ['one2many', 'many2one', 'many2many']:
                    multiple_records.append(name)
                else:
                    fields.append(name)
        return fields, multiple_records
