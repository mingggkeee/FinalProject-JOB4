from django.urls import path
from mypage import views

app_name = 'mypage'

urlpatterns = [
    path('home/', views.MyPageHomeView.as_view(), name='home'),

    # 저장하기 완료
    path('<str:pk>/update/', views.MypageUpdateView.as_view(), name="update"),

    # # 탈퇴
    # path('delete', views.MypageDeleteView.as_view(), name="delete"),

]