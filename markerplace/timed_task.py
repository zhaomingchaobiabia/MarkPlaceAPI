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
    subject = Offers.objects.raw('delete from offers where offer_seller_id = %s', params=(seller_id,))
    # subject = Offers.objects.filter(offer_seller_id=seller_id)
    # subject.delete()

def add_offer(data):
    sql = "insert into offers(product_name, product_fnac_id, offer_fnac_id,offer_seller_id,product_state,price," \
          "quantity,description,internal_comment,product_url,image,nb_messages,showcase,is_shipping_free," \
          "promotion,starts_at,ends_at,pro_price,trigger_customer_type,type_label) values(%s,%s,%s,%s,%s,%s,%s," \
          "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        if 'promotion' not in data:
            data['promotion'] = {'@type': '', 'starts_at': '', 'ends_at': '', 'price': '',
                                 'triggers': {'trigger_customer_type': ''}
                                 }
        if 'image' not in data:
            data['image'] = ''
        Offers.objects.raw(sql, args=(data['product_name'], data['product_fnac_id'], data['offer_fnac_id'],
                                      data['offer_seller_id'], data['product_state'], data['price'],
                                      data['quantity'],
                                      data['description'], data['internal_comment'], data['product_url'],
                                      data['image'],
                                      data['nb_messages'], data['showcase'], data['is_shipping_free'],
                                      data['promotion']['@type'], str_time(data['promotion']['starts_at']),
                                      end_time(data['promotion']['ends_at']),
                                      data['promotion']['price'],
                                      data['promotion']['triggers']['trigger_customer_type'],
                                      data['type_label']))
    except Exception as e:
        print(e)
        print(data['offer_seller_id'])


def task():
    paging = 1
    while True:
        try:
            data_dict = mark.offers_query(paging)['offers_query_response']['offer']
            print(data_dict)
            for data in data_dict:
                delete_offer(data_dict['offer_seller_id'])
                add_offer(data)
                print(data_dict['offer_seller_id'], '已更新')
        except:
            break
        paging += 1
