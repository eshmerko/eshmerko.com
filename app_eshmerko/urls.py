# urls.py вашего приложения
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('software_updates/', views.software_updates, name='software_updates'),
    path('download/<int:program_id>/', views.download_program, name='download_program'),
    path('api/check-update/<str:program_name>/<str:current_version>/', views.check_update),
    path('download/update/<int:update_id>/', views.download_update, name='download_update'),
    path('blog/', views.ArticleListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('blog/rss/', views.LatestArticlesFeed(), name='articles_rss'),
    path('portfolio/', views.PortfolioListView.as_view(), name='portfolio_list'),
    path('portfolio/category/<slug:slug>/', views.portfolio_category_view, name='portfolio_category'),
    path('portfolio/project/<slug:project_slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
