from django.views.generic import TemplateView, View

class MyPageHomeView(TemplateView):
    template_name = 'mypage/home.html'