from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('fillform/', login_required(Fill_Mycompany_form), name='Fill_Mycompany_form'),
    path('fillform/add/', login_required(add_profile), name='add_profile'),
    path('fillform/edit/<int:pk>/', login_required(edit_profile), name='edit_profile'),
    path('fillform/delete/<int:profile_id>/', login_required(delete_profile), name='delete_profile'),

    # path('fillform/delete/<int:pk>/', login_required(delete_profile), name='delete_profile'),

]
