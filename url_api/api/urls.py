from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.new_url, name='new-url'),
    path('find/', views.find_url, name='find-url')
]