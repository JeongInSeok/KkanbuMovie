from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('password/', views.chg_pw, name='chg_pw'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/member_del/',views.member_del, name='member_del'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/update/', views.profupdate, name='profupdate'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
] 
