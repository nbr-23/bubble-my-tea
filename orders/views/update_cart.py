from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class UpdateCartItemView(View):
    @method_decorator(csrf_exempt)  # Temporarily disable CSRF validation
    def dispatch(self, *args, **kwargs):
        return super(UpdateCartItemView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')
        sugar_level = request.POST.get('sugar_level')
        toppings = request.POST.get('toppings')
        
        # Here you would typically get the item from the cart and update its attributes
        # For demonstration, let's just assume success if we receive all parameters
        if item_id and quantity and sugar_level and toppings:
            return JsonResponse({'success': True, 'message': 'Cart item updated successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Missing data'})
