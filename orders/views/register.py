
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RegisterView(View):
    template_name = 'register.html'
    success_url = reverse_lazy('home') 
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    """def post(self, request, *args, **kwargs):
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password != confirm_password:
            return render(request, self.template_name, {
                'error_message': 'Les mots de passe ne correspondent pas.'
            })

        hashed_password = make_password(password)
        
        # Authentification de l'utilisateur
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {
                'error_message': 'Authentification échouée'
            })"""

