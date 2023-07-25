odoo.define('openeducat_quiz_match_following.openeducat_quiz_match_the_following', function (require) {
    'use strict';
    var core = require("web.core");
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var QWeb = core.qweb;
    var websiteRootData = require('website.root');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.quiz_data = publicWidget.Widget.extend({

        events: {
            'change select': '_getData',
        },
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
            $('.match_following').each(function () {
                self.question_id = parseInt($('.quiz_nxt').val());
                ajax.jsonRpc('/following/data', 'call', {
                    question_id: parseInt($('.quiz_nxt').val()),
                }).then(function (res) {
                    self._getquizdata(res);
                });
            })
        },
        _getquizdata: function (res) {
            // $('#wrapwrap').css('overflow', '');
            var self = this;
            res.forEach(function (value) {
                //create Div Question
                var div = document.createElement('div');
                var div_id = (value.id);
                self.div_data = div_id;
                // div.setAttribute("id", div_id);
                div.setAttribute("class", "col-md-6");
                $('#quiz_question' + self.question_id).append(div);

                //createElement div Answer
                var div = document.createElement('div');
                var div_answer = ("following_answer_box" + value.id);
                self.div_ans = div_answer;
                div.setAttribute("id", div_answer);
                div.setAttribute("class", "col-md-6 row");
                $('#quiz_question' + self.question_id).append(div);

                //createElement div option
                var div = document.createElement('div');
                var div_answer = ("all_" + value.id);
                self.question_id = value.id;
                self.div_option = div_answer;
                var add_class = ('drop' + self.question_id)
                div.setAttribute("id", div_answer);
                div.setAttribute("class", ("col-md-12 row question_box pb-4 ") + add_class);
                $('#quiz_question' + self.question_id).append(div);
                var hidden_field = `<input type="hidden" name="question_id" value="all_${self.question_id}">`
                $('#' + div_answer).append(hidden_field);
                var hidden_field_question_box = `<input type="hidden" name="question_option" value="all_question_option">`
                $('#' + div_answer).append(hidden_field_question_box);

                var traitInfo = value.question_data;
                traitInfo.sort(() => Math.random() * (traitInfo + 1.5));
                var given_anser = [];
                var not_given_anser = [];

                traitInfo.forEach(function (question) {
                    var div = document.createElement('div');
                    self.questiondiv = (question.id)
                    div.setAttribute("id", self.questiondiv);
                    div.setAttribute("class", "col-md-12 row quesionline");
                    $('#quiz_question' + self.question_id).append(div);

                    if (question.image != false) {
                        var image = document.createElement('img');
                        var image_id = ('image' + question.id)
                        var image_data = question.image;
                        image.setAttribute("id", image_id);
                        image.setAttribute("class", "child_image col-md-2")
                        $('#' + self.questiondiv).append(image);
                        $("#" + image_id).attr("src", "data:image/*;base64," + image_data);
                    }
                    //question create
                    var que = document.createElement('div');
                    var que_id = ("ans" + question.id);
                    que.setAttribute("id", que_id);
                    if (question.image == false) {
                        que.setAttribute('class', 'child_question col-md-6 my-2')
                    }
                    else {
                        que.setAttribute('class', 'child_question col-md-4 my-2')
                    }
                    if (question.question == false) {
                        var que_name = '';
                    }
                    else {
                        var que_name = question.question;
                    }
                    $('#' + self.questiondiv).append(que);

                    document.getElementById(que_id).innerHTML = que_name
                    //answer drop box create
                    var drop_div = document.createElement('div');
                    var drop_div_id = ("droppable" + question.id);
                    var drop_div_class = ("drop" + self.question_id)
                    drop_div.setAttribute('class', ('col-md-6 drop_btn_id ' + drop_div_class))
                    drop_div.setAttribute('id', 'option')
                    $("#" + self.questiondiv).append(drop_div);


                })
                traitInfo.sort(() => Math.random() - 0.5);
                var given_anser_list = [];
                value.question_data.forEach(function (question) {
                    if (question.name) {
                        given_anser.push(question);
                        given_anser_list.push(question.name);
                    }
                });
                not_given_anser = _.filter(value.question_data, function (q) {
                    return !given_anser_list.includes(q.default_answer);
                });
                var shuffle_not_given_answer = not_given_anser;
                shuffle_not_given_answer.sort(() => Math.random() * (shuffle_not_given_answer + 1.5));
                shuffle_not_given_answer.forEach(function (question) {
                    var answer = document.createElement('input');
                    var answer_id = ("answer" + question.id);
                    var answer_name = question.default_answer
                    answer.setAttribute('id', self.div_data)
                    var btn_class = ("following_question" + self.question_id);
                    answer.setAttribute('class', ('btn btn-secondary mybtn ') + btn_class)
                    answer.setAttribute('type', 'button');
                    answer.setAttribute('value', answer_name);
                    $("#" + self.div_option).append(answer);
                });
                given_anser.forEach(function (question) {
                    var answer = document.createElement('input');
                    var answer_id = ("answer" + question.id);
                    var answer_name = question.name
                    answer.setAttribute('id', self.div_data)
                    var btn_class = ("following_question" + self.question_id);
                    answer.setAttribute('class', ('btn btn-secondary mybtn ') + btn_class)
                    answer.setAttribute('type', 'button');
                    answer.setAttribute('value', answer_name);
                    $("#" + question.id).find('.drop_btn_id').append(answer);
                });
                var temp = ('.drop' + self.question_id);

                $('.following_question' + self.question_id).draggable({
                    revert: true,
                    placeholder: true,
                    scroll: true,
                    droptarget: ('.drop' + self.question_id),
                    stop: function (ent, ui) {
                    },
                    drop: function (evt, droptarget) {
                        var temp = $(droptarget).children().length;
                        if ($(this).parent().children().length == 1) {
                            $(this).parent().css('border', '2px solid #cbced4');
                        }
                        if (temp == 0) {
                            var demo = $(this).parent().find('input[name="question_option"]').val();
                            var id = $(this).parent().parent().attr('id');
                            var answerdata1 = {}
                            if (demo != 'all_question_option') {
                                answerdata1 = {
                                    'id': id,
                                    'answer': ''
                                }
                            }

                            $(this).appendTo(droptarget);
                            var answer = $(this).val();
                            var id = $(this).parent().parent().attr('id');
                            var answerdata = {
                                'id': id,
                                'answer': answer
                            }
                            ajax.jsonRpc('/quiz/followinganswer/data', 'call', {
                                'answerdata': answerdata,
                                'answerdata1': answerdata1
                            });
                        }
                        var answer_count = $(droptarget).children().val();
                        var droptarget_val = $(droptarget).attr('id');
                        var droptarget_val1 = $(this).parent().attr('id');
                        var demo = $(droptarget).parent().find('input[name="question_option"]').val();

                        if (droptarget_val1 == 'option') {
                            if (demo == 'all_question_option') {
                                if (answer_count == droptarget_val) {
                                    var demo = $(this).parent().parent().attr('id');
                                    var answerdata = {
                                        'id': demo,
                                        'answer': ''
                                    }
                                    ajax.jsonRpc('/quiz/followinganswer/data', 'call', {
                                        'answerdata': answerdata
                                    });
                                    $(this).appendTo(droptarget);
                                }
                            }
                        }
                        if ($(this).parent().children().length == 1) {
                            $(this).parent().css('border', '2px solid #707172');
                        }
                    }
                })
                $('.drop_btn_id').each(function (index) {
                    if ($(this).children().length == 1) {
                        $(this).css('border', '2px solid #707172');
                    }
                });
            });
            $(document).on('click', ".quiz_nxt", function (e) {
                var next_id = $(this).attr('next-id');
                check_req(next_id)
                if (self.que_req == 1) {
                    return false
                }
            });

            function check_req(next_id) {
                self.que_req = 0
                if ($('.que_show').length != 0) {
                    if (res[0].que_required == true) {
                        if ($('.question_box', ".que_show").find("input[type='button']").length == 0) {
                            change_que(next_id)
                        }
                    } else {
                        change_que(next_id)
                    }
                } else {
                    if (res[0].que_required == true) {
                        if ($('.question_box').find("input[type='button']").length != 0) {
                            $('#quiz_err_info').html('<div class="alert alert-danger">' + '<strong>Error!</strong> Answer is required ' + '</div>');
                            self.que_req = 1
                            return false
                        }
                    }
                }

            }
            $(document).on('click', ".quiz_finish", function (e) {
                if ($('.que_show').length != 0) {
                    if (res[0].que_required == true) {
                        if ($('.question_box', ".que_show").find("input[type='button']").length == 0) {
                        }
                        change_que(next_id)
                    }
                } else {
                    if (res[0].que_required == true) {
                        if ($('.question_box').find("input[type='button']").length == 0) {
                            if ($('#from_quiz').length != 0) {
                                $('#from_quiz').submit();
                            } else {
                                $('#from_quiz_dynamic').submit();
                            }
                        }
                        else {
                            $('#quiz_err_info').html('<div class="alert alert-danger">' + '<strong>Error!</strong> Answer is required ' + '</div>');
                            return false;
                        }
                    }
                    else {
                        if ($('#from_quiz').length != 0) {
                            $('#from_quiz').submit();
                        } else {
                            $('#from_quiz_dynamic').submit();
                        }
                    }
                }
            });

            function change_que(change_id) {
                $('#quiz_err_info').html('');
                var tmp_local_storage = JSON.parse(window.localStorage.getItem("quiz"));
                // tmp_local_storage.current_que_id = parseInt(change_id);
                window.localStorage.setItem("quiz", JSON.stringify(tmp_local_storage));
                var index_id = $('.que_show').attr('index-id');
                $("div[index-id='" + index_id + "']").addClass('que_hide').removeClass('que_show');
                $("div[index-id='" + change_id + "']").addClass('que_show').removeClass('que_hide');
                // for grid
                $("div[grid-index-id='" + index_id + "']").removeClass('que_active');
                $("div[grid-index-id='" + change_id + "']").addClass('que_active');
            }

        },
    });
    return publicWidget.registry.quiz_data;
});
