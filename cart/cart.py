import json
from decimal import Decimal

from django.conf import settings
from django.core import serializers

from .models import CartAuthCustomer


class Cart:
    def __init__(self, request):
        """ value 'products' is a dict
        structure: {serializers(model): tuple(int(qty), int(price * qty)) """

        _default_cart = {
            'products': {},
            'total_qty': '0',
            'total_price': '0',
        }
        self.qty_update = False
        self.user_is_authenticated = False
        if not request.user.is_authenticated:
            self.session = request.session
            self.cart = request.session.get(settings.CART_USER_SESSION, _default_cart)
        else:
            self.session = {settings.CART_USER_SESSION: _default_cart}
            self.cart, self.cart_model = self.get_cart_auth_customer(user=request.user)
            self.user_is_authenticated = True

    @staticmethod
    def get_cart_auth_customer(user):
        cart_customer = CartAuthCustomer.objects.get(customer=user)
        return json.loads(cart_customer.cart_customer), cart_customer

    def add_product(self, product, qty=1):
        # product = Smartphone.objects.get(pk=5)
        key_product = serializers.serialize('json', [product, ],
                                            fields=('product_name', 'price', 'product_image', 'manufacturer',
                                                    'subcategory'))  # str
        self.cart['products'][key_product] = self._add(key_product, product, qty)
        self.update()
        self.save()

    def _add(self, key_product, product, qty):
        price = product.price  # Decimal
        products = self.cart.get('products')
        if all((products, key_product in products.keys(), not self.qty_update)):
            qty += self.cart['products'][key_product][0]
        return qty, str(Decimal(qty) * price)

    def update_product_qty(self, product, qty):
        if qty <= 0:
            self.delete_product(product)
            return
        self.qty_update = True
        self.add_product(product, qty)
        self.qty_update = False

    def update(self):
        self.cart['total_qty'] = str(len(self.cart['products'].keys()))
        self.cart['total_price'] = str(self.get_total_price())
        self.session[settings.CART_USER_SESSION] = self.cart

    def delete_product(self, product):
        key_product = serializers.serialize('json', [product, ],
                                            fields=('product_name', 'price', 'product_image', 'manufacturer',
                                                    'subcategory'))  # str
        self.cart['products'].pop(key_product)
        self.update()
        self.save()

    def get_total_price(self):
        products = self.cart.get('products')
        total_price = 0
        if products:
            total_price = sum(list(map(lambda key: Decimal(products[key][1]), products)))
        return total_price

    def save(self):
        if not self.user_is_authenticated:
            self.session[settings.CART_USER_SESSION] = self.cart
            self.session.modified = True
        else:
            self.cart_model.cart_customer = json.dumps(self.cart)
            self.cart_model.save(update_fields=['cart_customer'])

    def __str__(self):
        return str(f"<Cart:(qty: {self.cart['total_qty']}, price: {self.cart['total_price']})>")