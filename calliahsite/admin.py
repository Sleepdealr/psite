from django.contrib import admin

from calliahsite import models

admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.HeaderArticle)
admin.site.register(models.HeaderLink)
admin.site.register(models.Redirect)
admin.site.register(models.ImageUpload)
