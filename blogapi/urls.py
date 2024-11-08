from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllPosts),
    path('add/', views.addPosts),
    path('get/<int:id>/', views.getPostById, name='get_post_by_id'),
    path('delete/<int:id>/', views.deletePost, name='delete_post'),
    path('update/<int:id>/', views.updatePost, name='update_post'),
]