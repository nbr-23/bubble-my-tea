from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        # If the user is already logged in, redirect to the homepage.
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect(self.success_url)
        
        # Otherwise, display the login form
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(self.success_url)

        # If the form is not valid, return to the form with an error message.
        return render(request, self.template_name, {'form': form, 'error_message': 'Invalid username or password'})

