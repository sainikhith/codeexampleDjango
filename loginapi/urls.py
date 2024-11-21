from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpost, name='login_post')
]