from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Program, Project, ProjectCategory

# Базовый класс с общими настройками
class BaseSitemap(Sitemap):
    protocol = 'https'  # Принудительно использовать HTTPS

class StaticViewSitemap(BaseSitemap):
    """Карта сайта для статических страниц"""
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['home', 'contacts', 'software_updates', 'blog', 'portfolio_list']
    
    def location(self, item):
        return reverse(item)

class ArticleSitemap(BaseSitemap):
    """Карта сайта для статей блога"""
    changefreq = 'weekly'
    priority = 0.7
    
    def items(self):
        return Article.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.published_date
    
    def location(self, obj):
        return obj.get_absolute_url()

class ProgramSitemap(BaseSitemap):
    """Карта сайта для программного обеспечения"""
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Program.objects.all()
    
    def location(self, obj):
        return reverse('download_program', args=[obj.id])

class ProjectSitemap(BaseSitemap):
    """Карта сайта для проектов портфолио"""
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Project.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('project_detail', kwargs={'project_slug': obj.slug})

class ProjectCategorySitemap(BaseSitemap):
    """Карта сайта для категорий проектов"""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return ProjectCategory.objects.all()
    
    def location(self, obj):
        return reverse('portfolio_category', kwargs={'slug': obj.slug})