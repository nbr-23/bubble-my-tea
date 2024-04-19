from django.views.generic import TemplateView
from orders.models.products import Products  
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

class ProductShopShowView(TemplateView):
    template_name = 'product_shop_show.html'

    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        return render(request, self.template_name, {'product': product})