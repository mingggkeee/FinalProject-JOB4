from django.urls import path
from account import views

app_name='account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/request/', views.LoginRequestView.as_view(), name='login_request'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/request/', views.RegisterRequestView.as_view(), name='register_request'),
]