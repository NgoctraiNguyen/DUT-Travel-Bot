from django.urls import path
from app import views

urlpatterns = [
    path('chatting', views.chatting, name= 'chat'),
    path('search', views.search, name= 'search'),
    path('login/', views.login_chatbot, name='login'),
    path('handle_login', views.handle_login, name='handle_login'),
    path('handle_logout', views.handle_logout, name='handle_logout'),
    path('',views.demo, name="demo"),
    path('predict/', views.predict, name='predict'),
    path('signup/', views.signup, name="signup"),
    path('handle_signup', views.handle_signup, name="handle_signup")
]