odoo.define('openeducat_quiz_drag_into_text.quiz_drag_into_text', function (require) {
    'use strict';
    var core = require("web.core");
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var QWeb = core.qweb;
    var publicWidget = require('web.public.widget');

    publicWidget.registry.drag_into_text_data = publicWidget.Widget.extend({

        events: {
            'change select': '_getData',
        },
        selector: '.quiz_start',

        jsLibs: [
            '/openeducat_quiz_match_following/static/src/js/draganddrop.js',
        ],
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
            $('.drag_question').each(function () {
                self.question_id = parseInt($('.quiz_nxt').val())
                ajax.jsonRpc('/DragIntoText', 'call', {
                    question_id: parseInt($('.quiz_nxt').val()),
                }).then(function (res) {
                    self._getquizdata(res);
                });
            })
        },
        _getquizdata: function (res) {
            var self = this

            res.forEach(function (question) {
                // create Option Div
                var div = document.createElement('div');
                self.option_div = ('draggable_option' + question.id)
                div.setAttribute("id", self.option_div);
                var div_class = ('all_drag_option drop_droptarget' + question.id)
                self.droptarget_btn = ('drop_droptarget' + question.id)
                div.setAttribute("class", div_class);
                $("#" + question.id).append(div);

                // create question Div
                var div = document.createElement('div');
                self.question_div = ('draggable_question' + question.id)
                div.setAttribute("id", self.question_div);
                div.setAttribute("class", " all_drag_question");
                $("#" + question.id).append(div);

                // Create Option Button
                var option = question.option
                option.forEach(function (q1) {
                    var answer = document.createElement('button');
                    var answer_id = ("answer" + question.id);
                    var answer_name = q1.option
                    var btn_class = ("drag_into_text_btn" + question.id);
                    answer.setAttribute('class', ('drag_into_text_mybtn ') + btn_class)
                    answer.setAttribute('text', answer_name);
                    answer.innerText = answer_name;

                    $("#" + self.option_div).append(answer);

                })
                // Create Question
                var que = document.createElement('p');
                self.que_id = ("ans" + question.id);
                que.setAttribute("class", question.id)
                que.setAttribute("id", self.que_id);
                var que_name = question.question;
                $("#" + self.question_div).append(que);
                document.getElementById(self.que_id).innerHTML = que_name

                // Draggable Buttion
                $('.drag_into_text_btn' + question.id).draggable({
                    revert: true,
                    placeholder: true,
                    scroll: true,
                    droptarget: ('.' + self.droptarget_btn),
                    drop: function (evt, droptarget) {
                        var temp = $(droptarget).attr('id');
                        if (temp != 'option1') {
                            $(this).appendTo(droptarget);
                        } else {
                            var demo = $(droptarget).children().length;
                            if (demo == 0) {
                                $(droptarget).html('');
                                $(this).appendTo(droptarget);
                                var data = $(this).parent().parent().attr('id');
                                var answerdata = $('#' + data).text()
                                var question_id = $('#' + data).attr('class');
                                var examid = $('input[name="config_data"]').val();
                                ajax.jsonRpc('/quiz/dragintotext/data', 'call', {
                                    'answerdata': answerdata,
                                    'question_id': question_id,
                                    'examid': examid
                                });
                            }
                        }
                    }
                })

            })
            $(document).on('click', ".quiz_finish", function (e) {
                self.que_required(res);
            });

            $(document).on('click', ".quiz_nxt", function (e) {
                self.next_id = $(this).attr('next-id');
                if (res[0].que_required == true) {
                    self.submit = 0;
                    if ($('.que_show').length != 0) {
                        $('span', ".que_show").each(function () {
                            if ($(this).attr('id') == 'option1') {
                                if ($(this).text()) {
                                    self.submit = 1
                                } else {
                                    self.submit = 0
                                    return false;
                                }
                            }
                        });
                    } else {
                        $('span', ".all_drag_question").each(function () {
                            if ($(this).text()) {
                                self.submit = 1
                                change_que(self.next_id);
                            } else {
                                self.submit = 0
                                $('#quiz_err_info').html('<div class="alert alert-danger">' + '<strong>Error!</strong> Answer is required ' + '</div>');
                                return false;
                            }
                        });
                    }
                    $('#quiz_err_info').html('');


                    if (self.submit == 1) {
                        change_que(self.next_id);
                    }
                    $('span', ".all_drag_question").each(function () {
                    });
                }else{
                    change_que(self.next_id);
                }
                if (self.submit == 0) {
                    return false;
                }

                function change_que(change_id) {
                    $('#quiz_err_info').html('');
                    var tmp_local_storage = JSON.parse(window.localStorage.getItem("quiz"));
                    // tmp_local_storage.current_que_id = parseInt($('.quiz_nxt').val())
                    window.localStorage.setItem("quiz", JSON.stringify(tmp_local_storage));
                    var index_id = $('.que_show').attr('index-id');
                    $("div[index-id='" + index_id + "']").addClass('que_hide').removeClass('que_show');
                    $("div[index-id='" + change_id + "']").addClass('que_show').removeClass('que_hide');
                    // for grid
                    $("div[grid-index-id='" + index_id + "']").removeClass('que_active');
                    $("div[grid-index-id='" + change_id + "']").addClass('que_active');
                }
            });
        },
        que_required: function (res) {
            if (res[0].que_required == true) {
                var submit = 0;
                $('span', ".all_drag_question").each(function () {
                    if ($(this).attr('id') == 'option1') {
                        if ($(this).text()) {
                            submit = 1
                        } else {
                            submit = 0
                            $('#quiz_err_info').html('<div class="alert alert-danger">' + '<strong>Error!</strong> Answer is required ' + '</div>');
                            return false;
                        }
                    }
                })
                if (submit == 1) {
                    if ($('#from_quiz').length != 0) {
                        $('#from_quiz').submit();
                    } else {
                        $('#from_quiz_dynamic').submit();
                    }
                }else{
                    return true;
                }
            }else{
                if ($('#from_quiz').length != 0) {
                    $('#from_quiz').submit();
                } else {
                    $('#from_quiz_dynamic').submit();
                }
            }
        },
    });
    return publicWidget.registry.drag_into_text_data;
});
