from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from app_eshmerko.sitemaps import StaticViewSitemap, ArticleSitemap, ProgramSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'static': StaticViewSitemap,
    'articles': ArticleSitemap,
    'programs': ProgramSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_eshmerko.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)