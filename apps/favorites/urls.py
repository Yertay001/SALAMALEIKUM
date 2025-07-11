from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('', views.favorites_list, name='favorites_list'),
]
