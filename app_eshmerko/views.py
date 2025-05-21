# views.py
from django.shortcuts import render, get_object_or_404
from .models import Program, Update, Article, Project, ProjectCategory, ProgramLaunch
from django.http import HttpResponse, FileResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from .serializers import ProgramLaunchSerializer
from django.db import transaction

import json
import requests
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

# Вставьте ваш токен и chat_id
TELEGRAM_BOT_TOKEN = '5876243681:AAGajxM9drvH8c8w5PcB2xRdPMs36ZdBMR0'
TELEGRAM_CHAT_ID = '314485159'

def home(request):
    """Представление для главной страницы"""
    return render(request, 'home.html')

def contacts(request):
    """Представление для страницы контактов"""
    return render(request, 'contact.html')

def software_updates(request):
    """Представление для страницы обновлений программного обеспечения"""
    # Получаем все программы вместе с их обновлениями
    programs = Program.objects.all().prefetch_related('updates')
    
    # Создаем словарь для хранения упорядоченных обновлений для каждой программы
    programs_with_updates = []
    
    # Для каждой программы получаем отсортированные обновления
    for program in programs:
        # Получаем обновления и сортируем их
        sorted_updates = program.updates.all().order_by('-version')
        
        # Добавляем программу и её отсортированные обновления в список
        programs_with_updates.append({
            'program': program,
            'updates': sorted_updates
        })
    
    # Рендерим шаблон с данными
    return render(request, 'upd.html', {
        'programs_with_updates': programs_with_updates
    })

def download_program(request, program_id):
    """Представление для скачивания программы"""
    program = get_object_or_404(Program, id=program_id)

    # Увеличиваем счетчик скачиваний
    program.increment_download_count()

    # Отправляем файл
    response = FileResponse(program.download_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename={program.download_file.name}'
    return response

@api_view(['GET'])
def check_update(request, program_name, current_version):
    try:
        program = Program.objects.get(name__iexact=program_name)
        latest_update = program.updates.filter(is_active=True).order_by('-version').first()
        
        if not latest_update:
            return Response({'error': 'No updates available'}, status=status.HTTP_404_NOT_FOUND)
        
        client_version = tuple(map(int, current_version.split('.')))
        server_version = latest_update.version_tuple()
        
        if server_version > client_version:
            data = {
                'update_available': True,
                'latest_version': latest_update.version,
                'release_date': latest_update.release_date,
                # Изменяем URL на страницу обновлений
                'download_url': request.build_absolute_uri(reverse('software_updates')),
                'changelog': latest_update.description
            }
            return Response(data)
        
        return Response({'update_available': False})
    
    except Program.DoesNotExist:
        return Response({'error': 'Program not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
def download_update(request, update_id):
    update = get_object_or_404(Update, id=update_id)
    
    if not update.file:
        return HttpResponse("File not found", status=404)
    
    # Увеличиваем счетчик скачиваний
    update.download_count += 1
    update.save(update_fields=['download_count'])  # Оптимизированное сохранение
    
    response = FileResponse(update.file.open(), filename=update.file.name.split('/')[-1])
    response['Content-Type'] = 'application/octet-stream'
    return response

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/blog_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    queryset = Article.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = {
            'title': 'Блог - Полезные статьи о разработке ПО',
            'description': 'Экспертные статьи и руководства по разработке программного обеспечения',
            'keywords': 'программирование, разработка ПО, IT статьи'
        }
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

class LatestArticlesFeed(Feed):
    title = "Последние статьи"
    description = "Новые публикации в блоге"
    link = "/blog/"

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-published_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.meta_description

class PortfolioListView(ListView):
    """Отображение списка всех проектов портфолио"""
    
    model = Project
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_items'
    paginate_by = 9  # Количество проектов на странице
    
    def get_queryset(self):
        """Фильтрация проектов"""
        queryset = super().get_queryset()
        
        # Фильтрация по категории (если указана в GET параметрах)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()  # Было через values_list
                
        # Добавление избранных проектов
        context['featured_projects'] = Project.objects.filter(
            is_featured=True
        )[:3]
        
        return context


class ProjectDetailView(DetailView):
    """Отображение детальной информации о проекте"""
    
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'project_slug'
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст"""
        context = super().get_context_data(**kwargs)
        
        # Добавление связанных проектов той же категории
        current_project = self.get_object()
        context['related_projects'] = Project.objects.filter(
            category=current_project.category
        ).exclude(
            id=current_project.id
        )[:3]
        
        return context


def portfolio_category_view(request, slug):
    """Отображение проектов определенной категории по слагу"""
    category = get_object_or_404(ProjectCategory, slug=slug)
    projects = Project.objects.filter(category=category)
    
    context = {
        'portfolio_items': projects,
        'category': category.name,  # Для совместимости с текущим шаблоном
        'categories': ProjectCategory.objects.all()
    }
    
    return render(request, 'portfolio/portfolio_list.html', context)

@csrf_exempt
def send_order(request):
    if request.method == 'POST':
        try:
            logger.info(">>> Запрос получен")

            data = json.loads(request.body)
            logger.info(f">>> Данные: {data}")

            service = data.get('service')
            name = data.get('name')
            phone = data.get('phone')
            message = data.get('message')

            text = f"📩 Новая заявка:\n\n" \
                   f"🛠 Услуга: {service}\n" \
                   f"👤 Имя: {name}\n" \
                   f"📞 Телефон: {phone}\n" \
                   f"💬 Сообщение: {message}"

            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}

            response = requests.post(telegram_url, data=payload, timeout=5)

            logger.info(f">>> Telegram response: {response.status_code}")

            if response.status_code == 200:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Ошибка Telegram'}, status=500)

        except json.JSONDecodeError:
            logger.exception("Ошибка при разборе JSON")
            return JsonResponse({'status': 'error', 'message': 'Невалидный JSON'}, status=400)

        except Exception as e:
            logger.exception("Ошибка при обработке запроса")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
class TrackLaunchView(APIView):
    def post(self, request):
        serializer = ProgramLaunchSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    install_id = serializer.validated_data['install_id']
                    defaults = {
                        'app_name': serializer.validated_data['app_name'],
                        'app_version': serializer.validated_data['app_version'],
                        'system_platform': serializer.validated_data.get('system_platform', ''),
                        'python_version': serializer.validated_data.get('python_version', ''),
                    }

                    # Пытаемся найти существующую запись
                    obj = ProgramLaunch.objects.filter(install_id=install_id).first()

                    if obj:
                        # Обновление существующей записи с F-выражением
                        ProgramLaunch.objects.filter(install_id=install_id).update(
                            launch_count=models.F('launch_count') + 1,
                            **defaults
                        )
                    else:
                        # Создание новой записи с начальным значением 1
                        ProgramLaunch.objects.create(
                            install_id=install_id,
                            launch_count=1,
                            **defaults
                        )

                    return Response({'status': 'success'}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Launch tracking error: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

