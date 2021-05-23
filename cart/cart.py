from django.conf import settings
from django.core import serializers

from decimal import Decimal


class Cart:
    def __init__(self, request):
        """ value 'products' is a dict
        structure: {serializers(model): tuple(int(qty), int(price * qty)) """

        _default_cart = {
            'products': {},
            'total_qty': 0,
            'total_price': 0,
        }
        self.session = request.session
        self.cart = request.session.get(settings.CART_USER_SESSION, _default_cart)

    def add_product(self, product, qty=1):
        # product = Smartphone.objects.get(pk=5)
        key_product = serializers.serialize('json', [product, ],
                                            fields=('product_name', 'price', 'product_image', 'manufacturer'))  # str
        self.cart['products'][key_product] = self._add(key_product, product, qty)
        self.update()
        self.save()

    def _add(self, key_product, product, qty):
        price = product.price  # Decimal
        products = self.cart.get('products')
        if all((products, key_product in products.keys())):
            qty += self.cart['products'][key_product][0]
        return qty, str(Decimal(qty) * price)

    def update_product_qty(self, product, qty):
        if qty <= 0:
            self.delete_product(product)
            return
        self.add_product(product, qty)

    def update(self):
        self.cart['total_qty'] = str(len(self.cart['products'].keys()))
        self.cart['total_price'] = str(self.get_total_price())
        self.session[settings.CART_USER_SESSION] = self.cart

    def delete_product(self, product):
        key_product = serializers.serialize('json', [product, ],
                                            fields=('product_name', 'price', 'product_image', 'manufacturer'))  # str
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
        self.session[settings.CART_USER_SESSION] = self.cart
        self.session.modified = True

    def delete(self):
        del self.session[settings.CART_USER_SESSION]
        self.session.modified = True

    def __str__(self):
        return str(f"<Cart:(qty: {self.cart['total_qty']}, price: {self.cart['total_price']})>")
