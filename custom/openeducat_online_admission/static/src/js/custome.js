odoo.define('openeducat_online_admission.student_registration', function (require) {
    "use strict";
    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    var websiteRootData = require('website.root');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;
    const time = require('web.time');

    publicWidget.registry.student_register = publicWidget.Widget.extend({
        selector: '.js_online_get_data',
        events:{'change #self_application': '_onchangedropdown',
                'change select[name="company_id"]': '_onCompanyChange',
                'change select[name="department_id"]': '_onDepartmentChange',
                'change select[name="program_id"]': '_onProgramChange',
//                'change select[name="register_id"]': '_onRegisterChange',
                'change select[name="marks_type_one"]': '_onMarksTypeChange',
                'change select[name="marks_type_two"]': '_onMarksTypeChange',
                'change select[name="marks_type_three"]': '_onMarksTypeChange',
                'change select[name="marks_type_four"]': '_onMarksTypeChange',
                'change select[name="marks_type_five"]': '_onMarksTypeChange',
                'change select[name="marks_type_sixth"]': '_onMarksTypeChange',


                'change .admission_form_date': '_onchangebirthdate',
                keydown: "_onKeydown",

                },

        xmlDependencies: ['/openeducat_online_admission/static/src/xml/custome.xml'],
        init: function(){
            this._super.apply(this,arguments);
        },
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then( function(){
                $("#birthdate").attr('placeholder', time.getLangDateFormat());
                $( "#birthdate" ).datepicker('destroy');

                self.$department = self.$('select[name="department_id"]');
                self.$departmentOptions = self.$department.filter(':enabled').find('option:not(:first)');


                self.$program = self.$('select[name="program_id"]');
                self.$programOptions = self.$program.filter(':enabled').find('option:not(:first)');

                self.$register = self.$('select[name="register_id"]');
                self.$registerOptions = self.$register.filter(':enabled').find('option:not(:first)');


                self._adaptDepartment();
                self._adaptProgram();
                self._adaptDiscipline();
                $( ".admission_form_date" ).each( function(){
                    self._initDateTimePicker($(this));
                });
            });

        },
        _formatDate: function(){
            var dateFormat = time.getLangDateFormat();
            var formatArr = ['Y','M','D'];
            for(var idx in formatArr){
                var chr =  formatArr[idx];
                var count = [...dateFormat].filter(x => x === chr).length;
                if(count > 2){
                    dateFormat = dateFormat.replace( `${chr.repeat(count)}`, `${chr.repeat(2)}` );
                }
            }
            dateFormat = dateFormat.toLowerCase()
            return dateFormat;
        },

        _initDateTimePicker: function ($dateGroup) {
            var self = this;
            var datetimepickerFormat = time.getLangDateFormat();
            $dateGroup.datetimepicker({
                format : datetimepickerFormat,
                minDate: 0,
                useCurrent: false,
                maxDate: moment(new Date()),
                viewDate: false,
                icons: {
                    time: 'fa fa-clock-o',
                    date: 'fa fa-calendar',
                    next: 'fa fa-chevron-right',
                    previous: 'fa fa-chevron-left',
                    up: 'fa fa-chevron-up',
                    down: 'fa fa-chevron-down',
                },
                locale : moment.locale(),
                allowInputToggle: true,
            });
            $dateGroup.on('change.datetimepicker', function(ev){
                self._onchangebirthdate(ev);
            })
        },

            //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */

         _onKeydown: function (ev) {

            console.table(ev.target.name)
            if (ev.target.name === 'total_marks_one' || ev.target.name === 'marks_obtained_one'){

                $("#marks_type_one").val("select_one").change();

            }
            if (ev.target.name === 'total_marks_two' || ev.target.name === 'marks_obtained_two'){

                $("#marks_type_two").val("select_two").change();

            }

            if (ev.target.name === 'total_marks_three' || ev.target.name === 'marks_obtained_three'){

                $("#marks_type_three").val("select_three").change();

            }
            if (ev.target.name === 'total_marks_four' || ev.target.name === 'marks_obtained_four'){

                $("#marks_type_four").val("select_four").change();

            }

            if (ev.target.name === 'total_marks_five' || ev.target.name === 'marks_obtained_five'){

                $("#marks_type_five").val("select_five").change();

            }
            if (ev.target.name === 'total_marks_sixth' || ev.target.name === 'marks_obtained_sixth'){

                $("#marks_type_sixth").val("select_sixth").change();

            }




        },


        _adaptDepartment: function () {
            var self = this;
            var $company = self.$('select[name="company_id"]');
            var companyID = ($company.val() || 0);
            self.$departmentOptions.detach();
            var $displayeddepartment = self.$departmentOptions.filter('[data-company_id=' + companyID + ']');
            var nb = $displayeddepartment.appendTo(self.$department).show().length;
//            self.$department.parent().toggle(nb >= 1);
        },


        _adaptProgram: function () {
            var self = this;
            var $department = self.$('select[name="department_id"]');
            var departmentID = ($department.val() || 0);
            self.$programOptions.detach();
            var $displayedprogram = self.$programOptions.filter('[data-department_id=' + departmentID + ']');
            var nb = $displayedprogram.appendTo(self.$program).show().length;
//            self.$department.parent().toggle(nb >= 1);
        },

        _adaptDiscipline: function () {
            var self = this;
            var $program = self.$('select[name="department_id"]');
            var ProgramID = ($program.val() || 0);
            self.$registerOptions.detach();
            console.log("=====================UOJ")
            console.log(ProgramID)
            console.log($program)
            var $displayedregister = self.$registerOptions.filter('[data-department_id=' + ProgramID + ']');
            var nb = $displayedregister.appendTo(self.$register).show().length;
//            self.$department.parent().toggle(nb >= 1);
        },

        _adaptMarksType: function () {
            var self = this;
            var $One = self.$('select[name="marks_type_one"]');
            var OneVal = ($One.val() || 0);
            const numX = document.getElementById("total_marks_one").value;
            const numY = document.getElementById("marks_obtained_one").value;

            if (OneVal == 'marks' && numX > 0 && numY > 0){
               var perOne = ((numY / numX ) * 100);
               document.getElementById("cgpa_or_marks_one").value = perOne.toFixed(2);
               $('#cgpa_or_marks_one').prop('readonly', true);
            }
            else {
                document.getElementById("cgpa_or_marks_one").value = '';
                $('#cgpa_or_marks_one').prop('readonly', false);
            }




//            =====================================================
            var $Two = self.$('select[name="marks_type_two"]');
            var TwoVal = ($Two.val() || 0);
            const numXTwo = document.getElementById("total_marks_two").value;
            const numYTwo = document.getElementById("marks_obtained_two").value;



            if (TwoVal == 'marks' && numXTwo > 0 && numYTwo > 0){
               var perTwo = ((numYTwo / numXTwo ) * 100);
               document.getElementById("cgpa_or_marks_two").value = perTwo.toFixed(2);
               $('#cgpa_or_marks_two').prop('readonly', true);
            }
            else {
                document.getElementById("cgpa_or_marks_two").value = '';
                $('#cgpa_or_marks_two').prop('readonly', false);
            }

            //            =====================================================
            var $Three = self.$('select[name="marks_type_three"]');
            var perThree = ($Three.val() || 0);
            const numXThree = document.getElementById("total_marks_three").value;
            const numYThree = document.getElementById("marks_obtained_three").value;



            if (perThree == 'marks' && numXTwo > 0 && numYTwo > 0){
               var perThree = ((numYThree / numXThree ) * 100);
               document.getElementById("cgpa_or_marks_three").value = perThree.toFixed(2);
               $('#cgpa_or_marks_three').prop('readonly', true);
            }
            else {
                document.getElementById("cgpa_or_marks_three").value = '';
                $('#cgpa_or_marks_three').prop('readonly', false);
            }

            //            =====================================================
            var $Four = self.$('select[name="marks_type_four"]');
            var perFour = ($Four.val() || 0);
            const numXFour = document.getElementById("total_marks_four").value;
            const numYFour = document.getElementById("marks_obtained_four").value;



            if (perFour == 'marks' && numXFour > 0 && numYFour > 0){
               var perFour = ((numYFour / numXFour ) * 100);
               document.getElementById("cgpa_or_marks_four").value = perFour.toFixed(2);
               $('#cgpa_or_marks_four').prop('readonly', true);
            }
            else {
                document.getElementById("cgpa_or_marks_four").value = '';
                $('#cgpa_or_marks_four').prop('readonly', false);
            }

            //            =====================================================
            var $Five = self.$('select[name="marks_type_five"]');
            var perFive = ($Five.val() || 0);
            const numXFive = document.getElementById("total_marks_five").value;
            const numYFive = document.getElementById("marks_obtained_five").value;



            if (perFive == 'marks' && numXFive > 0 && numYFive > 0){
               var perFive = ((numYFive / numXFive ) * 100);
               document.getElementById("cgpa_or_marks_five").value = perFive.toFixed(2);
               $('#cgpa_or_marks_five').prop('readonly', true);
            }
            else {
                document.getElementById("cgpa_or_marks_five").value = '';
                $('#cgpa_or_marks_five').prop('readonly', false);
            }

            //            =====================================================
                        var $sixth = self.$('select[name="marks_type_sixth"]');
            var persixth = ($sixth.val() || 0);
            const numXsixth = document.getElementById("total_marks_sixth").value;
            const numYsixth = document.getElementById("marks_obtained_sixth").value;



            if (persixth == 'marks' && numXsixth > 0 && numYsixth > 0){
               var persixth = ((numYsixth / numXsixth ) * 100);
               document.getElementById("cgpa_or_marks_sixth").value = persixth.toFixed(2);
               $('#cgpa_or_marks_sixth').prop('readonly', true);
            }
            else {
                document.getElementById("cgpa_or_marks_sixth").value = '';
                $('#cgpa_or_marks_sixth').prop('readonly', false);
            }


        },

        _adaptRegister: function () {
            var self = this;
            var $register = self.$('select[name="register_id"]');

            var RegisterID = ($register.val() || 0);

            var element = $register.find('option:selected');

            var selected = element.attr('data-year_equivalent');
            var year_of_degree = element.attr('data-year_of_degree');

            console.log(year_of_degree)
            console.log(selected)
            console.log("=============")
            if (year_of_degree == '2_year' && selected == '16'){
               selected =  '17'

            }
             if (year_of_degree == '2_year' && selected == '18'){
               selected =  '19'

            }
//            if (selected == '18'){
//               selected =  '22'
//
//            }

            console.log(year_of_degree)
            console.log(selected)
            console.log("=============")


            var selectedInt = parseInt(selected)



//            code start here


//            code end here

            $('#pedutable td.groupId').each(function(){
                // get current cell
                var currentCell = $(this);

                // get the cells groupid
                var groupid = currentCell.text();
                var groupidInt = parseInt(groupid)


                // determine if it the group id matches the selected value and hide/show
//                if(groupid !== selected){
//                    currentCell.parent().hide();
//                }
//                else{
//                    currentCell.parent().show();
//                }



                if(selected > groupid){
                    currentCell.parent().show();
                }
                else{
                    currentCell.parent().hide();
                }








            });
        },

        /**
         * @private
         */
        _onCompanyChange: function () {
            var self = this;
            self._adaptDepartment();
        },

        _onDepartmentChange: function () {
            var self = this;
//            self._adaptProgram();
                self._adaptDiscipline();
        },

        _onProgramChange: function () {
            var self = this;
            self._adaptDiscipline();
        },

        _onRegisterChange: function () {
            var self = this;
            self._adaptRegister();
        },

        _onMarksTypeChange: function () {
            var self = this;
            self._adaptMarksType();
        },



        /**
         * @private
         */

        _onchangedropdown: function(ev){
            var application = $(ev.currentTarget).val();
            ajax.jsonRpc('/get/application_data', 'call',
                {
                'application': application,
                }).then(function (data) {
                if (data['student_id'])
                {
                var student_data = qweb.render('GetStudentData',
                {
                    students: data['student_id'][0],
                    country: data['country_id']
                });
                $('.students').html(student_data);
                $('.country').html(student_data);
                }
                else if (data['country'])
                {
                  var others_data = qweb.render('GetOthersData',
                {
                    others: data['country'],
                });
                $('.others').html(others_data);
                }

            });
        },

        _onchangebirthdate: function(ev){
            var birth_date = $("input[name='birth_date']").val();
            var register_id = $("select[name='register_id']").val();
            var datetimepickerFormat = time.getLangDateFormat();
            var momentDate = moment(birth_date, datetimepickerFormat);
            var formattedDate = momentDate ? momentDate.toJSON() : '';
            if(register_id){
                ajax.jsonRpc('/check/birthdate', 'call',
                    {
                    'birthdate': formattedDate,
                    'register': register_id,
                    }).then(function (data) {
                    if (data['birthdate'])
                    {
                      alert('Not Eligible for Admission minimum required age is :'+ data['age']);
                      var birth_date = $("input[name='birth_date']").val('');
                    }
                    });
            }
            else{
                alert('Please Select a Course');
                var birth_date = $("input[name='birth_date']").val('');
            }
        }
    });

    return publicWidget.registry.student_register;
});
