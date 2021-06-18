import requests
import stripe

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from .api_clients.product import ProductApiClient, ProductSearchApiClient

stripe.api_key = settings.STRIPE_SECRET_KEY


def products_view(request):
    if request.method == "POST":
        params = {
            'product_type': request.POST.getlist('product_type[]', None),
            'product_effect': request.POST.getlist('product_effect[]', None),
            'skin_type': request.POST.getlist('skin_type[]', None),
            'product_brand': request.POST.getlist('product_brand[]', None),
            'search_query': request.POST.get('search_query',''),
            'selected_categories': request.POST.get('selected_categories',''),
            'page': request.POST.get('current_page','')
        }
        selected_options_type = list(map(int, params['product_type']))
        selected_options_effect = list(map(int, params['product_effect']))
        selected_options_skin = list(map(int, params['skin_type']))
        selected_options_brand = list(map(int, params['product_brand']))
        client = ProductApiClient()
        product_list = client.get_filtered_products(**params)
        category_data = client.get_category_data(
            f'categories/?category={params["selected_categories"]}')
        output_category = None
        video_link = None
        introduction = None
        pdf_link = None
        for data in category_data:
            video_link = data.get('video_link')
            introduction = data.get('introduction')
            pdf_link = data.get('pdf_link')
            if any([data.get('product_type'), data.get('product_brand'),
                    data.get('product_effect'), data.get('skin_type')]):
                template_category = get_template(
                    'products/category_card.html')
                context_category = {
                    'category_data': category_data,
                    'selected_product_type': selected_options_type,
                    'selected_options_brand': selected_options_brand,
                    'selected_options_effect': selected_options_effect,
                    'selected_options_skin': selected_options_skin
                }
                output_category = template_category.render(
                    context_category)
        template = get_template('products/product_cards.html')     
        context = {'products': product_list['results']}         
        output = template.render(context)
        total_size = product_list['count']
        pages = int(total_size/12)
        if (total_size % 12) > 0:
            total_pages = pages+1
        else:
            total_pages = pages
        return JsonResponse({
            'result': output,
            'currPage': request.POST['current_page'],
            'totalPage': total_pages,
            'totalSize': total_size,
            'results': product_list['results'],
            'category_results': output_category,
            'video_link': video_link,
            'introduction': introduction,
            'pdf_link': pdf_link})
    else:
        context = {
            'selected_category': request.GET.get('category', ''),
            'count': len(request.session.get('products', []))
        }
        return render(request, 'products/product.html', context)


def search_view(request):
    if request.method == 'POST':
        search_product_name = request.POST.get('search')
        product_search_api_client = ProductSearchApiClient()
        product_api_client = ProductApiClient()
        product_list = product_search_api_client.get_search_result(search_product_name)
        product_type = product_api_client.get_filters('product_type')
        product_effect = product_api_client.get_filters('product_effect')
        skin_type = product_api_client.get_filters('skin_type')
        product_brand = product_api_client.get_filters('product_brand')
        product_count = len(request.session.get['products'],[])
        context={
            'products':product_list,
            'product_type':product_type,
            'product_effect':product_effect,
            'skin_type':skin_type,
            'product_brand':product_brand,
            'count':product_count
        }
        return render(request, 'products/product.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        new_product_dict = {
            'id':request.POST.get('product_id'),
            'quantity':request.POST.get('quantity')
        }
        product_list = request.session.get('products',[])
        if product_list:
            for product in product_list:
                if product['id'] == new_product_dict['id']:
                    count = len(request.session.get('products',[]))
                    return JsonResponse({'message':'already','count':count})
            product_list.append(new_product_dict)
            request.session['products'] = product_list
        else:
            product_list.append(new_product_dict)
            request.session['products'] = product_list
        count = len(request.session.get('products',[]))
    return JsonResponse({'message':'success','count':count})


def charge(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        charge = stripe.Charge.create(
            amount=round(amount*100),
            currency='eur',
            description='A Django charge',
            source=request.POST.get('stripeToken')
        )
        params = {}
        address_check = request.POST.get('shipping_address_check')
        if address_check:
            params['firstname']=request.POST.get('firstname')
            params['lastname']=request.POST.get('lastname')
            params['phone']=request.POST.get('phone')
            params['email']=request.POST.get('email')
            params['shippingaddress1']=request.POST.get('shippingaddress1')
      
        params['total_amount']=request.POST.get('amount')
        params['order']=request.POST.get('order_id')
        params['doctor_id']=request.POST.get('doctor_id')
        params['customer_id']=request.POST.get('customer_id')
        params['shipping_id']=request.POST.get('shipping_id')
        params['payment_mode']= 'Stripe'
       
        if charge['status']=='succeeded':
            params['status']= "Success"
        else:
             params['status']= "Failed"
        params['transaction_id']= charge['balance_transaction']
        product_api_client = ProductSearchApiClient()
        response = product_api_client.get_payment_response(**params)
        if response['details'] == 'success':
            return render(request, 'products/charge.html',{'pdf_link':response['pdf_link']})
        else:
            return render(request, 'products/charge.html', {'error':'Something Went Wrong. Please try again later !!!'})


def single_product(request, pk):
    product = {}
    product_id = str(pk)
    api_url = settings.NEXTMOTION_MARKETPLACE_API_URL
    product=requests.get(f'{api_url}/products/single_product/{product_id}/')
    product_count = len(request.session.get('products',[]))
    product_api_client = ProductApiClient()
    categories = product_api_client.get_filters('categories')
    null = None
    product_info=eval(product.text)
    video_link = product_info.get('product_video')
    if video_link:
        video_list = video_link.split('=')
        video_list_raw = video_list[1].split('&')
        product_info['product_video']=video_list_raw[0]

    return render(request, 'products/single_product.html', {'product':product_info,'count':product_count,\
        'categories':categories})


def cart_view(request):
    if request.method == "POST":
        product_count = len(request.session.get('products',[]))
        count = len(request.POST.getlist('product_id'))
        products = []
        product_dict = {}
        product_list = request.POST.getlist('product_id')
        quantity_list = request.POST.getlist('quantity')
        selling_list = request.POST.getlist('selling_price')
        total = 0
        for i in range(0, count):
            product_dict['id'] = product_list[i]
            product_dict['quantity'] = quantity_list[i]
            total += (int(quantity_list[i]) * float(selling_list[i]))
            products.append(product_dict.copy())
        params = {
            'user_id':1,
            'total_amount':total,
            'status':'Active',
            'products':products,
            'email':request.POST.get('email'),
            'tel_number':request.POST.get('full_phone')
        }
        product_api_client = ProductSearchApiClient()
        response = product_api_client.get_cart_response(**params)
        if response['message'] == 'success':
            del request.session['products']
            request.session.modified = True
            return HttpResponseRedirect('/cart/?q=success')
        else:
            return HttpResponseRedirect('/cart/?q=failed')
        
    else:
        products_list = []
        message = request.GET.get('q')
        if message:
            if message == 'success':
                return render(request, 'cart/cart.html',
                        {'message': 'success'})
            else:
                product_count = len(request.session['products'])
                return render(request, 'cart/cart.html',
                            {'message': 'failed', 'count': product_count})
        product_count = len(request.session.get('products',[]))
        products = {}
        for data in request.session.get('products'):
            if data['id']:
                api_url = settings.NEXTMOTION_MARKETPLACE_API_URL
                product = requests.get(
                        f'{api_url}/products/single_product/{data["id"]}/')
                null = None
                products['product'] = (eval(product.text))
                products['selected_quantity'] = data['quantity']
            products_list.append(products.copy())
        total = 0
        total_vat = 0
        for product in products_list:
            amount = float(product['product']['selling_price'])
            quantity = int(product['selected_quantity'])
            product_total = float(amount * quantity)
            actual_selling_price = round((float(product['product']['product_vat']) * float(product['product']['selling_price']))/100, 2)
            total_vat += actual_selling_price
            total += (product_total+actual_selling_price)
            single_product_price = product_total + actual_selling_price
            product['product']['product_total'] = single_product_price
        context = products_list
        product_api_client = ProductApiClient()
        categories = product_api_client.get_filters('categories')
        return render(request, 'cart/cart.html',
                    {'products': context, 'total': round(total, 2),
                        'count': product_count, 'categories': categories,'total_vat': round(total_vat, 2)})


def payment_view(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        order_id = request.POST.get('order_id')
        params = {'product_id': product_id, 'order_id': order_id}
        product_api_client = ProductSearchApiClient()
        response = product_api_client.delete_order_product(**params)
        return JsonResponse(response)
    else:
        order_number = request.GET.get('token')
        product_api_client = ProductSearchApiClient()
        response = product_api_client.get_result(order_number)
        if response.get('status') == 'Already Paid':
            return render(request, 'cart/payment.html',
                            {'status': response['status']})
        total = 0
        total_vat = 0
        total_price = 0
        if response['product_list']:
            for data in response['product_list']:
                total_price += float(data['selling_price'])*int(
                    data['quantity'])+float(data['total_delivery_fee'])
                product_total = (float(data['selling_price']) * int(
                    data['quantity'])+float(data['product_vat']))
                data['product_total'] = round(product_total, 2)
                data['selling_price'] = float(data['selling_price'])
                total += (product_total+float(data['total_delivery_vat']))
                total_vat += float(data['product_vat'])+float(data['delivery_total_vat'])
            total_for_payment = (round(total, 2) * 100)
            context = response['product_list']
            other_info = response['others']
            return render(request, 'cart/payment.html', {'products': context, \
                                                         'key': settings.STRIPE_PUBLISHABLE_KEY, \
                                                         'total': round(total, 2),
                                                         'other_info': other_info,
                                                         'total_for_payment': total_for_payment,
                                                         'total_vat':round(total_vat, 2),
                                                         'total_price':round(total_price, 2)})
        else:
            return render(request, 'cart/payment.html')


def remove_product(request, pk):
    product_list = request.session.get('products')
    for i in range(len(product_list)):
        for k, v in product_list[i].items():
            if (k == 'id' and v == str(pk)):
                index = i
    del product_list[index]
    request.session['products'] = product_list
    return redirect('nm_marketplace_cart')


def update_product(request):
    data = request.POST.get('dataString')
    params = {'data': data}
    product_api_client = ProductSearchApiClient()
    response = product_api_client.update_order_product(**params)
    return JsonResponse(response)

