from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import mysql.connector
from mysql.connector import Error
from ..utils.db import get_db_connection
from datetime import datetime

class RegisterView(View):
    template_name = 'register.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'logout' in request.path:
            return self.logout_user(request)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            return render(request, self.template_name, {
                'error_message': 'Les mots de passe ne correspondent pas.'
            })

        hashed_password = make_password(password)
        connection = get_db_connection()
        if connection is None:
            return render(request, self.template_name, {
                'error_message': 'Connexion à la base de données échouée.'
            })

        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO users (first_name, last_name, email, password, is_admin)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (firstname, lastname, email, hashed_password, False))
            connection.commit()

            # Temporarily create a user instance for JWT generation (not saved to db)
            temp_user = User(username=email)
            temp_user.id = cursor.lastrowid  # Use the ID of the last inserted row

            # Generate JWT tokens
            refresh = RefreshToken.for_user(temp_user)  # This method now should not raise an error
            
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
                'error_message': f'Erreur lors de l’enregistrement de l’utilisateur: {err}'
            })
        finally:
            cursor.close()
            connection.close()

    def blacklist_refresh_token(refresh_token, connection):
        try:
            cursor = connection.cursor()
            blacklisted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO token_blacklist_blacklistedtoken (token_id, blacklisted_at)
            SELECT id, %s FROM token_blacklist_outstandingtoken WHERE token = %s;
            """
            cursor.execute(query, (blacklisted_at, refresh_token))
            connection.commit()
        except mysql.connector.Error as err:
            print("Failed to insert token into blacklist:", err)
        finally:
            cursor.close()

    def logout_user(self, request):
        refresh_token = request.COOKIES.get("refresh")  # Changed to get the token from cookies
        if not refresh_token:
            return JsonResponse({'error': 'No refresh token provided'}, status=400)

        connection = get_db_connection()
        if connection is None:
            return JsonResponse({'error': 'Database connection failed'}, status=500)

        self.blacklist_refresh_token(refresh_token, connection)
        connection.close()

        response = HttpResponseRedirect(reverse_lazy('login'))
        response.delete_cookie('refresh')  # Assuming the refresh token is stored in a cookie named 'refresh'
        response.delete_cookie('access')   # Also delete the access token cookie if it exists
        return response
