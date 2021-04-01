from django.urls import path
from mypage import views

app_name = 'mypage'

urlpatterns = [
    path('/', views.MyPageHomeView.as_view(), name='home'),
]