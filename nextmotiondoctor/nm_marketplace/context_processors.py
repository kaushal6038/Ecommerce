from .api_clients.product import ProductApiClient

def new_products(request):

    product_api_client = ProductApiClient()
    new_products = product_api_client.get_filters('new_products')
    product_api_client = ProductApiClient()
    all_categories = product_api_client.get_filters('categories')
    return ({'products_extra':{'new_products':new_products,'all_categories':all_categories}})
