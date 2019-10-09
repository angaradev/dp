from django.shortcuts import render


def subcat_redirect(request, pk):
    print(pk)
    return render(request, 'home/home.html', {})
