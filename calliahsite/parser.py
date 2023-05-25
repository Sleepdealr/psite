import html as htmllib
import urllib.parse
from urllib.parse import urlparse

import jinja2
import lxml.etree
import lxml.html
import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from .models import HeaderLink, HeaderArticle


def get_template_items(title):
    articles = []
    for article in HeaderArticle.objects.exclude(name=title):
        articles.append({"name": article.name, "link": article.link})
    links = []
    for link in HeaderLink.objects.order_by().exclude(name=title):
        links.append({"name": link.name, "link": link.link})
    return {
        "links": links,
        "image": ["Lain", "https://sleepdealer.xyz/img/pfp_lain.jpg"],
        "title": title,
        "articles": articles,
    }


class HighlightRenderer(mistune.HTMLRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None
        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(htmllib.escape(text.strip()))

    def block_quote(self, content):
        content = content[3:-5]
        out = '\n<blockquote>'
        for line in htmllib.escape(content.strip()).split("\n"):
            out += '\n<span class="quote">{}</span><br>'.format(line)
        return out + '\n</blockquote>'

    def heading(self, text, level):
        hash_ = urllib.parse.quote_plus(text)
        return "<h%d id='%s'>%s <a class='header_linker' href='#%s'>[#]</a></h%d>" % (
            level, hash_, text, hash_, level
        )


def parse_file(path):
    with open(path, "r") as f:
        unformatted = f.read()
    return parse_text(unformatted)


def parse_text(unformatted):
    md = mistune.create_markdown(
        renderer=HighlightRenderer(),
        plugins=["strikethrough", "table", "url", "task_lists", "def_list"]
    )
    html = md(unformatted)
    return html, get_headers(html)


def get_headers(html):
    root = lxml.html.fromstring(html)

    headers = []
    thesmallestlevel = 7
    for node in root.xpath('//h1|//h2|//h3|//h4|//h5//h6'):
        level = int(node.tag[-1])
        if level < thesmallestlevel:
            thesmallestlevel = level
        headers.append((
            urllib.parse.unquote_plus(node.attrib["id"]),
            level,  # -horrible hack
            "#%s" % node.attrib["id"])
        )

    headers = [(i[0], i[1] - thesmallestlevel, i[2]) for i in headers]

    md_template = jinja2.Template("""
{% for text, depth, link in contents %}
{{ "    " * depth }} - [{{ text }}]({{ link }})
{% endfor %}
    """)
    return mistune.html(md_template.render(contents=headers))
