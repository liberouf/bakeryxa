from django.shortcuts import render
from bakeries.models import mahsool, ReviewRating

def home(request):
    products = mahsool.objects.all().filter(is_available=True).order_by('created_date')

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'bakeries': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)
``