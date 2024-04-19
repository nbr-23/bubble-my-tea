from django.views.generic import TemplateView
from orders.models.products import Products  # Update this import based on your model location

class OrderItemsView(TemplateView):
    template_name = 'order_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        order_items = []
        total_price = 0.0

        for product_id, details in cart.items():
            product = Products.objects.get(id=product_id)
            sugar_level = details['sugar_level']
            toppings = details['toppings']
            quantity = details['quantity']
            
            extra_cost = 0.50 if toppings != 'None' else 0
            unit_price = product.price + extra_cost
            total_item_price = unit_price * quantity

            order_items.append({
                'id': product_id,
                'product_name': product.name,
                'quantity': quantity,
                'sugar_level': sugar_level,
                'toppings': toppings,
                'unit_price': unit_price,
                'total_price': total_item_price,
            })

            total_price += total_item_price

        context['order_items'] = order_items
        context['total_price'] = total_price
        return context
