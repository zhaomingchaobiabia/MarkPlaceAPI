from markerplace.market_api import MarketPlaceApi, MarketPlacePricingApi, MarketPlaceOrderApi, ClientOrderApi, \
    IncidentsApi
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import time
import math

mark = MarketPlaceApi()
mark_order = MarketPlaceOrderApi()
mark_query = MarketPlacePricingApi()
client = ClientOrderApi()
incident = IncidentsApi()


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
        print(status)
        return render(request, 'test/batch.html', {'dict_status': status})


@csrf_exempt
@fault_decorator
def offers_query(request):
    if request.method == 'GET':
        data_dict = mark.offers_query()['offers_query_response']['offer']
        if type(data_dict) is list:
            return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
        ls = []
        ls.append(data_dict)
        return render(request, 'test/offers_query.html', {'data_dict_ls': ls})

        # return render(request, 'test/basic-table.html', {'data_dict_ls': data_dict['offers_query_response']['offer']})


@csrf_exempt
@fault_decorator
def offers_query_date(request):
    data = request.POST
    dict_d = {}
    dict_d['date-type'] = data.get('date-type')
    print(type(data.get('min')))
    dict_d['min'] = data.get('min') + 'T00:00:00'
    dict_d['max'] = data.get('max') + 'T00:00:00'
    print(dict_d['max'])
    try:
        data_dict = mark.offers_query_date(dict_d)['offers_query_response']['offer']
    except:
        data_dict = ''
        return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
    if type(data_dict) is list:
        return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
    ls = []
    ls.append(data_dict)
    return render(request, 'test/offers_query.html', {'data_dict_ls': ls})


@csrf_exempt
@fault_decorator
def offers_query_quantity(request):
    data = request.POST
    print(data)
    dict_d = {}
    dict_d['quantity-type'] = data.get('quantity-type')
    dict_d['quantity'] = data.get('quantity')
    try:
        data_dict = mark.offers_query_quantity(dict_d)['offers_query_response']['offer']
    except:
        data_dict = ''
        return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
    if type(data_dict) is list:
        return render(request, 'test/offers_query.html', {'data_dict_ls': data_dict})
    ls = []
    ls.append(data_dict)
    return render(request, 'test/offers_query.html', {'data_dict_ls': ls})


@csrf_exempt
@fault_decorator
def batch_query(request):
    if request.method == 'GET':
        data = mark.batch_query()
        return render(request, 'batch_query.html', {'data_dict': data})


@csrf_exempt
@fault_decorator
def orders_query(request):
    if request.method == 'GET':
        dicts = {}
        dicts['paging'] = 1
    else:
        data = request.POST
        dicts = {}
        dicts['paging'] = data.get('paging')
    try:
        data_dict = mark_order.orders_query(dicts)['orders_query_response']['order']
    except:
        data_dict = ''
        return render(request, 'test/orders.html', {'data_dict_ls': data_dict})
    if type(data_dict) is list:
        return render(request, 'test/orders.html', {'data_dict_ls': data_dict})
    ls = []
    ls.append(data_dict)
    return render(request, 'test/orders.html', {'data_dict_ls': ls})


@csrf_exempt
@fault_decorator
def orders_query_date(request):
    data = request.POST
    dict_d = {}
    dict_d['paging'] = data.get('paging')
    dict_d['date-type'] = data.get('date-type')
    print(type(data.get('min')))
    if data.get('min') or data.get('max') == '':
        dict_d['date-type'] = ''
    dict_d['min'] = data.get('min') + 'T00:00:00'
    dict_d['max'] = data.get('max') + 'T23:59:59'
    dict_d['state'] = data.get('state')
    print(dict_d['max'])
    try:
        data_dict = mark_order.orders_query_date(dict_d)['orders_query_response']['order']
    except:
        data_dict = ''
        return render(request, 'test/orders.html', {'data_dict_ls': data_dict})

    if type(data_dict) is list:
        return render(request, 'test/orders.html', {'data_dict_ls': data_dict})
    ls = []
    ls.append(data_dict)
    return render(request, 'test/orders.html', {'data_dict_ls': ls})


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
        return render(request, 'test/orders.html', {'data_dict_ls': data_dict})
    if type(data_dict) is list:
        return render(request, 'test/orders.html', {'data_dict_ls': data_dict})
    else:
        ls = []
        ls.append(data_dict)
        return render(request, 'test/orders.html', {'data_dict_ls': ls})


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

        dict_data['order_detail_action'] = data.get('order_detail_action')
        data = mark_order.orders_update(dict_data)['orders_update_response']['order']
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
    if request.method == 'GET':
        return render(request, 'test/order_comments.html')
    if request.method == 'POST':
        data = request.POST
        dict_query = {'paging': data.get('paging')}
        dict_data = client.client_order_query(dict_query)
        return render(request, 'client_comments_show.html', {'data': dict_data})


@csrf_exempt
@fault_decorator
def order_comments_query_date(request):
    if request.method == 'POST':
        data = request.POST
        dict_d = {'paging': data.get('paging'), 'results_count': 50,
                  'date-type': data.get('date-type'), 'min': data.get('min') + 'T00:00:00',
                  'max': data.get('max') + 'T23:59:59'}
        data_dict = client.client_order_query_date(dict_d)
        return render(request, 'client_comments_show.html', {'data': data_dict})


@csrf_exempt
@fault_decorator
def order_comments_query_id(request):
    if request.method == 'POST':
        data = request.POST
        dict_d = {'order_fnac_id': data.get('order_fnac_id')}
        data_dict = client.client_order_query_id(dict_d)
        return render(request, 'client_comments_show.html', {'data': data_dict})


@csrf_exempt
@fault_decorator
def client_order_comments_update(request):
    if request.method == 'GET':
        return render(request, 'client_order_comments_update.html')
    if request.method == 'POST':
        data = request.POST
        data_dict = {'id': data.get('id'), 'comment_reply': data.get('comment_reply')}
        data = client.client_order_comments_update(data_dict)
        return render(request, 'client_order_comments_update.html', {'data': data})


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
        print(data_dict)
        data = incident.incidents_query(data_dict)
        return render(request, 'incidents_query.html', {'data': data})


# 废弃
@csrf_exempt
@fault_decorator
def incidents_query(request):
    if request.method == 'GET':
        return render(request, 'test/incidents.html')
    if request.method == 'POST':
        data = request.POST
        min = data.get('min') + 'T00:00:00'
        max = data.get('max') + 'T23:59:59'
        data_dict = {
            'results_count': 50, 'paging': data.get('paging'),
            'date_type': data.get('date-type'), 'min': min, 'max': max, 'status': data.get('status'),
        }
        print(data_dict)
        data = incident.incidents_query(data_dict)['incidents_query_response']['incident']
        print(data)
        for da in data:
            print(da['order_details_incident']['order_detail_incident'])
        if type(data) is list:
            for da in data:
                if not type(da['order_details_incident']['order_detail_incident']) is list:
                    da['order_details_incident']['order_detail_incident'] = [
                        da['order_details_incident']['order_detail_incident'], ]

            return render(request, 'test/incidents.html', {'dict_data_ls': data})
        ls = []
        if not type(data['order_details_incident']['order_detail_incident']) is list:
            data['order_details_incident']['order_detail_incident'] = [
                data['order_details_incident']['order_detail_incident'], ]
        ls.append(data)
        return render(request, 'test/incidents.html', {'dict_data_ls': ls})


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
    data_dict = mark_order.orders_query_id(param1)['orders_query_response']['order']['shipping_address']
    if type(data_dict) is list:
        return render(request, 'order_query_shop.html', {'data_dict': data_dict})
    ls = []
    ls.append(data_dict)
    return render(request, 'order_query_shop.html', {'data_dict': ls})


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
            'price': data.get('price')
        }
        batch_id = mark.update_offer_price(data_dict)
        time.sleep(1)
        status = mark.batch_status(batch_id)['batch_status_response']
        print(status)
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
    print(status)
    # return JsonResponse(status)
    return render(request, 'test/profile.html', {'dict_status': status})


@csrf_exempt
@fault_decorator
def offers_query_price(request):
    if request.method == 'POST':
        data = request.POST
        min_p = int(data.get('min_p'))
        max_p = int(data.get('max_p'))
        data_dict = mark.offers_query()['offers_query_response']['offer']
        print(data_dict)
        if type(data_dict) is list:
            lis = []
            for index in range(len(data_dict)):
                if min_p <= float(data_dict[index]['price']) <= max_p:
                    lis.append(data_dict[index])
            print(lis)
            return render(request, 'test/offers_query.html', {'data_dict_ls': lis})
        ls = []
        if min_p <= float(data_dict['price']) <= max_p:
            ls.append(data_dict)
        print(ls)
        return render(request, 'test/offers_query.html', {'data_dict_ls': ls})
