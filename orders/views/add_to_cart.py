from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

class AddToCartView(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            return JsonResponse({'error': 'Quantité invalide'}, status=400)

        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        return JsonResponse({'message': 'Produit ajouté au panier'}, status=200)
