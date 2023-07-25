odoo.define('openeducat_grading.widget', function(require) {
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
    var Qweb = core.qweb;

    var GridGradeBook = AbstractField.extend({
        supportedFieldTypes: ['char'],
        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            this.QuarterTermBool = false;
            this.creditAvailable = false;
        },
        _render: function(){
            this.$el.empty();
            var grid_data = JSON.parse(this.recordData.grade_book);
            var self = this;
            if(grid_data !== false){
                var $GridBookContainer = $(Qweb.render('grade_book_widget_template'));
                this.$GridBookContainer = $GridBookContainer;
                this.$el.append($GridBookContainer);
                $GridBookContainer.wrap('<div class="new-parent"></div>');
                var data = [];
                var dataLength = Object.keys(grid_data).length;
                var objectData = Object.keys(grid_data);
                var ColumnHeaders = ["Year","Semester","Quarter","Total"];
                var yearData = {};
                yearData['__children'] = [];
                for(var i=0; i< dataLength; i++){
                    //yearData['Year'] = objectData[i];
                    var yearDataLength = Object.keys(grid_data[objectData[i]]).length;
                    var yearDataKeys = Object.keys(grid_data[objectData[i]]);
                    var yearDataData = grid_data[objectData[i]];
                    //----Check Quarter---
                    for(var k=0;k < yearDataKeys.length; k++){
                        var currentNode =  yearDataKeys[k];
                        if(currentNode.includes("Quarter")){
                            this.QuarterTermBool = true;
                            break;
                        }
                    }
                    if(objectData[i].includes('Year') == false){
                        var semesterData = {};
                        semesterData['Semester'] = objectData[i];
                        semesterData['__children'] = [];
                        //var semesterSubData = {};
                        if(!this.QuarterTermBool){
                            if(ColumnHeaders.includes('Quarter')){
                                var inx = ColumnHeaders.indexOf('Quarter');
                                ColumnHeaders.splice(inx,1);
                            }
                            for(var j=0; j < yearDataLength; j++){
                                if(typeof(yearDataData[yearDataKeys[j]]) == 'object'){
                                    if(yearDataData[yearDataKeys[j]].hasOwnProperty('Credit')){
                                        this.creditAvailable = true;
                                        semesterData[yearDataKeys[j]] = {
                                            "Grade" : yearDataData[yearDataKeys[j]].Grade,
                                            "Mark" : yearDataData[yearDataKeys[j]].Mark,
                                            "Credit" : yearDataData[yearDataKeys[j]].Credit,
                                        };
                                    }else{
                                        semesterData[yearDataKeys[j]] = yearDataData[yearDataKeys[j]].Mark;
                                    }
                                }else{
                                    semesterData[yearDataKeys[j]] = yearDataData[yearDataKeys[j]];
                                }
                                ColumnHeaders.push(yearDataKeys[j]);
                                //semesterSubData[yearDataKeys[j]] = yearDataData[yearDataKeys[j]];
                            }
                            //semesterData['__children'].push(semesterSubData);
                            yearData['__children'].push(semesterData);
                        }else{
                            for(var l=0; l < yearDataLength; l++){
                                var quarterData = {};
                                if(typeof(yearDataData[yearDataKeys[l]]) == 'object'){
                                    var QuarterDataLength = Object.keys(yearDataData[yearDataKeys[l]]).length;
                                    var QuarterDataKeys = Object.keys(yearDataData[yearDataKeys[l]]);
                                    var QuarterDataData = yearDataData[yearDataKeys[l]];
                                    quarterData['Quarter'] = yearDataKeys[l];
                                    quarterData['Total'] = null;
                                    quarterData['__children'] = [];
                                    //var subQuarterData = {};
                                    for(var x=0; x < QuarterDataLength;x++){
                                        if(typeof(QuarterDataData[QuarterDataKeys[x]]) == 'object'){
                                            if(QuarterDataData[QuarterDataKeys[x]].hasOwnProperty('Credit')){
                                                this.creditAvailable = true;
                                                quarterData[QuarterDataKeys[x]] = {
                                                    "Grade" : QuarterDataData[QuarterDataKeys[x]].Grade,
                                                    "Mark" : QuarterDataData[QuarterDataKeys[x]].Mark,
                                                    "Credit" : QuarterDataData[QuarterDataKeys[x]].Credit,
                                                };
                                            }else{
                                                quarterData[QuarterDataKeys[x]] = QuarterDataData[QuarterDataKeys[x]].Mark;
                                            }
                                        }else{
                                            quarterData[QuarterDataKeys[x]] = QuarterDataData[QuarterDataKeys[x]];
                                        }
                                        //semesterData[QuarterDataKeys[x]] = null;
                                        ColumnHeaders.push(QuarterDataKeys[x]);
                                    }
                                    //quarterData['__children'].push(subQuarterData);
                                }else{
                                    semesterData['Total'] = yearDataData[yearDataKeys[l]];
                                    //semesterData[childrenDataKeys[j]] = null;
                                    ColumnHeaders.push(yearDataKeys[l]);
                                }
                                if(Object.keys(quarterData).length !== 0){
                                    //quarterArray.push(quarterData);
                                    semesterData['__children'].push(quarterData);
                                }
                            }
                            yearData['__children'].push(semesterData);
                        }
                    }else{
                        if(this.QuarterTermBool){
                            yearData['Year'] = objectData[i];
                            yearData['Semester'] = null;
                            yearData['Quarter'] = null;
                            yearData['Total'] = yearDataData;
                        }else{
                            yearData['Year'] = objectData[i];
                            yearData['Semester'] = null;
                            yearData['Total'] = yearDataData;
                        }
                    }
                }
                data.push(yearData);
                for(var s=0;s < data.length; s++){
                    var tempSemData = data[s];
                    var tempSemDataKeys = Object.keys(data[s]);
                    var tempSemDataLength = Object.keys(data[s]).length;
                    for(var l=0; l < ColumnHeaders.length; l++){
                        if(tempSemDataKeys.includes(ColumnHeaders[l]) == false && ColumnHeaders[l] != '__children'){
                            tempSemData[ColumnHeaders[l]] = null;
                        }
                    }
                }
                ColumnHeaders = ColumnHeaders.filter( function( item, index, inputArray ) {
                       return inputArray.indexOf(item) == index;
                });

                $GridBookContainer.handsontable({
                    data: data,
                    colHeaders: ColumnHeaders,
                    contextMenu: false,
                    editor: false,
                    disableVisualSelection: true,
                    nestedRows: true,
                    //width: 1080,
                    //height: 500,
                    licenseKey: 'non-commercial-and-evaluation',
                    className: "htCenter",
                });
                var hotInstance = $GridBookContainer.handsontable('getInstance');
                this.movePlugin = hotInstance.getPlugin('manualColumnMove');
                var moveHeaders = hotInstance.getColHeader();
                if(moveHeaders.includes('GPA')){
                    moveHeaders = hotInstance.getColHeader();
                    this.movePlugin.moveColumn(moveHeaders.indexOf('GPA'), moveHeaders.length - 1);
                }
                if(moveHeaders.includes('Grade')){
                    moveHeaders = hotInstance.getColHeader();
                    this.movePlugin.moveColumn(moveHeaders.indexOf('Grade'), moveHeaders.length - 1);
                }
                if(moveHeaders.includes('Total')){
                    moveHeaders = hotInstance.getColHeader();
                    this.movePlugin.moveColumn(moveHeaders.indexOf('Total'), moveHeaders.length - 1);
                }
                moveHeaders = hotInstance.getColHeader();
                if(this.creditAvailable){
                    var level2Header = [];
                    for(var p=0; p < moveHeaders.length; p++){
                        if(moveHeaders[p] != 'Total' && moveHeaders[p] != 'Semester' && moveHeaders[p] != 'Quarter' && moveHeaders[p] != 'Year' && moveHeaders[p] != 'GPA' && moveHeaders[p] != 'Grade'){
                            moveHeaders[p] = {
                                'label': moveHeaders[p] ,
                                'colspan': 3,
                            }
                            level2Header.push('Mark','Grade','Credit');
                        }else{
                            level2Header.push('');
                        }
                    }
                    var allHeaders = [];
                    allHeaders.push(moveHeaders);
                    allHeaders.push(level2Header);
                    var widthList = [80,80];
                    for(var h=0; h< level2Header.length - 2; h++){
                        widthList.push(65);
                    }
                    hotInstance.updateSettings({
                        nestedHeaders: allHeaders,
                        colWidths: widthList,
                    });
                    var hotInstanceData = hotInstance.getData();
                    if(this.QuarterTermBool){
                        var objectingStart = 2;
                    }else{
                        var objectingStart = 1;
                    }
                    for(var m = objectingStart; m < hotInstanceData.length - 1; m++){
                        var firstList = hotInstanceData[m];
                        var secondList = hotInstanceData[m + 1];
                        for(var n=0;n < firstList.length; n++){
                            if(typeof(firstList[n]) == 'object' && firstList[n] != null){
                                if(secondList[n] == null){
                                    secondList.splice(n , 0 , {
                                        'Mark': '',
                                        'Grade': '',
                                        'Credit': '',
                                    });
                                    secondList.splice(n+1, 1);
                                }
                            }
                        }
                    }
                    for(var q = hotInstanceData.length - 1; q > hotInstanceData.length - objectingStart - 1; q--){
                        var firstList = hotInstanceData[q];
                        var secondList = hotInstanceData[q - 1];
                        for(var w=0;w > firstList.length; w--){
                            if(typeof(firstList[w]) == 'object' && firstList[w] != null){
                                if(secondList[w] == null){
                                    secondList.splice(w , 0 , {
                                        'Mark': '',
                                        'Grade': '',
                                        'Credit': '',
                                    });
                                    secondList.splice(w+1, 1);
                                }
                            }
                        }
                    }
                    var headerLoopVal = 0;
                    for(var c=0; c < hotInstanceData.length; c++){
                        var subHotInstanceData = hotInstanceData[c];
                        for(var d=0;d < subHotInstanceData.length; d++){
                            if(typeof(subHotInstanceData[d]) == 'object' && subHotInstanceData[d] != null){
                                var subData = subHotInstanceData[d];
                                hotInstanceData[c].splice( d , 0 , subData.Mark);
                                hotInstanceData[c].splice( d+1 , 0 , subData.Grade);
                                hotInstanceData[c].splice( d+2 , 0 , subData.Credit);
                                hotInstanceData[c].splice( d+3 ,1);
                                if(hotInstanceData[c].length > headerLoopVal){
                                    headerLoopVal = hotInstanceData[c].length;
                                }
                            }
                        }
                    }
                    hotInstanceData.forEach(function(value,key){
                        var len = headerLoopVal - value.length;
                        if(len !== 0){
                            for(var w=0; w < len; w++){
                                if(self.QuarterTermBool){
                                    hotInstanceData[key].splice(hotInstanceData[key].length - 2,0,null);
                                }else{
                                    hotInstanceData[key].splice(hotInstanceData[key].length - 1,0,null);
                                }
                            }
                        }
                    });
                    hotInstance.loadData(hotInstanceData);
                }
                setTimeout(function(){ hotInstance.render(); },100);
            }else{
                var $GridBookContainer = $(Qweb.render('grade_book_no_data_template'));
                this.$el.append($GridBookContainer);
            }
        },
    });
    registry.add('grade_book_grid_widget',GridGradeBook)
    return {
        GridGradeBook : GridGradeBook,
    };
});