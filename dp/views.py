from django.shortcuts import render




def error404(request, exception=None):
    return render(request, 'errors/404.html', {})


def error500(request, exception=None):
    return render(request, 'errors/500.html', {})


def error403(request, exception=None):
    return render(request, 'errors/403.html', {})


def error400(request, exception=None):
    return render(request, 'errors/400.html', {})
