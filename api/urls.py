from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllPosts),
    path('add/', views.addPosts)
]