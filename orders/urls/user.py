from django.urls import path
from orders.views.login import LoginView
from orders.views.register import RegisterView
from orders.views.profile import ProfileView
from orders.views.reset import ResetView


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', RegisterView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('ask-reset/', ResetView.as_view(), name='reset'),  
]
