from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from markerplace_develop.markerAPI_develop import SalesPeriodsApi
from markerplace.views import fault_decorator
from django.http.response import JsonResponse
# from .models import User
import hashlib

sales = SalesPeriodsApi()


# Create your views here.

@csrf_exempt
@fault_decorator
def sales_periods_query(request):
    if request.method == 'GET':
        return render(request, 'test/sales_peoriods_query.html')
    if request.method == 'POST':
        data = request.POST
        dict_data = {'paging': data.get('paging'),
                     'date_type': data.get('date_type'), 'min': data.get('min') + 'T00:00:00',
                     'max': data.get('max') + 'T23:59:00',
                     'reference': data.get('reference')
                     }
        data = sales.sales_periods_query(dict_data)
        return render(request, 'sales.html', {'data': data})


@csrf_exempt
@fault_decorator
def pricing_query(request):
    if request.method == 'GET':
        return render(request, 'test/pricing_query.html')
    if request.method == 'POST':
        data = request.POST
        dict_data = {'sellers': data.get('sellers'), 'reference_type': data.get('reference-type'),
                     'reference': data.get('reference')
                     }
        data = sales.pricing_query(dict_data)['pricing_query_response']['pricing_product']
        return render(request, 'test/pricing_query.html', {'data': data})


# 登录验证
# def login_verify(func):
#     def inner(request, *args, **kwargs):
#         if 'loginFlag' in request.session:
#             return func(request, *args, **kwargs)
#
#         return redirect(to='login')
#
#     return inner
#


@csrf_exempt
@fault_decorator
def messages_query1(request):
    paging = request.GET.get('paging') if request.GET.get('paging') else 1
    data_dict = {'paging': paging}
    data_dict_ls = sales.messages_query(data_dict)['messages_query_response']
    print(data_dict_ls)
    total_page = data_dict_ls['total_paging']
    nb_total_result = data_dict_ls['nb_total_result']
    try:
        datas = data_dict_ls['message']
        if type(datas) is list:
            for li in datas:
                li['state'] = li['@state']
                li['archived'] = li['@archived']
                li['message_referer']['type'] = li['message_referer']['@type']
                li['message_referer']['text'] = li['message_referer']['#text']
                li['message_from']['type'] = li['message_from']['@type']
                li['message_from']['text'] = li['message_from']['#text']
            return render(request, 'test/message/message.html',
                          {'data_ls': datas, 'page': int(paging), 'total_page': int(total_page),
                           'nb_total_result': nb_total_result})
        ls = []
        datas['state'] = datas['@state']
        datas['archived'] = datas['@archived']
        datas['message_referer']['type'] = datas['message_referer']['@type']
        datas['message_referer']['text'] = datas['message_referer']['#text']
        datas['message_from']['type'] = datas['message_from']['@type']
        datas['message_from']['text'] = datas['message_from']['#text']
        ls.append(datas)
        return render(request, 'test/message/message.html',
                      {'data_ls': ls, 'page': int(paging), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result})
    except:
        return render(request, 'test/message/message.html',
                      {'data_ls': '', 'page': int(paging), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result})


# @login_verify
@csrf_exempt
@fault_decorator
def messages_query(request):
    paging = request.GET.get('paging') if request.GET.get('paging') else 1
    if request.GET.get('min') is None:
        return render(request, 'test/message/message.html')
    elif request.GET.get('min') == '':
        return render(request, 'test/message/message.html')
    data = request.GET
    data_dict = {'paging': paging,
                 'date_type': data.get('date_type'), 'min': data.get('min'),
                 'max': data.get('max')
                 }
    print(data_dict)
    data_dict_ls = sales.messages_query(data_dict)['messages_query_response']
    print(data_dict_ls)
    total_page = data_dict_ls['total_paging']
    nb_total_result = data_dict_ls['nb_total_result']
    try:
        datas = data_dict_ls['message']
        if type(datas) is list:
            for li in datas:
                li['state'] = li['@state']
                li['archived'] = li['@archived']
                li['message_referer']['type'] = li['message_referer']['@type']
                li['message_referer']['text'] = li['message_referer']['#text']
                li['message_from']['type'] = li['message_from']['@type']
                li['message_from']['text'] = li['message_from']['#text']
            return render(request, 'test/message/message_query_time.html',
                          {'data_ls': datas, 'max': data.get('max'), 'min': data.get('min'),
                           'date_type': data.get('date_type'), 'page': int(paging), 'total_page': int(total_page),
                           'nb_total_result': nb_total_result})
        ls = []
        datas['state'] = datas['@state']
        datas['archived'] = datas['@archived']
        datas['message_referer']['type'] = datas['message_referer']['@type']
        datas['message_referer']['text'] = datas['message_referer']['#text']
        datas['message_from']['type'] = datas['message_from']['@type']
        datas['message_from']['text'] = datas['message_from']['#text']
        ls.append(datas)
        return render(request, 'test/message/message_query_time.html',
                      {'data_ls': ls, 'max': data.get('max'), 'min': data.get('min'),
                       'date_type': data.get('date_type'), 'page': int(paging), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result})
    except:
        return render(request, 'test/message/message_query_time.html',
                      {'data_ls': '', 'max': data.get('max'), 'min': data.get('min'),
                       'date_type': data.get('date_type'), 'page': int(paging), 'total_page': int(total_page),
                       'nb_total_result': nb_total_result})


@csrf_exempt
@fault_decorator
def messages_query_type(request):
    if request.method == 'POST':
        data = request.POST
        # message_type message_archived message_state sort_by message_from_types
        data_dict = {'message_type': data.get('message_type'), 'message_archived': data.get('message_archived'),
                     'message_state': data.get('message_state'), 'sort_by': data.get('sort_type'),
                     'message_from_types': data.get('message_from_types')
                     }
        try:
            data = sales.messages_query_type(data_dict)['messages_query_response']['message']
            if type(data) is list:
                for li in data:
                    li['state'] = li['@state']
                    li['archived'] = li['@archived']
                    li['message_referer']['type'] = li['message_referer']['@type']
                    li['message_referer']['text'] = li['message_referer']['#text']
                    li['message_from']['type'] = li['message_from']['@type']
                    li['message_from']['text'] = li['message_from']['#text']
                return render(request, 'test/message/message.html', {'data_ls': data})
            ls = []
            data['state'] = data['@state']
            data['archived'] = data['@archived']
            data['message_referer']['type'] = data['message_referer']['@type']
            data['message_referer']['text'] = data['message_referer']['#text']
            data['message_from']['type'] = data['message_from']['@type']
            data['message_from']['text'] = data['message_from']['#text']
            ls.append(data)
            return render(request, 'test/message/message.html', {'data_ls': ls})
        except:
            return render(request, 'test/message/message.html', {'data_ls': ''})


@csrf_exempt
@fault_decorator
def message_update(request):
    if request.method == 'GET':
        return render(request, 'test/message/message_update.html')
    if request.method == 'POST':
        data = request.POST
        data_dict = {
            'id': data.get('id'), 'action1': data.get('action1'),
            'message_to': data.get('message_to'), 'message_subject': data.get('message_subject'),
            'message_description': data.get('message_description'), 'message_type': data.get('message_type')
        }
        try:
            data = sales.messages_update(data_dict)['messages_update_response']['message']
            data['status'] = data['@status']
        except:
            data = ''
        return render(request, 'test/message/message_update.html', {'data': data})


@csrf_exempt
@fault_decorator
def message_update_state(request):
    if request.method == 'POST':
        data = request.POST
        data_dict = {
            'action': data.get('action'), 'id': data.get('id')}
        try:
            data = sales.messages_update(data_dict)['messages_update_response']['message']['@status']
        except:
            data = 'error'
        return JsonResponse({'data': data})


def test1(request):
    return render(request, 'test/dashboard.html')

# 登录
# @csrf_exempt
# @fault_decorator
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     if request.method == 'POST':
#         user = request.POST.get('user')
#         if not User.objects.filter(user=user):
#             return render(request, 'login.html')
#         password = request.POST.get('password')
#
#         if User.objects.filter(user=user, password=password):
#             request.session['loginFlag'] = {'user': user}
#             return redirect(to='index')
#         return render(request, 'login.html')
