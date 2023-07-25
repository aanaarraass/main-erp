from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import calendar as cal
import pytz
import datetime
from datetime import datetime, timedelta, time
from dateutil import rrule
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Default Working Hours', help='Working hour of week')
    resource_id = fields.Many2one('resource.resource', 'Resource')


class CalendarAppointmentSlot(models.Model):
    _name = "calendar.appointment.slot"
    _description = "Booking Slot"

    week = fields.Selection([
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ], string='Week Day',
        help="Choose week day to allow users to take appointment that day")
    hour = fields.Float('Starting Hour', help='Appointment start hour')
    appointment_id = fields.Many2one('calendar.online.appointment',
                                     'Calendar Appointment', ondelete='cascade')

    @api.constrains('hour')
    def appointment_hour(self):
        if any(self.filtered(lambda slot: 0.00 > slot.hour or slot.hour >= 24.00)):
            raise ValidationError(_("Please enter a "
                                    "valid hour between 0:00 to 24:00 for your slots."))

    def name_get(self):
        week = dict(self._fields['week'].selection)
        return self.mapped(lambda slot: (
            slot.id, "%s, %02d:%02d" % (week.get(slot.week), int(slot.hour),
                                        int(round((slot.hour % 1) * 60)))))


class CalendarAppointmentQuestion(models.Model):
    _name = "calendar.appointment.question"
    _description = "Appointment Question"

    question = fields.Char("Question",
                           help='Add Question to ask user for getting the details')
    question_type = fields.Selection([
        ('char', 'Single Line Text'),
        ('text', 'Multi Line Text')
    ], string="Question Type", help='Type of question ask to user')

    placeholder = fields.Char('Placeholder')
    required_answer = fields.Boolean("Required Answer")
    appointment_id = fields.Many2one('calendar.online.appointment',
                                     'Online Appointment')


class CalendarOnlineAppointment(models.Model):
    _name = 'calendar.online.appointment'
    _description = "Booking calendar Appointment"
    _inherit = ['mail.thread', "website.seo.metadata", 'website.published.mixin',
                'qna.mixin']

    def _compute_count_app(self):
        for i in self:
            event = self.env['calendar.event'].search([('appointment_id', '=', i.id)])
            i.count_appointment = len(event)

    name = fields.Char("Name")
    code = fields.Char("Unique Code", readonly=True, index=True,
                       default=lambda self: _('New'),
                       tracking=True, help='Unique to identify appointment')
    employee_ids = fields.Many2many('hr.employee', 'employee_calendar_rel',
                                    'calendar_id', 'emp_id', string='Staff',
                                    domain=[('resource_calendar_id', '!=', False),
                                            ('user_id', '!=', False)],
                                    help='Staff line')
    resource_ids = fields.Many2many('resource.calendar.attendance',
                                    'calendar_attend_rel',
                                    'attendance_id', string='Resources')

    slots = fields.One2many('calendar.appointment.slot', 'appointment_id',
                            string='Appointment Slots',
                            help='User can select the slot which is in slot line')
    duration = fields.Float('Duration (in hours)', default=1.0, tracking=True,
                            help='Hour for appointment')
    appointment_date = fields.Date("Appointment Date")
    min_appointment_hours = fields.Float('Appointment before (hours)',
                                         default=1.0, tracking=True,
                                         help='Minimum hours before'
                                              ' that user take appointment')
    max_appointment_days = fields.Integer('Appointment not after (days)',
                                          tracking=True, default=10,
                                          help='Maximum days, Only those days'
                                          ' user take appointment')
    not_after_type = fields.Selection([
        ('calendar_days', 'Calendar Days'),
        ('business_days', 'Business Days'),
    ], string='not_after_type', default='calendar_days',
        help='Set the days')
    is_cancel = fields.Boolean("Allow Appointment Cancellation", tracking=True,
                               help='For appointment cancellation')
    min_appointment_cancel_duration = fields.Integer(
        'Cancel Appointment Before', tracking=True, default=1,
        help='User cancel appointment before duration')

    cancel_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ], string='Cancel In', default='hours', help='Types of time for cancel appointment')

    assign_method = fields.Selection([
        ('random', 'Random'),
        ('customer', 'Customer Selection'),
    ], string='Assignation', default='random',
        help='Set the method for assignation Staff')
    user_id = fields.Many2one('res.users', string='Team Leader', tracking=True,
                              default=lambda self: self.env.user, copy=False)
    default_timezone = fields.Selection(
        '_tz_get', string='Timezone', default=lambda self: self.env.user.tz,
        help='Set your timezone')
    reminders = fields.Many2many('calendar.alarm', string="Reminders")
    description = fields.Html("Description",
                              default="Thank You For Booking Appointment.",
                              help='Message for the user')
    location = fields.Char("Location")
    questions = fields.One2many('calendar.appointment.question', 'appointment_id',
                                string='Appointment Question',
                                help='Add the question to ask the user')
    count_appointment = fields.Integer(string='appointment',
                                       compute='_compute_count_app',
                                       help='Number of appointment which is booked')

    @api.constrains('employee_ids')
    def check_employee(self):
        if len(self.employee_ids.ids) == 0:
            raise ValidationError(_('Employee can not be empty.'))

    @api.onchange('duration')
    def onchange_duration(self):
        for record in self:
            if record.duration < 1:
                raise ValidationError(_('Duration Time can not be zero.'))

    def _compute_website_url(self):
        super(CalendarOnlineAppointment, self)._compute_website_url()
        for appointment in self:
            if appointment.id:
                appointment.website_url = '%s' % (appointment.id)

    def calendar_appointment_schedule(self):
        return {
            'name': _('Schedule Appointments'),
            'view_mode': 'tree,form,calendar',
            'res_model': 'calendar.event',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('appointment_id', 'in', self.ids)],
        }

    def open_website_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/booking',
            'target': 'self',
        }

    def _tz_get(self):
        return [(x, x) for x in pytz.all_timezones]

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'calendar.online.appointment') or 'New'
        result = super(CalendarOnlineAppointment, self).create(vals)
        return result

    def _slots_generate(self, first_day, last_day, timezone, check_date):
        def append_slot(day, slot):
            local_start = appt_tz.localize(
                datetime.combine(day, time(hour=int(slot.hour),
                                           minute=int(round((slot.hour % 1) * 60)))))
            local_end = appt_tz.localize(
                datetime.combine(day,
                                 time(hour=int(slot.hour),
                                      minute=int(round((slot.hour % 1) * 60)))) +
                relativedelta(hours=self.duration))

            slots.append({
                self.default_timezone: (
                    local_start,
                    local_end,
                ),
                timezone: (
                    local_start.astimezone(requested_tz),
                    local_end.astimezone(requested_tz),
                ),
                'UTC': (
                    local_start.astimezone(pytz.UTC).replace(tzinfo=None),
                    local_end.astimezone(pytz.UTC).replace(tzinfo=None),
                ),
                'slot': slot,
            })

        appt_tz = pytz.timezone(self.default_timezone)
        requested_tz = pytz.timezone(timezone)
        slots = []
        if self.min_appointment_hours > 18:
            if self.min_appointment_hours % 24 == 0:
                for slot in self.slots.filtered(
                        lambda x: int(x.week) == check_date.isoweekday()):
                    if slot.hour > first_day.hour + first_day.minute / 60.0:
                        append_slot(first_day.date(), slot)
            else:
                for slot in self.slots.filtered(
                        lambda x: int(x.week) == check_date.isoweekday()):
                    append_slot(first_day.date(), slot)
        else:
            for slot in self.slots.filtered(
                    lambda x: int(x.week) == first_day.isoweekday()):
                append_slot(first_day.date(), slot)
        slot_weekday = [int(weekday) - 1 for weekday in self.slots.mapped('week')]
        for day in rrule.rrule(rrule.DAILY,
                               dtstart=first_day.date() + timedelta(days=1),
                               until=last_day.date(),
                               byweekday=slot_weekday):
            for slot in self.slots.filtered(lambda x: x.week == day.isoweekday()):
                append_slot(day, slot)
        return slots

    def _get_slots(self, slots, first_day, last_day, employee=None):
        def get_available_slots(start_dt, end_dt, intervals):
            def get_start():
                def recursive_start(lower_bound, upper_bound):
                    if upper_bound - lower_bound <= 1:
                        if intervals[upper_bound][0] <= start_dt:
                            return upper_bound
                        return lower_bound
                    index = (upper_bound + lower_bound) // 2
                    if intervals[index][0] <= start_dt:
                        return recursive_start(index, upper_bound)
                    else:
                        return recursive_start(lower_bound, index)

                if start_dt <= intervals[0][0] - tolerance:
                    return -1
                if end_dt >= intervals[-1][1] + tolerance:
                    return -1
                return recursive_start(0, len(intervals) - 1)

            if not intervals:
                return False

            tolerance = timedelta(minutes=1)
            start_index = get_start()
            if start_index != -1:
                for index in range(start_index, len(intervals)):
                    if intervals[index][1] >= end_dt - tolerance:
                        return True
                    if len(intervals) == index + 1 or intervals[index + 1][0] - \
                            intervals[index][1] > tolerance:
                        return False
            return False

        def is_calendar_available(slot, events, employee):
            start_dt_string = slot['UTC'][0]
            end_dt_string = slot['UTC'][1]
            employee_tz = pytz.timezone(employee.user_id.tz
                                        or self.sudo().env.user.tz
                                        or slot['slot'].appointment_id.default_timezone
                                        or 'UTC')
            for ev in events.filtered(
                    lambda ev: ev.start < end_dt_string and ev.stop > start_dt_string):
                if ev.allday:
                    ev_start_dt = datetime.combine(
                        fields.Date.from_string(ev.start_date), time.min)
                    ev_stop_dt = datetime.combine(
                        fields.Date.from_string(ev.stop_date), time.max)
                    ev_start_dt = employee_tz.localize(ev_start_dt)\
                        .astimezone(pytz.UTC).replace(tzinfo=None)
                    ev_stop_dt = employee_tz.localize(ev_stop_dt)\
                        .astimezone(pytz.UTC).replace(tzinfo=None)
                    if ev_start_dt < slot['UTC'][1] and ev_stop_dt > slot['UTC'][0]:
                        return False
                else:
                    return False
            return True

        workhours = {}
        meetings = {}
        available_employees = [emp.with_context({'tz': emp.user_id.tz})
                               for emp in (employee or self.employee_ids)]
        for slot in slots:
            for emp_pos, emp in enumerate(available_employees):
                if emp_pos not in workhours:
                    workhours[emp_pos] = [
                        (interval[0].astimezone(pytz.UTC).replace(tzinfo=None),
                         interval[1].astimezone(pytz.UTC).replace(tzinfo=None))
                        for interval in emp.resource_calendar_id._work_intervals_batch(
                            first_day, last_day, resources=emp.resource_id,
                        )[emp.resource_id.id]
                    ]

                if get_available_slots(slot['UTC'][0], slot['UTC'][1],
                                       workhours[emp_pos]):
                    if emp_pos not in meetings:
                        meetings[emp_pos] = self.env['calendar.event'].search([
                            ('partner_ids.user_ids', '=', emp.user_id.id),
                            ('start', '<', fields.Datetime.to_string(
                                last_day.replace(hour=23, minute=59, second=59))),
                            ('stop', '>', fields.Datetime.to_string(
                                first_day.replace(hour=0, minute=0, second=0)))
                        ])

                    if is_calendar_available(slot, meetings[emp_pos], emp):
                        slot['employee_id'] = emp
                        break

    def _website_appointment(self, timezone, check_date, employee=None,
                             current_timezone=''):
        self.ensure_one()
        appt_tz = pytz.timezone(self.default_timezone)
        requested_tz = pytz.timezone(timezone)
        if self.min_appointment_hours > 0:
            first_day = requested_tz.fromutc(
                datetime(check_date.year, check_date.month, check_date.day) +
                relativedelta(hours=self.min_appointment_hours))
        else:
            first_day = requested_tz.fromutc(datetime(check_date.year,
                                                      check_date.month, check_date.day))
        last_day = datetime.combine(
            first_day.date() + timedelta(days=1), datetime.min.time())
        check_date = requested_tz.fromutc(datetime(check_date.year,
                                                   check_date.month, check_date.day))

        slots = self._slots_generate(
            first_day.astimezone(appt_tz),
            last_day.astimezone(appt_tz), timezone, check_date)
        if not employee or employee in self.employee_ids:
            self._get_slots(slots, first_day.astimezone(pytz.UTC),
                            last_day.astimezone(pytz.UTC), employee)
        today = requested_tz.fromutc(datetime.utcnow())
        start = today
        month_dates_calendar = cal.Calendar(0).monthdatescalendar
        months = []
        time_list = []
        while (start.year, start.month) <= (last_day.year, last_day.month):
            dates = month_dates_calendar(start.year, start.month)
            for week_index, week in enumerate(dates):
                for day_index, day in enumerate(week):
                    today_slots = []
                    while slots and (slots[0][timezone][0].date() <= day):
                        if (slots[0][timezone][0].date() == day) and \
                                ('employee_id' in slots[0]):
                            today_slots.append({
                                'datetime':
                                    slots[0][timezone][0].strftime('%Y-%m-%d %H:%M:%S'),
                                'hours': slots[0][timezone][0].strftime('%H:%M')
                            })

                            d1 = slots[0][timezone][0]
                            now = d1.astimezone(pytz.timezone(current_timezone))
                            tz = pytz.timezone(current_timezone)
                            now_tz = now.astimezone(tz)
                            time_list.append(
                                {'hours': now_tz.strftime('%H:%M')})
                        slots.pop(0)
                        dates = {
                            'time_list': time_list,
                        }

            months.append({
                'weeks': time_list,
            })
            start = start + relativedelta(months=1)
        return time_list

    def _website_appointment_all_slots(self, timezone, start_date,
                                       end_date, employee=None):
        self.ensure_one()
        appt_tz = pytz.timezone(self.default_timezone)
        requested_tz = pytz.timezone(timezone)
        first_day = requested_tz.fromutc(
            start_date + relativedelta(hours=self.min_appointment_hours))
        last_day = requested_tz.fromutc(
            end_date + relativedelta(hours=self.min_appointment_hours))
        slots = self._slots_generate(first_day.astimezone(appt_tz),
                                     last_day.astimezone(appt_tz), timezone)
        if not employee or employee in self.employee_ids:
            self._get_slots(slots, first_day.astimezone(pytz.UTC),
                            last_day.astimezone(pytz.UTC), employee)
        today = requested_tz.fromutc(datetime.utcnow())
        start = today
        month_dates_calendar = cal.Calendar(0).monthdatescalendar
        months = []
        time_list = []
        while (start.year, start.month) <= (last_day.year, last_day.month):
            dates = month_dates_calendar(start.year, start.month)
            for week_index, week in enumerate(dates):
                for day_index, day in enumerate(week):
                    today_slots = []
                    while slots and (slots[0][timezone][0].date() <= day):
                        if (slots[0][timezone][0].date() == day) and \
                                ('employee_id' in slots[0]):
                            today_slots.append({
                                'employee_id': slots[0]['employee_id'].id,
                                'datetime':
                                    slots[0][timezone][0].strftime('%Y-%m-%d %H:%M:%S'),
                                'hours': slots[0][timezone][0].strftime('%H:%M')
                            })

                            time_list.append(
                                {'hours': slots[0][timezone][0].strftime('%H:%M')})
                        slots.pop(0)
                        dates = {
                            'time_list': time_list,
                        }

            months.append({
                'weeks': time_list,
            })
            start = start + relativedelta(months=1)
        return time_list


class CalendarEvent(models.Model):
    _inherit = "calendar.event"
    appointment_id = fields.Many2one('calendar.online.appointment',
                                     'Online Appointment', readonly=True)
