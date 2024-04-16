from django.views.generic import TemplateView
from orders.models import products  # Assurez-vous d'importer le modèle Products

class ProductListView(TemplateView):
    template_name = 'product_list.html'
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = products.objects.all()
        return context
"""