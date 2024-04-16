from django.urls import path
from orders.views.products import ProductListView
from orders.views.product_add import ProductAddView
from orders.views.product_update import ProductUpdateView
from orders.views.product_delete import ProductDeleteView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='products_list'),
    path('product/add', ProductAddView.as_view(), name='product_add'),
    path('product/update/<int:product_id>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:product_id>/', ProductDeleteView.as_view(), name='product_delete')
    
]