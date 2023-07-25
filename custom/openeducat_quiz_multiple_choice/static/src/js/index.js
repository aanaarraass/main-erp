odoo.define('openeducat_quiz_multiple_choice.openeducat_quiz_multiple_choice_js', function (require) {
    'use strict';
    var core = require("web.core");
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var QWeb = core.qweb;
    var websiteRootData = require('website.root');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.multiple_choice = publicWidget.Widget.extend({
        events: {
            'change select': '_getData',
            'click .multiple_choice_image_div': '_getquizdata_onclick',
            'click .quiz_prv': 'result',
            'click .quiz_finish': 'result',
            'click .quiz_nxt': '_onclick_button',
            'click .quiz_multiple_choice_text': '_onclick_text',
        },
        jsLibs: [
        ],
        selector: '.quiz_start',

        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            var self = this;
            self.answerdata = []
            this._super.apply(this, arguments);
            core.bus.on('question_template_updated', this, this._getData);
        },
        _getData: function () {
            var self = this;
            self._setdefaultanswer();
        },
        _setdefaultanswer: function () {
            var self = this;
            setTimeout(function(){
            if ($('.card-body').find('.que_show').length == 0) {
                var change_id = window.localStorage.getItem("quiz_multiple_choice")
                if (change_id) {
                    $("div[index-id='" + change_id + "']").addClass('que_show').removeClass('que_hide');
                    $("div[grid-index-id='" + change_id + "']").addClass('que_active');
                }
            }
        },300)

            self.data = []
            $('.quiz_multiple_choice').each(function () {
                var data = {
                    id: $(this).attr('data'),
                    answer: false
                }
                self.data.push(data)
            });

            ajax.jsonRpc('/multiple/choice/data', 'call', {
                'answerdata': self.data
            }).then(function (res) {
                self.res = res;
                res.forEach(function (value) {
                    var traitInfo = value.question_data;
                    traitInfo.forEach(function (question) {
                        if (question.given_answer) {
                            if (question.que_type == 'text') {
                                $('#' + question.id).prop('checked', true);
                            }
                            if (question.que_type == 'image') {
                                $('#' + question.id).addClass('active');
                            }
                        }
                    });
                })
            });
        },
        _getquizdata_onclick: function (e) {
            var self = this;
            if ($(e.currentTarget).hasClass('active')) {
                $(e.currentTarget).removeClass('active');
                self.data = {
                    id: $(e.currentTarget).attr('id'),
                    answer: false
                }
            } else {
                $(e.currentTarget).addClass('active');

                self.data = {
                    id: $(e.currentTarget).attr('id'),
                    answer: true
                }
            }
            self.answerdata.push(self.data);
        },
        _onclick_text: function (e) {
            var self = this;
            self.data = {
                id: $(e.currentTarget).attr('id'),
                answer: $(e.currentTarget).is(':checked')
            }
            self.answerdata.push(self.data);
        },
        _onclick_button: function (e) {
            var self = this;
            self.result();
            var next_id = $(e.currentTarget).attr('next-id');
            self.change_que(next_id)
        },
        change_que(change_id) {
            $('#quiz_err_info').html('');
            var tmp_local_storage = JSON.parse(window.localStorage.getItem("quiz"));
            localStorage.setItem('quiz_multiple_choice', change_id);
            if (tmp_local_storage) {
                tmp_local_storage.current_que_id = parseInt(change_id);
                window.localStorage.setItem("quiz", JSON.stringify(tmp_local_storage));
            }
            var index_id = $('.que_show').attr('index-id');
            $("div[index-id='" + index_id + "']").addClass('que_hide').removeClass('que_show');
            $("div[index-id='" + change_id + "']").addClass('que_show').removeClass('que_hide');
            // for grid
            $("div[grid-index-id='" + index_id + "']").removeClass('que_active');
            $("div[grid-index-id='" + change_id + "']").addClass('que_active');
        },
        result() {
            var self = this
            ajax.jsonRpc('/quiz/multiple_choice/answer/data', 'call', {
                'answerdata': self.answerdata
            });
        },
    });
    return publicWidget.registry.multiple_choice;
});
