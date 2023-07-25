odoo.define('openeducat_asset_request_enterprise.asset_request_submit_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_request_asset_submit', {
    test: true,
    url: '/my/asset/asset-request',
},
    [
        {
            content: "select Laptop",
            extra_trigger: '#asset',
            trigger: 'form:has(input[name="assets"])',
        },
    ]
);
});
