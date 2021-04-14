from django.urls import path
from letter import views

app_name = 'letter'

urlpatterns = [
    path('result/', views.ResultView.as_view(), name='result'),
    path('analyze/', views.AnalyzeView.as_view(), name='analyze'),
    path('analyze/request/', views.AnalyzeRequestView.as_view(), name='analyze_request'),
]
