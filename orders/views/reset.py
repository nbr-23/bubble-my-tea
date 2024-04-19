from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class ResetView(TemplateView):
    template_name = 'ask-reset.html'
    
    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
     
        user_id = request.session['user_id']

       
        return super().get(request, *args, **kwargs)
    
