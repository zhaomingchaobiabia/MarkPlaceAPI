import datetime
import json
import requests
from .market_api import outter
from markerplace.market_api import MarketPlaceApi, MarketPlacePricingApi, MarketPlaceOrderApi, ClientOrderApi, \
    IncidentsApi
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .offer_sql import Sql
import xmltodict
import time
from django.core.paginator import Paginator
# from apscheduler.scheduler import Scheduler
from time import sleep

mark = MarketPlaceApi()
mark_order = MarketPlaceOrderApi()
mark_query = MarketPlacePricingApi()
client = ClientOrderApi()
incident = IncidentsApi()

sql = Sql()


def fault_decorator(func):
    func = func

    def inner(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return render(request, 'test/404.html')

    return inner


@fault_decorator
# Create your views here.
def index(request):
    return render(request, 'test/dashboard.html')


@csrf_exempt
@fault_decorator
def offers_update(request):
    if request.method == 'GET':
        return render(request, 'test/profile.html')
    if request.method == 'POST':
        dict_data = request.POST
        dic_da = {}
        dic_da['product_reference'] = dict_data.get('product_reference')
        dic_da['offer_reference'] = dict_data.get('offer_reference')
        dic_da['price'] = dict_data.get('price')
        dic_da['product_state'] = dict_data.get('product_state')
        dic_da['quantity'] = dict_data.get('quantity')
        dic_da['description'] = dict_data.get('description')
        dic_da['showcase'] = dict_data.get('showcase')
        dic_da['adherent_price'] = dict_data.get('adherent_price')
        dic_da['internal_comment'] = dict_data.get('internal_comment')
        dic_da['logistic_type_id'] = dict_data.get('logistic_type_id')
        dic_da['promotion-type'] = dict_data.get('promotion-type')
        dic_da['starts_at'] = dict_data.get('starts_at') + 'T00:00:00+02:00'
        dic_da['ends_at'] = dict_data.get('ends_at') + 'T23:59:00+02:00'
        dic_da['discount_type'] = dict_data.get('discount_type')
        dic_da['discount_value'] = dict_data.get('discount_value')
        dic_da['trigger_customer_type'] = dict_data.get('trigger_customer_type')
        dic_da['time_to_ship'] = dict_data.get('time_to_ship')
        dic_da['Promotion_uid'] = dict_data.get('Promotion_uid')
        dic_da['sales_period_reference'] = dict_data.get('sales_period_reference')
        batch_id = mark.offers_update(dic_da)
        # request.session['batch_id'] = batch_id
        # return redirect(batch_query_offer, {'batch_id': batch_id})
        return render(request, 'test/profile.html', {'batch_id': batch_id})


@csrf_exempt
@fault_decorator
def batch_status(request):
    if request.method == 'GET':
        return render(request, 'test/batch.html')
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        status = mark.batch_status(batch_id)['batch_status_response']
        try:
            status['status'] = status['@status']
            status['offer']['status'] = status['offer']['@status']
        except:
            status['status'] = ''
            status['offer']['status'] = ''
        try:
            status['offer']['error']['text'] = status['offer']['error']['#text']
        except:
            pass
        # print(status)
        return render(request, 'test/batch.html', {'dict_status': status})


@csrf_exempt
@fault_decorator
def offers_query(request):
    if request.method == 'GET':
        # data_dict = mark.offers_query()['offers_query_response']['offer']
        sql = 'select * from offers'
        result = Offers.objects.raw(sql)
        ls = []
        try:
            for data in result:
                # print(data)
                ls.append([data.image, data.product_name, data.offer_seller_id, data.price, data.quantity,
                           data.starts_at, data.ends_at, data.pro_price, data.is_shipping_free, data.product_url])
        except:
            ls = []
        if len(ls) == 0:
            ls = ''
        p = Paginator(ls, 10)
        page = int(request.GET.get("page")) if request.GET.get("page") else 1
        # 返回页面所需要的数据
        data = p.get_page(page)
        return render(request, 'test/offers_query.html', {'data_dict_ls': data, 'ls': len(ls), 'page': page})

    # return render(request, 'test/basic-table.html', {'data_dict_ls': data_dict['offers_query_response']['offer']})


@csrf_exempt
@fault_decorator
def offers_query_date(request):
    data = request.GET
    dict_d = {}
    dict_d['paging'] = int(request.GET.get("paging")) if request.GET.get("paging") else 1
    # dict_d['paging'] = data.get('paging')
    dict_d['date-type'] = data.get('date-type')
    # print(type(data.get('min')))
    dict_d['min'] = data.get('min') + 'T00:00:00'
    dict_d['max'] = data.get('max') + 'T00:00:00'
    # print(dict_d['max'])
    data_dict_l = mark.offers_query_date(dict_d)['offers_query_response']
    print(data_dict_l)
    num = data_dict_l['nb_total_result']
    page = data_dict_l['page']
    total_page = data_dict_l['total_paging']
    try:
        data_dict = data_dict_l['offer']
        print(data_dict)
    except:
        data_dict = ''
        # ls 总条数  page  当前页面   total_page  总页码
        return render(request, 'test/offer_query_time.html',
                      {'data_dict_ls': data_dict, 'ls': num, 'page': int(page), 'total_page': int(total_page),
                       'date_type': dict_d['date-type'],
                       'min': data.get('min'),
                       'max': data.get('max'), })
    if type(data_dict) is list:
        da_dict = {'data_dict_ls': data_dict, 'ls': num, 'date_type': dict_d['date-type'], 'min': data.get('min'),
                   'max': data.get('max'), 'page': int(page), 'total_page': int(total_page)}
        print(da_dict)
        return render(request, 'test/offer_query_time.html', da_dict)
    ls = []
    ls.append(data_dict)
    return render(request, 'test/offer_query_time.html',
                  {'data_dict_ls': ls, 'ls': num, 'page': int(page), 'total_page': int(total_page),
                   'date_type': dict_d['date-type'],
                   'min': data.get('min'),
                   'max': data.get('max')})


@csrf_exempt
@fault_decorator
def offers_query_quantity(request):
    data = request.GET
    # print(data)
    dict_d = {}
    # dict_d['paging'] = data.get('paging')
    quantity_type = data.get('quantity_type')
    quantity = data.get('quantity')
    dic_fla = {'Equals': '=', 'LessThan': '<',
               'GreaterThan': '<', 'LessThanOrEquals': '<=',
               'GreaterThanOrEquals': '>='}
    sql = f'select * from offers where quantity {dic_fla[quantity_type]} %s '
    result = Offers.objects.raw(sql, params=(quantity,))
    ls = []
    try:
        for data in result:
            # print(data)
            ls.append([data.image, data.product_name, data.offer_seller_id, data.price, data.quantity,
                       data.starts_at, data.ends_at, data.pro_price, data.is_shipping_free, data.product_url])
    except:
        ls = []
    if len(ls) == 0:
        ls = ''
    p = Paginator(ls, 10)
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    # 返回页面所需要的数据
    data = p.get_page(page)
    dicts = {'data_dict_ls': data, 'quantity_type': quantity_type,
             'quantity': quantity, 'ls': len(ls), 'page': page}
    return render(request, 'test/offer_query_quantity.html', dicts)


# try:
#     data_dict = mark.offers_query_quantity(dict_d)['offers_query_response']['offer']
# except:
#     data_dict = ''
#     return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
# if type(data_dict) is list:
#     return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
# ls = []
# ls.append(data_dict)

@csrf_exempt
@fault_decorator
def batch_query(request):
    if request.method == 'GET':
        data = mark.batch_query()
        return render(request, 'batch_query.html', {'data_dict': data})


@csrf_exempt
@fault_decorator
def orders_query(request):
    dicts = {}
    page = int(request.GET.get('paging')) if request.GET.get('paging') else 1
    dicts['paging'] = page
    print(dicts)
    data_dict_ls = mark_order.orders_query(dicts)['orders_query_response']
    total_page = data_dict_ls['total_paging']
    nb_total_result = data_dict_ls['nb_total_result']
    print(data_dict_ls)
    try:
        data_dict = data_dict_ls['order']
    except:
        data_dict = ''
        return render(request, 'test/orders.html',
                      {'data_dict_ls': data_dict, 'page': int(page), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result})
    if type(data_dict) is list:
        return render(request, 'test/orders.html',
                      {'data_dict_ls': data_dict, 'page': int(page), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result})
    ls = []
    ls.append(data_dict)
    return render(request, 'test/orders.html',
                  {'data_dict_ls': data_dict, 'page': int(page), 'total_page': int(total_page),
                   'nb_total_result': nb_total_result})


@csrf_exempt
# @fault_decorator
def orders_query_date(request):
    data = request.GET
    dict_d = {}
    dict_d['paging'] = data.get('paging') if data.get('paging') else 1
    dict_d['date-type'] = data.get('date-type')
    # print(type(data.get('min')))
    if data.get('min') == '' or data.get('max') == '':
        dict_d['date-type'] = ''
        dict_d['min'] = ''
        dict_d['max'] = ''
    else:
        dict_d['min'] = data.get('min') + 'T00:00:00'
        dict_d['max'] = data.get('max') + 'T23:59:59'
    dict_d['state'] = data.get('state')
    # print(dict_d['max'])
    print(dict_d)

    data_dict_ls = mark_order.orders_query_date(dict_d)['orders_query_response']
    page = data_dict_ls['page']
    total_page = data_dict_ls['total_paging']
    nb_total_result = data_dict_ls['nb_total_result']
    print(data_dict_ls)
    try:
        data_dict = data_dict_ls['order']
    except:
        data_dict = ''
        return render(request, 'test/orders_time.html',
                      {'data_dict_ls': data_dict, 'page': int(page), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result, 'date_type': data.get('date-type'), 'min': data.get('min'),
                       'max': data.get('max'), 'state': dict_d['state']})
    if type(data_dict) is list:
        return render(request, 'test/orders_time.html',
                      {'data_dict_ls': data_dict, 'page': int(page), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result, 'date_type': data.get('date-type'),
                       'min': data.get('min'),
                       'max': data.get('max'), 'state': dict_d['state']})
    ls = []
    ls.append(data_dict)
    return render(request, 'test/orders_time.html',
                  {'data_dict_ls': ls, 'page': int(page), 'total_page': int(total_page),
                   'nb_total_result': nb_total_result,
                   'date_type': data.get('date-type'), 'min': data.get('min'),
                   'max': data.get('max'), 'state': dict_d['state']})


@csrf_exempt
@fault_decorator
def orders_query_id(request):
    data = request.POST
    id = data.get('orders_fnac_id')
    if ',' in id:
        ls_id = id.split(',')
    else:
        ls_id = id
    try:
        data_dict = mark_order.orders_query_id(ls_id)['orders_query_response']['order']
    except:
        data_dict = ''
        return render(request, 'test/orders_id.html', {'data_dict_ls': data_dict})
    if type(data_dict) is list:
        return render(request, 'test/orders_id.html', {'data_dict_ls': data_dict})
    else:
        ls = []
        ls.append(data_dict)
        return render(request, 'test/orders_id.html', {'data_dict_ls': ls})


@csrf_exempt
@fault_decorator
def orders_update(request):
    if request.method == 'GET':
        return render(request, 'test/orders_update.html')
    if request.method == 'POST':
        data = request.POST
        dict_data = {}
        dict_data['order_id'] = data.get('orders_id')
        dict_data['action'] = data.get('action')
        dict_data['id1'] = data.get('id1')
        dict_data['order_detail_action1'] = data.get('order_detail_action1')
        if data.get('id2') is None:
            dict_data['id2'] = ''
            dict_data['order_detail_action2'] = ''
        else:
            dict_data['id2'] = data.get('id2')
            dict_data['order_detail_action2'] = data.get('order_detail_action2')

        # print(data.get('id1'), data.get('order_detail_action1'))
        # print(data.get('id2'), data.get('order_detail_action2'))

        data = mark_order.orders_update_one(dict_data)['orders_update_response']['order']
        if type(data) is list:
            return render(request, 'test/orders_update.html', {'data_dict_ls': data})
        ls = []
        ls.append(data)
        return render(request, 'test/orders_update.html', {'data_dict_ls': ls})


@csrf_exempt
@fault_decorator
def orders_update_accept(request):
    if request.method == 'GET':
        return render(request, 'order_update.html')
    if request.method == 'POST':
        data = request.POST
        dict_data = {}
        dict_data['order_id'] = data.get('order_id')
        dict_data['action'] = data.get('action')
        dict_data['order_detail_action'] = data.get('order_detail_action')
        dict_data['tracking_number'] = data.get('tracking_number')
        dict_data['tracking_company'] = data.get('tracking_company')
        data = mark_order.orders_update_accept(dict_data)
        return render(request, 'order_update.html', {'data': data})


@csrf_exempt
@fault_decorator
def carriers_query(request):
    data = mark_query.carriers_query()['carriers_query_response']['carrier']
    return render(request, 'test/sales_peoriods_query.html', {'data': data})


@csrf_exempt
@fault_decorator
def order_comments_query(request):
    paging = request.GET.get('paging') if request.GET.get('paging') else 1
    dict_data = client.client_order_query(paging)['client_order_comments_query_response']
    print(dict_data)
    total_page = dict_data['total_paging']
    nb_total_result = dict_data['nb_total_result']
    try:
        client_order_comment = dict_data['client_order_comment']
    except:
        client_order_comment = ''
        return render(request, 'test/order_comments.html',
                      {'total_page': int(total_page), 'page': int(paging), 'nb_total_result': nb_total_result,
                       'client_order_comment': client_order_comment})
    if type(client_order_comment) is list:
        return render(request, 'test/order_comments.html',
                      {'total_page': int(total_page), 'page': int(paging), 'nb_total_result': nb_total_result,
                       'client_order_comment': client_order_comment})
    ls = []
    ls.append(client_order_comment)
    return render(request, 'test/order_comments.html',
                  {'total_page': int(total_page), 'page': int(paging), 'nb_total_result': nb_total_result,
                   'client_order_comment': ls})


@csrf_exempt
@fault_decorator
def order_comments_query_date(request):
    if request.method == 'GET':
        data = request.GET
        paging = data.get('paging') if data.get('paging') else 1
        dict_d = {'paging': paging, 'results_count': 20,
                  'date-type': data.get('date-type'), 'min': data.get('min'),
                  'max': data.get('max')}
        dict_data = client.client_order_query_date(dict_d)['client_order_comments_query_response']
        total_page = dict_data['total_paging']
        nb_total_result = dict_data['nb_total_result']
        try:
            client_order_comment = dict_data['client_order_comment']
        except:
            client_order_comment = ''
            return render(request, 'test/order_comment_time.html',
                          {'date_type': data.get('date-type'), 'min': data.get('min'), 'max': data.get('max'),
                           'total_page': int(total_page), 'page': int(paging),
                           'nb_total_result': nb_total_result,
                           'client_order_comment': client_order_comment})
        if type(client_order_comment) is list:
            return render(request, 'test/order_comment_time.html',
                          {'date_type': data.get('date-type'), 'min': data.get('min'), 'max': data.get('max'),
                           'total_page': int(total_page), 'page': int(paging), 'nb_total_result': nb_total_result,
                           'client_order_comment': client_order_comment})
        ls = []
        ls.append(client_order_comment)
        return render(request, 'test/order_comment_time.html',
                      {'date_type': data.get('date-type'), 'min': data.get('min'), 'max': data.get('max'),
                       'total_page': int(total_page), 'page': int(paging), 'nb_total_result': nb_total_result,
                       'client_order_comment': ls})


@csrf_exempt
@fault_decorator
def order_comments_query_id(request):
    if request.method == 'POST':
        data = request.POST
        dict_d = {'order_fnac_id': data.get('order_fnac_id')}
        ls = []
        try:
            data_dict = client.client_order_query_id(dict_d)['client_order_comments_query_response'][
                'client_order_comment']
            ls.append(data_dict)
        except:
            ls = ''
        return render(request, 'test/order_comment_id.html', {'client_order_comment': ls})


@csrf_exempt
@fault_decorator
def client_order_comments_update(request):
    if request.method == 'GET':
        return render(request, 'client_order_comments_update.html')
    if request.method == 'POST':
        data = request.POST
        data_dict = {'id': data.get('id'), 'comment_reply': data.get('comment_reply')}
        try:
            datas = client.client_order_comments_update(data_dict)['client_order_comments_update_response']['comment']
            data = datas['@status']
        except:
            data = 'error'
        return render(request, 'test/order_comments.html', {'data': data})


# 废弃
@csrf_exempt
@fault_decorator
def incidents_query1(request):
    if request.method == 'GET':
        return render(request, 'incidents_query.html')
    if request.method == 'POST':
        data = request.POST
        incident_id = data.get('incident_id')
        incident_id = incident_id.split(',')
        order = data.get('order')
        order = order.split(',')
        if data.get('min') != '':
            min = data.get('min') + ':00'
            max = data.get('max') + ':00'
        else:
            min = ''
            max = ''
        data_dict = {
            'results_count': data.get('results_count'), 'paging': data.get('paging'),
            'date_type': data.get('date-type'), 'min': min, 'max': max, 'status': data.get('status'),
            'type': data.getlist('type'), 'incident_id': incident_id, 'closed_status': data.getlist('closed_status'),
            'waiting_for_seller_answer': data.get('waiting_for_seller_answer'), 'opened_by': data.get('opened_by'),
            'closed_by': data.get('closed_by'), 'sort_by': data.get('sort_by'), 'order': order
        }
        # print(data_dict)
        data = incident.incidents_query(data_dict)
        return render(request, 'incidents_query.html', {'data': data})


# 废弃
@csrf_exempt
# @fault_decorator
def incidents_query(request):
    datas = request.GET
    paging = request.GET.get('paging') if request.GET.get('paging') else 1
    print(paging)
    print(datas.get('min'))
    if datas.get('min') is None or datas.get('max') is None:
        return render(request, 'test/incidents_des.html')

    elif datas.get('min') == '' or datas.get('max') == '':
        return render(request, 'test/incidents_des.html')
    else:
        min = datas.get('min') + 'T00:00:00'
        max = datas.get('max') + 'T23:59:59'
        data_dict = {
            'paging': paging,
            'date_type': datas.get('date-type'), 'min': min, 'max': max,
        }
    print(data_dict)

    data_dict_ls = incident.incidents_query(data_dict)['incidents_query_response']
    print(datas)
    total_page = data_dict_ls['total_paging']
    nb_total_result = data_dict_ls['nb_total_result']
    try:
        data = data_dict_ls['incident']
        if type(data) is list:
            for da in data:
                if not type(da['order_details_incident']['order_detail_incident']) is list:
                    da['order_details_incident']['order_detail_incident'] = [
                        da['order_details_incident']['order_detail_incident'], ]

            return render(request, 'test/incidents.html',
                          {'dict_data_ls': data, 'date_type': datas.get('date-type'), 'min': datas.get('min'),
                           'max': datas.get('max'),
                           'total_page': int(total_page),
                           'nb_total_result': nb_total_result, 'page': int(paging)})
        ls = []
        if type(data['order_details_incident']['order_detail_incident']) is not list:
            data['order_details_incident']['order_detail_incident'] = [
                data['order_details_incident']['order_detail_incident'], ]
        ls.append(data)
        return render(request, 'test/incidents.html',
                      {'dict_data_ls': data, 'date_type': datas.get('date-type'), 'min': datas.get('min'),
                       'max': datas.get('max'),
                       'total_page': int(total_page),
                       'nb_total_result': nb_total_result, 'page': int(paging)})
    except:
        return render(request, 'test/incidents.html',
                      {'dict_data_ls': '', 'date_type': datas.get('date-type'), 'min': datas.get('min'),
                       'max': datas.get('max'),
                       'total_page': int(total_page),
                       'nb_total_result': nb_total_result, 'page': int(paging)})


@csrf_exempt
@fault_decorator
def incident_update(request):
    if request.method == 'GET':
        return render(request, 'incident_update.html')
    if request.method == 'POST':
        data = request.POST
        data_dict = {'order_id': data.get('order_id'), 'order_detail_id': data.get('order_detail_id'),
                     'refund_reason': data.get('refund_reason')}

        data = incident.incidents_update(data_dict)
        return render(request, 'incident_update.html', {'data': data})


@fault_decorator
def order(request, param1):
    data_dict = mark_order.orders_query_id(param1)['orders_query_response']['order']['order_detail']
    if type(data_dict) is list:
        return render(request, 'order_query_show.html', {'data_dict': data_dict})
    ls = []
    ls.append(data_dict)
    return render(request, 'order_query_show.html', {'data_dict': ls})


@fault_decorator
def order_shop(request, param1):
    data_dict = mark_order.orders_query_id(param1)['orders_query_response']['order']
    ship_data = data_dict['shipping_address']
    try:
        bill_data = data_dict['billing_address']
    except:
        bill_data = ''
    return render(request, 'order_query_shop.html', {'ship_data': ship_data, 'bill_data': bill_data})


@csrf_exempt
@fault_decorator
def delete_offer(request):
    if request.method == 'POST':
        data = request.POST
        data_dict = {'offer_reference': data.get('offer_reference')}
        batch_id = mark.delete_offer(data_dict)
        return render(request, 'test/profile.html', {'batch_id': batch_id})


@csrf_exempt
@fault_decorator
def update_offer_price(request):
    if request.method == 'POST':
        data = request.POST
        data_dict = {
            'offer_reference': data.get('offer_reference'),
            'price': data.get('price'),
            'quantity': data.get('quantity')
        }

        batch_id = mark.update_offer_price(data_dict)
        time.sleep(1)
        status = mark.batch_status(batch_id)['batch_status_response']
        # print(status)
        try:
            status['status'] = status['@status']
            status['offer']['status'] = status['offer']['@status']
        except:
            status['status'] = ''
            status['offer']['status'] = ''
        try:
            status['offer']['error']['text'] = status['offer']['error']['#text']
            status['offer']['product_fnac_id'] = ''
            status['offer']['offer_fnac_id'] = ''
        except:
            # pass
            status['offer']['error'] = {'text': ''}
        print(status)
        return JsonResponse(status)
        # return render(request, 'test/offers_query.html', {'dict_status': status})

        # data_dict = mark.batch_status({'batch_id': batch_id})
        # return render(request, 'test/offers_query.html', {'batch_id': batch_id})


@csrf_exempt
@fault_decorator
def batch_query_offer(request, param1):
    status = mark.batch_status(param1)['batch_status_response']
    try:
        status['status'] = status['@status']
        status['offer']['status'] = status['offer']['@status']
    except:
        status['status'] = ''
        status['offer']['status'] = ''
    try:
        status['offer']['error']['text'] = status['offer']['error']['#text']
    except:
        pass
    # print(status)
    # return JsonResponse(status)
    return render(request, 'test/profile.html', {'dict_status': status})


@csrf_exempt
@fault_decorator
# def offers_query_price(request):
#     data = request.GET
#     min_p = int(data.get('min_p'))
#     max_p = int(data.get('max_p'))
#     datas = sql.price(min_p, max_p)
#     if len(datas) == 0:
#         datas = ''
#     p = Paginator(datas, 10)
#     page = int(data.get("page")) if data.get("page") else 1
#     # 返回页面所需要的数据
#     data = p.get_page(page)
#     # data_dict = mark.offers_query(paging)['offers_query_response']['offer']
#     # if type(data_dict) is list:
#     #     lis = []
#     #     for index in range(len(data_dict)):
#     #         if min_p <= float(data_dict[index]['price']) <= max_p:
#     #             lis.append(data_dict[index])
#     #     return render(request, 'test/offers_query.html', {'data_dict_ls': lis})
#     # ls = []
#     # if min_p <= float(data_dict['price']) <= max_p:
#     #     ls.append(data_dict)
#
#     return render(request, 'test/offer_query-price.html', {'data_dict_ls': data, 'min_p': min_p, 'max_p': max_p})

@csrf_exempt
@fault_decorator
def search_name(request, param1):
    sql = 'select * from offers where product_name like %s'
    result = Offers.objects.raw(sql, params=(f'%{param1}%',))
    ls = []
    try:
        for data in result:
            # print(data)
            ls.append([data.image, data.product_name, data.offer_seller_id, data.price, data.quantity,
                       data.starts_at, data.ends_at, data.pro_price, data.is_shipping_free, data.product_url])
    except:
        ls = []
    if len(ls) == 0:
        ls = ''
    p = Paginator(ls, 10)
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    # 返回页面所需要的数据
    data = p.get_page(page)
    return render(request, 'test/offer_query_name.html',
                  {'data_dict_ls': data, 'ls': len(ls), 'page': page})


@csrf_exempt
@fault_decorator
def order_change(request):
    if request.method == 'POST':
        val = request.POST.get('order_id')
        try:
            detail = mark_order.orders_query_id(val)['orders_query_response']['order']['order_detail']
            if type(detail) is list:
                return JsonResponse({'len': len(detail)})
            return JsonResponse({'len': 1})
        except:
            return JsonResponse({'len': 'error'})


from .models import Offers


@csrf_exempt
@fault_decorator
def offers_query_price(request):
    min_p = request.GET.get('min_p')
    max_p = request.GET.get('max_p')
    offers = Offers()
    print(11)
    sql = 'select * from offers where price-pro_price > %s and price-pro_price < %s'
    result = Offers.objects.raw(sql, params=(min_p, max_p))
    ls = []
    try:
        for data in result:
            # print(data)
            ls.append([data.image, data.product_name, data.offer_seller_id, data.price, data.quantity,
                       data.starts_at, data.ends_at, data.pro_price, data.is_shipping_free, data.product_url])
    except:
        ls = []
    if len(ls) == 0:
        ls = ''
    p = Paginator(ls, 10)
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    # 返回页面所需要的数据
    data = p.get_page(page)
    return render(request, 'test/offer_query-price.html',
                  {'data_dict_ls': data, 'min_p': min_p, 'max_p': max_p, 'ls': len(ls), 'page': page})


@csrf_exempt
@fault_decorator
def offers_query_sort(request):
    sort = request.GET.get('sort')
    result = Offers.objects.filter(sort=sort)
    ls = []
    print(result)
    try:
        for data in result:
            # print(data)
            ls.append([data.image, data.product_name, data.offer_seller_id, data.price, data.quantity,
                       data.starts_at, data.ends_at, data.pro_price, data.is_shipping_free, data.product_url])
    except:
        ls = []
    if len(ls) == 0:
        ls = ''
    p = Paginator(ls, 10)
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    # 返回页面所需要的数据
    data = p.get_page(page)
    return render(request, 'test/offer_query-sort.html',
                  {'data_dict_ls': data, 'sort': sort, 'ls': len(ls), 'page': page})


@csrf_exempt
@fault_decorator
def offers_query_id(request):
    data = request.POST.get('seller_id')
    data_dict_ls = mark.offers_query_id(data)['offers_query_response']
    print(data_dict_ls)
    try:
        data_dict_l = data_dict_ls['offer']
    except:
        return render(request, 'test/offer_query_id.html', {'data_dict_ls': ''})
    if type(data_dict_l) is list:
        da_dict = {'data_dict_ls': data_dict_l}
        print(da_dict)
        return render(request, 'test/offer_query_id.html', {'data_dict_ls': da_dict})
    ls = []
    ls.append(data_dict_l)
    return render(request, 'test/offer_query_id.html', {'data_dict_ls': ls})
