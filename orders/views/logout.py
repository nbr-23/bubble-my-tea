from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import logout

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)  # Clears all sessions
        
        response = HttpResponseRedirect(reverse_lazy('login'))
        response.delete_cookie('refresh')
        response.delete_cookie('access')
        return response
