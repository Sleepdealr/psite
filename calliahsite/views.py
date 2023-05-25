import environ
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.shortcuts import redirect
from . import parser
from .models import Article, Category, Redirect

env = environ.Env()
environ.Env.read_env()


def index(request):
    template = loader.get_template('index.html')
    article = Article.objects.filter(slug="index")[0]
    featured = []
    for featured_article in Article.objects.filter(featured=True):
        featured.append({"title": featured_article.title, "link": "article/" + featured_article.slug})
    context = {
        "markdown": parser.parse_text(article.body)[0],
        "featured_articles": featured
    }
    context.update(parser.get_template_items(article.title))
    return HttpResponse(template.render(context, request))


def article(request, slug):
    template = loader.get_template('article.html')
    article = Article.objects.filter(slug=slug)[0]
    related = []
    for related_article in Article.objects.filter(category=article.category.id).exclude(title=article.title):
        related.append({"title": related_article.title, "link": "/article/" + related_article.slug})

    (parsed_html, headers) = parser.parse_text(article.body)
    context = {
        "md_html": parsed_html,
        "contents_html": headers,
        "category": article.category.name,
        "dt": article.pubdt,
        "updt": article.updt,
        "related": related,
        "othercategories": [q.name for q in Category.objects.exclude(id=article.category.id)],
        "embed_img": article.embed_img,
        "embed_desc": article.embed_desc,
    }
    context.update(parser.get_template_items(article.title))
    return HttpResponse(template.render(context, request))


def articles(request):
    template = loader.get_template("articles.html")
    all_ = Article.objects.exclude(title="Index")
    tree = {}
    for article in all_:
        if article.category.name not in tree.keys():
            tree[article.category.name] = [(article.title, article.pubdt, article.slug)]
        else:
            tree[article.category.name].append((article.title, str(article.pubdt), article.slug))

    context = {
        "tree": tree
    }
    context.update(parser.get_template_items("Articles"))
    return HttpResponse(template.render(context, request))


def contact(request):
    template = loader.get_template("contact.html")
    context = {
        "discord": env("DISCORD"),
        "email": env("EMAIL")
    }
    context.update(parser.get_template_items("Contact"))
    return HttpResponse(template.render(context, request))


def dbredirect(request, slug):
    link = Redirect.objects.filter(name=slug)[0]
    print(link.link)
    if link is not None:
        return redirect(link.link, request)
    return redirect("/", request)
