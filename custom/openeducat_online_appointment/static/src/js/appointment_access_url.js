odoo.define('website-appointment.access_url', function (require) {
"use strict";


var AbstractField = require('web.AbstractField');
var core = require('web.core');
var fieldRegistry = require('web.field_registry');
var QWeb = core.qweb;

var AppointmentAccessUrl = AbstractField.extend({
    events: _.extend({}, AbstractField.prototype.events,{
        'click .form_access_url': function(e){
            e.stopPropagation();
        },
    }),
    supportedFieldTypes: [],
    start: function () {
         this._super.apply(this, arguments);
         var base_url = this.getSession()['web.base.url'];
         var state = $.bbq.getState();
         var context = this.record.getContext({ fieldName : "id" });
         this.appointment_url = false;
         var appointment_id = false;
         var emp_id = this.record.data.id;
         if(context.parent_id){
            var appointment_id = context.parent_id;
         }
         if(appointment_id){
            this.appointment_url = base_url + '/booking?employee_id=' + emp_id + '?appointment_id=' + appointment_id;
         }
    },

    _render: function(){
        if(!this.appointment_url){ return; }
         var $app_url = "<a class='btn btn-primary form_access_url' href=" + this.appointment_url + ">Book</a>";
         this.$el.empty().removeClass('o_field_empty');
         this.$el.append($app_url);
    },
});

fieldRegistry.add('access_url', AppointmentAccessUrl);

});
