from django.views.generic import TemplateView
from orders.models.products import Products
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy  

class ProductShopView(TemplateView):
    template_name = 'product_shop.html'
    login_url = reverse_lazy('login')  

    def dispatch(self, request, *args, **kwargs):
        # Vérifier si l'utilisateur est connecté
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
        # If 'user_id' exists, retrieve additional information if necessary
        # For example, check the validity of the token or other security checks
        user_id = request.session['user_id']

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        return context