odoo.define('openeducat_asset_request_enterprise.asset_request_detail_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_asset_request_detail', {
    test: true,
    url: '/my/asset/asset-detail/1',
},
    [
        {
            content: "select Laptop",
            extra_trigger: '#asset_name',
            trigger: "span:contains(Laptop)",
        },
    ]
);
});
