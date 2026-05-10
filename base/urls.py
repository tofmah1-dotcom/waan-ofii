from django.urls import path
from . import views

urlpatterns = [
    # Gara fuula jalqabaatti (Dashboard) si geessa
    path('', views.home_view, name='home'), 
    
    # Meeshaa ittiin fe'uuf (Upload)
    path('upload/', views.upload_product, name='upload_product'),
]