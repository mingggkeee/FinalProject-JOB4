from django.views.generic.base import TemplateView, View
from django.shortcuts import redirect
from myauth.models import User
import requests


class HomeView(TemplateView):
    template_name = 'home.html'


class KakaoView(View):
    def get(self, request):
        app_rest_api_key = '9a0484415a32934fa843eab02d75fa8b'
        redirect_uri = 'http://127.0.0.1:8000/account/kakao/login/callback/'
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
        )


class KakaoCallbackView(View):
    def get(self, request):
        app_rest_api_key = '9a0484415a32934fa843eab02d75fa8b'
        redirect_uri = 'http://127.0.0.1:8000/account/kakao/login/callback/'

        user_token = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )
        token_response_json = token_request.json()
        error = token_response_json.get("error", None)

        access_token = token_response_json.get("access_token")

        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        age_range = kakao_account.get("age_range")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        birth = kakao_account.get("birthday")  # 0923 처럼 나옴
        gender = kakao_account.get("gender")

        userId = email.split("@")[0]

        request.session['user_id'] = userId
        request.session['username'] = nickname
        request.session['is_active'] = True

        print("kakao callback:", request.session.items())

        if not User.objects.filter(id=userId).exists():
            if gender == 'female':
                gender = 1
            else:
                gender = 0

            user = User.objects.create(id=userId,
                                       username=nickname,
                                       gender=gender,
                                       email=email)
            user.set_password(userId)
            user.save()
        return redirect("/")


class NaverCallbackView(View):
    def get(self, request):
        client_id = "84J2KKJNv7nH5f4cTaf4"
        secret_key = "UukLiKAcnu"
        redirect_uri = "http://127.0.0.1:8000/account/naver/login/callback/"

        code = request.GET.get("code")
        state = request.GET.get("state")
        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={secret_key}&redirect_uri={redirect_uri}&code={code}&state={state}"
        )
        token_response_json = token_request.json()

        access_token = token_response_json.get("access_token")
        refresh_token = token_response_json.get("refresh_token")

        profile_request = requests.post(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        message = profile_json.get("message")
        if message != 'success':
            print("exception")

        response = profile_json.get('response')
        gender = response.get('gender')
        email = response.get('email')
        phone = response.get('mobile')
        birth = response.get('birthyear')

        if gender == 'F':
            gender = 1
        else:
            gender = 0

        userId = email.split("@")[0]

        request.session['user_id'] = userId
        request.session['is_active'] = True

        if not User.objects.filter(id=userId).exists():
            if gender == 'female':
                gender = 1
            else:
                gender = 0

            user = User.objects.create(id=userId,
                                       username='annoymous',
                                       gender=gender,
                                       email=email,
                                       phone_number=phone)
            user.set_password(userId)
            user.save()

        return redirect("/")


#### Home search

from django.views.generic.base import TemplateView, View
from myauth.models import Company2, Task2
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.core import serializers


class FindCompanyView(View):
    def get(self, request):
        # print( request.GET['key'] )
        # Company.objects.filter(name=request.POST['key'])

        searched_companies = Company2.objects.filter(name__startswith=request.GET['key'])
        # print(find_data)

        serialized_searched_companies = serializers.serialize('json', searched_companies) # serialize : instance -> json string
        return JsonResponse(serialized_searched_companies, safe=False, json_dumps_params={'ensure_ascii':False})

class FindTaskView(View):
    def get(self, request):
        # print( request.GET['key'] )
        # Company.objects.filter(name=request.POST['key'])

        searched_companies = Task2.objects.filter(name__startswith=request.GET['key'])
        # print(find_data)

        serialized_searched_companies = serializers.serialize('json', searched_companies) # serialize : instance -> json string
        return JsonResponse(serialized_searched_companies, safe=False, json_dumps_params={'ensure_ascii':False})


# class FindTaskView(View):
#     def get(self, request):
#         searched_task = Task.objects.filter(name__startswith=request.GET['key'])