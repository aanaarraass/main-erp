from odoo.tests import common
import odoo.tests


class TestAppointmentCommon(common.TransactionCase):
    def setUp(self):
        super(TestAppointmentCommon, self).setUp()
        self.calendar_appointment = self.env['calendar.online.appointment']
        self.appointment_slot = self.env['calendar.appointment.slot']


@odoo.tests.common.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):

    def test_booking(self):
        self.start_tour("/", 'test_booking', login="admin")

    def test_booking_cancel(self):
        self.start_tour("/", 'test_booking_cancel', login="admin")
