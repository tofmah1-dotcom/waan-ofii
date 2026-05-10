from django.shortcuts import render, redirect
from .models import Product, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required # Inni kun murteessaa dha

def home_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.filter(is_active=True)
    
    categories = Category.objects.all()
    return render(request, 'base/home.html', {
        'products': products,
        'categories': categories,
        'query': query
    })

@login_required # Namni Login yoo godhe qofa meeshaa fe'uu danda'a
def upload_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        
        # Meeshaa uumuu
        Product.objects.create(
            seller=request.user,
            name=name,
            price=price,
            description=description,
            location=location,
            phone_number=phone,
            image=image
        )
        return redirect('home') # Gara home-tti si deebisa
        
    return render(request, 'base/upload.html')