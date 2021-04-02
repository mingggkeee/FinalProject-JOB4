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
    # print('recover id')
    def post(self, request):
        if request.method == "POST":
            # print(request.POST['email'])
            
            email = request.POST.get('email')
            result_id = User.objects.get(email=email)
            print(result_id)
            return render(request, 'account/register_done.html')

        return render(request, 'account/recover_id_done.html')

class RecoverPWView(TemplateView):
    template_name = 'account/recover_pw.html'

class RecoverPWRequestView(View):
    # print('recover pw')
    def post(self, request):
        if request.method == "POST":
            # print(request.POST['id'])
            # print(request.POST['email'])

            user_id = request.POST['id']
            result_id = User.objects.get(id=user_id)
            print(result_id.birth)
            # result_id = User.objects.get(email=email)
            
            user_email = request.POST['email']
            if user_email == result_id.email:
                print(result_id.password)
                return render(request, 'account/recover_pw_done.html')

            return render(request, 'home.html')

class RecoverPWRequestDoneView(View):
    def post(self, request):
        return render(request, '/account/recover-pw/request_pw_done copy.html')
    def password_edit(self):
        if request.method == 'POST':
            user = User.objects(password=request.POST["password"])
            print(result_id.password)

        if request.POST["password"] == request.POST["password_again"]:
            print(result_id.password)
            # user = User.objects.update(password=request.POST["password"])
            
            # if request.POST["password"] == request.POST["password"]:
    print('recover pw')


class DupCheckView(View):

    def get(self, request, key):
        from .user_repository import UserRepository
        import json

        repository = UserRepository()
        count = repository.select_count_by_userid(key)
        json_count = json.dumps(count, ensure_ascii=False)
        return HttpResponse(json_count, content_type="application/json")
