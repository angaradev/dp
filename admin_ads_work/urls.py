from django.contrib import admin
from django.urls import path
from .views import (
        ad_view,
        )
urlpatterns = [
            path('adgroup/<int:pk>/', ad_view, name='adgroup'),
            ]
 
