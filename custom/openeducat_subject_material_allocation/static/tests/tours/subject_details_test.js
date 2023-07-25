odoo.define('openeducat_subject_material_allocation.subject_detail', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_student_subject_details', {
    test: true,
    url: '/subject/details/1',
},
    [
        {
            content: "go to portal_student_subject_material_detail",
            trigger: "a[href*='/study/material/download/']"
        }
    ]
);

});
