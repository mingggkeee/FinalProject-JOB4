from django.urls import path
from letter import views

app_name = 'letter'

urlpatterns = [
    path('result/', views.ResultView.as_view(), name='result'),
]
