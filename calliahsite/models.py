from django.db import models

class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    slug = models.SlugField(max_length=40)
    title = models.CharField(max_length=200)
    body = models.TextField()
    pubdt = models.DateTimeField("Date Published")
    updt = models.DateTimeField("Date Updated")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured = models.BooleanField(null=True)
    embed_desc = models.CharField(max_length=100, default=None, blank=True, null=True)
    embed_img = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class HeaderLink(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class HeaderArticle(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Redirect(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ImageUpload(models.Model):
    specifications = models.FileField(upload_to="")
