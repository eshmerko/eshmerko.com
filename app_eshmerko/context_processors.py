from .jsonld import (
    JSONLDGenerator, HomepageJSONLD, ArticleJSONLD, ProjectJSONLD, 
    ProgramJSONLD, BlogListJSONLD, PortfolioListJSONLD, CategoryJSONLD
)
from .models import Article, Project, Program, ProjectCategory
from django.urls import resolve

def jsonld_context(request):
    """
    Контекстный процессор для добавления JSON-LD структурированных данных
    в зависимости от текущей страницы
    """
    # Определяем имя текущего URL-шаблона
    try:
        url_name = resolve(request.path_info).url_name
    except:
        url_name = None
    
    # Инициализация JSON-LD по умолчанию
    jsonld = JSONLDGenerator(request).get_jsonld()
    
    # Выбор соответствующего JSON-LD в зависимости от страницы
    if url_name == 'home':
        jsonld = HomepageJSONLD(request).get_jsonld()
    
    elif url_name == 'article_detail':
        # Для страницы отдельной статьи
        slug = resolve(request.path_info).kwargs.get('slug')
        if slug:
            try:
                article = Article.objects.get(slug=slug, is_published=True)
                jsonld = ArticleJSONLD(article, request).get_jsonld()
            except Article.DoesNotExist:
                pass
    
    elif url_name == 'project_detail':
        # Для страницы отдельного проекта
        project_slug = resolve(request.path_info).kwargs.get('project_slug')
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
                jsonld = ProjectJSONLD(project, request).get_jsonld()
            except Project.DoesNotExist:
                pass
    
    elif url_name == 'download_program':
        # Для страницы программы
        program_id = resolve(request.path_info).kwargs.get('program_id')
        if program_id:
            try:
                program = Program.objects.get(id=program_id)
                jsonld = ProgramJSONLD(program, request).get_jsonld()
            except Program.DoesNotExist:
                pass
    
    elif url_name == 'blog':
        # Для страницы блога
        jsonld = BlogListJSONLD(request).get_jsonld()
    
    elif url_name == 'portfolio_list':
        # Для страницы портфолио
        jsonld = PortfolioListJSONLD(request).get_jsonld()
    
    elif url_name == 'portfolio_category':
        # Для страницы категории проектов
        slug = resolve(request.path_info).kwargs.get('slug')
        if slug:
            try:
                category = ProjectCategory.objects.get(slug=slug)
                jsonld = CategoryJSONLD(category, request).get_jsonld()
            except ProjectCategory.DoesNotExist:
                pass
    
    # Возвращаем контекст с JSON-LD
    return {
        'jsonld_data': jsonld
    }