odoo.define('openeducat_dashboard_kpi.widgets', function(require) {
    "use strict";

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var basic_fields = require('web.basic_fields');
    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var session = require('web.session');
    var utils = require('web.utils');
    var config = require('web.config');
    var rpc = require('web.rpc');
    var GlobalFunction = require('openeducat_dashboard_kpi.FormattingFunction');
    var Qweb = core.qweb;
    var MAX_LEGEND_LENGTH = 25 * (Math.max(1, config.device.size_class));

    var ToDoListPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            this.state = {};
        },

        _render: function(){
            this.$el.empty();
            var rec = this.recordData;
            if (rec.type_of_element === 'to_do'){
                if (rec.to_do_list_count === '0'){
                     this.$el.append($('<div>').text("Add Values Into To-Do List."));
                }
                else{
                    this.RenderToDOListPreview();
                }
            }
        },
        RenderToDOListPreview : function(){
            var self = this;
            var field = this.recordData;
            var to_do_list_name =  field.name;
            var json_todo_list_data = JSON.parse(field.json_todo_list_data);
            var $ToDoListViewContainer = $(Qweb.render('to_do_list_view_container', {
                to_do_list_name: to_do_list_name,
                json_todo_list_data: json_todo_list_data,
            }));
            this.$el.append($ToDoListViewContainer);

        },

    });
    var KpiPreview = AbstractField.extend({

        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        file_type_word: {
            '/': 'jpg',
            'R': 'gif',
            'i': 'png',
            'P': 'svg+xml',
        },


        _render: function() {
            this.$el.empty();
            if (this.recordData.model_id && this.recordData.type_of_element === "kpi") {
                if (!this.recordData.ir_model_field_2) {
                    if (!(this.recordData.data_calculation_type === 'count')) {
                        if (this.recordData.store_field_data) {
                            this.KPIRender();
                        } else {
                            this.$el.append("Select a Record field ")
                        }
                    } else {
                        this.KPIRender();
                    }
                } else {
                    if (!(this.recordData.data_calculation_type === 'count') && !(this.recordData.data_calculation_type === 'count')) {
                        if (this.recordData.store_field_data_2 && this.recordData.store_field_data) {
                            this.KPIRender();
                        } else {
                            this.$el.append("Select a Record fields ")
                        }
                    } else if (!(this.recordData.data_calculation_type === 'count') && (this.recordData.data_calculation_type === 'count')) {
                        if (this.recordData.store_field_data_2) {
                            this.KPIRender();
                        } else {
                            this.$el.append("Select a Record field")
                        }
                    } else if ((this.recordData.data_calculation_type === 'count') && !(this.recordData.data_calculation_type === 'count')) {
                        if (this.recordData.store_field_data) {
                            this.KPIRender();
                        } else {
                            this.$el.append("Select a Record field")
                        }
                    } else {
                        this.KPIRender();
                    }
                }
            } else {
                this.$el.append("Select a Model first")
            }
        },
        Sum: function(count_1, count_2, item_info, field, target_1, $kpi_preview, kpi_data) {
            var self = this;
            var count = count_1 + count_2
            item_info['count'] = GlobalFunction.number_shorthand_function(count, 1);
            item_info['count_tooltip'] = count;
            item_info['target_enable'] = field.is_goal_enable;
            var color = (target_1 - count) > 0 ? "red" : "green";
            item_info.pre_arrow = (target_1 - count) > 0 ? "down" : "up";
            item_info['comparison'] = true;
            var target_deviation = (target_1 - count) > 0 ? Math.round(((target_1 - count) / target_1) * 100) : Math.round((Math.abs((target_1 - count)) / target_1) * 100);
            if (target_deviation !== Infinity) item_info.target_deviation = field_utils.format.integer(target_deviation) + "%";
            else {
                item_info.pre_arrow = false;
                item_info.target_deviation = target_deviation;
            }
            var target_progress_deviation = target_1 == 0 ? 0 : Math.round((count / target_1) * 100);
            item_info.target_progress_deviation = field_utils.format.integer(target_progress_deviation) + "%";
            $kpi_preview = $(Qweb.render("kpi_preview_template_2", item_info));
            $kpi_preview.find('.target_deviation').css({
                "color": color
            });
            if (this.recordData.target_view === "Progress Bar") {
                $kpi_preview.find('#progressbar').val(target_progress_deviation)
            }
            return $kpi_preview
        },
        Percentage: function(count_1, count_2, field, item_info, target_1, $kpi_preview) {
            var count = parseInt((count_1 / count_2) * 100);
            if (!count) count = 0;

            item_info['count'] = count ? field_utils.format.integer(count) + "%" : "0%";
            item_info['count_tooltip'] = count ? count + "%" : "0%";
            item_info.target_progress_deviation = item_info['count']
            target_1 = target_1 > 100 ? 100 : target_1;
            item_info.target = target_1 + "%";
            item_info.pre_arrow = (target_1 - count) > 0 ? "down" : "up";
            var color = (target_1 - count) > 0 ? "red" : "green";
            item_info['target_enable'] = field.is_goal_enable;
            item_info['comparison'] = false;
            item_info.target_deviation = item_info.target > 100 ? 100 : item_info.target;
            $kpi_preview = $(Qweb.render("kpi_preview_template_2", item_info));
            $kpi_preview.find('.target_deviation').css({
                "color": color
            });
            if (this.recordData.target_view === "Progress Bar") {
                $kpi_preview.find('#progressbar').val(count)
            }
            return $kpi_preview;
        },
        KPIRender: function() {
            var self = this;
            var field = this.recordData;
            var kpi_data = JSON.parse(field.kpi_data);
            var count_1 = kpi_data[0].record_data;
            var count_2 = kpi_data[1] ? kpi_data[1].record_data : undefined;
            var target_1 = kpi_data[0].target;
            var valid_date_selection = ['last_day', 'this_week', 'this_month', 'this_quarter', 'this_year'];
            var target_view = field.target_view,
                pre_view = field.prev_view;
            var rgba_background_color = GlobalFunction.convert_to_rgba_function(field.background_color);
            var font_color_rgba_format = GlobalFunction.convert_to_rgba_function(field.font_color)
            if (field.is_goal_enable) {
                var diffrence = 0.0
                diffrence = count_1 - target_1
                var acheive = diffrence >= 0 ? true : false;
                diffrence = Math.abs(diffrence);
                var deviation = Math.round((diffrence / target_1) * 100)
                if (deviation !== Infinity) deviation = deviation ? field_utils.format.integer(deviation) + '%' : 0 + '%';
            }
            if (field.previous_data_field && valid_date_selection.indexOf(field.date_domain_fields) >= 0) {
                var previous_period_data = kpi_data[0].previous_data_field;
                var pre_diffrence = (count_1 - previous_period_data);
                var pre_acheive = pre_diffrence > 0 ? true : false;
                pre_diffrence = Math.abs(pre_diffrence);
                var pre_deviation = previous_period_data ? field_utils.format.integer(parseInt((pre_diffrence / previous_period_data) * 100)) + '%' : "100%"
            }

            var rgba_icon_color = GlobalFunction.convert_to_rgba_function(field.default_icon_color)

            var item_info = {
                count_1: GlobalFunction.number_shorthand_function(kpi_data[0]['record_data'], 1),
                count_1_tooltip: kpi_data[0]['record_data'],
                count_2: kpi_data[1] ? String(kpi_data[1]['record_data']) : false,
                name: field.name ? field.name : field.model_id.data.display_name,
                target_progress_deviation: String(Math.round((count_1 / target_1) * 100)),
                selection_icon_field: field.selection_icon_field,
                default_icon: field.default_icon,
                icon_color: rgba_icon_color,
                target_deviation: deviation,
                target_arrow: acheive ? 'up' : 'down',
                enable_goal: field.is_goal_enable,
                previous_data_field: valid_date_selection.indexOf(field.date_domain_fields) >= 0 ? field.previous_data_field : false,
                target: GlobalFunction.number_shorthand_function(target_1, 1),
                previous_period_data: previous_period_data,
                pre_deviation: pre_deviation,
                pre_arrow: pre_acheive ? 'up' : 'down',
                target_view: field.target_view,
            }

            if (item_info.target_deviation === Infinity) item_info.target_arrow = false;
            item_info.target_progress_deviation = parseInt(item_info.target_progress_deviation) ? field_utils.format.integer(parseInt(item_info.target_progress_deviation)) : "0"
            if (field.icon) {
                if (!utils.is_bin_size(field.icon)) {
                    item_info['img_src'] = 'data:image/' + (self.file_type_word[field.icon[0]] || 'png') + ';base64,' + field.icon;
                } else {
                    item_info['img_src'] = session.url('/web/image', {
                        model: self.model,
                        id: JSON.stringify(self.res_id),
                        field: "icon",
                        unique: field_utils.format.datetime(self.recordData.__last_update).replace(/[^0-9]/g, ''),
                    });
                }
            }

            var $kpi_preview;
            if (!kpi_data[1]) {
                if (target_view === "Number" || !field.is_goal_enable) {
                    $kpi_preview = $(Qweb.render("kpi_preview_template", item_info));
                } else if (target_view === "Progress Bar" && field.is_goal_enable) {
                    $kpi_preview = $(Qweb.render("kpi_preview_template_3", item_info));
                    $kpi_preview.find('#progressbar').val(parseInt(item_info.target_progress_deviation));
                }

                if (field.is_goal_enable) {
                    if (acheive) {
                        $kpi_preview.find(".target_deviation").css({
                            "color": "green",
                        });
                    } else {
                        $kpi_preview.find(".target_deviation").css({
                            "color": "red",
                        });
                    }
                }
                if (field.previous_data_field && String(previous_period_data) && valid_date_selection.indexOf(field.date_domain_fields) >= 0) {
                    if (pre_acheive) {
                        $kpi_preview.find(".pre_deviation").css({
                            "color": "green",
                        });
                    } else {
                        $kpi_preview.find(".pre_deviation").css({
                            "color": "red",
                        });
                    }
                }
                if ($kpi_preview.find('.row').children().length !== 2) {
                    $kpi_preview.find('.row').children().addClass('text-center');
                }
            } else {
                switch (field.kpi_compare_field) {
                    case "None":
                        var count_tooltip = String(count_1) + "/" + String(count_2);
                        var count = String(GlobalFunction.number_shorthand_function(count_1, 1)) + "/" + String(GlobalFunction.number_shorthand_function(count_2, 1));
                        item_info['count'] = count;
                        item_info['count_tooltip'] = count_tooltip;
                        item_info['target_enable'] = false;
                        $kpi_preview = $(Qweb.render("kpi_preview_template_2", item_info));
                        break;
                    case "Sum":
                        $kpi_preview = self.Sum(count_1, count_2, item_info, field, target_1, $kpi_preview, kpi_data);
                        break;
                    case "Percentage":
                        $kpi_preview = self.Percentage(count_1, count_2, field, item_info, target_1, $kpi_preview);
                        break;
                    case "Ratio":
                        var gcd = self.get_gcd(Math.round(count_1), Math.round(count_2));
                        if (count_1 && count_2) {
                            item_info['count_tooltip'] = count_1 / gcd + ":" + count_2 / gcd;
                            item_info['count'] = GlobalFunction.number_shorthand_function(count_1 / gcd, 1) + ":" + GlobalFunction.number_shorthand_function(count_2 / gcd, 1);
                        } else {
                            item_info['count_tooltip'] = count_1 + ":" + count_2;
                            item_info['count'] = GlobalFunction.number_shorthand_function(count_1, 1) + ":" + GlobalFunction.number_shorthand_function(count_2, 1);
                        }
                        item_info['target_enable'] = false;
                        $kpi_preview = $(Qweb.render("kpi_preview_template_2", item_info));
                        break;
                }
            }
            $kpi_preview.css({
                "background-color": rgba_background_color,
                "color": font_color_rgba_format,
            });
            this.$el.append($kpi_preview);
        },

        get_gcd: function(a, b) {
            return (b == 0) ? a : this.get_gcd(b, a % b);
        },


    });
    var DashboardItemTheme = AbstractField.extend({

        supportedFieldTypes: ['char'],

        events: _.extend({}, AbstractField.prototype.events, {
            'click .dashboard_theme_input_container': 'dashboard_theme_input_container_click',
        }),

        _render: function() {
            var self = this;
            self.$el.empty();
            var $view = $(Qweb.render('dashboard_theme_view'));
            if (self.value) {
                $view.find("input[value='" + self.value + "']").prop("checked", true);
            }
            self.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.dashboard_theme_view_render').addClass('not_click');
            }
        },

        dashboard_theme_input_container_click: function(e) {
            var self = this;
            var $box = $(e.currentTarget).find(':input');
            if ($box.is(":checked")) {
                self.$el.find('.dashboard_theme_input').prop('checked', false)
                $box.prop("checked", true);
            } else {
                $box.prop("checked", false);
            }
            self._setValue($box[0].value);
        },
    });
    var ListViewPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            this.state = {};
        },

        _render: function() {
            this.$el.empty()
            var rec = this.recordData;
            if (rec.type_of_element === 'list_view') {
                if (rec.list_view_type == "ungrouped") {
                    if (rec.list_fields_data.count !== 0) {
                        this.RenderListView();
                    } else {
                        this.$el.append($('<div>').text("Select Fields to show in list view."));
                    }
                } else if (rec.list_view_type == "grouped") {
                    if (rec.list_data_grouping.count !== 0 && rec.group_chart_relation) {
                        if (rec.group_chart_field === 'relational_type' || rec.group_chart_field === 'selection' || rec.group_chart_field === 'other' || rec.group_chart_field === 'date_type' && rec.chart_group_field) {
                            this.RenderListView();
                        } else {
                            this.$el.append($('<div>').text("Select Group by Date to show list data."));
                        }

                    } else {
                        this.$el.append($('<div>').text("Select Fields and Group By to show in list view."));

                    }
                }
            }
        },

        RenderListView: function() {
            var self = this;
            var field = this.recordData;
            var list_view_name;
            var json_list_data = JSON.parse(field.json_list_data);
            var count = field.data_calculation_value;
            if (field.name) list_view_name = field.name;
            else if (field.model_name) list_view_name = field.model_id.data.display_name;
            else list_view_name = "Name";
            if (field.list_view_type === "ungrouped" && json_list_data) {
                var index_data = json_list_data.date_index;
                for (var i = 0; i < index_data.length; i++) {
                    for (var j = 0; j < json_list_data.data_rows.length; j++) {
                        var index = index_data[i]
                        var date = json_list_data.data_rows[j]["data"][index]
                        if (date) json_list_data.data_rows[j]["data"][index] = field_utils.format.datetime(moment(moment(date).utc(true)._d), {}, {
                            timezone: false
                        });
                        else json_list_data.data_rows[j]["data"][index] = "";
                    }
                }
            }

            if (field.json_list_data) {
                var data_rows = json_list_data.data_rows;
                for (var i = 0; i < json_list_data.data_rows.length; i++) {
                    for (var j = 0; j < json_list_data.data_rows[0]["data"].length; j++) {
                        if (typeof(json_list_data.data_rows[i].data[j]) === "number" || json_list_data.data_rows[i].data[j]) {
                            if (typeof(json_list_data.data_rows[i].data[j]) === "number") {
                                json_list_data.data_rows[i].data[j] = field_utils.format.float(json_list_data.data_rows[i].data[j], Float64Array)
                            }
                        } else {
                            json_list_data.data_rows[i].data[j] = "";
                        }
                    }
                }
            } else json_list_data = false;
            count = json_list_data && field.list_view_type === "ungrouped" ? count - json_list_data.data_rows.length : false;
            count = count ? count <=0 ? false : count : false;
            var $listViewContainer = $(Qweb.render('list_view_container', {
                list_view_name: list_view_name,
                json_list_data: json_list_data,
                count: count,
                layout: self.recordData.list_view_layout,
            }));
            if (!this.recordData.show_records === true) {
                $listViewContainer.find('#item_info').hide();
            }
            this.$el.append($listViewContainer);
        },
    });
    var WidgetToggle = AbstractField.extend({

        supportedFieldTypes: ['char'],

        events: _.extend({}, AbstractField.prototype.events, {
            'change .toggle_icon_input': 'toggle_icon_input_click',
        }),

        _render: function () {
            var self = this;
            self.$el.empty();


            var $view = $(Qweb.render('widget_toggle'));
            if (self.value) {
                $view.find("input[value='" + self.value + "']").prop("checked", true);
            }
            this.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.select_dashboard_item_toggle').addClass('not_click');
            }
        },

        toggle_icon_input_click: function (e) {
            var self = this;
            self._setValue(e.currentTarget.value);
        }
    });

    var WidgetToggleKPI = AbstractField.extend({

        supportedFieldTypes: ['char'],

        events: _.extend({}, AbstractField.prototype.events, {
            'change .toggle_icon_input': 'toggle_icon_input_click',
        }),

        _render: function () {
            var self = this;
            self.$el.empty();
            var $view = $(Qweb.render('kpi_type_selection_widget'));

            if (self.value) {
                $view.find("input[value='" + self.value + "']").prop("checked", true);
            }
            this.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.select_dashboard_item_toggle').addClass('not_click');
            }
        },
        toggle_icon_input_click: function (e) {
            var self = this;
            self._setValue(e.currentTarget.value);
        }
    });

    var WidgetToggleKpiTarget = AbstractField.extend({
        supportedFieldTypes: ['char'],

        events: _.extend({}, AbstractField.prototype.events, {
            'change .toggle_icon_input': 'toggle_icon_input_click',
        }),

        _render: function () {
            var self = this;
            self.$el.empty();


            var $view = $(Qweb.render('widget_toggle_kpi_target_view'));
            if (self.value) {
                $view.find("input[value='" + self.value + "']").prop("checked", true);
            }
            this.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.select_dashboard_item_toggle').addClass('not_click');
            }
        },

        toggle_icon_input_click: function (e) {
            var self = this;
            self._setValue(e.currentTarget.value);
        }
    });
    var ProItemPreview = AbstractField.extend({
        supportedFieldTypes: ['integer'],

        file_type_word: {
            '/': 'jpg',
            'R': 'gif',
            'i': 'png',
            'P': 'svg+xml',
        },

        dark_color_generator: function(color, opacity, percent) {
            var self = this;
            var num = parseInt(color.slice(1), 16),
                amt = Math.round(2.55 * percent),
                R = (num >> 16) + amt,
                G = (num >> 8 & 0x00FF) + amt,
                B = (num & 0x0000FF) + amt;
            return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 + (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1) + "," + opacity;
        },

        _render: function() {
            var self = this;
            var field = self.recordData;
            var $val;
            var item_info;
            var rgba_background_color, font_color_rgba_format, rgba_icon_color;
            self.$el.empty();
            rgba_background_color = GlobalFunction.convert_to_rgba_function(field.background_color)
            font_color_rgba_format = GlobalFunction.convert_to_rgba_function(field.font_color)
            rgba_icon_color = GlobalFunction.convert_to_rgba_function(field.default_icon_color)
            item_info = {
                name: field.name,
                count: GlobalFunction.number_shorthand_function(field.data_calculation_value, 1),
                selection_icon_field: field.selection_icon_field,
                default_icon: field.default_icon,
                icon_color: rgba_icon_color,
                count_tooltip: field.data_calculation_value,
            }
            if (field.icon) {

                if (!utils.is_bin_size(field.icon)) {
                    item_info['img_src'] = 'data:image/' + (self.file_type_word[field.icon[0]] || 'png') + ';base64,' + field.icon;
                } else {
                    item_info['img_src'] = session.url('/web/image', {
                        model: self.model,
                        id: JSON.stringify(self.res_id),
                        field: "icon",
                        unique: field_utils.format.datetime(self.recordData.__last_update).replace(/[^0-9]/g, ''),
                    });
                }

            }
            if (!field.name) {
                if (field.model_name) {
                    item_info['name'] = field.model_id.data.display_name;
                } else {
                    item_info['name'] = "Name";
                }
            }


            switch (field.layout) {
                case 'layout1':
                    $val = $(Qweb.render('database_list_layout1', item_info));
                    $val.css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format
                    });
                    break;

                case 'layout2':
                    $val = $(Qweb.render('dashboard_list_layout2', item_info));
                    var rgba_dark_background_color_l2 = GlobalFunction.convert_to_rgba_function(self.dark_color_generator(field.background_color.split(',')[0], field.background_color.split(',')[1], -10));
                    $val.find('.dashboard_icon_layout_2').css({
                        "background-color": rgba_dark_background_color_l2,
                    });
                    $val.css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format
                    });
                    break;

                case 'layout3':
                    $val = $(Qweb.render('db_list_preview_layout3', item_info));
                    $val.css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format
                    });
                    break;

                case 'layout4':
                    $val = $(Qweb.render('dashboarb_list_layout_4', item_info));
                    $val.find('.dashboard_icon_layout_4').css({
                        "background-color": rgba_background_color,
                    });
                    $val.find('.dashboard_item_preview_customize').css({
                        "color": rgba_background_color,
                    });
                    $val.find('.dashboard_item_preview_delete').css({
                        "color": rgba_background_color,
                    });
                    $val.css({
                        "border-color": rgba_background_color,
                        "color": font_color_rgba_format
                    });
                    break;

                case 'layout5':
                    $val = $(Qweb.render('dashboard_list_layout5', item_info));
                    $val.css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format
                    });
                    break;

                case 'layout6':
                    $val = $(Qweb.render('dashboard_list_preview_layout_6', item_info));
                    $val.css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format
                    });

                    break;

                case 'state_layout_1':
                    $val = $(Qweb.render('state_list_preview_layout',item_info));
                    $val.css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format,
                    });

                    break;

                case 'state_layout_2':
                    $val = $(Qweb.render('state_list_preview_layout_1', item_info));
                    $val.find('.side_bar_div').css({
                        "background-color": rgba_background_color,
                        "color": font_color_rgba_format,
                    });
                    $val.find('.dashboard_element_info_layout_3').css({
                        "color":font_color_rgba_format
                    })
                    break;

                default:
                    $val = $(Qweb.render('db_list_preview'));
                    break;

            }

            self.$el.append($val);
        },

    });
    var ImageWidgetPro = basic_fields.FieldBinaryImage.extend({

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            this.SelectedIcon = false;
            this.icon_set = ['home', 'check','times', 'clock-o', 'question', 'car', 'calendar', 'calendar-times-o', 'bar-chart', 'commenting-o', 'star-half-o', 'address-book-o', 'tachometer', 'search', 'money', 'line-chart', 'area-chart', 'pie-chart', 'check-square-o', 'users', 'shopping-cart', 'truck', 'user-circle-o', 'user-plus', 'sun-o', 'paper-plane', 'rss', 'gears', 'book'];
        },

        template: 'DashboardFieldBinaryImage',

        events: _.extend({}, basic_fields.FieldBinaryImage.prototype.events, {
            'click .icon_container_list': 'icon_container_list',
            'click .image_widget_icon_container': 'image_widget_icon_container',
            'click .icon_container_open_button': 'icon_container_open_button',
            'click .fa_icon_search': 'fa_icon_search',
            'keyup .modal_icon_input': 'modal_icon_input_enter',
        }),

        _render: function() {
            var self = this;
            var url = this.placeholder;
            if (self.value) {
                self.$('> img').remove();
                self.$('> span').remove();
                $('<span>').addClass('fa fa-' + self.recordData.default_icon + ' fa-5x').appendTo(self.$el).css('color', 'black');
            } else {
                var $img = $(Qweb.render("FieldBinaryImage-img", {
                    widget: this,
                    url: url
                }));
                self.$('> img').remove();
                self.$('> span').remove();
                self.$el.prepend($img);
            }

            var $icon_container_modal = $(Qweb.render('icon_container_modal_template', {
                fa_icons_set: self.icon_set
            }));

            $icon_container_modal.prependTo(self.$el);
        },

        image_widget_icon_container: function(e) {
            $('#icon_container_modal_id').modal({
                show: true,
            });

        },


        icon_container_list: function(e) {
            var self = this;
            self.SelectedIcon = $(e.currentTarget).find('span').attr('id').split('.')[1]
            _.each($('.icon_container_list'), function(selected_icon) {
                $(selected_icon).removeClass('icon_selected');
            });

            $(e.currentTarget).addClass('icon_selected')
            $('.icon_container_open_button').show()
        },

        icon_container_open_button: function(e) {
            var self = this;
            self._setValue(self.SelectedIcon);
        },

        fa_icon_search: function(e) {
            var self = this
            self.$el.find('.fa_search_icon').remove()
            var fa_icon_name = self.$el.find('.modal_icon_input')[0].value
            if (fa_icon_name.slice(0, 3) === "fa-") {
                fa_icon_name = fa_icon_name.slice(3)
            }
            var fa_icon_render = $('<div>').addClass('icon_container_list fa_search_icon')
            $('<span>').attr('id', '.' + fa_icon_name.toLocaleLowerCase()).addClass("fa fa-" + fa_icon_name.toLocaleLowerCase() + " fa-4x").appendTo($(fa_icon_render))
            $(fa_icon_render).appendTo(self.$el.find('.icon_container_grid_view'))
        },

        modal_icon_input_enter: function(e) {
            var self = this
            if (e.keyCode == 13) {
                self.$el.find('.fa_icon_search').click()
            }
        },
    });
    var ProColorPicker = AbstractField.extend({

        supportedFieldTypes: ['char'],

        events: _.extend({}, AbstractField.prototype.events, {
            'change.spectrum .dashboard_pro_color_picker': '_OnColorChange',
            'change .color_opacity': '_OnOpacityChange',
            'input .color_opacity': '_OnOpacityInput'
        }),

        jsLibs: [
            '/openeducat_dashboard_kpi/static/lib/js/spectrum.js'
        ],
        cssLibs: [
            '/openeducat_dashboard_kpi/static/lib/css/spectrum.css',
        ],

        _render: function() {
            this.$el.empty();
            var color_value = '#376CAE';
            var color_opacity = '0.99';
            if (this.value) {
                color_value = this.value.split(',')[0];
                color_opacity = this.value.split(',')[1];
            };
            var $view = $(Qweb.render('dashboard_pro_color_picker_opacity_view', {
                color_value: color_value,
                color_opacity: color_opacity
            }));

            this.$el.append($view)

            this.$el.find(".dashboard_pro_color_picker").spectrum({
                color: color_value,
                showInput: true,
                hideAfterPaletteSelect: true,

                clickoutFiresChange: true,
                showInitial: true,
                preferredFormat: "rgb",
            });

            if (this.mode === 'readonly') {
                this.$el.find('.dashboard_pro_color_picker').addClass('not_click');
                this.$el.find('.color_opacity').addClass('not_click');
                this.$el.find('.dashboard_pro_color_picker').spectrum("disable");
            } else {
                this.$el.find('.dashboard_pro_color_picker').spectrum("enable");
            }
        },
        _OnColorChange: function(e, tinycolor) {
            this._setValue(tinycolor.toHexString().concat("," + this.value.split(',')[1]));
        },

        _OnOpacityChange: function(event) {
            this._setValue(this.value.split(',')[0].concat("," + event.currentTarget.value));
        },

        _OnOpacityInput: function(event) {
            var self = this;
            var color;
            if (self.name == "background_color") {
                color = $('.dashboard_element_preview_color_picker').css("background-color")
                $('.dashboard_element_preview_color_picker').css("background-color", self.get_color_opacity_value(color, event.currentTarget.value))

                color = $('.dashboard_element_preview_layout_2').css("background-color")
                $('.dashboard_element_preview_layout_2').css("background-color", self.get_color_opacity_value(color, event.currentTarget.value))

            } else if (self.name == "default_icon_color") {
                color = $('.dashboard_icon_color_picker > span').css('color')
                $('.dashboard_icon_color_picker > span').css('color', self.get_color_opacity_value(color, event.currentTarget.value))
            } else if (self.name == "font_color") {
                color = $('.dashboard_element_preview').css("color")
                color = $('.dashboard_element_preview').css("color", self.get_color_opacity_value(color, event.currentTarget.value))
            }
        },

        get_color_opacity_value: function(color, val) {
            if (color) {
                return color.replace(color.split(',')[3], val + ")");
            } else {
                return false;
            }
        },


    });
    var GraphPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        jsLibs: [
            '/openeducat_dashboard_kpi/static/lib/js/Chart.bundle.min.js',
            '/openeducat_dashboard_kpi/static/lib/js/chartjs-plugin-datalabels.js'
        ],
        cssLibs: [
            '/openeducat_dashboard_kpi/static/lib/css/Chart.min.css'
        ],

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
        },

        start: function() {
            var self = this;
            self.default_chart_view();
            core.bus.on("DOM_updated", this, function() {
                if (self.shouldRenderChart && $.find('#MyChart').length > 0) self.renderChart();
            });
            Chart.plugins.unregister(ChartDataLabels);
            return this._super();
        },

        default_chart_view: function() {
            Chart.plugins.register({
                beforeDraw: function(c) {
                    var ctx = c.chart.ctx;
                    ctx.fillStyle = "white";
                    ctx.fillRect(0, 0, c.chart.width, c.chart.height);
                }
            });
            Chart.plugins.register({
                afterDraw: function(chart) {
                    if (chart.data.labels.length === 0) {
                        var ctx = chart.chart.ctx;
                        var width = chart.chart.width;
                        var height = chart.chart.height
                        chart.clear();

                        ctx.save();
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.font = "3rem 'Lucida Grande'";
                        ctx.fillText('No data available', width / 2, height / 2);
                        ctx.restore();
                    }
                }
            });

            Chart.Legend.prototype.afterFit = function() {
                var chart_type = this.chart.config.type;
                if (chart_type === "pie" || chart_type === "doughnut") {
                    this.height = this.height;
                } else {
                    this.height = this.height + 20;
                };
            }
        },

        _render: function() {
            this.$el.empty()
            if (this.recordData.type_of_element !== 'tile' && this.recordData.type_of_element !== 'kpi' && this.recordData.type_of_element !== 'list_view') {
                if (this.recordData.model_id) {
                    if (this.recordData.group_chart_field == 'date_type' && !this.recordData.chart_group_field) {
                        return this.$el.append($('<div>').text("Select Group by date to create chart based on date groupby"));
                    } else if (this.recordData.data_calculation_type_chart === "count" && !this.recordData.group_chart_relation) {
                        this.$el.append($('<div>').text("Select Group By to create chart view"));
                    } else if (this.recordData.data_calculation_type_chart !== "count" && (this.recordData.chart_data_calculation_field.count === 0 || !this.recordData.group_chart_relation)) {
                        this.$el.append($('<div>').text("Select Measure and Group By to create chart view"));
                    } else if (!this.recordData.data_calculation_type_chart) {
                        this.$el.append($('<div>').text("Select Chart Data Count Type"));
                    } else {
                        this._getChartData();
                    }
                } else {
                    this.$el.append($('<div>').text("Select a Model first."));
                }

            }

        },

        _getChartData: function() {
            var self = this;
            self.shouldRenderChart = true;
            var field = this.recordData;
            var chart_name;
            if (field.name) chart_name = field.name;
            else if (field.model_name) chart_name = field.model_id.data.display_name;
            else chart_name = "Name";

            this.chart_type = this.recordData.type_of_element.split('_')[0];
            this.chart_data = JSON.parse(this.recordData.chart_data);

            var $chartContainer = $(Qweb.render('chart_form_view_container', {
                chart_name: chart_name
            }));
            this.$el.append($chartContainer);

            switch (this.chart_type) {
                case "pie":
                case "doughnut":
                case "polarArea":
                    this.chart_family = "circle";
                    break;
                case "bar":
                case "horizontalBar":
                case "line":
                case "area":
                    this.chart_family = "square"
                    break;
                default:
                    this.chart_family = "none";
                    break;
            }

            if (this.chart_family === "circle") {
                if (this.chart_data && this.chart_data['labels'].length > 30) {
                    this.$el.find(".card-body").empty().append($("<div style='font-size:20px;'>Too many records for selected Chart Type. Consider using <strong>Domain</strong> to filter records or <strong>Record Limit</strong> to limit the no of records under <strong>30.</strong>"));
                    return;
                }
            }
            if ($.find('#MyChart').length > 0) {
                this.renderChart();
            }
        },

        renderChart: function() {
            var self = this;
            if (this.recordData.chart_data_calculation_field_2.count && this.recordData.type_of_element === 'bar_chart') {
                var self = this;
                var scales = {}
                scales.yAxes = [{
                        type: "linear",
                        display: true,
                        position: "left",
                        id: "y-axis-0",
                        gridLines: {
                            display: true
                        },
                        labels: {
                            show: true,
                        }
                    },
                    {
                        type: "linear",
                        display: true,
                        position: "right",
                        id: "y-axis-1",
                        labels: {
                            show: true,
                        },
                        ticks: {
                            beginAtZero: true,
                            callback: function(value, index, values) {
                                var selection = self.chart_data.selection;
                                if (selection === 'monetary') {
                                    var currency_id = self.chart_data.currency;
                                    var data = GlobalFunction.number_shorthand_function(value, 1);
                                    data = GlobalFunction.currency_monetary_function(data, currency_id);
                                    return data;
                                } else if (selection === 'custom') {
                                    var field = self.chart_data.field;
                                    return GlobalFunction.number_shorthand_function(value, 1) + ' ' + field;
                                } else {
                                    return GlobalFunction.number_shorthand_function(value, 1);
                                }
                            },
                        }
                    }
                ]

            }
            var chart_plugin = [];
//            if (this.recordData.show_data_value) {
                chart_plugin.push(ChartDataLabels);
//            }
            this.MyChart = new Chart($.find('#MyChart')[0], {
                type: this.chart_type === "area" ? "line" : this.chart_type,
                plugins: chart_plugin,
                data: {
                    labels: this.chart_data['labels'],
                    datasets: this.chart_data.datasets,
                },
                options: {
                    maintainAspectRatio: false,
                    animation: {
                        easing: 'easeInQuad',
                    },

                    layout: {
                        padding: {
                            bottom: 0,
                        }
                    },
                    scales: scales,
                    plugins: {
                        datalabels: {
                            backgroundColor: function(context) {
                                return context.dataset.backgroundColor;
                            },
                            borderRadius: 4,
                            color: 'white',
                            font: {
                                weight: 'bold'
                            },
                            anchor: 'center',
                            display: 'auto',
                            clamp: true,
                            formatter: function(value, ctx) {
                                let sum = 0;
                                let dataArr = ctx.dataset.data;
                                dataArr.map(data => {
                                    sum += data;
                                });
                                let percentage = sum === 0 ? 0 + "%" : (value * 100 / sum).toFixed(2) + "%";
                                return percentage;
                            },
                        },
                    },

                }
            });
            if (this.chart_data && this.chart_data["datasets"].length > 0) {
                self.ChartColors(this.recordData.chart_theme_selection, this.MyChart, this.chart_type, this.chart_family, this.recordData.show_data_value);
            }
        },

        HideFunction: function(options, recordData, ChartFamily, chartType) {
            return options;
        },

        ChartColors: function(palette, MyChart, ChartType, ChartFamily, show_data_value) {
            var self = this;
            var currentPalette = "cool";
            if (!palette) palette = currentPalette;
            currentPalette = palette;

            /*Gradients
              The keys are percentage and the values are the color in a rgba format.
              You can have as many "color stops" (%) as you like.
              0% and 100% is not optional.*/
            var gradient;
            switch (palette) {
                case 'cool':
                    gradient = {
                        0: [255, 255, 255, 1],
                        20: [220, 237, 200, 1],
                        45: [66, 179, 213, 1],
                        65: [26, 39, 62, 1],
                        100: [0, 0, 0, 1]
                    };
                    break;
                case 'warm':
                    gradient = {
                        0: [255, 255, 255, 1],
                        20: [254, 235, 101, 1],
                        45: [228, 82, 27, 1],
                        65: [77, 52, 47, 1],
                        100: [0, 0, 0, 1]
                    };
                    break;
                case 'neon':
                    gradient = {
                        0: [255, 255, 255, 1],
                        20: [255, 236, 179, 1],
                        45: [232, 82, 133, 1],
                        65: [106, 27, 154, 1],
                        100: [0, 0, 0, 1]
                    };
                    break;

                case 'default':
                    var color_set = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600', '#8a79fd', '#b1b5be', '#1c425c', '#8c2620', '#71ecef', '#0b4295', '#f2e6ce', '#1379e7']
            }

            var chartType = MyChart.config.type;

            switch (chartType) {
                case "pie":
                case "doughnut":
                case "polarArea":
                    var datasets = MyChart.config.data.datasets[0];
                    var setsCount = datasets.data.length;
                    break;
                case "bar":
                case "horizontalBar":
                case "line":
                    var datasets = MyChart.config.data.datasets;
                    var setsCount = datasets.length;
                    break;
            }

            var chartColors = [];

            if (palette !== "default") {
                var gradientKeys = Object.keys(gradient);
                gradientKeys.sort(function(a, b) {
                    return +a - +b;
                });
                for (var i = 0; i < setsCount; i++) {
                    var gradientIndex = (i + 1) * (100 / (setsCount + 1));
                    for (var j = 0; j < gradientKeys.length; j++) {
                        var gradientKey = gradientKeys[j];
                        if (gradientIndex === +gradientKey) {
                            chartColors[i] = 'rgba(' + gradient[gradientKey].toString() + ')';
                            break;
                        } else if (gradientIndex < +gradientKey) {
                            var prevKey = gradientKeys[j - 1];
                            var gradientPartIndex = (gradientIndex - prevKey) / (gradientKey - prevKey);
                            var color = [];
                            for (var k = 0; k < 4; k++) {
                                color[k] = gradient[prevKey][k] - ((gradient[prevKey][k] - gradient[gradientKey][k]) * gradientPartIndex);
                                if (k < 3) color[k] = Math.round(color[k]);
                            }
                            chartColors[i] = 'rgba(' + color.toString() + ')';
                            break;
                        }
                    }
                }
            } else {
                for (var i = 0, counter = 0; i < setsCount; i++, counter++) {
                    if (counter >= color_set.length) counter = 0;

                    chartColors.push(color_set[counter]);
                }

            }

            var datasets = MyChart.config.data.datasets;
            var options = MyChart.config.options;

            options.legend.labels.usePointStyle = true;
            if (ChartFamily == "circle") {
                if (show_data_value) {
                    options.legend.position = 'top';
                    options.layout.padding.top = 10;
                    options.layout.padding.bottom = 20;
                } else {
                    options.legend.position = 'bottom';
                }

                options = this.HideFunction(options, this.recordData, ChartFamily, chartType);

                options.plugins.datalabels.align = 'center';
                options.plugins.datalabels.anchor = 'end';
                options.plugins.datalabels.borderColor = 'white';
                options.plugins.datalabels.borderRadius = 25;
                options.plugins.datalabels.borderWidth = 2;
                options.plugins.datalabels.clamp = true;
                options.plugins.datalabels.clip = false;

                options.tooltips.callbacks = {
                    title: function(tooltipItem, data) {
                        var new_self = self;
                        var k_amount = data.datasets[tooltipItem[0].datasetIndex]['data'][tooltipItem[0].index];
                        var selection = new_self.chart_data.selection;
                        if (selection === 'monetary') {
                            var currency_id = new_self.chart_data.currency;
                            k_amount = GlobalFunction.currency_monetary_function(k_amount, currency_id);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount
                        } else if (selection === 'custom') {
                            var field = new_self.chart_data.field;
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount + " " + field;
                        } else {
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount
                        }
                    },
                    label: function(tooltipItem, data) {
                        return data.labels[tooltipItem.index];
                    },

                }
                for (var i = 0; i < datasets.length; i++) {
                    datasets[i].backgroundColor = chartColors;
                    datasets[i].borderColor = "rgba(255,255,255,1)";
                }
                if (this.recordData.semi_circle_chart && (chartType === "pie" || chartType === "doughnut")) {
                    options.rotation = 1 * Math.PI;
                    options.circumference = 1 * Math.PI;
                }
            } else if (ChartFamily == "square") {
                options = this.HideFunction(options, this.recordData, ChartFamily, chartType);

                options.scales.xAxes[0].gridLines.display = false;
                options.scales.yAxes[0].ticks.beginAtZero = true;
                options.plugins.datalabels.align = 'end';

                options.plugins.datalabels.formatter = function(value, ctx) {
                    var new_self = self;
                    var selection = new_self.chart_data.selection;
                    if (selection === 'monetary') {
                        var currency_id = new_self.chart_data.currency;
                        var data = GlobalFunction.number_shorthand_function(value, 1);
                        data = GlobalFunction.currency_monetary_function(data, currency_id);
                        return data;
                    } else if (selection === 'custom') {
                        var field = new_self.chart_data.field;
                        return GlobalFunction.number_shorthand_function(value, 1) + ' ' + field;
                    } else {
                        return GlobalFunction.number_shorthand_function(value, 1);
                    }
                };

                if (chartType === "line") {
                    options.plugins.datalabels.backgroundColor = function(context) {
                        return context.dataset.borderColor;
                    };
                }


                if (chartType === "horizontalBar") {
                    options.scales.xAxes[0].ticks.callback = function(value, index, values) {
                        var new_self = self;
                        var selection = new_self.chart_data.selection;
                        if (selection === 'monetary') {
                            var currency_id = new_self.chart_data.currency;
                            var data = GlobalFunction.number_shorthand_function(value, 1);
                            data = GlobalFunction.currency_monetary_function(data, currency_id);
                            return data;
                        } else if (selection === 'custom') {
                            var field = new_self.chart_data.field;
                            return GlobalFunction.number_shorthand_function(value, 1) + ' ' + field;
                        } else {
                            return GlobalFunction.number_shorthand_function(value, 1);
                        }
                    }
                    options.scales.xAxes[0].ticks.beginAtZero = true;
                } else {
                    options.scales.yAxes[0].ticks.callback = function(value, index, values) {
                        var new_self = self;
                        var selection = new_self.chart_data.selection;
                        if (selection === 'monetary') {
                            var currency_id = new_self.chart_data.currency;
                            var data = GlobalFunction.number_shorthand_function(value, 1);
                            data = GlobalFunction.currency_monetary_function(data, currency_id);
                            return data;
                        } else if (selection === 'custom') {
                            var field = new_self.chart_data.field;
                            return GlobalFunction.number_shorthand_function(value, 1) + ' ' + field;
                        } else {
                            return GlobalFunction.number_shorthand_function(value, 1);
                        }
                    }
                }
                options.tooltips.callbacks = {
                    label: function(tooltipItem, data) {
                        var new_self = self;
                        var k_amount = data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem.index];
                        var selection = new_self.chart_data.selection;
                        if (selection === 'monetary') {
                            var currency_id = new_self.chart_data.currency;
                            k_amount = GlobalFunction.currency_monetary_function(k_amount, currency_id);
                            return data.datasets[tooltipItem.datasetIndex]['label'] + " : " + k_amount
                        } else if (selection === 'custom') {
                            var field = new_self.chart_data.field;
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem.datasetIndex]['label'] + " : " + k_amount + " " + field;
                        } else {
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem.datasetIndex]['label'] + " : " + k_amount
                        }
                    }
                }

                for (var i = 0; i < datasets.length; i++) {
                    switch (ChartType) {
                        case "bar":
                        case "horizontalBar":
                            if (datasets[i].type && datasets[i].type == "line") {
                                datasets[i].borderColor = chartColors[i];
                                datasets[i].backgroundColor = "rgba(255,255,255,0)";
                                datasets[i]['datalabels'] = {
                                    backgroundColor: chartColors[i],
                                }

                            } else {
                                datasets[i].backgroundColor = chartColors[i];
                                datasets[i].borderColor = "rgba(255,255,255,0)";
                                options.scales.xAxes[0].stacked = this.recordData.bar_chart_stacked;
                                options.scales.yAxes[0].stacked = this.recordData.bar_chart_stacked;
                            }
                            break;
                        case "line":
                            datasets[i].borderColor = chartColors[i];
                            datasets[i].backgroundColor = "rgba(255,255,255,0)";
                            break;
                        case "area":
                            datasets[i].borderColor = chartColors[i];
                            break;
                    }
                }

            }
            MyChart.update();
            if (this.$el.find('canvas').height() < 250) {
                this.$el.find('canvas').height(250);
            }
        },


    });
    var DashboardAddTextWidget = AbstractField.extend({
        supportedFieldTypes: ['integer'],

        resetOnAnyFieldChange: true,

        _render: function(){
            var self = this;
            var add_text_info;
            var field = self.recordData;
            var $val;
            var rgba_background_color = GlobalFunction.convert_to_rgba_function(field.background_color)
            var font_style_selection = field.add_text_font_style;
            var font_color_rgba_format = GlobalFunction.convert_to_rgba_function(field.font_color)
            var add_text_align_field = field.add_text_align;
            var default_icon_color_rgba_format = GlobalFunction.convert_to_rgba_function(field.default_icon_color);
            self.$el.empty();
            if(field.add_text_font_style == 'custom'){
                var add_text_bold = (field.add_text_custom_bold == true) ? 'bold' : 'normal';
                var add_text_italic = (field.add_text_custom_italic == true) ? 'italic' : 'normal';
                var add_text_font_size = field.add_text_custom_font_size;
                add_text_info = {
                    name: field.name,
                    default_icon: field.default_icon,
                    main_content : field.add_text_main_content,
                    background_color : rgba_background_color,
                    default_icon_color_rgba_format: default_icon_color_rgba_format,
                    font_color : font_color_rgba_format,
                    font_style_selection : font_style_selection,
                    add_text_bold : add_text_bold,
                    add_text_italic : add_text_italic,
                    add_text_font_size : add_text_font_size,
                    add_text_align_field : add_text_align_field
                }
            }else{
                add_text_info = {
                    name: field.name,
                    default_icon: field.default_icon,
                    default_icon_color_rgba_format: default_icon_color_rgba_format,
                    main_content : field.add_text_main_content,
                    background_color : rgba_background_color,
                    font_color : font_color_rgba_format,
                    font_style_selection : font_style_selection,
                    add_text_align_field : add_text_align_field
                }
            }
                $val = $(Qweb.render('add_text_element_preview',add_text_info));
            self.$el.append($val);
        },
    });
    var DashboardAddLinkWidget = AbstractField.extend({
        supportedFieldTypes: ['integer'],

        resetOnAnyFieldChange: true,

        _render: function(){
            var self = this;
            var add_link_info;
            var field = self.recordData;
            var $val;
            var rgba_background_color = GlobalFunction.convert_to_rgba_function(field.background_color);
            var font_color_rgba_format = GlobalFunction.convert_to_rgba_function(field.font_color);
            var add_link_title = field.add_link_title;
            var add_link_title_name = field.name;
            self.$el.empty();
            add_link_info = {
                add_link_content : field.add_link_content,
                background_color : rgba_background_color,
                font_color : font_color_rgba_format,
                add_link_title : add_link_title,
                add_link_title_name : add_link_title_name
            }
            $val = $(Qweb.render('add_link_element_preview',add_link_info));
            self.$el.append($val);
        }
    });
    registry.add('dashboard_add_link_widget', DashboardAddLinkWidget);
    registry.add('dashboard_add_text_widget', DashboardAddTextWidget);
    registry.add('dashboard_pro_item_theme', DashboardItemTheme);
    registry.add('widget_toggle', WidgetToggle);
    registry.add('kpi_type_selection_widget', WidgetToggleKPI);
    registry.add('widget_toggle_kpi_target', WidgetToggleKpiTarget);
    registry.add('dashboard_pro_kpi_preview', KpiPreview);
    registry.add('dashboard_pro_list_view_preview', ListViewPreview);
    registry.add('dashboard_pro_item_preview', ProItemPreview);
    registry.add('image_widget_pro', ImageWidgetPro);
    registry.add('dashboard_pro_color_picker', ProColorPicker);
    registry.add('dashboard_pro_graph_preview', GraphPreview);
    registry.add('dashboard_pro_to_do_list',ToDoListPreview)
    return {
        DashboardItemTheme: DashboardItemTheme,
        KpiPreview: KpiPreview,
        WidgetToggle: WidgetToggle,
        WidgetToggleKPI: WidgetToggleKPI,
        WidgetToggleKpiTarget :WidgetToggleKpiTarget,
        ListViewPreview: ListViewPreview,
        ProItemPreview: ProItemPreview,
        ImageWidgetPro: ImageWidgetPro,
        ProColorPicker: ProColorPicker,
        GraphPreview: GraphPreview,
        ToDoListPreview : ToDoListPreview,
    };

});
