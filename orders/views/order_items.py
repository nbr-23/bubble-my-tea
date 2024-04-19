from django.views.generic import TemplateView
from django.http import JsonResponse
from orders.models.products import Products
import json
import logging

class OrderItemsView(TemplateView):
    template_name = 'order_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        order_items = []
        total_price = 0.0

        if not cart:
            logging.debug("Cart is empty")
        
        for product_id, details in cart.items():
            try:
                product = Products.objects.get(id=product_id)
                extra_cost = 0.50 if details.get('toppings') != 'None' else 0
                unit_price = product.price + extra_cost
                total_item_price = unit_price * details.get('quantity', 0)

                order_items.append({
                    'id': product_id,
                    'product_name': product.name,
                    'quantity': details.get('quantity', 0),
                    'sugar_level': details.get('sugar_level', 'Unknown'),
                    'toppings': details.get('toppings', 'None'),
                    'unit_price': unit_price,
                    'total_price': total_item_price,
                })

                total_price += total_item_price
            except Products.DoesNotExist:
                logging.error(f"Product with id {product_id} does not exist.")
            except Exception as e:
                logging.error(f"Error processing product {product_id}: {str(e)}")

        context['order_items'] = order_items
        context['order_items_json'] = json.dumps(order_items) if order_items else "[]"
        context['total_price'] = total_price
        return context
