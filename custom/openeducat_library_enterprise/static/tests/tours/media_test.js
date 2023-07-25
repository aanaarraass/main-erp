odoo.define('openeducat_library_enterprise.library_media_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('library_media', {
    test: true,
    url: '/library/media/1',
},
    [
        {
        content: "go to portal_media_queue_requested_list",
        trigger: "a[href^='/requested/queue/list/1']",
        },
        {
        content: "go to portal_media_purchase_requested_list",
        trigger: "a[href^='/requested/purchase/list/1']",
        },
        {
        content: "go to portal_media_movement_list",
        trigger: "a[href^='/media/movement/list/1']",
        },
    ]
);

});
