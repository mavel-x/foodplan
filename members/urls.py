from django.urls import path
from members import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.profile, name='profile'),
    path('subscription/', views.subscription, name='subscription')
]
