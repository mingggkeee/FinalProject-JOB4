from django.urls import path
from letter import views

app_name = 'letter'

urlpatterns = [
    path('result/', views.ResultView.as_view(), name='result'),
    path('analyze/', views.AnalyzeView.as_view(), name='analyze'),
    path('analyze/request/', views.AnalyzeRequestView.as_view(), name='analyze_request'),
path('company/', views.ShowCompany.as_view(), name='show_company'),
    path('task/', views.ShowTask.as_view(), name ='show_task'),
    # path('news/', views.NewsView.as_view(), name ='news'),
]
