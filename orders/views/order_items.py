from django.views.generic import TemplateView
from orders.models.order_items import OrderItem
from orders.models.products import Products  # Ajustez le chemin selon la structure de votre projet

class OrderItemsView(TemplateView):
    template_name = 'order_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Supposons que vous avez un modèle Order qui relie les OrderItems à un utilisateur
        # et que chaque utilisateur a un seul panier actif à la fois.
        cart = self.request.session.get('cart', {})
        order_items = []
        total_price = 0

        for product_id, quantity in cart.items():
            product = Products.objects.get(id=product_id)  # Assurez-vous que ce Product existe
            order_item = {
                'product_name': product.name,
                'quantity': quantity,
                'sugar_level': 'Medium',  # Mettre à jour selon vos attributs réels
                'toppings': 'Boba',       # Mettre à jour selon vos attributs réels
                'unit_price': product.price,
                'total_price': product.price * quantity
            }
            order_items.append(order_item)
            total_price += order_item['total_price']

        context['order_items'] = order_items
        context['total_price'] = total_price
        return context
