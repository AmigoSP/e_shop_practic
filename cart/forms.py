from django import forms


class CartUpdateProduct(forms.Form):
    product_qty = forms.IntegerField(min_value=0, label='Кол-во')
