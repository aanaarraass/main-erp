odoo.define('openeducat_library_enterprise.media_movement_list_tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('media_movement_list', {
    test: true,
    url: '/media/movement/list/1',
},
    [
        {
        content: "go to portal_media_movement_information",
        trigger: "a[href^='/media/movement/information/1/1']",
        },
    ]
);

});