from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'account/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # {'name':"rice", 'price':150}
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('account-login')

    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    transactions = user.transaction_set.all().order_by('-created_at')
    
    
    context = {'transactions':transactions}
    return render(request,'account/profile.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_user(request):
    user_list = User.objects.all()
    context = {'user_list':user_list}
    return render(request, 'account/edit_user.html', context)

@user_passes_test(lambda u: u.is_superuser)
def del_user(request,u_id):
    user = User.objects.get(pk=u_id)
    user.is_active = False
    user.save()
    return redirect('account-user-edit')

