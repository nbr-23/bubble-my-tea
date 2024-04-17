from django.urls import path
from orders.views.order_items import OrderItemsView
from orders.views.dashboard import DashboardView
from orders.views.admin import AdminView

urlpatterns = [
    path('order/items', OrderItemsView.as_view(), name='order_items'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
