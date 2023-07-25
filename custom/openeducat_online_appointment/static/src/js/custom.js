odoo.define('openeducat_online_appointment.custom', function (require) {
'use strict';

    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var websiteRootData = require('website.root');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;
//    var registry = require('web.field_registry');
    var publicWidget = require('web.public.widget');

    var AppointmentWidget = publicWidget.Widget.extend({
        selector: '.js_oe_appointment_booking',
        events: {
                'click .js-radio-services': '_onClickServices',
                'click .js-radio-staff': '_onClickSelectStaff',
                'click .appointment_booking': '_onClickAppointment',
                'click .service-submit': '_onClickSubmitService',
                'click .staff-submit': '_onClickSubmitStaff',
                'click .day': '_onClickCellContent',
                'click .btn_staff': '_onClickBtnStaff',
                'click .btn_book': '_onClickBtnBooking',
                'click .btn_time': '_onClickBtnTime',
                'click .js-random-radio-slot': '_onClickRandomSlot',
                'click .js-radio-slot': '_onClickSlot',
                'click .js-radio-slot': '_onClickTimeContinue',
                'click .js-random-radio-slot ':'_onClickTimeContinue',
                'click .appointment_name_bread': '_onAppointmentBreadcrumb',
                'click .date_name_bread':'_onDateBreadcrumb',
                'click .date_random_bread':'_onDateRandomBread',

        },
        xmlDependencies: ['/openeducat_online_appointment/static/src/xml/custom.xml'],
        init: function () {
            this._super.apply(this, arguments);
            core.bus.trigger('clear_cache');
        },

        async start(editable_mode) {
            if (editable_mode) {
                this.stop();
                return;
            }
            this.breadscrumb = {};
            var url = window.location;
            var str = url.search;
            var eq_ind = str.indexOf('=') + 1;
            var que_ind = str.indexOf('?', eq_ind);
            var eq_ind2 = str.indexOf('=', que_ind) + 1;
            var que_ind2 = str.indexOf('?', eq_ind2);
            var appointment_id = str.substring(eq_ind2);
            var emp_id = str.substring(eq_ind, que_ind);
            this.appointment_url_id = appointment_id
            this.emp_url_id = emp_id
            this.url = false
            this.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            if (appointment_id && emp_id){
                this.url = true
                await this._onClickSelectStaff();
            }
            var offset = new Date().getTimezoneOffset();
            $('.js_oe_appointment_booking').removeClass('d-none');
        },

        _onAppointmentBreadcrumb: function(e){
            e.preventDefault();
            if(this.url == true){
                $('#list li:eq(1)').remove();
            }
            $('.staff-select').remove();
            $('.time-select').remove();
            $('#list li:eq(0)').after('<li class="breadcrumb-item text-muted time-select"><a class="time_bread">Time</a></li>');
            $('.js-appointment-booking').removeClass('col-md-6');
            $('.js-appointment-booking').addClass('col-md-12');
            $('.confirm-app').removeClass('text-primary');
            $('.confirm-app').addClass('text-muted');
            $('.date-time-step-times').addClass('d-none');
            this._onClickSubmitService();
        },

        _onDateBreadcrumb: function(e){
            e.preventDefault();
            if(this.url == true){
                $('.appointment-select').find('a').remove();
                $('.time-select').remove();
                $('#list li:eq(1)').remove();
                $('#list li:eq(0)').after('<li class="breadcrumb-item text-muted time-select"><a class="time_bread">Time</a></li>');
                $('.staff-select').find('a').remove();
                this._onClickSelectStaff();
            }
            else{
            $('.time-select').remove();
            $('#list li:eq(1)').after('<li class="breadcrumb-item text-muted time-select"><a class="time_bread">Time</a></li>');
            $('.staff-select').find('a').remove();
            this._onClickSelectStaff();
            }
        },

        _onDateRandomBread: function(e){
            e.preventDefault();
            $('.time-select').remove();
            $('.confirm-app').remove();
            $('#list li:eq(0)').after('<li class="breadcrumb-item text-muted time-select"><a class="time_bread">Time</a></li>');
            $('#list li:eq(1)').after('<li class="text-muted breadcrumb-item confirm-app">Confirmation</li>');
            this._onClickSelectStaff();
        },

        _onClickAppointment: function(e){
            $(e.currentTarget).find('.js-radio-services').prop( "checked", true );
            this._onClickSubmitService();
        },
        _onClickServices: function(ev){
            $('.js-form-service-submit').removeClass('o_hidden');
        },

        _onClickBtnBooking: function(ev)
        {

             var service_type = $('.btn_book').data('appointment-id')

              ajax.jsonRpc('/get/booking', 'call',{
                'service_id': service_type,
                }).then(function (data) {

                var services = qweb.render('Booking',
                    {
                       'appointment_ids': data,
                    });
                $('.js-appointment-booking').html(services);
                $('.js-form-service-submit').removeClass('o_hidden');
                $( "input[value=" + service_type + "]").prop( "checked", true );
            });
        },

        _onClickBtnStaff: function(ev)
        {
            $('.step_staff').addClass('available')

            var staff_id = $('.btn_staff').data('staff-id')
            var is_staff = $('.btn_time').data('is-staff')
            var appointment_id = $('.btn_book').data('appointment-id')
             ajax.jsonRpc('/book/staff', 'call',
                {
                    'service_id': appointment_id,
                }).then(function (data) {
                if (data['time_slot'] == '0')
                {
                    $('.btn_book').data('appointment-id',data['appointment_id']);
                    if (data['staff_count'] == '0')
                    {
                        var staff = qweb.render('SelectStaff',
                        {
                           'staff_list': data['staff_list'],
                           'staff_count': data['staff_count'],
                           'appointment_id': data['appointment_id'],
                        });
                        $('.js-appointment-booking').html(staff);
                        $('.js-form-staff-submit').removeClass('o_hidden');
                        $( "input[value=" + staff_id + "]").prop( "checked", true );
                    }
                    else
                    {
                        $('.step_time').addClass('text-muted')
                        $('.btn_time').attr("disabled", 'disabled');
                    }
                }
                else {
                     $('.step_staff').addClass('o_hidden')
                     var appointment_id = $('.btn_book').data('appointment-id')
                      ajax.jsonRpc('/get/booking', 'call',{
                        'service_id': appointment_id,
                    }).then(function (data) {
                        var services = qweb.render('Booking',
                            {
                               'appointment_ids': data,
                            });
                        $('.js-appointment-booking').html(services);
                        $('.js-form-service-submit').removeClass('o_hidden');
                        $( "input[value=" + appointment_id + "]").prop( "checked", true );
                    });
                }
            });
        },



        _onClickSubmitService: function()
        {
            var self = this;
            if($("#cancel").length > 0){
                $("#cancel").remove();
            }
            var service_type = $("input[name='service']:checked").val() || this.breadscrumb['appointment_id'];
            var $selected_appointment = $("input[name='service']:checked").data();
            this.breadscrumb['appointment_name']= $selected_appointment ? $selected_appointment.name : this.breadscrumb['appointment_name'];
            $('#li1').remove();
            $('.btn_book').attr('data-appointment-id',service_type);
            $('.js-form-service-submit').addClass('o_hidden');
            var self = this
            ajax.jsonRpc('/book/staff', 'call',
            {
                'service_id': service_type,
            }).then(function (data) {
                $('.btn_book').data('appointment-id',data['appointment_id']);
                var slot_date_list , start_date ;
                var params = {
                'appointment_id': data['appointment_id'],
                'timezone': self.timezone,
                }
                ajax.jsonRpc('/get/slots', 'call',
                {
                     params
                }).then(function (slotdata) {
                    slot_date_list = slotdata['slot_date_list'];
                    start_date = slotdata['start_date'];
                    if (data['time_slot'] == 1){
                         $('.time-select').addClass('text-primary');
                         $('.btn_time').attr('data-appointment-id',service_type);
                         $('.btn_time').attr('data-is-staff',0);
                         $('.step_time').addClass('available');
                         $('.btn_time').removeAttr("disabled");
                         $('.step_staff').addClass('o_hidden');
                         $('.date-time-step-body').addClass('row');
                         $('.js-appointment-booking').removeClass('col-md-12');
                         $('.js-appointment-booking').addClass('col-md-6');
                    var date = qweb.render('SelectDate',
                        {
                            'staff_id': '',
                            'appointment_id': service_type,
                            'slot_date_list':slot_date_list,
                            'start_date':start_date,
                            'end_date':slotdata['end_date'],
                            'summary':slotdata['summary'],
                            });

                    $('.js-appointment-booking').html(date);
                    $('.appointment-bread').remove();
                    $('.appointment-select').append('<a class="appointment-bread" href="/booking">'+data['appointment_name']+'</a>');
                    $('.appointment-bread').addClass('text-success');
                    $('.time_bread').removeClass('text-muted');
                    $('.time_bread').addClass('text-primary');

                     var time_continue = qweb.render('TimeBack',
                        {
                            'staff_id': '',
                            'appointment_id': service_type,
                        });
                     $('.js-bk-continue').html(time_continue);
                }
                else
                {

                    $('.step_staff').addClass('available');
                    $('.step_staff').removeClass('o_hidden');
                    $('.btn_staff').removeAttr("disabled");
                    $('.btn_time').attr('data-is-staff',1);
                    $('.btn_time').attr('data-appointment-id',service_type);
                    $('.js-appointment-booking').addClass('row');

                    var staff = qweb.render('SelectStaff',
                    {
                       'staff_list': data['staff_list'],
                       'staff_count': data['staff_count'],
                       'appointment_id': data['appointment_id'],
                       'appointment_name': data['appointment_name'],
                    });
                    if(self.url == false){
                    $('#list li:eq(0)').after('<li class="breadcrumb-item text-primary staff-select" id="li_staff"><a class="staff_bread" >Staff</a></li>');
                    }
                    else{
                    $('#list li:eq(0)').after('<li class="breadcrumb-item url_staff text-primary staff-select" id="li_staff"><a class="staff_bread" >Staff</a></li>');
                    }
                    var seen = {};
                    $('.staff-select').each(function() {
                      var txt = $(this).text();
                      if (seen[txt])
                          $(this).remove();
                      else
                          seen[txt] = true;
                    });
                   $('.js-appointment-booking').html(staff);
                   $('.appointment-bread').remove();
                    $('.appointment-select').append('<a class="appointment-bread" href="/booking">'+data['appointment_name']+'</a>');
                    $('.appointment-bread').addClass('text-success');

                    var continue_data = qweb.render('ContinueStaff',
                        {
                            'appointment_id': data['appointment_id'],
                        });
                    $('.js-bk-continue').html(continue_data);
                   }
                });
            });
        },


        async _onClickSelectStaff()
        {
            $('.date-time-step-body').addClass('row');
            $('.js-appointment-booking').removeClass('col-md-12');
            $('.js-appointment-booking').addClass('col-md-6');
            $('.staff-select').removeClass('text-primary');
            $('.staff-select').addClass('text-success');
            $('.time_bread').addClass('text-primary');
            $('.confirm-app').addClass('text-muted');
            $('.js-get-time-slots').removeClass('o_hidden');
            $('.js-get-time-slots').removeClass('d-none');
            $('.js-select-date').removeClass('o_hidden');
            $('.js-select-date').removeClass('d-none');

            var $staff_name =  this.breadscrumb['staff_name'];;
            this.breadscrumb['staff_name']= $staff_name;
            var selected_appointment_name = $("input[name='appointment_name']").val();
            var staff_type = $("input[name='staff']:checked").val() || $("input[name='staff_id']").val() || this.emp_url_id
            var staff_id = $("input[name='staff_id']").val() || this.emp_url_id
            var appointment_id = $("input[name='appointment_id']").val() || this.appointment_url_id
            $('.js-form-staff-submit').removeClass('o_hidden');
            $('.btn_time').attr('data-staff-id',staff_type);
            $('.btn_time').attr('data-appointment-id',appointment_id);
            this.breadscrumb['appointment_id']= appointment_id;
            $('.js-form-staff-back').addClass('o_hidden')
            $('.js-form-staff-submit').addClass('o_hidden')
            $('.step_time').addClass('available')
            $('.btn_time').removeAttr("disabled");
            $('.btn_staff').attr('data-staff-id',staff_type);
            $('.btn_staff').attr('data-appointment-id',appointment_id);
            $('.js-appointment-booking').empty();
            var params = {
                'appointment_id': appointment_id,
                'staff_id': staff_type,
                'timezone': this.timezone,
            }
            var self = this;
            ajax.jsonRpc('/get/slots', 'call',
            {
                 params
            }).then(function (data) {
                var date = qweb.render('SelectDate',
                    {
                        'staff_id': staff_type,
                        'appointment_id': appointment_id,
                        'start_date':data['start_date'],
                        'end_date':data['end_date'],
                        'slot_date_list':data['slot_date_list'],
                        'summary':data['summary'],
                    });
                if(self.url == true){
                    $('.appointment-bread').remove('a');
                    $('.appointment-select').append('<a class="appointment-bread" href="/booking">'+data['summary']+'</a>');
                    $('.appointment-select').addClass('text-success');
                    if(data['assign_method'] == 'customer'){
                        $('.url_staff').remove();
                        $('#list li:eq(0)').after('<li class="breadcrumb-item text-success staff-select" id="li_staff"><a class="appointment_name_bread" href="#" style="cursor: pointer;">'+data['staff_name']+'</a></li>');
                    }
                    else{
                        $('#list li:eq(0)').after('<li class="breadcrumb-item text-success staff-select" id="li_staff"><a>'+data['staff_name']+'</a></li>');
                    }
                }
                else{
                    $('.staff-select').append('<a class="appointment_name_bread" href="#" style="cursor: pointer;">'+data['staff_name']+'</a>');

                }
                $('.js-appointment-booking').html(date);
                $('.staff_bread').remove();
                $('.date-time-step-times').removeClass('d-none');
                $('.time_bread').removeClass('text-muted');
                $('.time_bread').addClass('text-primary');
                var time_continue = qweb.render('TimeBack',
                    {
                        'staff_id': staff_type,
                        'appointment_id': appointment_id,
                    });
                $('.js-bk-continue').html(time_continue);
                return true;
            });
        },

        _onClickSubmitStaff: function(ev)
        {
            var staff_type = $("input[name='staff']:checked").val() || this.emp_url_id
            var appointment_id = $("input[name='appointment_id']").val() || this.appointment_url_id
            $('.btn_time').attr('data-staff-id',staff_type);
            $('.btn_time').attr('data-appointment-id',appointment_id);
            $('.js-form-staff-back').addClass('o_hidden')
            $('.js-form-staff-submit').addClass('o_hidden')
            $('.step_time').addClass('available')
            $('.btn_time').removeAttr("disabled");
            $('.btn_staff').attr('data-staff-id',staff_type);
            $('.btn_staff').attr('data-appointment-id',appointment_id);
            var select_date = $("input[name='start_date']").val();
            var date = qweb.render('SelectDate',
                {
                    'staff_id': staff_type,
                    'appointment_id': appointment_id,
                    'select_date':select_date,
                });
            $('.js-appointment-booking').html(date);
            $('.js-select-date').removeClass('d-none');

            var time_continue = qweb.render('TimeBack',
                {
                    'staff_id': staff_type,
                    'appointment_id': appointment_id,
                });
            $('.js-bk-continue').html(time_continue);

        },

        _onClickBtnTime: function(ev){

            var appointment_id = $('.btn_book').data('appointment-id')
            var staff = $('.btn_book').data('staff-id')
            var date = qweb.render('SelectDate',
                {
                    'staff_id': staff,
                    'appointment_id': appointment_id,
                });
            $('.js-appointment-booking').html(date);
        },

        _onClickCellContent: function(ev)
        {
            $('.day').removeClass('today')
            $(ev.currentTarget).addClass('today')
            var s_date = $(ev.currentTarget).data('date')
           var sel_date = $(ev.currentTarget).data('date');
           sel_date = new Date(sel_date);
           var date = sel_date.getDate();
           var month = sel_date.getMonth() + 1;
           var year = sel_date.getFullYear();
           var week = sel_date.getDay();
           var staff_id = $("input[name='staff_id']").val() || this.emp_url_id
           var appointment_id = $("input[name='appointment_id']").val() || this.appointment_url_id
           var start_date = $("input[name='start_date']").val();
           var end_date = $("input[name='end_date']").val();
           var date_select = sel_date.toLocaleString('en-us', { weekday: 'long', month:'long', day:'2-digit' });
           $('.js-select-date').html(date_select);
           var params = {
                'month': month,
                'year': year,
                'date': date,
                'week': week,
                'staff_id': staff_id,
                'appointment_id': appointment_id,
                'end_date':end_date,
                'start_date':start_date,
                'timezone': this.timezone
           }
            ajax.jsonRpc('/check/availability', 'call',
            {
                 params
            }).then(function (data) {
                $('.js-appointment-booking').attr('data-date',data['date'])
                if (staff_id)
                {
                    var staff = qweb.render('TimeSlots',
                    {
                        'slots': data['slot'],
                        'date': data['date'],
                        'appointment_id': appointment_id,
                        'staff_id': staff_id,
                        'date_select':date_select,
                    });
                    $('.js-get-time-slots').html(staff);
                }
                else
                {
                    var staff = qweb.render('RandomTimeSlots',
                    {
                        'slots': data['slot'],
                        'date': data['date'],
                        'appointment_id': appointment_id,
                        'staff_id': staff_id,
                        'date_select':date_select,
                    });
                    $('.js-get-time-slots').html(staff);
                }

                $('.js-get-emp').addClass('o_hidden')
            });
        },

        _onClickSlot: function(ev)
        {
             $('.time-continue').removeClass('o_hidden')

        },

        _onClickRandomSlot: function(ev)
        {
            $('.time-select').removeClass('text-primary');
            $('.time-select').addClass('text-success');
            $('.confirm-app').removeClass('text-muted ');
            $('.confirm-app').addClass('text-primary ');

            var data_date = $
            var appointment_id = $('.btn_book').data('appointment-id')
            var time = $("input[name='time']:checked").val();
            var date_select = $("input[name='date_select']").val();
            var month = $('.last').attr('get-month-id');
            var year = $('.last').attr('get-year-id');
            var date = $('.js-random-radio-slot').attr('data-date');
            var week = $('.last').attr('week-id');
            var params = {
                'month': month,
                'year': year,
                'date': date,
                'week': week,
                'time': time,
                'appointment_id': appointment_id,
                'timezone': this.timezone
           }
             ajax.jsonRpc('/check/employee', 'call',
            {
                 params
            }).then(function (data) {
                if (data['msg'])
                {
                    alert(data['msg']);
                }
                else
                {  if (data['emp_name'])
                    {
                        var staff = qweb.render('RandomEmployee',
                        {
                            'emp_data': data['emp_name'] + ' is available',
                        });
                    }
                    else
                    {
                        var staff = qweb.render('RandomEmployee',
                        {
                            'emp_data': '',
                        });
                    }
                    var staff = qweb.render('RandomEmployee',
                    {
                        'emp_data': data['emp_name'] + ' is available',
                    });
                    $('.js-get-emp').removeClass('o_hidden')
                    $('.js-get-emp').html(staff);
                    $('.time-continue').removeClass('o_hidden');
                    $('.btn_time').attr('data-emp-id',data['emp_id']);
                }
            });
        },

        _onClickTimeContinue: function(ev){
            var self = this;
            $('.time-select').removeClass('text-muted');
            $('.time-select').removeClass('text-primary');
            $('.time-select').addClass('text-success');
            $('.confirm-app').removeClass('text-muted');
            $('.confirm-app').addClass('text-primary');
            var time = $("input[name='time']:checked").val();
            var appointment_id = $('.btn_book').data('appointment-id') || this.appointment_url_id
            var a_name = $('.btn_book').data('appointment-name')
            var emp_id = $('.btn_time').data('emp-id')
            var staff_id = $("input[name='staff_id']").val();
            var month = $('.last').attr('get-month-id');
            var year = $(ev.currentTarget).data('year');
            var week = $('.last').attr('week-id');
            var date = $('.js-appointment-booking').attr('data-date');
            this.breadscrumb['date']= date;
            $('.js-get-time-slots').addClass('o_hidden');
            $('.js-get-time-slots').addClass('d-none');
            $('.js-select-date').addClass('o_hidden');
            $('.js-select-date').addClass('d-none');
            $('.js-appointment-booking').removeClass('col-md-12');
            $('.js-appointment-booking').addClass('col-md-6');
            var params = {
                'appointment_id': appointment_id,
           }
            ajax.jsonRpc('/get/customer/details', 'call',
            {
                params
            }).then(function (data) {
                var staff = qweb.render('CustomerForm',
                {
                    'name': data['name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'partner_id': data['partner_id'],
                    'staff_id': emp_id || staff_id,
                    'appointment_id': appointment_id,
                    'time': time,
                    'month': month,
                    'year': year,
                    'date': date,
                    'week': week,
                    'questions':data['questions'],
                    'timezone':self.timezone
                });
                $('.js-appointment-booking').html(staff);
                $('.js-appointment-booking').removeClass('col-md-6');
                $('.js-form-time-back').addClass('o_hidden');
                $('.time_bread').remove();
                var date_select = $("input[name='date_select']").val();
                if (staff_id.length == 0){
                    $('.time-select').append('<input name="staff_id" class="d-none" value='+staff_id+ ' />'+'<a class="time_bread date_random_bread" href="#" style="cursor: pointer;" data-staff-id='+staff_id+'>'+date+', '+time+'</a>');
                }
                else{
                    $('.time-select').append('<input name="staff_id" class="d-none" value='+staff_id+ ' />'+'<a class="time_bread date_name_bread" href="#" style="cursor: pointer;" data-staff-id='+staff_id+'>'+date+', '+time+'</a>');
                }
             });
        },
    });
//    websiteRootData.websiteRootRegistry.add(AppointmentWidget, '.js_oe_appointment_booking');
        publicWidget.registry.AppointmentWidget = AppointmentWidget;
        return AppointmentWidget;
}); 