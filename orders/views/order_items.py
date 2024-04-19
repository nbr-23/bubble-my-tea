from django.views.generic import TemplateView
from orders.models.order_items import OrderItem

class OrderItemsView(TemplateView):
    template_name = 'order_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        order_items = OrderItem.objects.all()
        # Actual user 
        #order_items = OrderItem.objects.filter(order_id=self.request.user.orders.id)
        
        # Total price
        total_price = sum(item.product.price * item.quantity for item in order_items)
        context['order_items'] = order_items
        context['total_price'] = total_price
        return context

