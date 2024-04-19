from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

class RemoveCartItemView(View):
    @method_decorator(csrf_exempt)  # Temporarily disable CSRF validation
    def dispatch(self, *args, **kwargs):
        return super(RemoveCartItemView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        
        # Here you would typically remove the item from the cart
        if item_id:
            return JsonResponse({'success': True, 'message': 'Item removed successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Item ID not provided'})
