from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import mysql.connector
from mysql.connector import Error
from ..utils.db import get_db_connection

User = get_user_model()

class RegisterView(View):
    template_name = 'register.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            return render(request, self.template_name, {
                'error_message': 'Passwords do not match.'
            })

        hashed_password = make_password(password)
        connection = get_db_connection()
        if connection is None:
            return render(request, self.template_name, {
                'error_message': 'Database connection failed.'
            })

        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO users (first_name, last_name, email, password, is_admin)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (firstname, lastname, email, hashed_password, False))
            connection.commit()
            user_id = cursor.lastrowid  # Get the ID of the last inserted row

            # Manually configure the session
            request.session['user_id'] = user_id
            request.session['email'] = email

            # Create a temporary user instance for JWT generation
            temp_user = User(id=user_id, email=email, password=hashed_password)
            refresh = RefreshToken.for_user(temp_user)
            
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            response = JsonResponse(tokens)
            response.set_cookie(key='refresh', value=str(refresh), httponly=True)
            response.set_cookie(key='access', value=str(refresh.access_token), httponly=True)
            return HttpResponseRedirect(self.success_url)

        except mysql.connector.Error as err:
            return render(request, self.template_name, {
                'error_message': f'Error during user registration: {err}'
            })
        finally:
            cursor.close()
            connection.close()
