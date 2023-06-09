
from django.http import JsonResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def api_order_response(dict_filter, List_of_OutputSelector=None, new_headers=None):
    url = "https://www.findsports.com.au/do/WS/NetoAPI"
    parent_dict = {}
    dict_export_status = {}
    dict_filter = dict_filter.copy()
    dict_filter['OutputSelector'] = List_of_OutputSelector
    dict_export_status["ExportStatus"] = "Exported"
    dict_filter["UpdateResults"] = dict_export_status
    parent_dict['Filter'] = dict_filter
    payload = json.dumps(parent_dict)
    product_headers_order = {
        'NETOAPI_ACTION': "GetOrder",
        'NETOAPI_USERNAME': "API-User-Product",
        'NETOAPI_KEY': "v0fmsHHYPqfq99lFnPJ1kQbIgynkbLJq",
        'Accept': "application/json",
        'Content-Type': "application/javascript",
        'cache-control': "no-cache",
        'Postman-Token': "2473156a-3bcc-4a64-8079-04c3a395b5ea"
    }
    if new_headers is None:
        header = product_headers_order
        response = requests.request("POST", url, data=payload, headers=header)
        json1_data = json.loads(response.text)
    return json1_data



from django.core.paginator import Paginator

def order_view(request):
    dict_filter = {
        'OrderStatus': ['Pending Pickup', 'Pending Dispatch', 'On Hold', 'Backorder Approved', 'Pack', 'New Backorder', 'New', 'Pick', 'Uncommitted']
    }
    output_selector = ['OrderID', 'OrderStatus', 'ShippingOption', 'SalesChannel', 'OrderLine', 'DatePlaced', 'OrderLine.ItemNotes', 'InternalOrderNotes', 'Supplier', 'CustomerRef3', 'CustomerRef4', 'CustomerRef5', 'CustomerRef6', 'CustomerRef7']
    
    order_data = api_order_response(dict_filter, output_selector)
    order_data = order_data['Order']
    total_orders = len(order_data)

    paginator = Paginator(order_data, 10) # Show 10 orders per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'total_orders':total_orders, 'page_obj': page_obj})






def Fiter_order_view(request):
    dict_filter = {
        'DatePlacedFrom': "2022-06-01 00:00:00",
        'OrderStatus': ['Pending Pickup', 'Pending Dispatch', 'On Hold', 'Backorder Approved', 'Pack', 'New Backorder', 'New', 'Pick', 'Uncommitted']
    }
    if request.method == "POST":
        if request.POST.get('DatePlacedFrom'):
            DatePlacedFrom = request.POST.get('DatePlacedFrom')
            dict_filter['DatePlacedFrom'] = DatePlacedFrom
        if request.POST.get('OrderStatus'):
            OrderStatus = request.POST.get('OrderStatus')
            dict_filter['OrderStatus'] = OrderStatus
            
    output_selector = ['OrderID', 'OrderStatus', 'ShippingOption', 'SalesChannel', 'OrderLine', 'DatePlaced', 'OrderLine.ItemNotes', 'InternalOrderNotes', 'Supplier', 'CustomerRef3', 'CustomerRef4', 'CustomerRef5', 'CustomerRef6', 'CustomerRef7']
    order_data = api_order_response(dict_filter, output_selector)
    order_data = order_data['Order']
    
    return render(request, 'order.html', {'order_data': order_data})








# API Headers
product_headers_products = {
    'NETOAPI_ACTION': "GetItem",
    'NETOAPI_USERNAME': "API-User-Product",
    'NETOAPI_KEY': "v0fmsHHYPqfq99lFnPJ1kQbIgynkbLJq",
    'Accept': "application/json",
    'Content-Type': "application/javascript",
    'cache-control': "no-cache",
    'Postman-Token': "2473156a-3bcc-4a64-8079-04c3a395b5ea"
}

# Function to call API
def api_product_response(dict_filter, List_of_OutputSelector=None, new_headers=None):
    url = "https://www.findsports.com.au/do/WS/NetoAPI"
    parent_dict = {}
    dict_export_status = {}
    dict_filter['OutputSelector'] = List_of_OutputSelector
    dict_export_status["ExportStatus"] = "Exported"
    dict_filter["UpdateResults"] = dict_export_status
    parent_dict['Filter'] = dict_filter
    payload = json.dumps(parent_dict)

    if new_headers is None:
        header = product_headers_products

    response = requests.request("POST", url, data=payload, headers=header)
    json_data = response.json()

    return json_data

@csrf_exempt
def product_info_api(request):
    if request.method == "POST":
        # data = json.loads(request.body)
        # sku = data.get("sku")

        # Call the API function to get product information
        product_info = api_product_response(
            {'SKU': 415245143},
            ['SKU', 'PrimarySupplier', 'DefaultPrice'],
            None
        )

        return JsonResponse(product_info)

    return JsonResponse({"error": "Invalid request method."})
