from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomRegistrationForm
from account.models import UserProfile
from django.contrib.auth.models import User
from utils.email_service import * 

def register_view(request):

    form = CustomRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        login(request, user)
        send_template_email(user,'emails/signup.html')
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
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            ip_address = request.META.get('REMOTE_ADDR', 'unknown') 
            context = {
                'user_agent': user_agent,
                'ip_address': ip_address,
            }
            send_template_email(user, user_agent, ip_address, 'emails/login.html')
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
                    ip_address = request.META.get('REMOTE_ADDR', 'unknown') 
                    context = {
                        'user_agent': user_agent,
                        'ip_address': ip_address,
                        }                    
                    send_template_email(user, user_agent, ip_address, 'emails/Failed_Login_Attempt.html')
                except User.DoesNotExist:
                    pass
    return render(request, 'login.html', {'form': form})

#logout
def user_logout(request):
    logout(request)
    return redirect('home')
