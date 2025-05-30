from django.urls import path
from . import views

urlpatterns = [
    path('', views.slider, name='slider'),
    path('detect/', views.detect_news, name='detect_news'),
    path('history/', views.history, name='history'),
    path('slider/', views.slider, name='slider'),  # Add this 
]