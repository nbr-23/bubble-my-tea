from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from ..utils.db import get_db_connection

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return HttpResponseRedirect(reverse_lazy('login'))
        
        user_id = request.session['user_id']
        conn = get_db_connection()
        if not conn:
            return render(request, self.template_name, {'error': 'Database connection could not be established.'})
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    o.id AS OrderID,
                    o.date AS OrderDate,
                    o.total_price AS TotalPrice,
                    p.name AS ProductName,
                    oi.quantity AS Quantity,
                    oi.toppings AS Toppings,
                    p.price AS Price
                FROM
                    orders o
                    INNER JOIN users u ON o.user_id = u.id
                    INNER JOIN OrderItem oi ON o.id = oi.order_id
                    INNER JOIN Products p ON oi.product_id = p.id
                WHERE
                    u.id = %s
                ORDER BY
                    o.id DESC, oi.id ASC;
            """, (user_id,))
            rows = cursor.fetchall()
        finally:
            conn.close()

        orders = {}
        for row in rows:
            order_id = row['OrderID']
            if order_id not in orders:
                orders[order_id] = {
                    'OrderDate': row['OrderDate'],
                    'TotalPrice': row['TotalPrice'],
                    'Items': []
                }
            orders[order_id]['Items'].append({
                'ProductName': row['ProductName'],
                'Quantity': row['Quantity'],
                'Toppings': row['Toppings'],
                'Price': row['Price']
            })

        # Convert orders dictionary to a sorted list
        sorted_orders = sorted(orders.values(), key=lambda x: x['OrderDate'], reverse=True)

        return render(request, self.template_name, {'orders': sorted_orders})
