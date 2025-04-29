from django.contrib import admin
from django.db import models
from .models import Program, Update
from django.utils.safestring import mark_safe

class UpdateInline(admin.TabularInline):
    model = Update
    extra = 1  # количество пустых форм для добавления новых обновлений

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_description', 'download_count')
    inlines = [UpdateInline]  # Добавляем возможность редактировать обновления в форме программы
    
    # Использование текстового редактора для поля description
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 10, 'cols': 80})},
    }
    
    # Метод для отображения HTML в списке программ
    def display_description(self, obj):
        return mark_safe(obj.description)
    display_description.short_description = 'Description'
    
    # Метод для безопасной обработки HTML
    def save_model(self, request, obj, form, change):
        # Здесь можно добавить дополнительную очистку HTML, если нужно
        super().save_model(request, obj, form, change)

admin.site.register(Program, ProgramAdmin)
admin.site.register(Update)