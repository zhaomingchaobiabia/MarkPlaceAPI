import pymysql
from datetime import datetime


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


class Sql:

    def __init__(self):
        self.connect = pymysql.connect('207.148.2.37', 'zhaomingchao', 'Zhaomingchao28!', 'fnac_api')
        self.cursor = self.connect.cursor()

    def price(self, min_p, max_p):
        sql = 'select * from offers_master where price-pro_price > %s and price-pro_price < %s'
        self.cursor.execute(sql, args=(min_p, max_p))
        # print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def offer_all(self):
        sql = 'select * from offers_master '
        self.cursor.execute(sql)
        # print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def offer_quantity(self, fla, num):
        dic_fla = {'Equals': '=', 'LessThan': '<',
                   'GreaterThan': '<', 'LessThanOrEquals': '<=',
                   'GreaterThanOrEquals': '>='}
        sql = f'select * from offers_master where quantity {dic_fla[fla]} %s'
        self.cursor.execute(sql, args=(num,))
        # print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def save_offer(self, data):
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
            self.cursor.execute(sql, args=(data['product_name'], data['product_fnac_id'], data['offer_fnac_id'],
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
            self.connect.commit()
        except Exception as e:
            print(e)
            print(data['offer_seller_id'])
            self.connect.rollback()

    def data_copy(self):
        try:
            sql = 'truncate table offers_master'
            sql2 = 'INSERT INTO offers_master SELECT * FROM offers'
            sql3 = 'truncate table offers'
            self.cursor.execute(sql)
            print(sql)
            self.cursor.execute(sql2)
            print(sql2)
            self.cursor.execute(sql3)
            print(sql3)
            self.connect.commit()
        except:
            self.connect.rollback()


sql = Sql()
sql.price(100, 200)
