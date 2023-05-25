from django.contrib import admin

from .models import Article, Category, HeaderArticle, HeaderLink, Redirect

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(HeaderArticle)
admin.site.register(HeaderLink)
admin.site.register(Redirect)
