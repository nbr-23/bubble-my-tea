from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from orders.models.products import Products   

@method_decorator(require_POST, name='dispatch')
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        sugar_level = request.POST.get('sugar_level', 'Normal')
        toppings = request.POST.get('toppings', 'None')

        if quantity < 1:
            return JsonResponse({'error': 'Quantité invalide'}, status=400)

        product = Products.objects.get(id=product_id)
        extra_cost = 0.50 if toppings != 'None' else 0
        total_price = (product.price + extra_cost) * quantity

        cart = request.session.get('cart', {})
        cart_item = {
            'quantity': quantity,
            'sugar_level': sugar_level,
            'toppings': toppings,
            'unit_price': product.price + extra_cost,
            'total_price': total_price
        }

        cart[product_id] = cart_item
        request.session['cart'] = cart
        
        return JsonResponse({'message': 'Produit ajouté au panier'}, status=200)
