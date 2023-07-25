odoo.define('openeducat_secure.qr_code_scanner', function (require) {
    "use strict";


    var core = require('web.core');
    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');
    var dom = require('web.dom');
    var session = require('web.session');
    var publicWidget = require('web.public.widget');
    var Widget = require("web.Widget");
    var websiteRootData = require('website.root');
    var _t = core._t;
    var _lt = core._lt;

    var qr_code_scanner = publicWidget.Widget.extend({
        jsLibs: [
            '/openeducat_secure/static/src/js/qrcode-reader.min.js',
        ],
        cssLibs: [
            '/openeducat_secure/static/src/css/qrcode-reader.min.css'
        ],
        xmlDependencies: [
        ],
        init: function (parent, action) {
            this._super.apply(this, arguments);

        },
        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            $.qrCodeReader.jsQRpath = "/openeducat_secure/static/src/js/jsQR.min.js";
            try {
                this.$el.find('#open_qr').qrCodeReader({
                    audioFeedback: false,
                    callback: function (code) {
                        self._verify(code);
                    }
                });
            } catch (err) {
            }
        },

        _verify: function(code){
            var self = this;
            return ajax.jsonRpc('/verify/binary', 'call', {
                'binary': code
            }).then(function (res) {

                
                if (res === "False"){
                    var $template = $(core.qweb.render('error_page',{
                        single: res.single,
                        multiple:res.multiple,
                    }));
                    $('.qr_scanner').after($template);
                    $('.qr_scanner').remove();

                }

                else{
                    self._showdata(res);

                }
            });
               
        },
        _showdata : function(res){

            var $template = res;
            $('.qr_scanner').html($template);
            //$('.qr_scanner').remove();

        }
    });
//    websiteRootData.websiteRootRegistry.add(qr_code_scanner, '.qr_scanner');
   publicWidget.registry.qr_code_scanner = qr_code_scanner
    return qr_code_scanner;


});