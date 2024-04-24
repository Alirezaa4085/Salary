from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from account.models import UserProfile

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # ایجاد UserProfile همزمان با ایجاد کاربر
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {'form': form})

#logout
def user_logout(request):
    logout(request)
    return redirect('home')
