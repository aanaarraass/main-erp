odoo.define('openeducat_student_leave_enterprise.date_validation', function (require) {
    "use strict";
    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    var websiteRootData = require('website.root');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;
    const time = require('web.time');

    var DateValidation = publicWidget.Widget.extend({
        events:{
            'change #date_change': '_onChangeDateValidation',
        },
        selector: '.student_portal_view',

        init: function(){
            this._super.apply(this,arguments);
            $("input[name='start_date']").datepicker();
            $("input[name='end_date']").datepicker();
        },
        start: function(){
            this._super.apply(this,arguments);
        },
        _onChangeDateValidation: function(ev){
            var start_date = $("input[name='start_date']").val();
            var end_date = $("input[name='end_date']").val();
            var student_id = $("input[name='student_id']").val();
            if (end_date < start_date){
                alert('Start Date should be smaller than End Date.');
                end_date = $("input[name='end_date']").val('');
            }
            else{
            ajax.jsonRpc("/check/leave/data",'call',{
                start_date: start_date,
                end_date: end_date,
                student_id: student_id,
                date_format: _t.database.parameters.date_format,
            }).then(function(data){
                if (data > 0){
                    alert('You already have Leave Request available on this Date')
                    start_date = $("input[name='start_date']").val('');
                    end_date = $("input[name='end_date']").val('');
                }
            });
            }
        },
    });

//    websiteRootData.websiteRootRegistry.add(DateValidation, '.js_get_data');
    return DateValidation
});
