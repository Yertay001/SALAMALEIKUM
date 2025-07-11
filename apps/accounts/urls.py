from django.urls import path
from .views import register, login_view, check_auth_code, logout_view, profile, edit_profile


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view , name='login'), 
    path('check-auth-code/', check_auth_code, name='check_auth_code'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

]