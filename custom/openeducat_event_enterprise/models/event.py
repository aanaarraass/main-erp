
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models
from datetime import datetime


class OpEvent(models.Model):
    _inherit = "event.event"

    def search_read_for_app(self):
        if self.env.user.partner_id.is_student:
            res = self.sudo().search([('state', '!=', 'draft')])
            apps = self.env['ir.model'].sudo().search(
                [('model', '=', 'event.event.ticket')])
            upcomming = []
            past = []
            for event in res:
                date = datetime.today()
                if event.date_begin >= date:
                    upcoming_dict = ({
                        'start_date': event.date_begin,
                        'end_date': event.date_end,
                        'event_name': event.name,
                        'organized_by': event.organizer_id.name,
                        'category': event.event_type_id.name,
                        'price': 0,
                        'status': event.state,
                    })
                    for address in event.address_id:
                        upcoming_dict.update({
                            'location': {
                                'street': address.street,
                                'street2': address.street2,
                                'city': address.city,
                                'state': address.state_id.name,
                                'zip': address.zip,
                                'country': address.country_id.name
                            }
                        })
                    price_list = []
                    if apps.name == 'Event Ticket':
                        for ticket in event.event_ticket_ids:
                            price_list.append({
                                'type': ticket.name,
                                'price': ticket.price,
                                'deadline': ticket.deadline
                            })
                    upcoming_dict['price'] = price_list
                    upcomming.append(upcoming_dict)
                else:
                    past_dict = ({
                        'start_date': event.date_begin,
                        'end_date': event.date_end,
                        'event_name': event.name,
                        'organized_by': event.organizer_id.name,
                        'category': event.event_type_id.name,
                        'price': 0,
                        'status': event.state,
                    })
                    for address in event.address_id:
                        past_dict.update({
                            'location': {
                                'street': address.street,
                                'street2': address.street2,
                                'city': address.city,
                                'state': address.state_id.name,
                                'zip': address.zip,
                                'country': address.country_id.name
                            }
                        })
                    price_list = []
                    if apps.name == 'Event Ticket':
                        for ticket in event.event_ticket_ids:
                            price_list.append({
                                'type': ticket.name,
                                'price': ticket.price,
                                'deadline': ticket.deadline
                            })
                    past_dict['price'] = price_list
                    past.append(past_dict)
            return {
                'upcomming_event': upcomming,
                'past_event': past,
            }
