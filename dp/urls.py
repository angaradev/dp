from django.contrib import admin
from django.urls import path
from blogs.views import blogs, blog
from django.conf import settings
from django.conf.urls.static import static
from home.views import home
from products.views import newparts, subcat, cars, cars_subcats, detailed


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', blogs, name='blogs'),
    path('blogs/<slug:slug>/', blog, name='blog'),
    path('', home, name='home'),
    path('newparts/', newparts, name='newparts'),
    path('subcat/<slug:slug>/', subcat, name='subcat'),
    path('zapchasti/<str:car>/', cars, name='car_page'),
    path('zapchasti/<str:car>/<slug:slug>/', cars_subcats, name='car_page_subcats'),
    path('product/<int:pk>/', detailed, name='detailed'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
