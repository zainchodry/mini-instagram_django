from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from . forms import LoginForm


app_name = 'accounts'

urlpatterns = [
    path("register", Register, name = 'register'),
    path("accounts/login/", auth_views.LoginView.as_view(template_name = 'login.html', authentication_form = LoginForm), name = 'login'),
    path('logout', logout, name='logout'),
    path('u/<str:username>/', profile_detail, name='profile_detail'),
    path('u/<str:username>/follow/', toggle_follow, name='toggle_follow'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('search/', user_search, name='search'),
    path('', index, name='index'),
]


