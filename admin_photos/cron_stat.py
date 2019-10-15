from .models import PhotoStatistic
from django.contrib.auth.decorators import login_required
from products.models import Products
from django.shortcuts import redirect
import datetime

@login_required
def make_stat(request):
    qs = Products.objects.values('img_check')
    checked = len(qs.filter(img_check=True))
    unchecked = len(qs.filter(img_check=False))
    print(datetime.date.today)

    try:
        obj = PhotoStatistic(
            checked_count = checked,
            unchecked_count = unchecked,
            checked_date = datetime.date.today()
            )
        obj.save()
    except:

        obj = PhotoStatistic.objects.filter(checked_date = datetime.date.today())
    
    
    return redirect('/api/chart/data/')
