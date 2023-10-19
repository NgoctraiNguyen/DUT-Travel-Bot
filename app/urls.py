from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatting', views.chatting, name= 'chat'),
    path('search', views.search, name= 'search')
]