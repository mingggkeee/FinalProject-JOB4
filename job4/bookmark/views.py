from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import View

from myauth.models import Bookmark, User, Letter2

class BookmarkLV(ListView):
    template_name = "bookmark/bookmark_list.html"

    def get_queryset(self):

        return Bookmark.objects.all().filter(user_id=self.request.session['user_id'])


class BookmarkSaveView(View):

    def get(self, request):
        uid = request.GET.get('user_id')
        lid = request.GET.get('letter_id')

        try:
            found_user = User.objects.get(id=uid)
            found_letter = Letter2.objects.get(letter_id=lid)

            bookmark = Bookmark.objects.create(user=found_user,
                                               letter=found_letter)

            bookmark.save()

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

