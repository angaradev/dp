from django.contrib import admin
from django.urls import path
from .views import (
        ad_view,
        ad_all_groups_view,
        ad_camps,
        make_ads_by_kernel,
        adds_templates,
        make_templates,
        make_same_path,
        adgroups_del,
        )
urlpatterns = [
            path('adgroup/<int:camp_id>/<int:pk>/', ad_view, name='adgroup'),
            path('adgroupview/<int:camp_id>/', ad_all_groups_view, name='adgroupview'),
            path('adcamps/', ad_camps, name='adcamps'),
            path('main/', make_ads_by_kernel, name='main'),
            path('adtemplate/<int:camp_id>/', adds_templates, name='adtemplate'),
            path('maketemplates/<int:camp_id>/', make_templates, name='maketemplates'),
            path('makesamepath/<int:camp_id>/', make_same_path, name='makesamepath'),
            path('adgroupsdelete/<int:camp_id>/', adgroups_del, name='adgroupsdelete'),
            ]
 
