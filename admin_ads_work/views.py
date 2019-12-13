from django.shortcuts import render
from .forms import AdGroupForm, CarForm, CampFormSingle, CampEditForm, CampCreateForm
from .models import AdGroups, Keywords, Negative, Adds, Campaigns, Cars, AddsTemplate
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import redirect
from group_dict.models import Groups, KernelReadyCommercial
from django.contrib.auth.decorators import login_required
import re
import pymorphy2 as pm
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
import csv


@login_required
def make_headliner_copy(request, camp_id):
    qs = Campaigns.objects.get(id=camp_id)
    form = CampFormSingle(request.POST)
    campForm = CampEditForm(instance=qs )
    if request.method == 'POST':
        if request.POST.get('camp_name'):
            camp_form = campForm(request.POST)
            if camp_form.is_valid:
                campForm.save()
            else:
                camt_form = campForm()
        camp_from = request.POST.get('camp_from', None)
        if camp_from:
            if form.is_valid():
                adgroups = AdGroups.objects.filter(camp_id=Campaigns.objects.get(id=int(camp_from)))
                for adgroup in adgroups:
                    n_adgroup, created = AdGroups.objects.get_or_create(group_id=adgroup.group_id, ad_group_name=adgroup.ad_group_name,
                            max_cpc=adgroup.max_cpc,
                            max_cpm=adgroup.max_cpm,
                            final_url=adgroup.final_url,
                            camp_id=qs,
                            inner_labels=adgroup.inner_labels,
                            dont_use = adgroup.dont_use
                            )
                
                    ads = adgroup.adds_set.all()
                    pluses = adgroup.keywords_set.all()
                    minuses = adgroup.negative_set.all()
                    for plus in pluses:
                        p, pc = Keywords.objects.get_or_create(group=n_adgroup, keyword=plus.keyword,
                                labels=plus.labels, criterion_type=plus.criterion_type,
                                max_cpc=plus.max_cpc
                                )
                    for minus in minuses:
                        m, mc = Negative.objects.get_or_create(group=n_adgroup, negative=minus.negative)
                    for ad in ads:
                        a, ac = Adds.objects.get_or_create(ad_group=n_adgroup,
                               headline1=ad.headline1,
                               headline2=ad.headline2,
                               headline3=ad.headline3,
                               path1=ad.path1,
                               path2=ad.path2,
                               description1=ad.description1,
                               description2=ad.description2,
                               variant=ad.variant,
                               camp_id=qs
                                )

    context = {
            'form':form,
            'campform': campForm,
            }
    return render(request, 'admin/adgroups/single_ad_group.html', context)




@login_required
def get_google_csv(request, camp_id):
    resp = HttpResponse(content_type='text/csv', charset='utf-16')
    resp['Content-Disposition'] = 'attachment; filename="google_test.csv"'
    qs = AdGroups.objects.filter(camp_id=Campaigns.objects.get(id=camp_id)).exclude(dont_use=True)
    writer = csv.writer(resp)

    writer.writerow(['Campaign', 'Labels', 'Budget', 'Budget type', 'Campaign Type', 'Networks', 'Ad Group',
        'Max CPC', 'Max CPM', 'Final URL', 'Criterion Type', 'Keyword', 'Description Line 1', 'Description Line 2',
        'Headline 1', 'Headline 2', 'Headline 3', 'Path 1', 'Path 2'        
        ])
    
    for row in qs:
        plus_obj = row.keywords_set.all()

        minus_list = [x.negative for x in row.negative_set.all()]
        minus = ' '.join(minus_list)
        ads = row.adds_set.all()
        row.ad_group_name = row.ad_group_name.title()
        writer.writerow([row.camp_id, '', '', '', '', '', row.ad_group_name, row.max_cpc, row.max_cpm, '', '', '', '', '', '', '', '', '', '' ])

        for m in minus_list:
            writer.writerow([row.camp_id, '', '', '', '', '', row.ad_group_name, '', '', '',
                'Negative Broad', m, '', '', '', '', '', '', ''  ])

        for plus in plus_obj:

            writer.writerow([row.camp_id, plus.labels, '', '', '', '', row.ad_group_name, plus.max_cpc, '', '',
                plus.criterion_type, plus.keyword, '', '', '', '', '', '', ''  ])

        for ad in ads:
            writer.writerow([row.camp_id, plus.labels, '', '', '', '', row.ad_group_name, '', '', row.final_url,
                '', '', ad.description1, ad.description2, ad.headline1,
                ad.headline2, ad.headline3, ad.path1, ad.path2])
        #ads[0].description1, ads[0].description2, ads[0].headline1,
        #        ads[0].headline2, ads[0].headline3, ads[0].path1, ads[0].path2


        #writer.writerow([row.camp_id, '', '', '', '', '', row.ad_group_name, '', '', row.final_url, '', '', '', '', '', '', '',
        #        '', '', '' ])
    return resp
    #return redirect('ad:adcamps')

@login_required
def get_yandex_csv(request, camp_id):
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="yandex_test.csv"'
    qs = AdGroups.objects.filter(camp_id=Campaigns.objects.get(id=camp_id), dont_use=False)
    writer = csv.writer(resp)
    writer.writerow(['Предложение текстовых блоков для рекламной кампании'])
    writer.writerow(['', '', '', 'Тип кампании:', 'Текстово-графическая кампания'])
    writer.writerow(['', '','', '№ заказа'])
    writer.writerow(['', '','', 'Минус-фразы на кампанию:'])
    writer.writerow(['Доп. объявление группы', 'Тип объявления', 'Мобильное объявление', 'ID группы', 'Название группы',
	'Номер группы', 'Статус \"Мало показов\"', 'ID фразы', 'Фраза (с минус-словами)', 'ID объявления', 'Заголовок 1',
	'Заголовок 2', 'Текст', 'заголовок 1', 'заголовок 2', 'текст', 'Ссылка', 'Отображаемая ссылка', 'Регион',
	'Ставка', 'Ставка в сетях', 'Контакты', 'Статус объявления', 'Статус фразы', 'Заголовки быстрых ссылок',
	'Описания быстрых ссылок', 'Адреса быстрых ссылок', 'Турбо-страницы быстрых ссылок', 'Параметр 1', 'Параметр 2',
	'Метки', 'Изображение', 'Креатив', 'Статус модерации креатива', 'Турбо-страница', 'Уточнения',
	'Минус-фразы на группу', 'Возрастные ограничения', 'Ссылка на приложение в магазине', 'Тип устройства', 'Тип связи',
	'Версия ОС', 'Трекинговая ссылка', 'Иконка', 'Рейтинг', 'Количество оценок', 'Цена' ])
    camp = Campaigns.objects.get(id=camp_id)	
    fast_link = camp.fast_link_yand
    fast_link_desc = camp.fast_link_yand_desc
    fast_link_url = camp.fast_link_yand_url
    for row in qs:
        plus_obj = row.keywords_set.all()
        minus_list = [x.negative for x in row.negative_set.all()]
        minus = ' '.join(minus_list)
        ads = row.adds_set.all()
        for plus in plus_obj:
            plus.keyword = plus.keyword.replace('+', '')
            writer.writerow(['-',  'Текстово-графическое', '-', '', row.ad_group_name, row.id, '', '', plus.keyword + ' ' + minus,
            '',  ads[0].headline1, ads[0].headline2, ads[0].description1, '', '', '', row.final_url,
            ads[0].path1,'', '', '', '', '', '', fast_link, fast_link_desc, fast_link_url, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', ''])
            writer.writerow(['+',  'Текстово-графическое', '-', '', row.ad_group_name, row.id, '', '', plus.keyword + ' ' + minus,
            '',  ads[1].headline1, ads[1].headline2, ads[1].description1, '', '', '', row.final_url, ads[1].path1,'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            writer.writerow(['+',  'Текстово-графическое', '-', '', row.ad_group_name, row.id, '', '', plus.keyword + ' ' + minus,
            '',  ads[2].headline1, ads[2].headline2, ads[2].description1, '', '', '', row.final_url, ads[2].path1,'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    return resp




@login_required
def ad_view(request, camp_id, pk):
    group = Groups.objects.get(id=pk)
    c_id = Campaigns.objects.get(id=camp_id)
    ad_group_create = AdGroups.objects.get_or_create(group_id=group, ad_group_name=group.name, camp_id=c_id)
    ad_group = AdGroups.objects.get(group_id=pk, camp_id=camp_id)
    keywords_formset = inlineformset_factory(AdGroups, Keywords, fields=('keyword',), extra=1)
    negative_formset = inlineformset_factory(AdGroups, Negative, fields=('negative',), extra=1)
    adds_formset = inlineformset_factory(AdGroups, Adds, exclude=('ad_group',), extra=1, max_num=3)
    if request.method == 'POST':
        form = AdGroupForm(request.POST, instance=ad_group)
        formset = keywords_formset(request.POST, instance=ad_group)
        n_f = negative_formset(request.POST, instance=ad_group)
        adds_f = adds_formset(request.POST, instance=ad_group)
        if form.is_valid() or formset.is_valid() or n_f.is_valid() or adds_f.is_valid():
            if form.is_valid():
                form.save()
            if formset.is_valid():
                formset.save()
            if n_f.is_valid():
                n_f.save()
            if adds_f.is_valid():
                adds_f.save()
            return redirect('ad:adgroupview', camp_id)
    else:
        form = AdGroupForm(instance=ad_group)
        formset = keywords_formset(instance=ad_group)
        n_f = negative_formset(instance=ad_group)
        adds_f = adds_formset(instance=ad_group)
        
    context = {
            'adform': form,
            'keyform': formset,
            'negativeform': n_f,
            'addsform': adds_f,
            'camp_id': camp_id,
            }
    return render(request, 'admin/adgroups/adgroup.html', context)


@login_required
def ad_all_groups_view(request, camp_id):
    qs = AdGroups.objects.filter(camp_id=camp_id).order_by('ad_group_name')
    total = qs.count()
    not_ready = qs.filter(chk=False).count()
    ready = total - not_ready
    counts = {'total': total, 'ready': ready, 'not_ready': not_ready}
    qs_camp = Campaigns.objects.all().annotate(num_ads=Count('adgroups')).order_by('camp_name')
    CampFormset = modelformset_factory(Campaigns, fields=('camp_name', 'fast_link_yand', 'fast_link_yand_desc', 'fast_link_yand_url'), extra=1)
    if request.method == 'POST':
        camp_form = CampFormset(request.POST, queryset=qs_camp)
        if camp_form.is_valid():
            camp_form.save()
            return redirect('ad:adgroupview', camp_id)
    else:
        camp_form = CampFormset(queryset=qs_camp)
    context = {
            'objects': qs,
            'counts': counts,
            'camp_id': camp_id,
            'campform': camp_form,
            }
    return render(request, 'admin/adgroups/adgroups_view_all.html', context)


@login_required
def ad_camps(request):
    car_form = CarForm(request.POST)
    if request.method == 'POST' and request.POST.get('select_car') == 'submited':
        if car_form.is_valid():
            car = car_form.cleaned_data.get('car')
            request.session['car'] = car 
        return redirect('ad:adcamps')

    qs = Campaigns.objects.all().annotate(num_ads=Count('adgroups')).order_by('camp_name')
    camp_form = CampCreateForm(request.POST)
    if request.method == 'POST' and request.POST.get('camp_create'):
        if camp_form.is_valid():
            camp_form.save()
            return redirect('ad:adcamps')

    context = {
            'objects': qs,
            'campform': camp_form,
            'carform': car_form,
            }
    return render(request, 'admin/adgroups/campaigns.html', context)


#Эта функция будет создавать рекламные группы на основе ядра текущей машины
#Берет дату из таблицы с временно откатегоризированным ядром, сопоставляет
# с группами и заливает в таблицу с группами объявлений
#Нужно заплить вставку полных плюсов, полных минусов, урлов, внутренних лайблов,
#простановку типов соответствия и словоформ в минусах
@login_required
def make_ads_by_kernel(request, camp_id):
    
    #Эта функция делает типы соответствия и всталяет в ключевые слова плюс
    def make_match_type(full_plus, adgroup_id):
        def add_plus(string):
            l = string.split()
            nl = ['+' + x for x in l]
            return ' '.join(nl)

        camp_car = Campaigns.objects.get(id=camp_id)
        car = camp_car.car.car_rus
        plus_list = [s.strip() + ' ' + car for s in full_plus.splitlines()]
        for p in plus_list:
            match = [(add_plus(p), 'Broad'), ('"' + p + '"', 'Phrase'), ('[' + p + ']', 'Exact')]
            
            for m in match:
                new = Keywords.objects.get_or_create(
                    group=AdGroups.objects.get(id=adgroup_id),
                    keyword = m[0],
                    criterion_type = m[1],
                   )
    #Эти функции для работы с минус словами
    def remove_dupes(lst):
        output = []
        for l in lst:
            if l not in output:
                output.append(l)
        return output

    def make_minus_forms(full_minus, adgroup_id):
        morph = pm.MorphAnalyzer()
        minus_list = [s.strip() for s in full_minus.splitlines()]
        n_list = []
        for m in minus_list:
            if len(m.split()) == 1:
                word = morph.parse(m)[0]
                forms = word.lexeme
                for f in forms:
                    n_list.append(f.word)
        pre_final_list = remove_dupes(minus_list + n_list)
        final_list = ['-' +x for x in pre_final_list]
        for fl in final_list:
            new_minus = Negative.objects.get_or_create(
                    group=AdGroups.objects.get(id=adgroup_id),
                    negative = fl
                    )
        return final_list
    
    #camp_id = request.GET.get('mk_adgroups', None)
    if camp_id:
        qs = KernelReadyCommercial.objects.values('group_id').distinct()
        for q in qs:
            try:
                n_qs = Groups.objects.get(id=q['group_id'])
                new = AdGroups.objects.get_or_create(
                        group_id=n_qs, ad_group_name=n_qs.name,
                        camp_id=Campaigns.objects.get(id=camp_id),
                        final_url = 'http://ducatoparts.ru/some/path/' + n_qs.old_group_id + '/'
                        )
            except:
                print('Not inserted: ', q)
        #Вставляем плюс слова с модификаторами соответствия
        get_adGroup = AdGroups.objects.filter(camp_id=Campaigns.objects.get(id=camp_id))
        for ga in get_adGroup:
            full_plus = Groups.objects.get(id=ga.group_id.id)
            make_match_type(full_plus.full_plus, ga.id )
            make_minus_forms(full_plus.full_minus, ga.id)

    context = {

            }
    return render(request, 'admin/adgroups/main.html', context)

#Эта функция для создания шаблонов для рекламных объявлений
@login_required
def adds_templates(request, camp_id):
    
    qs = AddsTemplate.objects.filter(camaign=camp_id)
    TemplateFormset = modelformset_factory(AddsTemplate, fields=(
        'camaign',
        'headline1',
        'headline2',
        'headline3',
        'description1',
        'description2',
        'description3',
        'path1',
        'path2',
        'variant',
        ), extra=1, max_num=3)

    if request.method == 'POST':
        temp_form = TemplateFormset(request.POST, queryset=qs)
        if temp_form.is_valid():
            temp_form.save()
            return redirect('ad:adtemplate', camp_id)
    else:
        temp_form = TemplateFormset(queryset=qs)

    context = {
                'tempform': temp_form,
                }
    return render(request, 'admin/adgroups/templates.html', context)
        
# Эта функция заполняет всю компанию обьявлениями по шаблонам так же может удалять заполненные
# Нужно добавить заполнение конечного урл 
# Машина добавляется в ключах
@login_required
def make_templates(request, camp_id):
    camp_id = Campaigns.objects.get(id=camp_id)
    if request.GET.get('delete_templates') == 'True':
        clear_ad = Adds.objects.filter(camp_id=camp_id).delete()
    elif request.GET.get('copy_desc') == 'True':
        qs = AdGroups.objects.filter(camp_id=camp_id)
        templates = AddsTemplate.objects.filter(camaign=camp_id)
        for q in qs:
            adds = Adds.objects.filter(ad_group=q)
            for (ad, t) in zip(adds, templates):
                ad.headline2 = t.headline2
                ad.headline3 = t.headline3
                ad.description1 = t.description1
                ad.description2 = t.description2
                ad.save()

        
    else:
        qs = AdGroups.objects.filter(camp_id=camp_id)
        templates = AddsTemplate.objects.filter(camaign=camp_id)
        for q in qs:
            for t in templates:
                keywords = Keywords.objects.filter(group=q).first()
                if keywords:
                    key = keywords.keyword.title()
                    key = re.sub(r'[\]\[\+]', '', key)
                    key = key[:30]
                else:
                    key = t.headline1.title()

                ad, created = Adds.objects.get_or_create(
                    ad_group=q,
                    headline1 = key, 
                    headline2 = t.headline2,
                    headline3 = t.headline3,
                    description1 = t.description1,
                    description2 = t.description2,
                    description3 = t.description3,
                    path1 = t.path1,
                    path2 = t.path2,
                    variant = t.variant,
                    camp_id = camp_id 
                    )
     

    return redirect('ad:adcamps')

@login_required
def make_same_path(request, camp_id):
    qs = AdGroups.objects.filter(camp_id=Campaigns.objects.get(id=camp_id))
    for q in qs:
        paths = q.adds_set.all()
        paths.update(
        path1 = paths[0].path1,
        path2 = paths[0].path2,
        headline1 = paths[0].headline1
        )
    return redirect('ad:adcamps')


# Очищаем таблицы admin_ads_work_adgroups, admin_ads_work_keywords, admin_ads_work_negative
@login_required
def adgroups_del(request, camp_id):
    adgroups_del = AdGroups.objects.filter(camp_id=Campaigns.objects.get(id=camp_id))
    keys_del = Keywords.objects.filter(group_id__in=adgroups_del)
    negative_del = Negative.objects.filter(group_id__in=adgroups_del)
    try:
        keys_del.all().delete()
        negative_del.all().delete()
        adgroups_del.delete()
    except:
        print("something wrong")
    return redirect('ad:adcamps')
    

    










