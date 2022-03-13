from statistics import quantiles
from django.shortcuts import render, redirect, get_object_or_404
from bakeries.models import mahsool, ghanadi
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, mahsool_id):
    current_user = request.user
    mahsoole = mahsool.objects.get(id=mahsool_id) #get the product       
    if current_user.is_authenticated:
        if request.method == 'POST':        
           kiloo = int(request.POST['kiloo'])
           is_cart_item_exists = CartItem.objects.filter(mahsool=mahsoole, user=current_user).exists()
           if is_cart_item_exists:
                product = CartItem.objects.get(mahsool=mahsoole, user=current_user)
                product.kiloo+=kiloo
                product.save()
           else:    
                 item = CartItem.objects.create(mahsool=mahsoole, kiloo = kiloo, user=current_user)
        return redirect('cart')
    # If the user is not authenticated
    else:
        if request.method == 'POST':
              kiloo = int(request.POST['kiloo'])
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        is_cart_item_exists = CartItem.objects.filter(mahsool=mahsoole, cart=cart).exists()
        if is_cart_item_exists:
                product = CartItem.objects.get(mahsool=mahsoole, cart=cart)
                product.kiloo+=kiloo
                product.save()
        else:
          item = CartItem.objects.create(mahsool=mahsoole, kiloo = kiloo, cart=cart)
        return redirect('cart')



def remove_cart(request, mahsool_id, cart_item_id):
    
    mahsooll = get_object_or_404(mahsool, id=mahsool_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(mahsool=mahsooll, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(mahsool=mahsooll, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, mahsool_id, cart_item_id):
    mahsooll = get_object_or_404(mahsool, id=mahsool_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(mahsool=mahsooll, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(mahsool=mahsooll, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, kiloo=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.mahsool.price * cart_item.kiloo)
            kiloo += cart_item.kiloo
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'kiloo': kiloo,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, kiloo=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.mahsool.price * cart_item.kiloo)
            kiloo += cart_item.kiloo
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'kiloo': kiloo,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/checkout.html', context)

