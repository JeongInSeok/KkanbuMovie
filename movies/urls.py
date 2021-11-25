from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='recommended'),
    path('search/', views.search, name='search'),
]
