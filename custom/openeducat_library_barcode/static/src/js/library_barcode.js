odoo.define('openeducat_library_barcode.EventScanView', function (require) {
"use strict";

var core = require('web.core');
var Session = require('web.session');
// var Notification = require('web.Notification');
var AbstractAction = require('web.AbstractAction');

var QWeb = core.qweb;
var _t = core._t;

// Success Notification with thumbs-up icon
// var Success = Notification.extend({
//     template: 'openeducat_library_barcode_success'
// });
//
// var NotificationSuccess = NotificationManager.extend({
//     success: function(title, text, sticky) {
//         return this.display(new Success(this, title, text, sticky));
//     }
// });

// load widget with main barcode scanning View
var EventScanView = AbstractAction.extend({
    template: 'openeducat_library_barcode_template',
    events: {
        'keypress #openeducat_library_barcode': 'on_manual_scan',
        'keypress #openeducat_library_barcode1': 'on_manual_scan',
        'click .o_event_info1': 'on_manual_scan',
        'click #btn_return': 'returnClick',
        'click #btn_main_menu': 'menuClick',
        'click #btn_issue': 'issueClick',
        'change #mySelect': 'selectClick',
    },

    init: function(parent, action) {
        this._super.apply(this, arguments);
        this.message_demo_barcodes = action.params.message_demo_barcodes;
        this.action = action;
        this.parent = parent;
    },

    start: function() {
        var self = this;
        // this.notification_manager = new NotificationSuccess();
        // this.notification_manager.appendTo(self.parent.$el);
        core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
        self.start_clock();
        return this._super().then(function() {
            if (self.message_demo_barcodes) {
                self.setup_message_demo_barcodes();
            }
        });
    },
    on_manual_scan: function(e) {
        var self = this;
        if (e.which === 13) { 
            var self = this;
            var value = $(e.currentTarget).val().trim();
            var MediaValue = document.getElementById('openeducat_library_barcode').value;
            var LibraryCardValue = document.getElementById('openeducat_library_barcode1').value;
            var ttype = document.getElementById('mySelect').value;
            if (ttype == 'issue') {
		        var x = 0;
		        var y = 0;
		        if (MediaValue) {
		        	var MediaVal = MediaValue.substring(0, 3);
		        	if (MediaVal == 'MUB') {
		        		var x = MediaValue;
		        	}
		        	if (MediaVal == 'LCB') {
		        		var y = MediaValue;
		        	}
		        }
		        if (LibraryCardValue) {
		        	var LibraryCardVal = LibraryCardValue.substring(0, 3);
		        	if (LibraryCardVal == 'MUB') {
		        		var x = LibraryCardValue;
		        	}
		        	if (LibraryCardVal == 'LCB') {
		        		var y = LibraryCardValue;
		        	}
		        }
		        if ((x == 0) && (y == 0)) {
                    self.displayNotification({title: _t('Warning'), message: "Barcode is not valid", type: 'danger'});
		        }
		        if (x != 0) {
		        	document.getElementById('openeducat_library_barcode').value = x;
		        } else {
		        	document.getElementById('openeducat_library_barcode').value = '';
		        }
		        if (y != 0) {
		        	document.getElementById('openeducat_library_barcode1').value = y;
		        } else {
		        	document.getElementById('openeducat_library_barcode1').value = '';
		        }
		        if (value && (x != 0) && (y != 0)) {
		            this.on_barcode_scanned_manual(value, MediaValue, LibraryCardValue);
		            $(e.currentTarget).val('');
		        }
            } else {
            	var x = 0;
            	var MediaVal = MediaValue.substring(0, 3);
            	if (MediaVal == 'MUB') {
		        		var x = MediaValue;
		        	}
            	if (x != 0) {
            		this.on_media_scan(MediaValue);
            	} else {
            		self.displayNotification({title: _t('Warning'), message: "Barcode is not valid", type: 'danger'});
            	}
            }
        }
    },

    on_media_scan: function(barcode) {
	    var self = this;
	    Session.rpc('/openeducat_library_barcode/return_media', {
             barcode: barcode,
        }).then(function(result) {
        	if (result.success) {
//        		self.notification_manager.success(result.success);
                document.getElementById('openeducat_library_barcode').value = '';
                document.getElementById('openeducat_library_barcode1').value = '';
                if(result.success){
                    self.$el.html(QWeb.render("LibraryBarcodeReturnMessage", {widget:result},));
                    setTimeout( function() {self.$el.html(QWeb.render("openeducat_library_barcode_template", {},));},5000);
                }
        	} else if (result.warning) {
                self.displayNotification({title: _t('Warning'), message: result.warning, type:'danger'});
            }
            if (result.penalty > 0.0) {
               self.$el.html(QWeb.render("LibraryBarcodePenaltyMessage", {widget:result},));
               setTimeout( function() {self.$el.html(QWeb.render("openeducat_library_barcode_template", {},));},5000);
            }
        });
    },
    _onBarcodeScanned: function(barcode) {
        var self = this;
        var ttype = $('#mySelect').attr('value');
        if(barcode == 'issue_book'){
            $('#return_text').hide();
            $("#btn_issue").trigger("click");
            $("#mySelect").attr('value','issue');
        }
        if(String(barcode) == 'return_book'){
            $('#issue_text').hide();
            $("#btn_return").trigger("click")
            $("#mySelect").attr('value','return');
        }
        if(ttype == 'issue' || ttype == 'return'){
    	if (barcode) {
        	var self = this;
        	var MediaVal = barcode.substring(0, 3);
            if (MediaVal == 'MUB') {
                $('#openeducat_library_barcode').val(barcode);
                if (ttype == 'issue') {
                    $('#issue_text').hide();
                    $('#issue_text_1').show();
                }
            } else if (MediaVal == 'LCB') {
                $('#openeducat_library_barcode1').val(barcode);
            }
            var MediaValue = $('#openeducat_library_barcode').val();
            var LibraryCardValue = $('#openeducat_library_barcode1').val();
            if (ttype == 'issue') {
                if (MediaValue && LibraryCardValue) {
                    this.on_barcode_scanned_manual(barcode, MediaValue, LibraryCardValue);
                }
            } else {
	        	if (MediaValue) {
	        		this.on_media_scan(MediaValue);
	        	} else {
	        		self.displayNotification({title: _t('Warning'), message: "Barcode is not valid", type: 'danger'});
	        	}
            }
            }
        }
    },
    on_barcode_scanned_manual: function(barcode, MediaValue, LibraryCardValue) {
        var self = this;
        Session.rpc('/openeducat_library_barcode/register_attendee', {
             barcode: barcode,
             media_barcode: MediaValue,
             librarycard_barcode: LibraryCardValue,
        }).then(function(result) {
            if (result.success) {
                document.getElementById('openeducat_library_barcode').value = '';
                document.getElementById('openeducat_library_barcode1').value = '';
                $("#mySelect").attr('value','none');
                if(result.success){
                    self.$el.html(QWeb.render("LibraryBarcodeGreetingMessage", {widget:result},));
                    setTimeout( function() {self.$el.html(QWeb.render("openeducat_library_barcode_template", {},));},5000);
                }
            } else if (result.warning) {
                self.displayNotification({title: _t('Warning'), message: result.warning, type: 'danger'});
            }
        });
    },

    start_clock: function () {
        this.clock_start = setInterval(function() {this.$(".o_library_barcode_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));}, 500);
        // First clock refresh before interval to avoid delay
        this.$(".o_library_barcode_clock").show().text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit', second:'2-digit'}));
    },

    destroy: function () {
       clearInterval(this.clock_start);
       this._super.apply(this, arguments);
    },
    returnClick: function(){
        $("#mySelect").attr('value','return');
        $("#openeducat_library_barcode").value = ''
        $("#openeducat_library_barcode1").value = ''
        $("#openeducat_library_barcode").css('display','');
        $("#openeducat_library_barcode1").css('display','none');
        $("#btn_issue").css('display','none');
        $("#btn_return").css('display','none');
        $("#btn_main_menu").css('display','block');
        $("#return_text").css('display','block');
        $("#issue_text_1").css('display','none');
        // setTimeout( function() { $("#btn_main_menu").trigger("click");}, 5000);
    },
    
    issueClick: function(){

        $("#mySelect").attr('value','issue');

        $("#openeducat_library_barcode").css('display','');
        $("#openeducat_library_barcode1").css('display','');
        $("#btn_issue").css('display','none');
        $("#btn_return").css('display','none');
        $("#btn_main_menu").css('display','block');
        $("#openeducat_library_barcode").value = ''
        $("#openeducat_library_barcode1").value = ''
        $("#issue_text").css('display','block');
        // setTimeout( function() { $("#btn_main_menu").trigger("click");},10000);
    },
    
    menuClick: function(){
        $("#mySelect").attr('value','none');
        $("#openeducat_library_barcode").value = ''
        $("#openeducat_library_barcode1").value = ''
        $("#btn_issue").css('display','block');
        $("#btn_return").css('display','block');
        $("#btn_main_menu").css('display','none');
        $("#openeducat_library_barcode").css('display','none');
        $("#openeducat_library_barcode1").css('display','none');
        $("#issue_text").css('display','none');
        $("#issue_text_1").css('display','none');
        $("#return_text").css('display','none');
    },
    
    selectClick: function(){
        var x = $("mySelect").value;
        if (x == 'return') {
            $('#openeducat_library_barcode1').css('display','none');
            $('#openeducat_library_barcode').value = '';
            $('#openeducat_library_barcode1').value = '';
        } else {
            $('#openeducat_library_barcode1').css('display','none');
            $('#openeducat_library_barcode').value = '';
            $('#openeducat_library_barcode1').value = '';
        }
    },
    
});

core.action_registry.add('openeducat_library_barcode.scan_view', EventScanView);

return {
    // Success: Success,
    // NotificationSuccess: NotificationSuccess,
    EventScanView: EventScanView
};

});
