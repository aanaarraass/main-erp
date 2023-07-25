odoo.define('openeducat_library_enterprise.media_queue_request_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_media_queue_request', {
    test: true,
    url: '/media/queue/request/1',
},
    [
        {
        content: "go to portal_library_queue_craete",
        trigger: "form[action^='/queue/request/submit/'] .btn-primary"
        },
    ]
);

});
