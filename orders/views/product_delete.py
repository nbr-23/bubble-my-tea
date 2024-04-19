from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from orders.models.products import Products  
from django.db import connection

class ProductDeleteView(TemplateView):
    template_name = 'product_delete.html'
    
    
    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))

        user_id = request.session['user_id']

       
        return super().get(request, *args, **kwargs)

    def post(self, request, product_id):
       
        product = get_object_or_404(Products, id=product_id)

       
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Products WHERE id = %s", [product_id])

       
        return redirect('/product')