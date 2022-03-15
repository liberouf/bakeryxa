from email import contentmanager
from multiprocessing import context
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ghanadi,mahsool
from .forms import mahsoolForm,ReviewForm
from django.contrib.gis.geos import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import ReviewRating
from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import GeometryDistance     




def bakeries(request):
    #bakeries = ghanadi.objects.order_by('-rating')[0]
    bakeries = ghanadi.objects.all()
    bakeries_count = bakeries.count()
    context = {
            'bakeries': bakeries,
            'bakeries_count': bakeries_count,

                                                    }
    return render(request , 'bakeries/bakeries.html',context) 

def bakerieszone(request):
    #bakeries = ghanadi.objects.order_by('-rating')[0]
    for product in product:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    if request.user.position:
        ref_location = request.user.position
    else:
        ref_location = Point(51.3753,35.7448 ,srid=4326)
    bakeries_zone = ghanadi.objects.filter(position__distance_lte=(ref_location, D(m=5000))).annotate(distance=GeometryDistance('position', ref_location)) 
    bakeries=bakeries_zone
    bakeries_count = bakeries.count()
    
    context = {
            'bakeries': bakeries,
            'bakeries_count': bakeries_count,

                                                    }
    return render(request , 'bakeries/bakeries-zone.html',context) 

def mahsoolat(request,id):
    ghanadii = ghanadi.objects.get(id=id)
    mahsoola = mahsool.objects.all().filter(ghanadish_id=id)
    mahsoola_count = mahsoola.count()

    context = {
            'ghanadi':ghanadii,
            'id' : id,
            'mahsoola': mahsoola,
            'mahsoola_count': mahsoola_count,
                                                    }
    return render(request , 'bakeries/mahsoolat.html',context) 


@login_required(login_url = 'ghanadilogin')
def mahsool_jadid(request,id):  
      ghanadii=ghanadi.objects.get(id=id)
      if request.method == 'POST':
            formset = mahsoolForm(request.POST,request.FILES)
            if formset.is_valid():
               form = formset.save(commit=False)
               form.ghanadish = ghanadii
               form.save()
               messages.success(request, 'bashe pas inam sabt shud')
               return HttpResponseRedirect(reverse('mahsoolat', args=[id]))    

            return HttpResponse('nashud')    

      else: 
          if request.user == ghanadii.owner:
             form = mahsoolForm()
             context = {
                'form': form,
                'id':id,
                                }   
             return render(request, 'bakeries/mahsool-jadid.html', context)
          else:
             return HttpResponse('you are not owner')
   


def mahsool_detail(request,id):
    mahsoole = mahsool.objects.get(id=id)
    reviews = ReviewRating.objects.filter(product_id=mahsoole.id, status=True)
    context = {
                    'mahsoole':mahsoole,
                    'reviews':reviews,
    }
    return render(request , 'bakeries/mahsool_detail.html' ,context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            mahsoola = mahsool.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            mahsoola_count = mahsoola.count()
            context = {
               'mahsoola': mahsoola,
               'mahsoola_count': mahsoola_count,
                  }
        return render(request, 'bakeries/mahsoolat.html', context)

    else:
        
      return HttpResponse('chizi peida nashud')

def submit_review(request, mahsool_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=mahsool_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = mahsool_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
