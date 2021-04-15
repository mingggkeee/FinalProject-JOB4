from django.contrib import admin

from bookmark.models import Bookmark

# Register your models here.

class BookmarkAdmin(admin.ModelAdmin):
    """
    Bookmark 모델이 관리자 앱에서 어떻게 다루어지는지 설정하는 클래스
    """
    list_display = ['id', 'title', 'url']

# admin.site.register(Bookmark) # - admin 앱의 기본 관리 방식으로 관리
admin.site.register(Bookmark, BookmarkAdmin) # 사용자 정의된 방식으로 관리하도록 모델 등록
