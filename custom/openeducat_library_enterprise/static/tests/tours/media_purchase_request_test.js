odoo.define('openeducat_library_enterprise.media_purchase_request_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_media_purchase_request', {
    test: true,
    url: '/media/purchase/request/1',
},
    [
        {
        content: "go to portal_submit_media_purchase_request ",
        trigger: "form[action^='/purchase/request/submit/'] .btn-primary"
        },
    ]
);

});
