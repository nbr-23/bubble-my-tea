from django.urls import path
from orders.views.order import OrderView
from orders.views.dashboard import DashboardView
from orders.views.admin import AdminView

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
