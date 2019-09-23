from django.shortcuts import render
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import redirect


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
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('blogs')
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
        login(request, new_user)
    context = {
                'form': form,
            }
    return redirect('home') 



def logout_view(request):
    logout(request)
    context = {
                
            }
    return redirect('home') 
