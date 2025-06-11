from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store import models as store_models

def index(request):
    products = store_models.Product.objects.filter(status="Published",featured=True)
    testimonial=store_models.Testimonial.objects.all()
    context = {
        'products': products,
        'testimonial':testimonial,
    }
    return render(request,"store/index.html",context)



def about(request):
    return render(request,"store/about.html")


def products(request):
    products = store_models.Product.objects.filter(status="Published")
    categories=store_models.Category.objects.all()
    context = {
        'products': products,
        'categories':categories
    }
    return render(request,"store/products.html",context)



def ourteam(request):
    teammembers = store_models.TeamMember.objects.all()
    context = {
        'teammembers': teammembers,
    }
    return render(request, "store/ourteam.html", context)


def contact(request):
    return render(request,"store/contact.html")



def product_detail(request,slug):
        # Get the specific product
    product = get_object_or_404(
        store_models.Product.objects.prefetch_related(
            'specifications',
            'features',
            'support_docs'
        ),
        status="Published",
        slug=slug
    )
        
        # Get related products, limited to 4
    related_products = store_models.Product.objects.filter(
            category=product.category,
        ).exclude(id=product.id)[:4]
        
    context = {
            "product": product,
            "related_products": related_products,  # Changed from related_product
        }
        
        # Pass the context to the template
    return render(request, "store/product_detail.html", context)
        
    