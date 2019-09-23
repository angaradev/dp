from django.shortcuts import render
from .forms import UserLoginForm


from django.contrib.auth import(
        authenticate,
        get_user_model,
        login,
        logout,
        )



def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

    context = {
                'form': form,

            
            }
    return render(request, 'accounts/login.html', context)



def register_view(request):
    context = {

            }
    return render(request, 'accounts/register.html', context)



def logout_view(request):
    context = {

            }
    return render(request, 'accounts/logout.html', context)
