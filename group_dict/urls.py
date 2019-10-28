
from django.contrib import admin
from django.urls import path
from .views import insert_kernel, main_work, check_group, change_group
urlpatterns = [
            path('insertkernel/', insert_kernel, name='insert_kernel'),
            path('mainwork/', main_work, name='main_work'),
            path('checkgroup/', check_group, name='check_group'),
            path('changegroup/<int:pk>/', change_group, name='change_group'),
        ]
