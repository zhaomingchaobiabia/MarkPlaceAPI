import time

from .models import Offers
from .market_api import MarketPlaceApi
from datetime import datetime
from .views import mark


# 定时获取offer
def query_offer(seller_id):
    subject = Offers.objects.filter(offer_seller_id=seller_id)
    print(subject)
    return subject


def str_time(dat):
    if dat == '':
        return ''
    # bucket['key_as_string']= '2018-08-06T10:00:00.000Z' 

    date_ = str(datetime.strptime(dat, "%Y-%m-%dT%H:%M:%S+%f:00"))
    date_ = date_.split('.')[0]

    # local_time = 2018-08-06 18:00:00
    return date_
    # local_time = date_ + timedelta(hours=8)


def end_time(dat):
    if dat == '':
        return ''
    # bucket['key_as_string']= '2018-08-06T10:00:00.000Z' 

    date_ = str(datetime.strptime(dat, "%Y-%m-%dT%H:%M:%S+%f:00"))
    date_ = date_.split('.')[0]

    # local_time = 2018-08-06 18:00:00
    return date_


def delete_offer(seller_id):
    subject = Offers.objects.filter(offer_seller_id=seller_id)
    subject.delete()


def query_id(ls):
    subject = Offers.objects.all()
    for data in subject:
        if data.offer_seller_id not in ls:
            delete_offer(data.offer_seller_id)


def add_offer(data):
    try:
        if 'promotion' not in data:
            data['promotion'] = {'@type': '', 'starts_at': '', 'ends_at': '', 'price': '',
                                 'triggers': {'trigger_customer_type': ''}
                                 }
        if 'image' not in data:
            data['image'] = ''
        offers = Offers(product_name=data['product_name'], product_fnac_id=data['product_fnac_id'],
                        offer_fnac_id=data['offer_fnac_id'],
                        offer_seller_id=data['offer_seller_id'], product_state=data['product_state'],
                        price=data['price'], quantity=data['quantity'], description=data['description'],
                        internal_comment=data['internal_comment'], product_url=data['product_url'],
                        image=data['image'], nb_messages=data['nb_messages'], showcase=data['showcase'],
                        is_shipping_free=data['is_shipping_free'], promotion=data['promotion']['@type'],
                        starts_at=str_time(data['promotion']['starts_at']),
                        ends_at=str_time(data['promotion']['ends_at']),
                        pro_price=data['promotion']['price'],
                        trigger_customer_type=data['promotion']['triggers']['trigger_customer_type'],
                        type_label=data['type_label'])
        offers.save()
    except Exception as e:
        print(e)
        print(data['offer_seller_id'])


def task():
    print('运行:', time.strftime('%Y-%m-%d %H:%M:%S'))
    paging = 1
    lis_id = []
    while True:
        try:
            data_dict = mark.offers_query(paging)['offers_query_response']['offer']
            ls = []
            if type(data_dict) is not list:
                data_dict = ls.append(data_dict)
            for data in data_dict:
                delete_offer(data['offer_seller_id'])
                add_offer(data)
                lis_id.append(data['offer_seller_id'])
                print(data['offer_seller_id'], '已更新')
        except Exception as e:
            print(e)
            print('本次结束:', time.strftime('%Y-%m-%d %H:%M:%S'))
            break

        paging += 1
    query_id(lis_id)
