from django.views.generic import TemplateView



class ProductListView(TemplateView):
    template_name = 'order.html'
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        return context"""