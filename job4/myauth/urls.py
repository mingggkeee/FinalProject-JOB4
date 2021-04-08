from django.urls import path
from myauth import views

app_name = 'myauth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/request/', views.LoginRequestView.as_view(), name='login_request'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/dupcheck/<str:key>/', views.DupCheckView.as_view(), name='dupcheck'),
    path('recover-id/', views.RecoverIDView.as_view(), name='recover_id'),
    path('recover-id/request/', views.RecoverIDRequestView.as_view(), name='recover_id_request'),
    path('recover-pw/', views.RecoverPWView.as_view(), name='recover_pw'),
    path('recover-pw/request/', views.RecoverPWRequestView.as_view(), name='recover_pw_request'),
    path('recover-pw/request/done/', views.RecoverPWRequestDoneView.as_view(), name='recover_pw_request_done'),
]
