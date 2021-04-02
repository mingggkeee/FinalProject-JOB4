from django.shortcuts import render
from django.views.generic import View, TemplateView

class LoginView(TemplateView):
    template_name = 'account/login.html'

class LoginRequestView(View):
    print('hi')

class RegisterView(TemplateView):
    template_name = 'account/register.html'

class RegisterRequestView(View):
    print('hello')