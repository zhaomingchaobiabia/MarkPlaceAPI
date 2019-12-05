from django.shortcuts import render
from markerplace.market_api import MarketPlaceApi, MarketPlacePricingApi, MarketPlaceOrderApi
from django.shortcuts import render, redirect, reverse
import hashlib, json
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import datetime
import time

mark = MarketPlaceApi()
mark_order = MarketPlaceOrderApi()
mark_query = MarketPlacePricingApi()


# Create your views here.
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def offers_update(request):
    if request.method == 'GET':
        return render(request, 'offer_update.html')
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
        dic_da['treatment'] = dict_data.get('treatment')
        dic_da['pictures'] = dict_data.get('pictures')
        dic_da['logistic_type_id'] = dict_data.get('logistic_type_id')
        dic_da['is_shipping_free'] = dict_data.get('is_shipping_free')
        dic_da['promotion'] = dict_data.get('promotion')
        dic_da['time_to_ship'] = dict_data.get('time_to_ship')
        print(dic_da)
        batch_id = mark.offers_update(dic_da)
        return render(request, 'offer_update.html', {'batch_id': batch_id})


@csrf_exempt
def batch_status(request):
    if request.method == 'GET':
        return render(request, 'batch_status.html')
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        status = mark.batch_status(batch_id)
        print(status)
        return render(request, 'batch_status.html', {'status': status})


@csrf_exempt
def offers_query(request):
    if request.method == 'GET':
        return render(request, 'offers_query.html')
    if request.method == 'POST':
        data = request.POST
        print(data)
        dict_d = {}
        dict_d['paging'] = data.get('paging')
        dict_d['results_count'] = data.get('results_count')
        dict_d['product_fnac_id'] = data.get('product_fnac_id')
        dict_d['offer_fnac_id'] = data.get('offer_fnac_id')
        dict_d['offer_seller_id'] = data.get('offer_seller_id')
        dict_d['promotion_types'] = data.get('promotion_types')
        data_dict = mark.offers_query(dict_d)
        return render(request, 'offers_query_show.html', {'data_dict_ls': data_dict['offers_query_response']['offer']})


@csrf_exempt
def offers_query_date(request):
    data = request.POST
    dict_d = {}
    dict_d['paging'] = data.get('paging')
    dict_d['results_count'] = data.get('results_count')
    dict_d['date-type'] = data.get('date-type')
    print(type(data.get('min')))
    dict_d['min'] = data.get('min') + ':00'
    dict_d['max'] = data.get('max') + ':00'
    print(dict_d['max'])
    data_dict = mark.offers_query_date(dict_d)
    return render(request, 'offers_query_show.html', {'data_dict_ls': data_dict['offers_query_response']['offer']})


@csrf_exempt
def offers_query_quantity(request):
    data = request.POST
    print(data)
    dict_d = {}
    dict_d['paging'] = data.get('paging')
    dict_d['results_count'] = data.get('results_count')
    dict_d['quantity-type'] = data.get('quantity-type')
    dict_d['quantity'] = data.get('quantity')
    data_dict = mark.offers_query_quantity(dict_d)
    return render(request, 'offers_query_show.html', {'data_dict_ls': data_dict['offers_query_response']['offer']})


@csrf_exempt
def batch_query(request):
    if request.method == 'GET':
        data = mark.batch_query()
        return render(request, 'batch_query.html', {'data_dict': data})


@csrf_exempt
def orders_query(request):
    if request.method == 'GET':
        return render(request, 'orders_query.html')
    if request.method == 'POST':
        data = request.POST
        dicts = {}
        dicts['results_count'] = data.get('results_count')
        dicts['paging'] = data.get('paging')
        data_dict = mark_order.orders_query(dicts)
        return render(request, 'order_query_show.html', {'data_dict': data_dict})


@csrf_exempt
def orders_query_date(request):
    data = request.POST
    dict_d = {}
    dict_d['paging'] = data.get('paging')
    dict_d['results_count'] = data.get('results_count')
    dict_d['date-type'] = data.get('date-type')
    print(type(data.get('min')))
    dict_d['min'] = data.get('min') + ':00'
    dict_d['max'] = data.get('max') + ':00'
    dict_d['state'] = data.get('state')
    print(dict_d['max'])
    data_dict = mark_order.orders_query_date(dict_d)
    return render(request, 'order_query_show.html', {'data_dict': data_dict})


@csrf_exempt
def orders_query_id(request):
    data = request.POST
    ls_id = data.get('orders_fnac_id')
    if ',' in ls_id:
        ls_id = ','.join(ls_id)
    data_dict = mark_order.orders_query_id(ls_id)
    return render(request, 'order_query_show.html', {'data_dict': data_dict})


def order_update(request):
    if request.method == 'GET':
        return render(request, 'order_update.html')
    if request.method == 'POST':
        data = request.POST

    return None


@csrf_exempt
def carriers_query(request):
    data = mark_query.carriers_query()['carriers_query_response']['carrier']
    return render(request, 'index.html', {'data_dict': data})


def carriers_update_accept(request):
    if request.method == 'POST':
        data = request.POST
        
    return None