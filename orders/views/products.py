from django.views.generic import TemplateView
from orders.models.products import Products  
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from orders.models.users import User 

class ProductListView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
      
        user_id = request.session['user_id']

       
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        
        # Check if authentified and Il est admin , on sait jamais :)
        user_id = self.request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
            is_admin = user.is_admin
        except User.DoesNotExist:
            is_admin = False
        
        context['is_admin'] = is_admin
        return context
