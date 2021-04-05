import json
from functools import lru_cache

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
# from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings

from .models import User


class LoginView(TemplateView):
    template_name = 'account/login.html'


class LoginRequestView(TemplateView):
    def post(self, request):
        if request.method == "POST":
            if User.objects.filter(id=request.POST["user-id"]).exists():
                    user = User.objects.get(id=request.POST["user-id"])

                    if user.password == request.POST["password"]:
                        request.session['user-id'] = user.id
                        request.session['is_active'] = True

                        remember = request.POST.get('auto', False)
                        if remember == 'on':
                            request.session['remember'] = True
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                        else:
                            request.session['remember'] = False
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                            request.session.set_expiry(1800)

                        return redirect('/')

            return redirect('/account/login')


class LogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect('/')


class RegisterView(TemplateView):
    template_name = 'account/register.html'

    def post(self, request):
        if request.method == "POST":
            if request.POST["password"] == request.POST["repeat-password"]:
                user = User.objects.create(id=request.POST["id"],
                                           password=request.POST["password"],
                                           birth=request.POST["birth"],
                                           email=request.POST["email"],
                                           phone_number=request.POST["phone_number"],
                                           address=request.POST["address"],
                                           gender=request.POST["gender"])
                return render(request, 'account/register_done.html')

            # return render(request, 'account/register.html')
            return redirect('/account/register')


class RecoverIDView(TemplateView):
    template_name = 'account/recover_id.html'


class RecoverIDRequestView(View):
    def post(self, request):
        if request.method == "POST":
            email = request.POST.get('email')
            print(email)
            if User.objects.filter(email=email).exists() and \
                User.objects.filter(email=email).count() == 1:

                userObj = User.objects.get(email=email)

                # start of sending email

                from django.core import mail
                from django.template.loader import render_to_string

                connection = mail.get_connection()

                connection.open()

                template = 'account/recover_id_email.html'
                html_content = render_to_string(template)

                email = mail.EmailMultiAlternatives(
                    'ID recovery from JOB4',
                    'this is a test.',
                    'ssac.job4@gmail.com',
                    ['dksskgus923@naver.com'],
                    connection=connection,
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                # end of sending email

                return render(request, 'account/recover_id_done.html')
            else:
                return redirect('/account/recover-id/')


class RecoverPWView(TemplateView):
    template_name = 'account/recover_pw.html'


class RecoverPWRequestView(View):
    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['id']
            userObj = User.objects.get(id=user_id)

            user_email = request.POST['email']
            if user_email == userObj.email:
                print(userObj.password)
                request.session['id'] = user_id
                return render(request, 'account/recover_pw_done.html')

            # email이 다름
            return redirect('/')

class RecoverPWRequestDoneView(View):
    def post(self, request):
        if request.method == 'POST':
            pw = request.POST['password']
            if pw == request.POST['password_again']:
                userObj = User.objects.get(id=request.session['id'])
                userObj.password = pw
                userObj.save()

                return redirect('/account/login/')

        return redirect('/')


class DupCheckView(View):
    def get(self, request, key):
        from .user_repository import UserRepository
        import json

        repository = UserRepository()
        count = repository.select_count_by_userid(key)
        json_count = json.dumps(count, ensure_ascii=False)
        return HttpResponse(json_count, content_type="application/json")
