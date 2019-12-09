from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from markerplace_develop.markerAPI_develop import SalesPeriodsApi

sales = SalesPeriodsApi()


# Create your views here.

@csrf_exempt
def sales_periods_query(request):
    if request.method == 'GET':
        return render(request, 'test/sales_peoriods_query.html')
    if request.method == 'POST':
        data = request.POST
        dict_data = {'results_count': data.get('results_count'), 'paging': data.get('paging'),
                     'date_type': data.get('date_type'), 'min': data.get('min') + ':00',
                     'max': data.get('max') + ':00'
                     }
        data = sales.sales_periods_query(dict_data)
        return render(request, 'sales.html', {'data': data})


@csrf_exempt
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


@csrf_exempt
def messages_query(request):
    if request.method == 'GET':
        return render(request, 'test/message.html')
    if request.method == 'POST':
        data = request.POST
        data_dict = {'results_count': data.get('results_count'), 'paging': data.get('paging'),
                     'date_type': data.get('date_type'), 'min': data.get('min'),
                     'max': data.get('max')
                     }
        data = sales.messages_query(data_dict)
        return render(request, 'messages_query.html', {'data': data})


@csrf_exempt
def messages_query_type(request):
    if request.method == 'POST':
        data = request.POST
        # message_type message_archived message_state sort_by message_from_types
        data_dict = {'message_type': data.get('message_type'), 'message_archived': data.get('message_archived'),
                     'message_state': data.get('message_state'), 'sort_by': data.get('sort_type'),
                     'message_from_types': data.get('message_from_types')
                     }
        data = sales.messages_query_type(data_dict)
        return render(request, 'messages_query.html', {'data': data})


@csrf_exempt
def message_update(request):
    if request.method == 'GET':
        return render(request, 'test/message_update.html')
    if request.method == 'POST':
        data = request.POST
        data_dict = {
            'action': data.get('action'), 'id': data.get('id'), 'action1': data.get('action1'),
            'message_to': data.get('message_to'), 'message_subject': data.get('message_subject'),
            'message_description': data.get('message_description'), 'message_type': data.get('message_type')
        }
        data = sales.messages_update(data_dict)
        return render(request, 'messages_update.html', {'data': data})


def test1(request):
    return render(request, 'test/themifyicon.html')