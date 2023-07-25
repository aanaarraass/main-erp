odoo.define('openeducat_student_leave_enterprise.student_leave_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('student_leave_list', {
    test: true,
    url: '/my/time_off/',
},
        [
            {
                content: "select Sumita S Dani",
                extra_trigger: '#student_id',
                trigger: "span:contains(Sumita S Dani)",
            },
            {
                content: "go to portal_student_time_off_request",
                trigger: "a[href*='/time_off/request/']"
            },
        ]
);

tour.register('student_leave_request', {
    test: true,
    url: '/time_off/request/',
},
        [
            {
                content: "select Sumita S Dani",
                extra_trigger: '#student_id',
                trigger: "form:has(input[name='student_id'])",
            },
        ]
);

tour.register('parent_leave_list', {
    test: true,
    url: '/my/time_off/1',
},
        [
            {
                content: "select Sumita S Dani",
                extra_trigger: '#student_id',
                trigger: "span:contains(Sumita S Dani)",
            },
        ]
);
});