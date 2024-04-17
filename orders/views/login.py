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

class LoginView(View):
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        connection = get_db_connection()
        
        if connection is None:
            return JsonResponse({'error': 'Database connection failed'}, status=500)
        
        cursor = connection.cursor()
        try:
            query = "SELECT id, password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_record = cursor.fetchone()
            cursor.fetchall()

            if user_record:
                user_id, hashed_password = user_record
                if check_password(password, hashed_password):
                    # Creating the user for JWT without using the ORM for database queries
                    temp_user = User(username=email)
                    temp_user.id = user_id  # this line is necessary for Django to manage the session
                    
                    # Manually configuring the session (alternative to `login(request, user)`)
                    request.session['user_id'] = user_id
                    request.session['email'] = email
                    
                    # Generating JWT
                    refresh = RefreshToken.for_user(temp_user)
                    
                    tokens = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                    response = JsonResponse(tokens)
                    response.set_cookie(key='refresh', value=str(refresh), httponly=True)
                    response.set_cookie(key='access', value=str(refresh.access_token), httponly=True)
                    return HttpResponseRedirect(self.success_url)
                else:
                    return render(request, self.template_name, {'error_message': 'Invalid password'})
            else:
                return render(request, self.template_name, {'error_message': 'Email not found'})
        except Error as err:
            return JsonResponse({'error': f'SQL Error: {err}'}, status=500)
        finally:
            cursor.close()
            connection.close()
