from django.views.generic import TemplateView, View, UpdateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from myauth.models import User
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

class MyPageHomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        print(request.session.keys())
        user_id = request.session['user_id']
        current_user = User.objects.filter(id=user_id)
        context = {'current_user': current_user[0]}
        return render(request, "mypage/home.html", context=context)

class MypageUpdateView(View):
    def post(self, request, *args, **kwargs):
        users = User.objects.filter(id=request.POST['id'])
        user = users[0]
        user.username = request.POST['username']
        user.phone_number = request.POST['phone_number']
        user.gender = request.POST['gender']
        user.birth = request.POST['birth']
        user.address = request.POST['address']
        user.email = request.POST['email']
        user.save()

        redirect_url = reverse_lazy('mypage:home')
        return HttpResponseRedirect(redirect_url)

# class MypageDeleteView(View):

#     def delete(request):
#     if request.method == 'POST':
#         request.user.delete()
#         return redirect('mypage:home')
#     return HttpResponseRedirect(redirect_url)
