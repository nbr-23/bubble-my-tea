from django.views.generic import TemplateView
from orders.models.products import Products
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy  
from orders.models.users import User 

class ProductShopView(TemplateView):
    template_name = 'product_shop.html'
    login_url = reverse_lazy('login')  

    def dispatch(self, request, *args, **kwargs):
        # Vérifier si l'utilisateur est connecté
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
     
        user_id = request.session['user_id']

        try:
            user = User.objects.get(id=user_id)
            is_admin = user.is_admin
        except User.DoesNotExist:
            is_admin = False
        
        context = {
        'is_admin': is_admin
        }

      
        return super().get(request, *args, **kwargs, **context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        
      
        user_id = self.request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
            is_admin = user.is_admin
        except User.DoesNotExist:
            is_admin = False
        
        context['is_admin'] = is_admin
        return context