from django.urls import path

from bookmark import views

app_name = 'bookmark'

urlpatterns = [
    path('', views.BookmarkLV.as_view(), name="index"),
    # path('<str:pk>/', BookmarkDV.as_view(), name="detail"),
    path('save/', views.BookmarkSaveView.as_view(), name="save"),
]