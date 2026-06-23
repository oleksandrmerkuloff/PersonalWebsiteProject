from django.contrib import admin
from adminsortable2.admin import SortableTabularInline, SortableAdminMixin

from .models import Post, Tag, PostChapter


class PostChapterInline(SortableTabularInline):
    model = PostChapter
    extra = 1
    fields = ["subtitle", "content", "image"]


class PostAdmin(SortableAdminMixin, admin.ModelAdmin):
    fields = ["title", "outline", "tags"]
    list_display = ["title", "created_at", "updated_at"]
    list_display_links = ["title"]
    list_filter = ["tags"]
    list_per_page = 50
    search_fields = ["title"]
    sortable_by = ["name", "created_at", "updated_at"]
    inlines = [PostChapterInline]


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
