from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

class ProcessPaymentView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order_items = data.get('order_items', [])
            
            if not order_items:
                return JsonResponse({"status": "error", "message": "Empty cart"}, status=400)

            with connection.cursor() as cursor:
                user_id = request.session.get('user_id')
                cursor.execute("""
                    INSERT INTO orders (user_id, total_price, date)
                    VALUES (%s, %s, NOW());
                """, [user_id, sum(item['total_price'] for item in order_items)])
                order_id = cursor.lastrowid  # Retrieves the ID of the newly inserted order

                for item in order_items:
                    cursor.execute("""
                        INSERT INTO OrderItem (order_id, product_id, quantity, sugar_level, toppings)
                        VALUES (%s, %s, %s, %s, %s);
                    """, [order_id, item['id'], item['quantity'], item['sugar_level'], item['toppings']])

            request.session.pop('cart', None)  # Clear the cart from session after payment
            return JsonResponse({"status": "success", "message": "Payment processed successfully", "order_id": order_id})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
