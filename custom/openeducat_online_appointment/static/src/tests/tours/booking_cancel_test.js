odoo.define('openeducat_online_appointment.booking_cancel_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_booking_cancel', {
    test: true,
    url: '/booking/cancel',
},
    [
        {
            content: "select Meeting with Principle",
            extra_trigger: '.appointment_name',
            trigger: 'span:contains(Meeting with Principle)',
        },
    ]
);

});