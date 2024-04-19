from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import mysql.connector
from django.contrib.auth.models import User
from mysql.connector import Error
from ..utils.db import get_db_connection
from django.contrib.auth import login

class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse_lazy('login'))  # Redirect to login if no user is logged in

        context = self.get_user_info(user_id)
        # Check for a success message in the session
        if 'success_message' in request.session:
            context['success_message'] = request.session.pop('success_message')  # Use pop to remove the message after it's retrieved
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Authentication required'}, status=403)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if self.update_user_info(user_id, first_name, last_name, email, phone_number, address):
            request.session['success_message'] = "Votre profile à été mise à jour"
            return HttpResponseRedirect(reverse_lazy('profile'))  # Redirect to the profile page with success message
        else:
            return JsonResponse({'error': 'Failed to update profile'}, status=500)

    def get_user_info(self, user_id):
        connection = get_db_connection()
        if connection is None:
            return {'error': 'Database connection could not be established'}
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT first_name, last_name, email, phone_number, address FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                return {
                    'first_name': result[0],
                    'last_name': result[1],
                    'email': result[2],
                    'phone_number': result[3],
                    'address': result[4]
                }
        except Error as e:
            print(f"SQL Error: {e}")
            return {}
        finally:
            cursor.close()
            connection.close()

    def update_user_info(self, user_id, first_name, last_name, email, phone_number, address):
        connection = get_db_connection()
        if connection is None:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
            UPDATE users SET first_name = %s, last_name = %s, email = %s, phone_number = %s, address = %s
            WHERE id = %s
            """
            cursor.execute(query, (first_name, last_name, email, phone_number, address, user_id))
            connection.commit()
            return True
        except Error as e:
            print(f"SQL Error: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
