from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import mysql.connector
from mysql.connector import Error
from ..utils.db import get_db_connection

from orders.models.users import User

class LoginView(View):
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        connection = get_db_connection()
        
        if connection is None:
            return JsonResponse({'error': 'Database connection failed'}, status=500)
        
        try:
            cursor = connection.cursor()
            query = "SELECT id, password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_record = cursor.fetchone()

            if user_record:
                user_id, hashed_password = user_record
                if check_password(password, hashed_password):
                    # Create JWT tokens
                    temp_user = User(username=email)
                    temp_user.id = user_id  # Manually set the user ID to the fetched ID

                    refresh = RefreshToken.for_user(temp_user)
                    response = HttpResponseRedirect(self.success_url)
                    response.set_cookie(key='refresh', value=str(refresh), httponly=True)
                    response.set_cookie(key='access', value=str(refresh.access_token), httponly=True)
                    return response
                else:
                    return render(request, self.template_name, {'error_message': 'Invalid password'})
            else:
                return render(request, self.template_name, {'error_message': 'Email not found'})

        except mysql.connector.Error as err:
            return JsonResponse({'error': f'SQL Error: {err}'}, status=500)
        
        finally:
            cursor.close()
            connection.close()

