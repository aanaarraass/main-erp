
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import logging
from .test_transportation_common import TestTransportationCommon


class TestComapny(TestTransportationCommon):

    def setUp(self):
        super(TestComapny, self).setUp()

    def test_case_1_company(self):
        company = self.res_company.search([])
        logging.info('Details of Transportation Company')
        logging.info(
            'transportation_enterprise_onboard_panel : %s :  ' % (
                company.transportation_enterprise_onboard_panel))
        logging.info('onboarding_route_layout_state : %s :  ' % (
            company.onboarding_route_layout_state))
        logging.info(
            'onboarding_stop_layout_state : %s :  ' % (
                company.onboarding_stop_layout_state))
        logging.info('onboarding_trip_layout_state : %s :  ' % (
            company.onboarding_trip_layout_state))
        logging.info(
            'onboarding_vehicle_layout_state : %s :  ' % (
                company.onboarding_vehicle_layout_state))

        company.action_close_transportation_panel_onboarding()
        company.action_onboarding_route_layout()
        company.action_onboarding_stop_layout()
        company.action_onboarding_trip_layout()
        company.action_onboarding_vehicle_layout()
        company.update_transportation_onboarding_state()


class TestRoute(TestTransportationCommon):

    def setUp(self):
        super(TestRoute, self).setUp()

    def test_case_1_route(self):
        route = self.op_route.search([])

        for route in route:
            logging.info('Details of Transportation route')
            logging.info('Name : %s :  ' % (route.name))
            logging.info('stop_ids : %s :  ' % (route.stop_ids))
            logging.info('cost : %s :  ' % (route.cost))
            logging.info('vehicle_id : %s :  ' % (route.vehicle_id))
            logging.info('company_id : %s :  ' % (route.company_id))

        route.action_onboarding_route_layout()


class TestRouteLine(TestTransportationCommon):

    def setUp(self):
        super(TestRouteLine, self).setUp()

    def test_case_1_route_line(self):
        route_line = self.op_route_line.search([])
        for route_line in route_line:
            logging.info('Details of Transportation route line')
            logging.info('Name : %s :  ' % (route_line.name))
            logging.info('route_id : %s :  ' % (route_line.route_id))
            logging.info('route_type : %s :  ' % (route_line.route_type))
            logging.info('route_stop_ids : %s :  ' % (route_line.route_stop_ids))
            logging.info('route_passenger_ids : %s :  ' %
                         (route_line.route_passenger_ids))
            logging.info('route_date : %s :  ' % (route_line.route_date))
            logging.info('start_time : %s :  ' % (route_line.start_time))
            logging.info('driver_id : %s :  ' % (route_line.driver_id))
            logging.info('state : %s :  ' % (route_line.state))
            logging.info('company_id : %s :  ' % (route_line.company_id))

        route_line.onchange_route_id()
        route_line.start_trip()
        route_line.end_trip()
        route_line.create_route_stop_line()
        route_line.action_onboarding_trip_layout()


class TestStop(TestTransportationCommon):

    def setUp(self):
        super(TestStop, self).setUp()

    def test_case_1_stop(self):
        stop = self.op_stop.search([])

        for stop in stop:
            logging.info('Details of Transportation stop')
            logging.info('Name : %s :  ' % (stop.name))
            logging.info('sequence : %s :  ' % (stop.sequence))
            logging.info('partner_ids : %s :  ' % (stop.partner_ids))
            logging.info('estimated_arrival_conf : %s :  ' %
                         (stop.estimated_arrival_conf))
            logging.info('route_id  : %s  :' % (stop.route_id))
            logging.info('company_id : %s :  ' % (stop.company_id))

        stop.check_capacity()
        stop.action_onboarding_stop_layout()


class TestStopline(TestTransportationCommon):

    def setUp(self):
        super(TestStopline, self).setUp()

    def test_case_1_stop_line(self):
        self.op_stop_line.search([])


class TestVehicle(TestTransportationCommon):

    def setUp(self):
        super(TestVehicle, self).setUp()

    def test_case_1_vehical(self):
        vehicale = self.op_vehicle.search([])
        for vehicales in vehicale:
            logging.info('%s  : ' % (vehicales.company_id))
        vehicale.action_onboarding_vehicle_layout()
