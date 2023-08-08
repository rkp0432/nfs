from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('contact/', views.contact),
    path('properties/', views.properties),
    path('partners/', views.partners),
    path('terms/', views.terms),
    path('privacy/', views.privacy),
    
]
