
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import TransactionCase
from odoo.addons.website.tools import MockRequest
from ..controllers import main


class LibraryBarcodeControllerTests(TransactionCase):
    def setUp(self):
        super(LibraryBarcodeControllerTests, self).setUp()
        self.BarcodeController = main.EventBarcode()


class TestBarcodeController(LibraryBarcodeControllerTests):

    def setUp(self):
        super(TestBarcodeController, self).setUp()

    def test_case_library_barcode(self):
        self.BarcodeController = main.EventBarcode()
        data = self.env.ref('openeducat_library.op_media_unit_2').barcode
        card = self.env.ref('openeducat_library.op_library_card_1').number
        with MockRequest(self.env):
            self.cookies = self.BarcodeController.\
                register_attendee(media_barcode=data, librarycard_barcode=card)
            self.cookies = self.BarcodeController.return_media(barcode=data)
