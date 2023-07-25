odoo.define('openeducat_quiz_sort_paragraphs.quiz_sort_paragraphs', function (require) {
    'use strict';
    var core = require("web.core");
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");

    var QWeb = core.qweb;
    var websiteRootData = require('website.root');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.quiz_sort_paragraph = publicWidget.Widget.extend({

        events: {
            'change select': '_getData',
            'click #final_finish': '_getanswerdata',
            'click .quiz_finish': '_getanswerdata',
            'click .quiz_nxt': '_getanswerdata',
        },
        xmlDependencies: ['/openeducat_quiz_match_following/static/src/xml/quiz_match_following.xml'],

        jsLibs: [
            '/openeducat_quiz_match_following/static/src/js/draganddrop.js',
        ],
        selector: '.quiz_start',

        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            core.bus.on('question_template_updated', this, this._getData);
        },
        _getData: function () {
            var self = this;
            $('.sort_paragraphs_question').each(function () {
                self.question_id = $('.quiz_nxt').val();
                ajax.jsonRpc('/sort/paragraphs', 'call', {
                    question_id: $('.quiz_nxt').val(),
                }).then(function (res) {
                    self._getquizdata(res);
                });
            })
        },
        _getquizdata: function (res) {
            var self = this
            res.forEach(function (value) {
                var option = value.question_data;
                $(function () {
                    $("." + value.id).sortable();
                });
                $("." + value.id).on("sortchange", function (event, ui) {
                    alert("hello")
                });
                self.temp = 0;
                option.forEach(function (data) {
                    var question = data.default_answer;
                    self.temp++;
                    $("." + value.id).append('<li class="ui-state-default answer' + self.temp + ' sort_option' + value.id + '" id="sort_answer"><span class="ui-icon ui-icon-triangle-2-n-s"></span>' + question + '<span style=" visibility: hidden;">$$$</span></li>');
                })

                $("#sort_btn" + value.id).on("click", function (e) {
                    var temp = $(e.currentTarget).attr('data');
                    var data = $('.sort_option' + temp).text();

                    var text = "hello $$$ abc $$$ what is data abc data hello";
                    var regex = new RegExp("data(.*?)data", 'g');
                    var loop = text.match(regex);
                    loop.forEach(function (l) {
                        l.replace("data", "");
                    })
                });
            })
            $(document).on('click', ".quiz_finish", function (e) {
                if ($('#from_quiz').length != 0) {
                    $('#from_quiz').submit();
                } else {
                    $('#from_quiz_dynamic').submit();
                }
            });
        },
        _getanswerdata: function (res, e) {

            let temp = $('.sort_paragraphs_question').attr('id');
            var temp1 = $('.sort_paragraphs_question').length;
            var answer = {}, all_data = [];

            for (let i = 0; i < temp1; i++) {
                var x = Number(temp) + Number(i)
                var data = $('.sort_option' + x).text();
                var que_type = $('#' + x).attr('value');
                answer.id = x
                answer.que_type = que_type
                answer.answer = data
                all_data.push(answer);
                answer = {}
            }
            ajax.jsonRpc('/quiz/sortparagraphs/alldata', 'call', {
                'answer_data': data,
                'answerdata': temp,
                'all_data': all_data
            });
        },

    });
    return publicWidget.registry.quiz_sort_paragraph;

});
