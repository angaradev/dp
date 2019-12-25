from django.contrib import admin
from django.urls import path
from blogs.views import blogs, blog, oldblog, oldblogs
from django.conf import settings
from django.conf.urls.static import static
from home.views import home, about
from django.conf.urls import include
from products.views import newparts, subcat, cars, cars_subcats, detailed, search, del_car
from accounts.views import login_view, register_view, logout_view, account_view
from admin_photos.views import (admin_photos_view, admin_photos_statistic, admin_photo_listing,
admin_detailed_view,upload_files, create_dirs, admin_photo_search, ChartData, make_stat)
from admin_photos.views import admin_empty_listing, nocat_product
from home.views import home, about, payment, contacts, delivery, guaranties, policy, requsites, reviews, thankyoucall
from admin_photos.cron_stat import make_stat
from .sitemaps import BlogsSitemap, StaticViewsSitemap, CategoriesSitemap, ProductsSitemap, ZapchastiCarSitemap
from .sitemaps import ZapchastiCarSubcatSitemap, OldBlogsSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from products.cart_views import cart_view, add_to_cart, remove_from_cart, update_cart, clear_cart, order_view
from products.cart_views import order_success, add_to_wish, remove_wish, see_wish, clear_wish
from interlink.views import subcat_ducato_redirect, subcat_boxer_redirect, subcat_jumper_redirect, analog_part_brand
from email_form.views import e_form_view, footer_form




handler404 = 'dp.views.error404'
handler500 = 'dp.views.error500'
handler403 = 'dp.views.error403'
handler400 = 'dp.views.error400'


sitemaps = {
        'blogs': BlogsSitemap,
        'oldblogs': OldBlogsSitemap,
        'static': StaticViewsSitemap,
        'categories': CategoriesSitemap,
        'zapchasti': ZapchastiCarSitemap,
        'zapchasticat': ZapchastiCarSubcatSitemap,
        'products': ProductsSitemap,
        }




urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', blogs, name='blogs'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('account/', account_view, name='account'),
    path('blogs/<slug:slug>/', blog, name='blog'),
    path('articles/<int:pk>/', oldblog, name='oldblog'),
    path('articles/', oldblogs, name='oldblogs'),
    path('', home, name='home'),
    path('thankyoucall/', thankyoucall, name='thankyoucall'),
    path('newparts/', newparts, name='newparts'),
    path('subcat/<slug:slug>/', subcat, name='subcat'),
    path('delcar/<str:car>/<slug:slug>/', del_car, name='delcar'),
    path('zapchasti/<str:car>/', cars, name='car_page'),
    path('zapchasti/<str:car>/<slug:slug>/', cars_subcats, name='car_page_subcats'),
    path('product/<int:pk>/', detailed, name='detailed'),
    path('search/', search, name='search'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('adminphotos/', admin_photos_view, name='adminphotos'),
    path('adminphotosstatistic/', admin_photos_statistic, name='adminphotosstatistic'),
    path('adminphotolisting/<int:pk>/', admin_photo_listing, name='adminphotolisting'),
    path('adminemptylisting/', admin_empty_listing, name='adminemptylisting'),
    path('admindetailedview/<int:pk>/', admin_detailed_view, name='admin_detailed_view'),
    path('adminfilesupload/<int:pk>/', upload_files, name='adminfilesupload'),
    path('adminnocat/', nocat_product, name='adminnocat'),
    path('createdirs/', create_dirs, name='createdirs'),
    path('adminphotosearch/', admin_photo_search, name='adminphotosearch'),
    path('about/', about, name='about'),
    path('reviews/', reviews, name='reviews'),
    path('payment/', payment, name='payment'),
    path('contacts/', contacts, name='contacts'),
    path('delivery/', delivery, name='delivery'),
    path('guaranties/', guaranties, name='guaranties'),
    path('policy/', policy, name='policy'),
    path('requsites/', requsites, name='requsites'),
    path('footerform/', footer_form, name='footer_form'),
    path('api/chart/data/', ChartData.as_view()),
    path('api/chart/insertdata/', make_stat),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', TemplateView.as_view(template_name='home/robots.txt', content_type='text/plain')),
    path('cart/', cart_view, name='cart'),
    path('wish/', see_wish, name='wish'),
    path('addtocart/', add_to_cart, name='add_to_cart'),
    path('addtowish/', add_to_wish, name='add_to_wish'),
    path('removefromcart/', remove_from_cart, name='remove_from_cart'),
    path('removefromwish/', remove_wish, name='remove_wish'),
    path('updatecart/', update_cart, name='update_cart'),
    path('clearcart', clear_cart, name='clear_cart'),
    path('clearwish', clear_wish, name='clear_wish'),
    path('order/', order_view, name='order'),
    path('ordersuccess/<str:order_n>/', order_success, name='order_success'),
    path('subcategory/', include(('interlink.urls', 'interlink'), namespace='interl')),
    path('dictionary/', include(('group_dict.urls', 'dictionary'), namespace='dictionary')),
    path('fiat-ducato-250/subcategory/<int:pk>/', subcat_ducato_redirect, name='sub_ducato_redir'),
    path('fiat-ducato-250-new/subcategory/<int:pk>/', subcat_ducato_redirect, name='sub_ducato_redir'),
    path('fiat-ducato-244/subcategory/<int:pk>/', subcat_ducato_redirect, name='sub_ducato_redir'),
    path('peugeot-boxer/subcategory/<int:pk>/', subcat_boxer_redirect, name='sub_boxer_redir'),
    path('peugeot-boxer-1/subcategory/<int:pk>/', subcat_boxer_redirect, name='sub_boxer_redir'),
    path('peugeot-boxer-2/subcategory/<int:pk>/', subcat_boxer_redirect, name='sub_boxer_redir'),
    path('peugeot-boxer-3/subcategory/<int:pk>/', subcat_boxer_redirect, name='sub_boxer_redir'),
    path('citroen-jumper/subcategory/<int:pk>/', subcat_jumper_redirect, name='sub_jumper_redir'),
    path('citroen-jumper-1/subcategory/<int:pk>/', subcat_jumper_redirect, name='sub_jumper_redir'),
    path('citroen-jumper-2/subcategory/<int:pk>/', subcat_jumper_redirect, name='sub_jumper_redir'),
    path('citroen-jumper-3/subcategory/<int:pk>/', subcat_jumper_redirect, name='sub_jumper_redir'),
    path('analognumber/<str:old_url>/', analog_part_brand, name='analog'),
    path('catalognumber/<str:old_url>/', analog_part_brand, name='analog'),
    path('emailformsend', e_form_view, name='send_e_form'),
    path('ad/', include(('admin_ads_work.urls', 'admin_ads_works'), namespace='ad')),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
