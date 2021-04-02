import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
# from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings

from .models import User

# Create your views here.
class LoginView(TemplateView):
    template_name = 'account/login.html'

class LoginRequestView(TemplateView):
    def post(self, request):
        print(request.POST["user-id"])
        print(User.objects.filter(id=request.POST["user-id"]).exists())
        if request.method == "POST":
            # user 부분 수정 필요
            # models.py 에서 수정하고 user 를 가져와서 확인
            try:
                if User.objects.filter(id=request.POST["user-id"]).exists():
                    user = User.objects.get(id=request.POST["user-id"])

                    if user.password == request.POST["password"]:
                        request.session['user-id'] = user.id
                        request.session['is_active'] = True

                        remember = request.POST.get('auto', False)
                        if remember=='on':
                            request.session['remember'] = True
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                        else:
                            request.session['remember'] = False
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                            request.session.set_expiry(1800)

                        return render(request, 'home.html')
            except:
                return render(request, 'account/login.html')

class LogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect('/')

class RegisterView(TemplateView):
    template_name = 'account/register.html'

    def post(self, request):
        if request.method == "POST":
            if request.POST["password"] == request.POST["repeat-password"]:
                user = User.objects.create(id=request.POST["id"], \
                                           password=request.POST["password"], \
                                           birth=request.POST["birth"], \
                                           email=request.POST["email"], \
                                           phone_number=request.POST["phone_number"], \
                                           address=request.POST["address"], \
                                           gender=request.POST["gender"])
                return render(request, 'account/register_done.html')

            return render(request, 'account/register.html')

# class RegisterRequestView(TemplateView):
#     def post(self, request):
#         if request.method == "POST":
#             if request.POST["password"] == request.POST["repeat-password"]:
#                 user = User.objects.create(id=request.POST["id"], \
#                                            password=request.POST["password"], \
#                                            birth=request.POST["birth"], \
#                                            email=request.POST["email"], \
#                                            phone_number=request.POST["phone_number"], \
#                                            address=request.POST["address"], \
#                                            gender=request.POST["gender"])
#                 return render(request, 'account/register_done.html')

#             return render(request, 'account/register.html')

class RecoverIDView(TemplateView):
    template_name = 'account/recover_id.html'

class RecoverIDRequestView(View):
    print('recover id')

class RecoverPWView(TemplateView):
    template_name = 'account/recover_pw.html'

class RecoverPWRequestView(View):
    print('recover pw')


class DupCheckView(View):

    def get(self, request, key):
        from .user_repository import UserRepository
        import json

        repository = UserRepository()
        count = repository.select_count_by_userid(key)
        json_count = json.dumps(count, ensure_ascii=False)
        return HttpResponse(json_count, content_type="application/json")
