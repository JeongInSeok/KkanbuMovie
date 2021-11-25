from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    path('<int:review_pk>/comments/create/', views.create_comment, name='create_comment'),
    path('<int:review_pk>/like/', views.like, name='like'),
    path('kkanbumap/',views.kakaomap, name='kakaomap'),
]
