from django.conf import settings
from .base import BaseApi


class ProductApiClient(BaseApi):

    def __init__(self):
        super().__init__(settings.NEXTMOTION_MARKETPLACE_API_URL)

    def get_products(self):
        return self.get('products/?no_page')

    def get_filters(self, url):
        return self.get('products/{}/'.format(url))

    def get_filtered_products(self, **params):
        return self.get_filter_product('products/filter/', **params)

    def get_category_data(self, url):
        return self.get('products/{}'.format(url))


class ProductSearchApiClient(BaseApi):

    def __init__(self):
        super().__init__(settings.NEXTMOTION_MARKETPLACE_API_URL)

    def get_search_result(self, search_product_name):
        return self.get('products/search/?name={}&sort={}&no_page'
                        .format(search_product_name,\
                                search_product_name))

    def get_cart_response(self, **params):
        return self.post('orders/create/', **params)

    def get_result(self, token):
        return self.get_product('products/view/',token)

    def get_payment_response(self, **params):
        return self.post('orders/payment/', **params)

    def delete_order_product(self, **params):
        return self.post('orders/remove_product/', **params)
    
    def update_order_product(self, **params):
        return self.post('orders/update_product/', **params)


   