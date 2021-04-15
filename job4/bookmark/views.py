from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View

from myauth.models import Bookmark, User, Letter2

class BookmarkLV(ListView):
    # context_object_name = "object_list" : 템플릿으로 전달하는 데이터 이름(변수명), 명시적으로 지정하지 않을 경우 object_list 사용
    template_name = "bookmark/bookmark_list.html" # 지정하지 않을 경우 bookmark_list.html

    def get_queryset(self):
        # user_id = self.request.session['user_id']
        # print(user_id)
        return Bookmark.objects.all().filter(user_id=self.request.session['user_id'])


class BookmarkSaveView(View):

    def get(self, request):
        uid = request.GET.get('user_id')
        lid = request.GET.get('letter_id')

        try:
            found_user = User.objects.get(id=uid)
            found_letter = Letter2.objects.get(letter_id=lid)

            print(found_letter.letter_id)

            bookmark = Bookmark.objects.create(user_id=found_user,
                                               letter_id=found_letter)

            status = 'success'

        except:
            status = "error"

        import json

        if status == 'error':
            context = {'status': status}
            result = json.dumps(context, ensure_ascii=False)

            return HttpResponse(result, content_type="application/json")


        context = {'status': status, 'username': found_user.username}
        result = json.dumps(context, ensure_ascii=False)

        return HttpResponse(result, content_type="application/json")

