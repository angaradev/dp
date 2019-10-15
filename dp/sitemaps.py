from django.contrib.sitemaps import Sitemap
from blogs.models import Blogs, OldBlogs
from products.models import Categories, Products
from django.shortcuts import reverse




class BlogsSitemap(Sitemap):

    def items(self):
        return Blogs.objects.all()


class OldBlogsSitemap(Sitemap):

    def items(self):
        return OldBlogs.objects.all()



class StaticViewsSitemap(Sitemap):

    def items(self):
        return ['about',
                'payment',
                'contacts',
                'delivery',
                'guaranties',
                'requsites',
                ]


    def location(self, item):

        return reverse(item)
class CategoriesSitemap(Sitemap):

    def items(self):
        return Categories.objects.all()


class ProductsSitemap(Sitemap):

    def items(self):
        return Products.objects.all()
    

class ZapchastiCarSitemap(Sitemap):

    def items(self):
        
        cars = Products.objects.values('car').distinct()
        car_list = [ car['car'] for  car in cars ]
        return car_list
    
    def location(self, item):
        return reverse('car_page', kwargs=({'car': item}))

class ZapchastiCarSubcatSitemap(Sitemap):
    
    def items(self):
        cars = ZapchastiCarSitemap.items(self)
        parts = Products.objects.all()
        l = []
        for car in cars:
            qs = parts.filter(car=car)
            for u in qs:
                for ur in u.cat.all():
                    l.append([car, ur.slug])
        return l

    def location(self, item):
        return reverse('car_page_subcats', args=(item))





