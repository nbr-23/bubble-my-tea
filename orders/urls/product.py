from django.urls import path
from orders.views.products import ProductListView
from orders.views.product_add import ProductAddView
from orders.views.product_update import ProductUpdateView
from orders.views.product_delete import ProductDeleteView
from orders.views.product_show import ProductShowView
from orders.views.product_shop import ProductShopView
from orders.views.product_shop_show import ProductShopShowView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='products_list'),
    path('product/shop', ProductShopView.as_view(), name='product_shop'),
    path('product/shop/show/<int:product_id>/', ProductShopShowView.as_view(), name='product_shop_show'),
    path('product/add', ProductAddView.as_view(), name='product_add'),
    path('product/show/<int:product_id>/', ProductShowView.as_view(), name='product_show'),
    path('product/update/<int:product_id>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:product_id>/', ProductDeleteView.as_view(), name='product_delete')
    
]