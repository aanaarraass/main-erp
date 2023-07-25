odoo.define('openeducat_library_enterprise.queue_request_submit_our', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_queue_request_submit', {
    test: true,
    url: '/queue/request/submit/1',
},
    [
        {
        content: "go to portal_media_queue_requested_list ",
        trigger: "a[href^='/requested/queue/list/']"
        },
    ]
);

});
