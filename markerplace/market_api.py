# api接口脚本
import requests
import json
import xmltodict

import xml.etree.ElementTree as ET


# 验证失败 重新获取token
def outter(func):
    func = func

    def inner(self, *args, **kwargs):
        try:
            if func(self, *args, **kwargs) == 400:
                #     print(111)
                self.authentication()
                return func(self, *args, **kwargs)

            return func(self, *args, **kwargs)
        except:
            # if func(self, *args, **kwargs) == 400:
            #     print(111)
            self.authentication()
            return func(self, *args, **kwargs)

    return inner


class MarketPlaceApi:
    def __init__(self):
        self.url = 'https://marketplace.ws.fd-recette.net/api.php'
        self.headers = {"Content-Type": "text/xml"}
        self.partner_id = 'E572D914-F603-4E7F-D023-4839FD7695A3'
        self.shop_id = '8290D0BD-61BB-95A9-C33C-74B811429051'
        self.key = 'D48CB7CD-70CB-6982-216D-95BD0C4438CF'
        self.xmlns = 'http://www.fnac.com/schemas/mp-dialog.xsd'

    # 身份验证 返回token
    def authentication(self):
        url = self.url + '/auth'
        data_dict = {
            'auth': {'@xmlns': self.xmlns, 'shop_id': self.shop_id, 'partner_id': self.partner_id,
                     'key': self.key}}
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        content = self.xml_to_dict(response.text)
        self.token = content['auth_response']['token']
        return self.token

    def xml_to_dict(self, response):
        '''
        :param response: 将xml响应转化为dict
        :return:
        '''
        content = xmltodict.parse(response)
        content_str = json.dumps(content)
        new_dict = json.loads(content_str)
        return new_dict

    # 定价更新
    @outter
    def offers_update(self, l_dict, *args, **kwargs):
        """
        :param args: 接收一个字典数组
        :param kwargs:
        :return:
        """
        # self.authentication()

        data_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token}}
        li_dict = {"product_reference": {"@type": "Ean", "#text": l_dict['product_reference']},
                   "offer_reference": {"@type": "SellerSku", "#text": l_dict['offer_reference']},
                   "price": l_dict['price'],
                   "product_state": l_dict['product_state'],
                   "quantity": l_dict['quantity'], "description": l_dict['description'],
                   "adherent_price": l_dict['adherent_price'],
                   "internal_comment": l_dict['internal_comment'],
                   "showcase": l_dict['showcase'],
                   "logistic_type_id": l_dict['logistic_type_id'],
                   "time_to_ship": l_dict['time_to_ship'],
                   'promotion': {
                       '@type': l_dict['promotion-type'],
                       'sales_period_reference': l_dict['sales_period_reference'],
                       'promotion_uid': l_dict['Promotion_uid'],
                       'starts_at': l_dict['starts_at'], 'ends_at': l_dict['ends_at'],
                       'discount_type': l_dict['discount_type'],
                       'discount_value': l_dict['discount_value'],
                       'triggers': {
                           'trigger_customer_type': l_dict['trigger_customer_type'],
                       }
                   }
                   }
        for k in list(li_dict.keys()):
            if not li_dict[k]:
                del li_dict[k]
        data_dict['offers_update']['offer'] = li_dict
        xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(xml)
        response = requests.post(self.url + '/offers_update', headers=self.headers, data=xml.encode())
        print(response.text)
        if response.status_code == 200:
            batch_id = self.xml_to_dict(response.text)['offers_update_response']['batch_id']
            return batch_id
        return 400

    @outter
    def update_offer_price(self, update_dict):
        # self.authentication()
        data_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'offer': {
                                  'offer_reference': {'@type': 'SellerSku', '#text': update_dict['offer_reference']},
                                  'price': update_dict['price']
                              }
                              }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(self.url + '/offers_update', headers=self.headers, data=data_xml.encode())
        print(response.text)
        if response.status_code == 200:
            batch_id = self.xml_to_dict(response.text)['offers_update_response']['batch_id']
            return batch_id
        return 400

    @outter
    def delete_offer(self, dicts):
        # self.authentication()
        data_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'offer': {
                                  'offer_reference': {'@type': 'SellerSku', '#text': dicts['offer_reference']},
                                  'treatment': 'delete'
                              }
                              }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(self.url + '/offers_update', headers=self.headers, data=data_xml.encode())
        if response.status_code == 200:
            batch_id = self.xml_to_dict(response.text)['offers_update_response']['batch_id']
            return batch_id
        return 400

    @outter
    def batch_status(self, batch_id):
        '''
        :param batch_id: 获取批处理状态
        :return:
        '''
        # self.authentication()
        batch_dict = {
            'batch_status': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, 'batch_id': batch_id}}
        batch_xml = xmltodict.unparse(batch_dict, encoding='utf-8')
        url = self.url + '/batch_status'
        response = requests.post(url, headers=self.headers, data=batch_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dic = self.xml_to_dict(response.text)
            return response_dic
        return 400

    @outter
    def offers_query(self):
        '''
        :param qu_dict:传入一个字典
        :return:
        '''
        # self.authentication()

        dict_data = {
            'offers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 100,
                             'paging': 1}}

        # dict_data['offers_query']['promotion_types'] = {'@type': qu_dict['promotion_types']}

        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/offers_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400

    @outter
    def offers_query_date(self, qu_dict):
        '''
        :param qu_dict:传入一个字典
        :return:
        '''
        # self.authentication()
        dict_data = {
            'offers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 100,
                             'paging': 1,
                             'date': {'@type': qu_dict['date-type'], 'min': qu_dict['min'], 'max': qu_dict['max']}
                             }
        }
        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/offers_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400

    @outter
    def offers_query_quantity(self, qu_dict):
        '''
        :param qu_dict:传入一个字典
        :return:
        '''
        # self.authentication()
        dict_data = {
            'offers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 100,
                             'paging': 1}}
        dict_data['offers_query']['quantity'] = {'@mode': qu_dict['quantity-type'], '@value': qu_dict['quantity']}
        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/offers_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400

    @outter
    def batch_query(self):
        '''批次查询
        :return:返回批次列表（batch_id	来自fnac的批次唯一标识符	xs：string	0-1
                            nb_lines	要处理的行数	xs：int	0-1
                            created_at	批次的创建日期），
                正在处理的数，等待处理的批数
        '''
        # self.authentication()
        batch_dict = {
            'batch_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                            '@token': self.token}}
        batch_xml = xmltodict.unparse(batch_dict, encoding='utf-8')
        url = self.url + '/batch_query'
        response = requests.post(url, headers=self.headers, data=batch_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)

            return response_dict
        return 400


class MarketPlaceOrderApi(MarketPlaceApi):
    @outter
    def orders_update(self, update_dict):
        # self.authentication()
        ls = []
        print(update_dict['order_id'])
        if ',' in update_dict['order_id']:
            lis_id = update_dict['order_id'].split(',')
            for id in lis_id:
                ls.append({'@order_id': id, '@action': update_dict['action'],
                           'order_detail': {'action': update_dict['order_detail_action']}
                           })
        else:
            ls = {'@order_id': update_dict['order_id'], '@action': update_dict['action'],
                  'order_detail': {'action': update_dict['order_detail_action']}
                  }
        dict_data = {
            'orders_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'order': ls
                              }
        }
        data_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        print(data_xml)
        url = self.url + '/orders_update'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    @outter
    def orders_update_accept(self, update_dict):
        # self.authentication()
        dict_data = {
            'orders_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'order': {'@order_id': update_dict['order_id'], '@action': update_dict['action']},
                              'order_detail': {'action': update_dict['order_detail_action'],
                                               'tracking_number': update_dict['tracking_number'],
                                               'tracking_company': update_dict['tracking_company']
                                               }
                              }
        }
        data_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/orders_update'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    # 废弃
    @outter
    def orders_query1(self, query_dict):
        '''
        :param query_dict: 订单查询 接收一个字典
        :return:
        '''
        # self.authentication()
        order_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token, '@results_count': query_dict['results_count']}}
        order_dict['offers_update']['paging'] = query_dict['paging']
        order_dict['offers_update']['states']['state'] = query_dict['state']
        order_dict['offers_update']['date'] = {'min': query_dict['min'], 'max': query_dict['max']}
        order_dict['offers_update']['order_fnac_id'] = query_dict['order_fnac_id']
        order_xml = xmltodict.unparse(order_dict, encoding='utf-8')
        url = self.url + '/order_query'
        response = requests.post(url, headers=self.headers, data=order_xml.encode('utf-8'))
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        self.authentication()
        self.orders_query(query_dict)

    @outter
    def orders_query(self, query_dict):
        '''
                :param query_dict: 订单查询 接收一个字典
                :return:
                '''
        # self.authentication()
        order_dict = {
            'orders_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 100}}
        order_dict['orders_query']['paging'] = query_dict['paging']
        order_xml = xmltodict.unparse(order_dict, encoding='utf-8')
        url = self.url + '/orders_query'
        response = requests.post(url, headers=self.headers, data=order_xml.encode('utf-8'))
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        return 400

    @outter
    def orders_query_date(self, qu_dict):
        '''
                :param qu_dict:传入一个字典
                :return:
                '''
        # self.authentication()
        dict_data = {
            'orders_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 100,
                             'paging': qu_dict['paging'],
                             'states': {'state': qu_dict['state']},
                             'date': {'@type': qu_dict['date-type'], 'min': qu_dict['min'], 'max': qu_dict['max']}
                             }
        }
        if qu_dict['date-type'] == '':
            dict_data['orders_query'].pop('date')
        if qu_dict['state'] == 'ALL':
            dict_data['orders_query'].pop('states')
        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/orders_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400

    @outter
    def orders_query_id(self, qu_ls):
        '''
                :param qu_dict:传入一个字典
                :return:
                '''
        # self.authentication()
        dict_data = {
            'orders_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token,
                             'orders_fnac_id': {'order_fnac_id': qu_ls}
                             }
        }
        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/orders_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400


class MarketPlacePricingApi(MarketPlaceApi):
    @outter
    def pricing_query(self, query_dict):
        '''
        :param query_dict:定价查询
        :return:
        '''
        # self.authentication()
        pricing_dict = {
            'pricing_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token, '@sellers': query_dict['sellers']}}
        pricing_dict['pricing_query']['product_reference '] = {'@type': 'Ean',
                                                               '#text': query_dict['product_reference']}
        pricing_xml = xmltodict.unparse(pricing_dict, encoding='UTF-8')
        url = self.url + '/pricing_query'
        response = requests.post(url, headers=self.headers, data=pricing_xml)
        if response.status_code == 200:
            print(response.text)
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        print(response.text)
        return 400
        # self.authentication()
        # self.pricing_query(query_dict)

    @outter
    def carriers_query(self):

        # self.authentication()
        pricing_dict = {
            'carriers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                               '@token': self.token, 'query': 'all'}}
        pricing_xml = xmltodict.unparse(pricing_dict, encoding='UTF-8')
        url = self.url + '/carriers_query'
        response = requests.post(url, headers=self.headers, data=pricing_xml)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        print(response.text)
        return 400


class ClientOrderApi(MarketPlaceApi):
    # 废弃
    @outter
    def client_order_query1(self, client_query):
        '''
        客户订单评论查询
        :param client_query:
        :return:
        '''
        # self.authentication()
        client_dict = {
            'client_order_comments_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                            '@partner_id': self.partner_id,
                                            '@token': self.token, '@results_count': client_query['results_count']}}
        client_dict['client_order_comments_query']['paging'] = client_query['paging']
        client_dict['client_order_comments_query']['date'] = {'@type': client_query['type'], 'min': client_query['min'],
                                                              'max': client_query['max']}
        client_dict['client_order_comments_query']['client_order_comment_id'] = client_query['client_order_comment_id']
        client_dict['client_order_comments_query']['order_fnac_id'] = client_query['order_fnac_id']
        client_xml = xmltodict.unparse(client_dict, encoding='utf-8')
        url = self.url + '/client_order_comments_query'
        response = requests.post(url, headers=self.headers, data=client_xml.encode('utf-8'))
        if response.status_code == 200:
            print(response.text)
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        print(response.text)
        return 400

    @outter
    def client_order_query(self, client_query):
        '''
        客户订单评论查询
        :param client_query:
        :return:
        '''
        # self.authentication()
        client_dict = {
            'client_order_comments_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                            '@partner_id': self.partner_id,
                                            '@token': self.token, '@results_count': '50',
                                            'paging': client_query['paging']}}
        client_xml = xmltodict.unparse(client_dict, encoding='utf-8')
        url = self.url + '/client_order_comments_query'
        response = requests.post(url, headers=self.headers, data=client_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        response_dict = self.xml_to_dict(response.text)
        return 400
        # return response_dict['client_order_comments_query_response']['error']['#text']

    @outter
    def client_order_query_id(self, client_query):
        '''
        客户订单评论查询
        :param client_query:
        :return:
        '''
        # self.authentication()
        client_dict = {
            'client_order_comments_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                            '@partner_id': self.partner_id,
                                            '@token': self.token, 'order_fnac_id': client_query['order_fnac_id']}}
        client_xml = xmltodict.unparse(client_dict, encoding='utf-8')
        url = self.url + '/client_order_comments_query'
        response = requests.post(url, headers=self.headers, data=client_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        response_dict = self.xml_to_dict(response.text)
        return 400
        # return response_dict['client_order_comments_query_response']['error']['#text']

    @outter
    def client_order_query_date(self, client_query):
        '''
        客户订单评论查询
        :param client_query:
        :return:
        '''
        # self.authentication()
        client_dict = {
            'client_order_comments_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                            '@partner_id': self.partner_id,
                                            '@token': self.token, '@results_count': client_query['results_count'],
                                            'paging': client_query['paging'],
                                            'date': {'@type': client_query['date-type'], 'min': client_query['min'],
                                                     'max': client_query['max']}
                                            }
        }
        client_xml = xmltodict.unparse(client_dict, encoding='utf-8')
        url = self.url + '/client_order_comments_query'
        response = requests.post(url, headers=self.headers, data=client_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        response_dict = self.xml_to_dict(response.text)
        return 400
        # return response_dict['client_order_comments_query_response']['error']['#text']

    @outter
    def client_order_comments_update(self, client_query):
        '''
        客户订单评论更新
        :param client_query:
        :return:
        '''
        # self.authentication()
        client_dict = {
            'client_order_comments_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                             '@partner_id': self.partner_id,
                                             '@token': self.token,
                                             'comment': {'@id': client_query['id'],
                                                         'comment_reply': client_query['comment_reply']}
                                             }
        }
        client_xml = xmltodict.unparse(client_dict, encoding='utf-8')
        url = self.url + '/client_order_comments_update'
        response = requests.post(url, headers=self.headers, data=client_xml.encode('utf-8'))
        print(response.text)
        if response == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        return 400

    @outter
    def carriers_query(self):
        '''
        运营商查询
        :return:
        '''
        # self.authentication()
        carriers_dict = {
            'carriers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                               '@partner_id': self.partner_id,
                               '@token': self.token, 'query': 'all'}}
        carriers_xml = xmltodict.unparse(carriers_dict, encoding='utf-8')
        url = self.url + '/carriers_query'
        response = requests.post(url, headers=self.headers, data=carriers_xml.encode('UTF-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        return 400


class IncidentsApi(MarketPlaceApi):
    # 废弃
    @outter
    def incidents_query1(self, query_dict):
        # self.authentication()
        data_dict = {
            'incidents_query ': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                 '@partner_id': self.partner_id,
                                 '@token': self.token, '@results_count': query_dict['results_count'],
                                 'paging': query_dict['paging'],
                                 'date': {'@type': query_dict['date_type'], 'min': query_dict['min'],
                                          'max': query_dict['max']},
                                 'status': query_dict['status'], 'types': {'type': query_dict['type']},
                                 'incidents_id': {'incident_id': query_dict['incident_id']},
                                 'closed_statuses': {'closed_status': query_dict['closed_status']},
                                 'waiting_for_seller_answer': query_dict['waiting_for_seller_answer'],
                                 'opened_by': query_dict['opened_by'], 'closed_by': query_dict['closed_by'],
                                 'sort_by': query_dict['sort_by'],
                                 'orders': {'order': query_dict['order']}
                                 }
        }

        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(data_xml)
        url = self.url + '/incidents_query'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return 400

    @outter
    def incidents_query(self, query_dict):
        # self.authentication()
        data_dict = {
            'incidents_query ': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                 '@partner_id': self.partner_id,
                                 '@token': self.token, '@results_count': query_dict['results_count'],
                                 'paging': query_dict['paging'],
                                 'date': {'@type': query_dict['date_type'], 'min': query_dict['min'],
                                          'max': query_dict['max']},
                                 }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(data_xml)
        url = self.url + '/incidents_query'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return 400

    @outter
    def incidents_update(self, update_dict):
        # self.authentication()
        data_dict = {
            'incidents_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id,
                                 '@partner_id': self.partner_id,
                                 '@token': self.token,
                                 'order': {'@order_id': update_dict['order_id'], '@action': 'refund',
                                           'order_detail': {
                                               'order_detail_id': update_dict['order_detail_id'],
                                               'refund_reason': update_dict['refund_reason']
                                           }}
                                 }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        url = self.url + '/incidents_update'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return 400


if __name__ == '__main__':
    # mark1 = ClientOrderApi()
    # mark1.client_order_query({'results_count': '3', 'paging': '1'})
    # id = mark1.carriers_query()
    # print(id)
    mark = MarketPlaceApi()
    mark.authentication()
    # mark.batch_query()
    # marks = MarketPlacePricingApi()
    # id = marks.pricing_query({'sellers': 'all', 'product_reference': '0886971942323'})
    # print(id)
    # mark.batch_status('98449C05-3928-F0ED-D7E8-E6D70A3B9E5A')
    # id = mark.offers_query(
    #     {'results_count': '3', 'paging': '1', 'min': '2019-11-04T14:15:38+01:00', 'max': '2019-12-04T14:15:38+01:00'})
    # print(id)
    # id = mark.offers_update([{'product_reference': '12', 'offer_reference': 'DAS', 'price': '25', 'product_state': '11',
    #                           'quantity': '2', 'description': 'das', 'showcase': '2'},
    #                          {'product_reference': '23', 'offer_reference': 'DAS', 'price': '25', 'product_state': '11',
    #                           'quantity': '3', 'description': 'das', 'showcase': '1'}])
    # print(id)
    # mark.offers_query()
