from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from orders.models.order_items import OrderItem
from django.db import connection

class OrderItemsView(TemplateView):
    template_name = 'order_items.html'
    
    SUGAR_LEVEL_CHOICES = [
        ('Low', ('Low')),
        ('Normal', ('Normal')),
        ('High', ('High')),
    ]
    
    TOPPINGS_CHOICES = [
        ('None', ('Sans topping')),
        ('Popping Boba', ('Popping Boba + 0,50 €')),
        ('Jelly', ('Jelly + 0,50 €')),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        order_items = OrderItem.objects.all()
        
        total_price = sum(item.product.price * item.quantity for item in order_items)
        
        for item in order_items:
            if item.toppings != 'None':
                total_price += 0.50

        
        context['order_items'] = order_items
        context['total_price'] = total_price
        context['sugar_level_choices'] = self.SUGAR_LEVEL_CHOICES
        context['toppings_choices'] = self.TOPPINGS_CHOICES
        
        return context

    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
        # If 'user_id' exists, retrieve additional information if necessary
        # For example, check the validity of the token or other security checks
        user_id = request.session['user_id']

        # Render the dashboard page if everything is correct
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Get the product IDs from the form data
        product_ids = request.POST.getlist('product_id')
        # Loop through the product IDs and add them to the order
        

        
        for product_id in product_ids:
            # Get the product object
            product = Product.objects.get(pk=product_id)
       
            
            sql_query = "INSERT INTO OrderItem (order_id, product_id, quantity, sugar_level, toppings) VALUES (%s, %s, %s, %s, %s)"
            values = (order_id, product_id, 1, 'Normal', 'None') 
            with connection.cursor() as cursor:
                cursor.execute(sql_query, values)


  
        return HttpResponseRedirect(reverse_lazy('order_confirm'))

   
     
