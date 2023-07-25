odoo.define('openeducat_library_enterprise.request_queue_list_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_media_queue_request_submit', {
    test: true,
    url: '/requested/queue/list/1',
},
    [
        {
        content: "select Troposhere In Detail",
        extra_trigger: '#req_media',
        trigger: 'span:contains(Troposhere In Detail)',
        },
    ]
);

});