import base64
import json
import math
import random
from datetime import datetime, time, timedelta

import pytz
from babel.dates import format_datetime
from dateutil.relativedelta import relativedelta
from odoo import http, fields
from odoo.http import request
from odoo.tools import html2plaintext, DEFAULT_SERVER_DATETIME_FORMAT as dtf
from odoo.tools.float_utils import float_round
from pytz import timezone
from werkzeug.urls import url_encode


class WebsiteCalendarAppointment(http.Controller):
    _references_per_page = 12

    @http.route(['/booking'], type='http', auth="public",
                csrf=False, website=True)
    def booking_details(self, **kw):
        values = {}
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        appointment_ids = appointment_rec.search([])
        values.update({
            'appointment_ids': appointment_ids,
            'cancel': '',
        })
        for i in appointment_ids:
            if i.assign_method == "customer" and (len(i.employee_ids) == 1):
                i.assign_method = "random"
        return request.render("openeducat_online_appointment.booking", values)

    @http.route(['/booking/cancel'], type='http',
                auth="public", csrf=False, website=True)
    def cancel_details(self, **kw):
        values = {}
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        appointment_ids = appointment_rec.search([])
        values.update({
            'appointment_ids': appointment_ids,
            'cancel': 'cancel',
        })
        return request.render("openeducat_online_appointment.booking", values)

    @http.route(['/get/booking'], type='json', auth="public",
                csrf=False, website=True)
    def get_booking(self, **kw):
        values = []
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        appointment_ids = appointment_rec.search([])
        for appointment_id in appointment_ids:
            values.append({
                'id': appointment_id.id,
                'name': appointment_id.name,
                'duration': appointment_id.duration,
                'cancel': appointment_id.cancel,
            })

        return values

    @http.route(['/book/staff',
                 ], type='json', auth="public", website=True)
    def get_services(self, service_id):
        staff_list = []
        staff_count = 0
        time_slot = 0
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        appointment_id = appointment_rec.search([('id', '=', service_id)])
        if appointment_id:
            if appointment_id.assign_method == 'random':
                time_slot = 1
            else:
                for staff in appointment_id.employee_ids:
                    staff_list.append({
                        'id': staff.id,
                        'name': staff.name
                    })
        else:
            staff_count = 1

        return {
            'appointment_name': appointment_id.name,
            'staff_list': staff_list,
            'staff_count': staff_count,
            'time_slot': time_slot,
            'appointment_id': appointment_id.id,
        }

    def float_to_time(self, hours):
        if hours == 24.0:
            return time.max
        fractional, integral = math.modf(hours)
        return time(int(integral),
                    int(float_round(60 * fractional, precision_digits=0)), 0)

    @http.route(['/get/slots',
                 ], type='json', auth="public", website=True)
    def get_slots(self, params):
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        event = request.env['calendar.event'].sudo().search([])
        appointment = appointment_rec.browse(int(params.get('appointment_id')))
        slot_date_list = []
        today = datetime.now().date()

        staff_rec = request.env['hr.employee'].sudo()
        staff_name = ''
        if type(params.get('staff_id')) == str \
                and len(params.get('staff_id')) != 0 \
                and (params.get('staff_id')) != '/':
            staff = staff_rec.browse(int(params.get('staff_id')))
            staff_name = staff.name

        if appointment.not_after_type == 'calendar_days':
            max_days = appointment.max_appointment_days
        else:
            start_day = today
            end_day = today + timedelta(days=appointment.max_appointment_days)
            day_generator = (start_day + timedelta(x + 1)
                             for x in range((end_day - start_day).days))
            days = sum(1 for day in day_generator if day.weekday() < 5)
            reminder_day = appointment.max_appointment_days - days
            max_days = appointment.max_appointment_days + reminder_day
        for day in range(max_days + 1):
            current_date = today + timedelta(days=day)
            slott = appointment.sudo()._website_appointment(
                appointment.default_timezone, current_date, '', params.get('timezone'))
            if len(slott) != 0:
                for day in slott:
                    for data in day:
                        day_data = day[data]
                        week_day = current_date.weekday() + 1
                        for slot in appointment.slots:
                            if slot.week == str(week_day):
                                slot_date_list.append(
                                    {'date': str(current_date), "time": day_data})
        end_date = current_date
        res = []
        eventdatetime = []
        for event in event:
            now_tz = event.start
            if params.get('timezone') == appointment.default_timezone:
                now = now_tz.astimezone(pytz.timezone(appointment.default_timezone))
                tz = pytz.timezone(appointment.default_timezone)
                now_tz = now.astimezone(tz)
            eventdatetime.append({'date': now_tz.strftime("%Y-%m-%d"),
                                  "time": now_tz.strftime("%H:%M")})

        today = datetime.now(pytz.timezone(params.get('timezone')))
        now_utc = datetime.now(timezone(params.get('timezone')))
        tz_session = pytz.timezone(params.get('timezone'))

        for i in slot_date_list:
            date_object = datetime.strptime(i['date'] + ' '
                                            + i['time'], '%Y-%m-%d %H:%M')
            slot_date = tz_session.localize(
                fields.Datetime.from_string(date_object))
            if (now_utc <= slot_date) and (i not in res) \
                    and (i not in eventdatetime):
                res.append(i)
        return {
            'staff_name': staff_name,
            'start_date': today,
            'end_date': end_date,
            'slot_date_list': json.dumps(res),
            'summary': appointment.name,
            'assign_method': appointment.assign_method,
        }

    @http.route(['/check/availability',
                 ], type='json', auth="public", website=True)
    def check_availability(self, params):
        if params.get('year') and params.get('month') and params.get('date'):
            get_date = str(params.get('year')) + '-' + str(
                params.get('month')) + '-' + str(
                params.get('date'))
            check_date = datetime.strptime(get_date, '%Y-%m-%d')
            staff_rec = request.env['hr.employee'].sudo()
            appointment_rec = request.env['calendar.online.appointment'].sudo()
            appointment = appointment_rec.browse(int(params.get('appointment_id')))
            event = request.env['calendar.event'].sudo().search([])
            min_hour = appointment.min_appointment_hours
            request.session['timezone'] = appointment.default_timezone
            if appointment and appointment.assign_method == 'customer':
                staff_details = staff_rec.search([('id', '=', params.get('staff_id'))])
                slot = appointment.sudo()._website_appointment(
                    appointment.default_timezone, check_date, staff_details,
                    params.get('timezone'))
            else:
                slot = appointment.sudo()._website_appointment(
                    appointment.default_timezone, check_date, '',
                    params.get('timezone'))

            start_date = params.get('start_date')
            end_date = params.get('end_date') + " 23:59:59"
            start_date = datetime.strptime(
                start_date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=int(min_hour))
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            slots = []
            eventdatetime = []
            for event in event:
                now_tz = event.start
                if params.get('timezone') == appointment.default_timezone:
                    now = now_tz.astimezone(pytz.timezone(appointment.default_timezone))
                    tz = pytz.timezone(appointment.default_timezone)
                    now_tz = now.astimezone(tz)
                eventdatetime.append(now_tz.strftime("%Y-%m-%d %H:%M:%S"))
            for i in slot:
                time = datetime.strptime(i['hours'], '%H:%M').time()
                check_time = check_date + timedelta(
                    hours=int(time.hour), minutes=int(time.minute))
                time_check = check_time.strftime("%Y-%m-%d %H:%M:%S")
                if start_date < check_time and (time_check not in eventdatetime):
                    slots.append(i)
            if (start_date > check_date or end_date < check_date) \
                    and start_date.date() != check_date.date():
                return {'slot': [],
                        'date': check_date.date(),
                        'start_date': start_date,
                        'end_date': end_date,
                        }
            else:
                return {'slot': slots,
                        'date': check_date.date(),
                        'start_date': start_date,
                        'end_date': end_date,
                        }
        else:
            return False

    @http.route(['/check/employee',
                 ], type='json', auth="public", website=True)
    def check_employee(self, params):
        get_date = str(params.get('date'))
        check_date = datetime.strptime(get_date, '%Y-%m-%d')
        week_day = check_date.weekday()
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        events = request.env['calendar.event'].sudo().search([])
        employee = request.env['hr.employee'].sudo().search([])
        appointment = appointment_rec.browse(int(params.get('appointment_id')))
        emp_list = []

        get_date = get_date + ' ' + params.get('time') + ':00'
        tz_session = pytz.timezone(params.get('timezone'))
        date_start = tz_session.localize(fields.Datetime.from_string(get_date))
        tz = pytz.timezone(appointment.default_timezone)
        emp_time = str(date_start.astimezone(tz).time())[:-3]
        get_time = emp_time.split(':')[-2:]
        appt_tz = pytz.timezone(appointment.default_timezone)
        requested_tz = pytz.timezone(appointment.default_timezone)
        start_date = requested_tz.fromutc(
            check_date + relativedelta(hours=int(get_time[0])))
        if appointment:
            local_start = appt_tz.localize(
                datetime.combine(start_date, time(
                    hour=int(get_time[0]),
                    minute=int(round((int(get_time[0]) % 1) * 60))))).astimezone(
                pytz.UTC).replace(tzinfo=None)
            local_end = appt_tz.localize(
                datetime.combine(start_date, time(
                    hour=int(get_time[0]),
                    minute=int(round((int(get_time[0]) % 1) * 60)))) + relativedelta(
                    hours=appointment.duration)).astimezone(pytz.UTC).replace(
                tzinfo=None)
            for emp in appointment.employee_ids:
                for attendance in emp.resource_calendar_id.attendance_ids:
                    if attendance.dayofweek == str(week_day) and attendance:
                        if (int(emp_time[:2]) >= int(attendance.hour_from)) and \
                                (int(emp_time[:2]) <= int(attendance.hour_to)):
                            emp_list.append(emp)
            for ev in events.filtered(
                    lambda ev: ev.start < local_end and ev.stop > local_start):
                emp_rec = employee.search([('user_id', '=', ev.user_id.id)], limit=1)
                if emp_rec and emp_rec in emp_list:
                    emp_list.remove(emp_rec)
        random_emp = random.choice(emp_list)

        if random_emp:
            return {
                'emp_id': random_emp.id,
                'emp_name': random_emp.name,
            }
        else:
            return {
                'msg': 'Employee not available'
            }

    @http.route(['/get/customer/details',
                 ], type='json', auth="public", website=True)
    def get_customer_details(self, params):
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        appointment = appointment_rec.browse(int(params.get('appointment_id')))
        question_data = []
        for question_id in appointment.question_ids:
            answer = []
            for answer_id in question_id.answer_ids:
                answer.append(answer_id.name)
            dict_data = {
                'question_id': question_id.id,
                'question_name': question_id.name,
                'question_type': question_id.question_type,
                'required_answer': question_id.required_answer,
                'answer': answer,
            }
            question_data.append(dict_data)

        return {
            'name':
                request.env.user.name if not
                request.env.user._is_public() and request.env.user.name else '',
            'email':
                request.env.user.email if not
                request.env.user._is_public() and request.env.user.email else '',
            'phone':
                request.env.user.partner_id.mobile if not
                request.env.user._is_public() and request.env.user.partner_id.mobile
                else '',
            'partner_id':
                request.env.user.partner_id.id if not
                request.env.user._is_public() else '',
            'questions': question_data,
        }

    @http.route(['/submit/booking',
                 ], type='http', auth="public", website=True)
    def submit_booking(self, **kw):
        partner_rec = request.env['res.partner'].sudo()
        emp_rec = request.env['hr.employee'].sudo()
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        appointment = appointment_rec.browse(int(kw.get('appointment_id')))
        question = appointment.question_ids
        str_check = ""
        qn_description = "Name: " + kw.get('name') + "\n" + \
                         "Phone: " + kw.get('phone') + \
                         "\n" + "Email: " + kw.get('email') + "\n"
        filelist = []
        for i in question:
            if ('question_' + str(i.id)) in kw:
                qn_description += \
                    i.name + " - " + kw.get('question_' + str(i.id)) + "\n"

            for j in i.answer_ids:
                if ('question_' + str(i.id) + j.name) in kw:
                    str_check += j.name + " "

            if ('question_' + str(i.id) + 'file') in kw:
                if type(kw.get('question_' + str(i.id) + 'file')) != str:
                    qn_description += i.name + " - " + kw.get(
                        'question_' + str(i.id) + 'file').filename + "\n"
                    filelist.append(kw.get('question_' + str(i.id) + 'file'))

            if i.question_type == 'checkbox':
                if len(str_check) != 0:
                    qn_description += i.name + " - " + str_check + "\n"
                str_check = ""

        get_date = kw.get('date')
        staff_id = kw.get('staff_id')
        check_date = datetime.strptime(get_date, '%Y-%m-%d')
        week_day = check_date.weekday()
        appointment_rec = request.env['calendar.online.appointment'].sudo()
        events = request.env['calendar.event'].sudo().search([])
        employee = request.env['hr.employee'].sudo().search([])
        appointment = appointment_rec.browse(int(kw.get('appointment_id')))
        emp_list = []

        get_date = get_date + ' ' + kw.get('time') + ':00'
        tz_session = pytz.timezone(kw.get('timezone'))
        date_start = tz_session.localize(fields.Datetime.from_string(get_date))
        tz = pytz.timezone(appointment.default_timezone)
        emp_time = str(date_start.astimezone(tz).time())[:-3]
        get_time = emp_time.split(':')[-2:]
        appt_tz = pytz.timezone(appointment.default_timezone)
        requested_tz = pytz.timezone(appointment.default_timezone)
        start_date = requested_tz.fromutc(
            check_date + relativedelta(hours=int(get_time[0])))
        if appointment:
            local_start = appt_tz.localize(
                datetime.combine(start_date, time(
                    hour=int(get_time[0]),
                    minute=int(round((int(get_time[0]) % 1) * 60))))).astimezone(
                pytz.UTC).replace(tzinfo=None)
            local_end = appt_tz.localize(
                datetime.combine(start_date, time(
                    hour=int(get_time[0]),
                    minute=int(round((int(get_time[0]) % 1) * 60)))) + relativedelta(
                    hours=appointment.duration)).astimezone(pytz.UTC).replace(
                tzinfo=None)
            for emp in appointment.employee_ids:
                for attendance in emp.resource_calendar_id.attendance_ids:
                    if attendance.dayofweek == str(week_day) and attendance:
                        if (int(emp_time[:2]) >= int(attendance.hour_from)) and \
                                (int(emp_time[:2]) <= int(attendance.hour_to)):
                            emp_list.append(emp)
            for ev in events.filtered(
                    lambda ev: ev.start < local_end and ev.stop > local_start):
                emp_rec = employee.search([('user_id', '=', ev.user_id.id)], limit=1)
                if emp_rec and emp_rec in emp_list:
                    emp_list.remove(emp_rec)

        if staff_id == '':
            random_emp = random.choice(emp_list)
            Employee = emp_rec.browse(random_emp.id)
        else:
            Employee = emp_rec.browse(int(staff_id))
        Partner = partner_rec.search([('email', '=like', kw.get('email'))], limit=1)

        hour = ""
        for i in kw.get('time'):
            if i == ':':
                break
            else:
                hour += i

        get_date = str(kw.get('date') + ' ' + kw.get('time') + ':00')
        tz_session = pytz.timezone(kw.get('timezone'))
        date_start = tz_session.localize(
            fields.Datetime.from_string(get_date)).astimezone(pytz.utc)
        date_start1 = tz_session.localize(fields.Datetime.from_string(get_date))
        date_end = date_start + relativedelta(hours=appointment.duration)
        if Partner:
            Partner.write({
                'mobile': kw.get('phone'),
                'name': kw.get('name'),
            })
        else:
            Partner = partner_rec.create({
                'name': kw.get('name'),
                'phone': kw.get('phone'),
                'email': kw.get('email'),
            })
        categ_id = request.env.ref('openeducat_online_appointment'
                                   '.calendar_appointment_event')
        alarm_ids = appointment.reminders and [(6, 0, appointment.reminders.ids)] or []
        partner_ids = list(set([Employee.user_id.partner_id.id] + [Partner.id]))
        format_func = format_datetime
        if html2plaintext(appointment.description.encode('utf-8')):
            description = html2plaintext(appointment.description
                                         .encode('utf-8')) + "\n" + qn_description
        else:
            description = qn_description
        date_start_suffix = ""
        event = request.env['calendar.event'].sudo().create({
            'name': '%s with %s' % (appointment.name, Employee.name),
            'start': date_start.strftime(dtf),
            'start_date': start_date.strftime(dtf),
            'stop': date_end.strftime(dtf),
            'allday': False,
            'duration': appointment.duration,
            'location': appointment.location,
            'alarm_ids': alarm_ids,
            'partner_ids': [[6, False, [pid for pid in partner_ids]]],
            'categ_ids': [(4, categ_id.id, False)],
            'appointment_id': appointment.id,
            'user_id': Employee.user_id.id,
            'description': description,
        })
        if 'name' in request.params:
            for attachment in filelist:
                attached_file = attachment.read()
                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'calendar.event',
                    'res_id': event.id,
                    'type': 'binary',
                    'datas': base64.encodebytes(attached_file),
                })

        event.attendee_ids.write({'state': 'accepted'})
        locale = request.env.context.get('lang', 'en_US')
        day_name = format_func(date_start, 'EEE', locale=locale)
        date_start1 = day_name + ' ' + format_func(date_start1,
                                                   locale=locale) + date_start_suffix
        start_date = fields.Datetime.from_string(event.start).strftime('%Y%m%dT%H%M%SZ')
        stop_date = fields.Datetime.from_string(event.stop).strftime('%Y%m%dT%H%M%SZ')
        param = {
            'action': 'TEMPLATE',
            'text': event.name,
            'dates': start_date + '/' + stop_date,
            'details': event.description,
            'location': event.location,
        }

        return request.render("openeducat_online_appointment.confirm_appointment", {
            'google_event_url': 'https://www.google.com/calendar/render?' +
                                url_encode(param),
            'event': event,
            'partner': Partner,
            'appointment': appointment,
            'check_date': date_start1,
            'employee': Employee,
            'timezone': kw.get('timezone'),
            'location': appointment.location,
            'qn_description': qn_description,
        })

    @http.route(['/cancel/appointment/<int:calender_id>'], type='http',
                auth='public', website=True)
    def cancel(self, calender_id, **post):
        request.env['calendar.event'].sudo().search([('id', '=', calender_id)]).unlink()
        return request.redirect('/booking/cancel')
