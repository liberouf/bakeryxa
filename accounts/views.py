from django.db.models.fields.files import ImageFileDescriptor
from django.shortcuts import render, redirect
from bakeries.forms import mahsoolForm
from bakeries.views import bakeries
from .forms import accountsForm, ghanadiForm
from .models import Account
from cart.models import CartItem,Cart
from order.models import Order,OrderProduct
from bakeries.models import ghanadi
from django.contrib import messages, auth
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
import requests
from rest_framework import viewsets
from rest_framework_gis import filters
from .models import Account
from .serializers import accountSerializer
from django.contrib.gis.geos import Point

import json



 
def register(request):

    if request.method == 'POST':
        form = accountsForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            position = form.cleaned_data['position']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.position=position
            user.is_owner = False
            user.save()

            messages.success(request, 'sabt nam shodi')

            name_owner = f'{user.first_name} {user.last_name}'

            return redirect('login')    
    else:
        form = accountsForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        emaill = request.POST['email']
        passwordd = request.POST['password']

        user = auth.authenticate(email=emaill, password=passwordd)

        if user :

            
            #cart = Cart.objects.get(cart_id=_cart_id(request))
            #is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            try: 
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart, is_active=True).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart, is_active=True) 
                    print(cart_item)
                    for item in cart_item:
                            is_in_cart_item_exists = CartItem.objects.filter(mahsool=item.mahsool, user=user).exists()    
                            if is_in_cart_item_exists:
                                product = CartItem.objects.get(mahsool=item.mahsool, user=user) 
                                product.kiloo+=int(item.kiloo)   
                                product.save()
                            else:        
                                item.user=user
                                item.save()
            except:
                 pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
               # next='/cart/checkout/'
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else: 
            messages.error(request, 'Invalid login credentials')
            return HttpResponse('fail')
    return render(request,'accounts/login.html')   

#######################################################################################  OWner
@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    user = request.user
   # userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        #'userprofile': userprofile,
        'user':user,
    }
    return render(request, 'accounts/dashboard.html', context)


def ownerregister(request):
    if request.method == 'POST':
        form = accountsForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            position = form.cleaned_data['position']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.position = position
            user.is_owner = True
            user.save()

            auth.login(request, user)
            name_owner = f'{first_name} {last_name}'

            messages.success(request, 'sabt nam shodi')
            context = {
                         'owner': user,
                         'form' : ghanadiForm,
                         'name_owner':name_owner,
                                         }
            return render(request, 'accounts/ghanadiregister.html', context)
    else:
        form = accountsForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/ownerregister.html', context)
  
def storefile(file):
    with open("uploads/images/pic.jpg" , "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)   




def ghanadiregister(request):
    if request.method == 'POST':    
        #ownerr = Account.objects.get(email='owner')
        form = ghanadiForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            ownerid = request.user.id
            owner = Account.objects.get(id=ownerid)
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            position = form.cleaned_data['position']
            username = owner.email.split("@")[0]
            images = request.FILES['images']
            storefile(images)
            user = ghanadi.objects.create_user( owner=owner, name=name, username=username, password=password , images=images)
            print(form.errors)
            user.phone = phone
            user.position = position
            user.address = form.cleaned_data['address']
            #userr = Account.objects.get(pk=user.id)
            #user.image = image
            user.save()     

            messages.success(request, 'ghanadi sabt nam shod')
            
            return redirect('ghanadilogin')
    else:
       
        form = ghanadiForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/ghanadiregister.html', context)
  



def ghanadilogin(request):
    if request.method == 'POST':
        emaill = request.POST['email']
        passwordd = request.POST['password']

        user = authenticate(email=emaill, password=passwordd)
        if user:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('bakeries')
        else: 
            messages.error(request, 'Invalid login credentials')
            return HttpResponse('fail')
    
    return render(request,'accounts/ghanadilogin.html')   



@login_required(login_url = 'login' or 'ghanadilogin')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')