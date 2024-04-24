from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('fillform/', login_required(Fill_Mycompany_form), name='Fill_Mycompany_form'),
    path('add_profile/', add_profile, name='add_profile'),
    path('edit_profile/<int:pk>/', edit_profile, name='edit_profile'),

        
]