from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages  # Import the Django messages framework
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
            messages.error(request, 'Connection à la base de données échouée.')
            return render(request, self.template_name)
        
        cursor = connection.cursor()
        try:
            query = "SELECT id, password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_record = cursor.fetchone()

            if user_record:
                user_id, hashed_password = user_record
                if check_password(password, hashed_password):
                    temp_user = User(username=email)
                    temp_user.id = user_id
                    request.session['user_id'] = user_id
                    request.session['email'] = email
                    
                    refresh = RefreshToken.for_user(temp_user)
                    response = HttpResponseRedirect(self.success_url)
                    response.set_cookie(key='refresh', value=str(refresh), httponly=True)
                    response.set_cookie(key='access', value=str(refresh.access_token), httponly=True)
                    return response
                else:
                    messages.error(request, 'Identifiants incorrects.')
            else:
                messages.error(request, 'Identifiants incorrects.')
        except Error as err:
            messages.error(request, f'Erreur SQL: {err}')
        finally:
            cursor.close()
            connection.close()

        return render(request, self.template_name)
