from django.urls import path
from accountsapi.views import loginpost, RegisterView , ProfileView

urlpatterns = [
    path('login', loginpost, name='login_post'),
    path('signup', RegisterView.as_view()),
    path('profile', ProfileView.as_view())
]