odoo.define('openeducat_library_enterprise.media_movement_information_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('media_movement_information', {
    test: true,
    url: '/media/movement/information/1',
},
    [
        {
        content: "select 2",
        extra_trigger: "#media_movement_ids",
        trigger: "div:contains(2)",
        },
    ]
);

});