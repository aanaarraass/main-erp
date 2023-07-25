odoo.define('openeducat_lms_h5p.upload_material', function (require) {
'use strict';

var core = require('web.core');
var Dialog = require('web.Dialog');
var publicWidget = require('web.public.widget');
var utils = require('web.utils');

var QWeb = core.qweb;
var _t = core._t;
var LmsUpload = require('openeducat_lms_website.upload_material');


    LmsUpload.LmsUploadDialog.include({
        xmlDependencies: (LmsUpload.LmsUploadDialog.prototype.xmlDependencies || [])
        .concat(['/openeducat_lms_h5p/static/src/xml/material_upload.xml']),
        _setup: function () {
            this._super.apply(this, arguments);
            this.slide_type_data.h5p_url = {
                icon: 'fa fa-link',
                label: _t('H5P URL'),
                template: 'openeducat_lms_h5p.upload.modal.h5purl',
            };
            this.slide_type_data.h5p_iframe = {
                icon: 'fa fa-file-o',
                label: _t('H5P Iframe'),
                template: 'openeducat_lms_h5p.upload.modal.h5piframe',
            };
        },
        _formValidateGetValues: function(forcePublished){
            var res = this._super.apply(this, arguments);
            res['document_url'] = this._formGetFieldValue('document_url')
            res['iframe_video_data'] = this._formGetFieldValue('iframe_video_data')
            return res;
        },
        });
});