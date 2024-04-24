from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from account.forms import UserProfileForm 
from account.models import UserProfile
from salary.models import SalaryInformation
from django.http import JsonResponse


def Fill_Mycompany_form(request):
     # یافتن کاربری که لاگین کرده است
    current_user = request.user
    # دریافت همه اطلاعات UserProfile ها از پایگاه داده
    user_profiles = UserProfile.objects.filter(user=current_user)

    return render(request, 'profile.html', {'user_profiles': user_profiles})

def pay(request, salary_info_id):
    salary_info = get_object_or_404(SalaryInformation, id=salary_info_id)

    # انجام عملیات واریزی، به عنوان مثال اینجا یک فیلد در SalaryInformation را به True تغییر می‌دهیم
    salary_info.paid = True
    salary_info.save()

    return JsonResponse({'success': True})



def add_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # بدست آوردن یوزری که لاگین کرده است
            user = request.user
            # ذخیره کردن یوزر به عنوان مقدار فیلد user در فرم
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('dashboard')  # یا هر مسیر دیگری که مد نظر شماست
    else:
        form = UserProfileForm()
    return render(request, 'add_profile.html', {'form': form})

def edit_profile(request, pk):
    user_profile = UserProfile.objects.get(pk=pk)
    form = UserProfileForm(request.POST or None, instance=user_profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')  # یا هر مسیر دیگری که مد نظر شماست
    return render(request, 'edit_profile.html', {'form': form})