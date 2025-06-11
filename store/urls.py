from django.urls import path

from store import views
app_name = "store"

urlpatterns = [
    path("",views.index,name="index"),
    path('about/', views.about, name='about'),
    path("products/",views.products,name='products'),
    path("ourteam/",views.ourteam,name='ourteam'),
    path("contact/",views.contact,name='contact'),
    path("detail/<slug>/",views.product_detail,name="product_detail"),
] 