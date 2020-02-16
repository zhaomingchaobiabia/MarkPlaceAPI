from .views import mark, mark_order, incident
from markerplace_develop.views import sales
from .models import OfferOrder


def offer():
    content = mark.offers_query(1)
    return content['offers_query_response']['nb_total_result']


def order():
    content = mark_order.orders_query({'paging': 1})
    return content['orders_query_response']['nb_total_result']


def message():
    content = sales.messages_query({'paging': 1})
    return content['messages_query_response']['nb_total_result']


def incidents():
    content = incident.incidents_query({'paging': 1})
    return content['incidents_query_response']['nb_total_result']


def get_task():
    offer_num = offer()
    order_num = order()
    message_num = message()
    incident_num = incidents()
    subject = OfferOrder.objects.create(id=1, offer=offer_num, order=order_num, message=message_num,
                                        incident=incident_num)
    subject.save()
