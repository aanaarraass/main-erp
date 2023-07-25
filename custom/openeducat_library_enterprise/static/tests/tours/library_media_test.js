odoo.define('openeducat_library_enterprise.library_all_media_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('test_library_media', {
    test: true,
    url: '/library/media',
},
    [
        {
        content: "select Troposhere In Detail",
        extra_trigger: '#test',
        trigger: 'span:contains(Troposhere)',
        },
    ]
);

});