"""job4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, KakaoCallbackView, NaverCallbackView
from django.views.generic.base import TemplateView

### Home Search
from .views import FindCompanyView, FindTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="Home"),
    # custom apps
    path('myauth/', include('myauth.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('mypage/', include('mypage.urls')),
    path('letter/', include('letter.urls')),
    # allauth : social login
    path('accounts/', include('allauth.urls')),
    # social login
    path('account/kakao/login/callback/', KakaoCallbackView.as_view(), name="kakao_callback"),
    path('account/naver/login/callback/', NaverCallbackView.as_view(), name="naver_callback"),

    ### Home search
    path('find/company', FindCompanyView.as_view(), name="find_company"),
    path('find/task', FindTaskView.as_view(), name="find_task"),


]
