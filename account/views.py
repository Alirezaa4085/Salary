from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomRegistrationForm
from account.models import UserProfile
from django.contrib.auth.models import User

from utils.email_service import * 
from django.core.mail import send_mail

def register_view(request):

    form = CustomRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        UserProfile.objects.create(user=user)
        login(request, user)
        send_email('فعالسازی حساب کاربری', 'یک اکانت جدید با ایمیل شما در سایت ما ساخته شد', [user.email])
        send_emailtemplate('فعالسازی حساب کاربری', user.email, {'user': user}, 'emails/activate_account.html')

        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            # print(user.email)
            send_email('هک شدیم', 'یه کصکشی توی اکانتت لاگین کرد', [user.email])
            # send_emailtemplate('فعالسازی حساب کاربری', 'alirezalucifer@gmail.com',  {'user': user}, 'emails/activate_account.html')

            login(request, user)
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    send_email('کیرمم نمیتونن بخورن', 'کصکشا سعی کردن بیان تو اکانتت که کیر خوردن', [user.email])
                except User.DoesNotExist:
                    pass
    return render(request, 'login.html', {'form': form})

#logout
def user_logout(request):
    logout(request)
    return redirect('home')
