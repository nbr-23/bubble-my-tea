from django.views.generic import TemplateView




class OrderConfirmView(TemplateView):
    template_name = 'order_confirm.html'

   