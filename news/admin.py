from django.contrib import admin

from .models import Article, Editor, WeshyMerch, tags


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Editor)
admin.site.register(Article, ArticleAdmin)
admin.site.register(tags)
admin.site.register(WeshyMerch)