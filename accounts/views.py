from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, UserAccountForm, ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from products.models import Orders




from django.contrib.auth import(
        authenticate,
        get_user_model,
        login,
        logout,
        )





def account_view(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username) 
        orders = Orders.objects.all()
        initial_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                }
        initial_data_profile = {
                'phone': user.profile.phone,
                'address': user.profile.address,
                'country': user.profile.country,
                }
        if request.method == 'POST':
            user_form = UserAccountForm(request.POST or None, instance=request.user, initial=initial_data)
            profile_form = ProfileForm(request.POST or None, instance=request.user.profile, initial=initial_data_profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()            
                profile_form.save()
        else:
           user_form = UserAccountForm(initial=initial_data)
           profile_form = ProfileForm(initial=initial_data_profile)
    else:
        return redirect('login')
            
    context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'orders': orders,
            }
    return render(request, 'accounts/account.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('account')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('account')
    context = {
                'form': form,
            }
    return render(request, 'accounts/login.html', context)



def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        if login(request, new_user):
            return redirect('account')
    context = {
                'form': form,
            }
    return render(request, 'accounts/register.html', context)



def logout_view(request):
    logout(request)
    context = {
                
            }
    return redirect('home') 
