from django.urls import path
from orders.views.products import ProductListView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='products_list')
]