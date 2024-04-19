from django.views.generic import TemplateView
from orders.models.products import Products  
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from orders.models.users import User 


class ProductShowView(TemplateView):
    template_name = 'product_show.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))

        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
            is_admin = user.is_admin
        except User.DoesNotExist:
            is_admin = False
        
       
        self.is_admin = is_admin

     
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        return render(request, self.template_name, {'product': product, 'is_admin': self.is_admin})