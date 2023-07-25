odoo.define('openeducat_online_appointment.booking_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_booking', {
    test: true,
    url: '/booking',
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