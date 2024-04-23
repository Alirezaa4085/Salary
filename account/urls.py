from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns=[
    
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', login_required(user_logout), name='logout'),
   
]
