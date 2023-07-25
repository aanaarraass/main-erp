odoo.define('openeducat_quiz_match_images.openeducat_quiz_match_the_following_images', function (require) {
    'use strict';
    var core = require("web.core");
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var QWeb = core.qweb;
    var websiteRootData = require('website.root');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.quiz_match_images = publicWidget.Widget.extend({
        selector: '.quiz_start',
        events: {
            'change select': '_getData',
        },
        jsLibs: [
            '/openeducat_quiz_match_images/static/src/js/draganddrop.js',
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
            $('.match_following_images').each(function () {
                self.question_id = parseInt($('.quiz_nxt').val());
                ajax.jsonRpc('/following/images/data', 'call', {
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

                var mfi_drop_area = 'mfi_drop_area'+value.id

                var div = document.createElement('div');
                var div_id = (value.id);
                self.div_data = div_id;
                div.setAttribute("id", div_id);
                div.setAttribute("class", 'row');
                $('#quiz_question' + div_id).append(div);


                var question = document.createElement('div');
                question.setAttribute("class", "col-md-6 row question mx-0 border bg-white");
                $('#quiz_question' + self.question_id).append(question);
                $('#' + div_id).append(question);

                var answer = document.createElement('div');
                answer.setAttribute("class", "col-md-6 row answer mx-0 bg-info-light border");
                $('#quiz_question' + self.question_id).append(answer);
                $('#' + div_id).append(answer);



                var img_count = 1;
                var traitInfo = value.question_data;
                traitInfo.sort(() => Math.random() * (traitInfo + 1.5));
                traitInfo.forEach(function (question) {

                    var div = document.createElement('div');
                    div.setAttribute("id", question.id);
                    div.setAttribute("class", 'col-md-4 mfi_answer_box');
                    $(answer).append(div);

                    var div1 = document.createElement('div');
                    div1.setAttribute("class", 'mfi_drop_box '+mfi_drop_area);
                    $(div).append(div1);

                    var children_div = document.createElement('div');
                    children_div.setAttribute("id", '');
                    children_div.setAttribute("class", ' children_img_que ');
                    $(div1).append(children_div);

                    var image = document.createElement('img');
                    var image_data = question.default_answer;
                    image.setAttribute("class", "droppable_answer child_image")
                    $(image).attr("src", "data:image/*;base64," + image_data);
                    $(children_div).append(image);

                    var children_div = document.createElement('div');
                    children_div.setAttribute("id", '');
                    children_div.setAttribute("class", 'children_img_ans');
                    $(div1).append(children_div);

                    img_count += img_count;
                })
                var que_count = 1
                value.question_data.sort(() => Math.random() - 0.5)
                value.question_data.forEach(function (data) {
                    var div = document.createElement('div');
                    div.setAttribute("id", 'que_list' + que_count);
                    div.setAttribute("class", ' col-md-4 px-0 mfi_question_box');
                    $(question).append(div);

                    var div1 = document.createElement('div');
                    div1.setAttribute("class", 'mfi_drop_box '+mfi_drop_area);
                    $(div).append(div1);

                    var image = document.createElement('img');
                    var image_data = data.image;
                    image.setAttribute("class", "draggable_question child_image")
                    image.setAttribute("style", "z-index: 1;")
                    image.setAttribute("data", image_data)
                    image.setAttribute("id", "question" + que_count)
                    $(image).attr("src", "data:image/*;base64," + image_data);
                    $(div1).append(image);

                    var image = document.createElement('img');
                    image.setAttribute("class", "d-none child_image second_image")
                    image.setAttribute("style", "opacity: 0.5;")
                    $(image).attr("src", "data:image/*;base64," + image_data);
                    $(div1).append(image);
                    que_count = que_count + 1;
                });

                $('.mfi_answer_box').on('click', function () {
                    if ($(this).find('.mfi_question').length == 1) {
                        var question = $(this).find('.draggable_question');
                        let text = $(question).attr('id');
                        let result = text.replace("question", "");
                        var que_id = 'que_list' + result
                        var que = ($(this).parent().parent().find('#' + que_id).find('.'+mfi_drop_area));
                        var ans = $(this).find('.draggable_question')
                        $(ans).appendTo(que);
                        // $(this).find('.mfi_answer').removeClass('mfi_answer');
                        // $(this).find('.mfi_question').removeClass('mfi_question');

                        var id = $(this).attr('id');
                        var answerdata = {
                            'id': parseInt(id),
                            'answer': ''
                        }
                        ajax.jsonRpc('/quiz/match_images/answer/data', 'call', {
                            'answerdata': answerdata
                        });

                        removeClass();
                    }
                });

                $('.draggable_question').draggable({
                    revert: true,
                    placeholder: true,
                    scroll: true,
                    droptarget: ('.'+mfi_drop_area),
                    stop: function (ent, ui) { },
                    drop: function (evt, droptarget) {
                        $(droptarget).addClass("dropped");

                        if ($(droptarget).parent().find('.children_img_ans').length == 0) {
                            if ($(droptarget).children().length == 0) {
                                var id = $(this).parent().parent().parent().attr('id');

                                // $(this).parent().removeClass('mfi_answer');
                                // $(this).parent().parent().find('.children_img_que').removeClass('mfi_question');
                                $(this).appendTo(droptarget);

                                var answerdata = {
                                    'id': parseInt(id),
                                    'answer': ''
                                }
                                ajax.jsonRpc('/quiz/match_images/answer/data', 'call', {
                                    'answerdata': answerdata
                                });
                            }
                        } else {
                            if ($(droptarget).find('.child_image').length == 1) {
                                var temp = $(droptarget).parent().find('.children_img_ans')
                                // $(temp).addClass('mfi_answer');
                                // $(temp).parent().find('.children_img_que').addClass('mfi_question');
                                $(this).appendTo(temp);
                                var id = $(droptarget).parent().attr('id');
                                var ans = $(this).attr('data');
                                var answerdata = {
                                    'id': parseInt(id),
                                    'answer': ans
                                }
                                ajax.jsonRpc('/quiz/match_images/answer/data', 'call', {
                                    'answerdata': answerdata
                                });
                            }
                        }
                        removeClass();
                      
                    }
                });

            });
            function removeClass(){
                $( ".mfi_answer_box" ).each(function( index ) {
                    if($(this).find('.draggable_question').length == 1){
                        $(this).find('.children_img_que').addClass('mfi_question');
                        $(this).find('.children_img_ans').addClass('mfi_answer');

                        $(this).find('.mfi_drop_box').css('border','2px dashed rgb(0, 144, 240)')
                    }
                    else{
                        $(this).find('.mfi_answer').removeClass('mfi_answer');
                        $(this).find('.mfi_question').removeClass('mfi_question');
                        $(this).find('.mfi_drop_box').css('border','')
                    }
                  });
                $( ".mfi_question_box" ).each(function( index ) {
                    if($(this).find('.draggable_question').length == 0){
                        $(this).find('.second_image').removeClass('d-none')
                    }else{
                        $(this).find('.second_image').addClass('d-none')
                    }
                  });
            }
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
    return publicWidget.registry.quiz_match_images; 
});
