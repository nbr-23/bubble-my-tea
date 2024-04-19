from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from ..utils.db import get_db_connection

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
        
        user_id = request.session['user_id']

        # Connect to the database
        conn = get_db_connection()
        if conn is None:
            return render(request, self.template_name, {'error': 'Database connection could not be established.'})
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT
                o.date AS OrderDate,
                o.total_price AS TotalPrice,
                p.name AS ProductName,
                oi.quantity AS Quantity,
                oi.toppings AS Toppings
            FROM
                orders o
                INNER JOIN users u ON o.user_id = u.id
                INNER JOIN OrderItem oi ON o.id = oi.order_id
                INNER JOIN Products p ON oi.product_id = p.id
            WHERE
                u.id = %s
            ORDER BY
                o.date DESC;
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
        finally:
            conn.close()

        # Pass the results to the template
        return render(request, self.template_name, {'orders': results})