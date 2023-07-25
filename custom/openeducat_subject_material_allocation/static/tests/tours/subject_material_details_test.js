odoo.define('openeducat_subject_material_allocation.subject_material_detail', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_subject_material_details', {
    test: true,
    url: '/subject/material/detail/1',
},
    [
        {
            content: "go to download_study_material",
            trigger: "a[href*='/subject/material/detail/']"
        }
    ]
);

});
