
from .test_appointment_common import TestAppointmentCommon
from datetime import datetime, timedelta


class TestSlot(TestAppointmentCommon):
    def setUp(self):
        super(TestSlot, self).setUp()

    def test_case_1_slot(self):
        slots = self.appointment_slot.search([])

        for slot in slots:
            slot.appointment_hour()
            slot.name_get()


class TestAppointment(TestAppointmentCommon):

    def setUp(self):
        super(TestAppointment, self).setUp()

    def test_case_1_calendar_appointment(self):
        appointments = self.calendar_appointment.search([])

        for appointment in appointments:
            appointment._compute_count_app()
            appointment.calendar_appointment_schedule()
            appointment.open_website_url()
            appointment._tz_get()
            appointment._website_appointment('Europe/Brussels',
                                             datetime.now().date() + timedelta(days=1),
                                             employee=None,
                                             current_timezone='Europe/Brussels')
            appointment.ensure_one()
            appointment._slots_generate(datetime.now(), datetime.now(),
                                        'Europe/Brussels', datetime.now())
            appointment._get_slots([], datetime.now(), datetime.now())
