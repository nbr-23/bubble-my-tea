from django.urls import path
from orders.views.products import ProductListView
from orders.views.product_add import ProductAddView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='products_list'),
    path('product/add', ProductAddView.as_view(), name='product_add')
]