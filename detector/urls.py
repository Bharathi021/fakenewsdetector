from django.urls import path
from . import views

urlpatterns = [
    path('', views.slider, name='slider'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('detect/', views.detect_news, name='detect_news'),
    path('history/', views.history, name='history'),
    path('slider/', views.slider, name='slider'),  # Add this line
]