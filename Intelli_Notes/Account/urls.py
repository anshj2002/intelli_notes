from django.urls import path
from . import views

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('set_username/', views.set_username, name='set_username'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('', views.home, name='home'),  # Assuming you have a home view
]
