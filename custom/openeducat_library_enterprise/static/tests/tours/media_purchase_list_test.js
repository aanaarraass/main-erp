odoo.define('openeducat_library_enterprise.purchase_request_list_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('media_purchase_list', {
    test: true,
    url: '/requested/purchase/list/1',
},
    [
        {
        content: "go to portal_library_media_purchase_create",
        trigger: "a[href^='/media/purchase/request']",
        },
    ]
);

});