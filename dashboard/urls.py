from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns=[

path('dashboard/', login_required(dashboard), name='dashboard'),
path('', login_required(home), name='home'),

]
