# views.py
from django.shortcuts import render, get_object_or_404
from .models import Program, Update
from django.http import HttpResponse, FileResponse

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