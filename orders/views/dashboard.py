from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
        # If 'user_id' exists, retrieve additional information if necessary
        # For example, check the validity of the token or other security checks
        user_id = request.session['user_id']
        

        # Render the dashboard page if everything is correct
        return super().get(request, *args, **kwargs)
