
from django.contrib import admin
from django.urls import path
from .views import (insert_kernel,
        main_work,
        check_group,
        change_group,
        view_groups,
        view_group,
        categorizer,
        kernel_clean,
        load_kernel,
        insert_data,
        get_csv,
        split_kernel,
        split_kernel_clean,
        )
urlpatterns = [
            path('insertkernel/<str:mode>/', insert_kernel, name='insert_kernel'),
            path('mainwork/', main_work, name='main_work'),
            path('checkgroup/', check_group, name='check_group'),
            path('changegroup/<int:pk>/', change_group, name='change_group'),
            path('viewgroups/', view_groups, name='view_groups'),
            path('viewgroup/<int:pk>/', view_group, name='view_group'),
            path('categorizer/', categorizer, name='categorizer'),
            path('kernelclean/', kernel_clean, name='kernelclean'),
            path('loadkernel/', load_kernel, name='loadkernel'),
            path('insertdata/', insert_data, name='insertdata'),
            path('getcsv/<str:mode>/', get_csv, name='getcsv'),
            path('splitkernel/', split_kernel, name='splitkernel'),
            path('splitkernelclean/', split_kernel_clean, name='splitkernelclean'),
        ]
