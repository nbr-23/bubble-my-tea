from django.views.generic import TemplateView
from orders.models.products import Products  
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class ProductShopShowView(TemplateView):
    template_name = 'product_shop_show.html'
    
        
    def get_user(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
    
        user_id = request.session['user_id']

     
        return super().get_user(request, *args, **kwargs)
    


    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        return render(request, self.template_name, {'product': product})
    