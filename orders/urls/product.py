from django.urls import path
from orders.views.products import ProductListView
from orders.views.product_add import ProductAddView
from orders.views.product_update import ProductUpdateView
from orders.views.product_delete import ProductDeleteView
from orders.views.product_show import ProductShowView
from orders.views.product_shop import ProductShopView
from orders.views.product_shop_show import ProductShopShowView
from orders.views.add_to_cart import AddToCartView
from orders.views.remove_from_cart import RemoveCartItemView
from orders.views.update_cart import UpdateCartItemView
from orders.views.update_cart import UpdateCartItemView
from orders.views.payment import ProcessPaymentView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='products_list'),
    path('product/shop', ProductShopView.as_view(), name='product_shop'),
    path('product/shop/show/<int:product_id>/', ProductShopShowView.as_view(), name='product_shop_show'),
    path('product/add', ProductAddView.as_view(), name='product_add'),
    path('product/show/<int:product_id>/', ProductShowView.as_view(), name='product_show'),
    path('product/update/<int:product_id>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:product_id>/', ProductDeleteView.as_view(), name='product_delete'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/', RemoveCartItemView.as_view(), name='remove_from_cart'),
    path('update_cart/', UpdateCartItemView.as_view(), name='update_cart'),
    path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    
]