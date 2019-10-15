from django.contrib import admin
from django.urls import path
from .views import subcat_redirect
urlpatterns = [
            path('<int:pk>/', subcat_redirect, name='sub_redir'),
        ]
