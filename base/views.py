from django.shortcuts import render, redirect
from .models import Product, Category
from django.db.models import Q

def home_view(request):
    query = request.GET.get('q') # Barbaachaaf
    if query:
        # Meeshaa maqaan ykn ibsa isaan barbaaduu
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

def upload_product(request):
    if request.method == "POST":
        # Form irraa data sassaabuu
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        
        Product.objects.create(
            seller=request.user,
            name=name,
            price=price,
            description=description,
            location=location,
            phone_number=phone,
            image=image
        )
        return redirect('/')
    return render(request, 'base/upload.html')