from django.contrib import admin
from django.urls import path
from blogs.views import blogs, blog
from django.conf import settings
from django.conf.urls.static import static
from home.views import home, about
from django.conf.urls import include
from products.views import newparts, subcat, cars, cars_subcats, detailed
from accounts.views import login_view, register_view, logout_view
from admin_photos.views import admin_photos_view, admin_photos_statistic, admin_photo_listing, admin_detailed_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', blogs, name='blogs'),
    path('login/', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register_view, name='register'),
    path('blogs/<slug:slug>/', blog, name='blog'),
    path('', home, name='home'),
    path('newparts/', newparts, name='newparts'),
    path('subcat/<slug:slug>/', subcat, name='subcat'),
    path('zapchasti/<str:car>/', cars, name='car_page'),
    path('zapchasti/<str:car>/<slug:slug>/', cars_subcats, name='car_page_subcats'),
    path('product/<int:pk>/', detailed, name='detailed'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('adminphotos/', admin_photos_view, name='adminphotos'),
    path('adminphotosstatistic/', admin_photos_statistic, name='adminphotosstatistic'),
    path('adminphotolisting/<int:pk>', admin_photo_listing, name='adminphotolisting'),
    path('admindetailedview/<int:pk>/', admin_detailed_view, name='admin_detailed_view'),
    path('about/', about, name='about'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
