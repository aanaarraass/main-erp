odoo.define('openeducat_lms_interactive_video.material_detail_view_intractive_video', function (require) {
    'use strict';
    var core = require("web.core");
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var QWeb = core.qweb;
    var start_quiz = require('openeducat_quiz.quiz');
    var publicWidget = require('web.public.widget');
    publicWidget.registry.interactive_video = publicWidget.Widget.extend({

        events: {
            'click .quiz_finish ': '_quiz_finish',
            'click .iv-close-img-btn': '_closebtn',
            'click #iv-start': '_start_video',
        },
        xmlDependencies: [],
        selector: '#interactive_video_data',

        jsLibs: [
        ],

        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            var self = this;
            this._super.apply(this, arguments).then(function () {   
                self._getData();
            });

        },
        _getData: function () {
            var self = this;
            ajax.jsonRpc('/interactive/video', 'call', {
                video_id: parseInt($('#interactive_video_data').attr('class'))
            }).then(function (res) {
                self._getquizdata(res);
            });
        },
        _start_video: function () {
            this.video_play_paush.play();
            $('#iv-start').hide();
        },
        _quiz_finish: function () {
            var values = {}

            var data = $('.form-horizontal').find('.form-group').each(function () {
                if ($(this).find('input:checked').val()) {
                    var question = $(this).find('input:checked').val();
                    var answer = $(this).find('input:checked').attr('name');
                    values[answer] = question;
                }
                if ($(this).find('textarea').val()) {
                    var question = $(this).find('textarea').attr('name')
                    var answer = $(this).find('textarea').val()
                    values[answer] = question;
                }
                if ($(this).find('input').attr('type') == 'text') {
                    var question = $(this).find('input').val()
                    var answer = $(this).find('textarea').attr('name')
                    values[answer] = question;
                }
                if ($(this).find('textarea').attr('type') == 'textarea') {
                    var question = $(this).find('textarea').val()
                    var answer = $(this).find('textarea').attr('name')
                    values[answer] = question;
                }
            });
            var data = $('.form-horizontal').find('input').serializeArray().reduce(function (obj, item) {
                obj[item.name] = item.value;
                return obj;
            }, {});

            var quiz_data = Object.assign({}, values, data);
            ajax.jsonRpc('/interactive/video/quiz/finish', 'call', {
                quiz_data: quiz_data
            }).then(function (res) {
                var div = document.createElement('div')
                var div_data = 'iv-result' + $('#span_interactive_question').attr('value');
                div.setAttribute("id", div_data);
                div.setAttribute("class", "iv-quiz-result");
                div.innerHTML = res;
                $("#quiz_video_data").append(div);
            });
            $('.form-horizontal').remove();
        },
        _closebtn: function () {
            var self = this;
            $('.iv-question-show').hide();
            if ($("#video_quiz").css("display") != "none") {
                $('#video_quiz').hide();
                $('.form-horizontal').remove();
            }
            self.video_play_paush.play();
        },
        _getquizdata: function (res) {
            if (res) {
                var self = this;
                const player1 = document.querySelector('.player');
                self.video_play_paush = player1.querySelector('.viewer');
                var video_player = document.getElementById('v');
                var v_duration = video_player.duration;

                res.forEach(function (value) {
                    self.video_data = []
                    self.video_data.push(value.id)
                    $(".video_duration").append('<image class="iv-video-duration" id="vd_btn' + value.id + '" src="/openeducat_lms_interactive_video/static/src/img/img.jpeg"></image>');
                    var time = (((100 * value.time) / v_duration) + "%");
                    var btn_id = ("vd_btn" + value.id);
                    document.getElementById(btn_id).style.left = time;
                })

                video_player.ontimeupdate = function () { myFunction() };
                function myFunction() {
                    if ($('.pushable').css('display') == 'none') {
                        $('#video_quiz').hide();
                        $('.form-horizontal').remove();
                        $('.iv-quiz-result').hide();
                    }
                    $('.pushable').hide();
                    $('#iv-start').hide();
                    $('.player__controls').show();

                    res.forEach(function (value) {
                        var show = video_player.currentTime >= value.time && video_player.currentTime < value.time + 5;
                        if (show) {
                            var span = document.getElementById('span_interactive_question');
                            span.setAttribute("data", value.id);
                            span.setAttribute("value", value.quiz);
                            $('#span_interactive_question').text(value.question);
                            $('.pushable').show();
                            var div = document.getElementById("quiz_video_data");
                            div.setAttribute('class', value.quiz);
                        }
                        else {
                            $('#' + value.id).hide();
                        }
                    })

                    var video_btn = document.getElementById('id_pushable');
                    video_btn.onclick = function () { interactiveactive_que_btn() };
                    function interactiveactive_que_btn() {
                        var span = $('#span_interactive_question').attr('data');
                        var quiz_type = $("#" + span).attr('data');
                        if (quiz_type == 'description') {
                            var visible = $("#" + span).css("display");
                            if (visible == "none") {
                                $('.iv-question-show').hide();
                                $('#' + span).show();
                                self.video_play_paush.pause();
                            } else {
                                $('.iv-question-show').hide();
                                self.video_play_paush.play();
                            }
                        } else {
                            var visible = $("#video_quiz").css("display");
                            if (visible == "none") {
                                $('.iv-quiz-result').hide();
                                var result = 'iv-result' + $('#span_interactive_question').attr('value');
                                if ($('#' + result).length == 1) {
                                    $('#' + result).show();
                                } else {
                                    ajax.jsonRpc('/interactive/video/quiz', 'call', {
                                        video_id: $('.front').attr('value')
                                    }).then(function (res) {
                                        $("#quiz_video_data").append(res);
                                        $('.form-horizontal').replaceWith('<div class="form-horizontal">' + $('.form-horizontal').html() + '</div>');
                                        localStorage.clear('quiz');
                                        if ($('.match_following').length != 0) {
                                            var temp = new  publicWidget.registry.quiz_data(self);
                                            temp.appendTo(self.$el);
                                        }
                                        if ($('#drag_into_text_data').length != 0) {
                                            var drag_into_text = new publicWidget.registry.drag_into_text_data(self);
                                            drag_into_text.appendTo(self.$el);
                                        }
                                        if ($('#sort_paragraphs_data').length != 0) {
                                            var sort_paragraphs = new publicWidget.registry.quiz_sort_paragraph(self);
                                            sort_paragraphs.appendTo(self.$el);
                                        }
                                        start_quiz();
                                        $('.card').css('border', 'none');
                                    });
                                }
                                $('#video_quiz').show();
                                self.video_play_paush.pause();
                            }
                            else {
                                $('#video_quiz').hide();
                                $('.iv-quiz-result').hide();
                                $('.form-horizontal').remove();
                                self.video_play_paush.play();
                            }
                        }
                    }
                    // if(v_duration == video_player.currentTime) {}
                }
                const player = document.querySelector('.player');
                const video = player.querySelector('.viewer');
                const progress = player.querySelector('.progress');
                const progressBar = player.querySelector('.progress__filled');
                const toggle = player.querySelector('.toggle');
                const fullscreen = player.querySelector('.player__fullscreen');
                const skipButtons = player.querySelectorAll('[data-skip]');
                const ranges = player.querySelectorAll('.player__slider');

                function togglePlay() {
                    if (video.paused) {
                        $('.iv-question-show').hide();
                        if ($("#video_quiz").css("display") != "none") {
                            $('#video_quiz').hide();
                            $('.form-horizontal').remove();
                        }
                        video.play();
                        if ($(window).width() < 767) {
                            player.requestFullscreen();
                            fullscreen.textContent = '↙';
                            $('#v').css('margin-top', '60%');
                        }
                    } else {
                        video.pause();
                    }
                }

                function spaceBarTogglePlay(e) {
                    if (e.keyCode == 32) {
                        togglePlay();
                    }
                    if (e.keyCode == 102 || e.keyCode == 70) {
                        toggleFullscreen();
                    }
                }

                function updateButton() {
                    const icon = this.paused ? '►' : '❚❚';
                    toggle.textContent = icon;
                }

                function skip() {
                    video.currentTime += parseFloat(this.dataset.skip);
                }

                function handleRangeUpdate() {
                    const sliderValue = this.value;
                    this.setAttribute('title', sliderValue);
                    video[this.name] = sliderValue;
                }

                function handleProgress() {
                    const percent = (video.currentTime / video.duration) * 100;
                    progressBar.style.flexBasis = `${percent}%`;
                }

                function scrub(e) {
                    const scrubTime = (e.offsetX / progress.offsetWidth) * video.duration;
                    video.currentTime = scrubTime;
                }

                function toggleFullscreen() {
                    if (!document.fullscreenElement) {
                        player.requestFullscreen();
                        fullscreen.textContent = '↙';
                        $('#v').css('margin-top', '60%');

                    } else {
                        if (document.exitFullscreen) {
                            document.exitFullscreen();
                            $('#v').css('margin-top', '0%');
                            fullscreen.textContent = '️️️️↔️';

                        }
                    }
                }

                // event listeners
                video.addEventListener('click', togglePlay);
                video.addEventListener('play', updateButton);
                video.addEventListener('pause', updateButton);
                video.addEventListener('timeupdate', handleProgress);

                fullscreen.addEventListener('click', toggleFullscreen);
                video.addEventListener('dblclick', toggleFullscreen);

                toggle.addEventListener('click', togglePlay);
                document.addEventListener('keypress', spaceBarTogglePlay);
                skipButtons.forEach(button => button.addEventListener('click', skip));
                ranges.forEach(range => range.addEventListener('change', handleRangeUpdate));
                ranges.forEach(range => range.addEventListener('mousemove', handleRangeUpdate));

                let mousedown = false;
                progress.addEventListener('click', scrub);
                progress.addEventListener('mousemove', (e) => mousedown && scrub(e));
                progress.addEventListener('mousedown', () => mousedown = true);
                progress.addEventListener('mouseup', () => mousedown = false);
            }
        },
    });
    return publicWidget.registry.interactive_video;
});
