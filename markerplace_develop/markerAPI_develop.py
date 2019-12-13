from markerplace.market_api import MarketPlaceApi
from markerplace.market_api import outter
import xmltodict
import requests


class SalesPeriodsApi(MarketPlaceApi):
    @outter
    def sales_periods_query(self, query_dict):
        # self.authentication()
        data_dict = {
            'sales_periods_query':
                {
                    '@xmlns': self.xmlns, '@shop_id': self.shop_id,
                    '@partner_id': self.partner_id,
                    '@token': self.token, '@results_count': 50,
                    'paging': query_dict['paging'],
                    'date': {'@type': query_dict['date_type'], 'min': query_dict['min'],
                             'max': query_dict['max']},
                    'reference': query_dict['reference']
                }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        url = self.url + '/sales_periods_query'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    # 定价查询
    @outter
    def pricing_query(self, query_dict):
        # self.authentication()
        data_dict = {
            'pricing_query':
                {
                    '@xmlns': self.xmlns, '@shop_id': self.shop_id,
                    '@partner_id': self.partner_id,
                    '@token': self.token, '@sellers': query_dict['sellers'],
                    'product_reference': {'@type': query_dict['reference_type'],
                                          '#text': query_dict['reference']}
                }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(data_xml)
        url = self.url + '/pricing_query'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    @outter
    def messages_query(self, query_dict):
        # self.authentication()
        data_dict = {
            'messages_query':
                {
                    '@xmlns': self.xmlns, '@shop_id': self.shop_id,
                    '@partner_id': self.partner_id,
                    '@token': self.token, '@results_count': 50,
                    'paging': query_dict['paging'],
                    'date': {'@type': query_dict['date_type'], 'min': query_dict['min'] + 'T00:00:00',
                             'max': query_dict['max'] + 'T23:59:59'}
                }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(data_xml)
        url = self.url + '/messages_query'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    @outter
    def messages_query_type(self, query_dict):
        # self.authentication()
        data_dict = {
            'messages_query':
                {
                    '@xmlns': self.xmlns, '@shop_id': self.shop_id,
                    '@partner_id': self.partner_id,
                    '@token': self.token, 'message_type': query_dict['message_type'],
                    'message_archived': query_dict['message_archived'],
                    'message_state': query_dict['message_state'],
                    # 'sort_by': {'@type': query_dict['sort_type']},
                    # 'message_from_types': query_dict['message_from_types']
                }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(data_xml)
        url = self.url + '/messages_query'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    @outter
    def messages_update(self, update_dict):
        # self.authentication()
        data_dict = {
            'messages_update':
                {
                    '@xmlns': self.xmlns, '@shop_id': self.shop_id,
                    '@partner_id': self.partner_id,
                    '@token': self.token,
                    'message': [{'@action': update_dict['action'], "@id": update_dict['id']},
                                {'@action': update_dict['action1'], '@id': update_dict['id'],
                                 'message_to': update_dict['message_to'],
                                 'message_subject': update_dict['message_subject'],
                                 'message_description': update_dict['message_description'],
                                 'message_type': update_dict['message_type']}
                                ]
                }
        }
        url = self.url + '/messages_update'
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code