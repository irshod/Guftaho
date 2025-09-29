from django.contrib.sitemaps import Sitemap
from .models import Poet, Book, Poem


class PoetSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Poet.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class BookSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class PoemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Poem.objects.all()

    def lastmod(self, obj):
        return obj.updated_at