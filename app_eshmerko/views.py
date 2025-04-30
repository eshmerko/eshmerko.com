# views.py
from django.shortcuts import render, get_object_or_404
from .models import Program, Update
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
                'download_url': request.build_absolute_uri(
                    f'/download/update/{latest_update.id}/'
                ),
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
    
    response = FileResponse(update.file.open(), filename=update.file.name.split('/')[-1])
    response['Content-Type'] = 'application/octet-stream'
    return response