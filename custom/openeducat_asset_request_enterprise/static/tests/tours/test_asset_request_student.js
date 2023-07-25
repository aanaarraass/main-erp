odoo.define('openeducat_asset_request_enterprise.student_asset_request_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_asset_request_student', {
    test: true,
    url: '/my/asset-request',
},
    [
        {
            content: "select Laptop",
            extra_trigger: '#request_asset',
            trigger: "span:contains(Laptop)",
        },
    ]
);
});
