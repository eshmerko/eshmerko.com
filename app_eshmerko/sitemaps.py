from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Program

class StaticViewSitemap(Sitemap):
    """Карта сайта для статических страниц"""
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['home', 'contacts', 'software_updates', 'blog']
    
    def location(self, item):
        return reverse(item)

class ArticleSitemap(Sitemap):
    """Карта сайта для статей блога"""
    changefreq = 'weekly'
    priority = 0.7
    
    def items(self):
        return Article.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.published_date
    
    def location(self, obj):
        return obj.get_absolute_url()

class ProgramSitemap(Sitemap):
    """Карта сайта для программного обеспечения"""
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Program.objects.all()
    
    def location(self, obj):
        return reverse('download_program', args=[obj.id])