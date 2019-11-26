from django.shortcuts import render
from .forms import AdGroupForm
from .models import AdGroups, Keywords, Negative
from django.forms import inlineformset_factory
from django.shortcuts import redirect


def ad_view(request, pk):
    ad_group = AdGroups.objects.get(group_id=pk)
    keywords_formset = inlineformset_factory(AdGroups, Keywords, fields=('keyword',), extra=1)
    negative_formset = inlineformset_factory(AdGroups, Negative, fields=('negative',), extra=1)
    if request.method == 'POST':
        form = AdGroupForm(request.POST, instance=ad_group)
        formset = keywords_formset(request.POST, instance=ad_group)
        n_f = negative_formset(request.POST, instance=ad_group)
        if form.is_valid() or formset.is_valid() or n_f.is_valid():
            form.save()
            formset.save()
            n_f.save()
            return redirect('ad:adgroup', pk)
    else:
        form = AdGroupForm(instance=ad_group)
        formset = keywords_formset(instance=ad_group)
        n_f = negative_formset(instance=ad_group)
        
    context = {
            'adform': form,
            'keyform': formset,
            'negativeform': n_f,
            }
    return render(request, 'admin/adgroups/adgroup.html', context)
