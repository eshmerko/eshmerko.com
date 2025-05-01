from django.contrib import admin
from django.db import models
from .models import Program, Update, Article
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published', 'views')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_date', 'views')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'meta_description', 'content', 'keywords')
        }),
        ('Настройки публикации', {
            'fields': ('is_published',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # При редактировании существующего объекта
            return self.readonly_fields + ('published_date',)
        return self.readonly_fields

class UpdateInline(admin.TabularInline):
    model = Update
    extra = 1  # количество пустых форм для добавления новых обновлений

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_description', 'download_count')
    inlines = [UpdateInline]  # Добавляем возможность редактировать обновления в форме программы
    
    # Метод для отображения краткого описания HTML в списке программ
    def display_description(self, obj):
        return strip_tags(obj.description)[:50] + "..." if obj.description else ""  # Изменил отображение
    display_description.short_description = 'Описание'  # Изменил название

    # Метод для безопасной обработки HTML
    def save_model(self, request, obj, form, change):
        # Здесь можно добавить дополнительную очистку HTML, если нужно
        super().save_model(request, obj, form, change)

admin.site.register(Program, ProgramAdmin)
# admin.site.unregister(Update)  # Убираем эту строку - мы регистрируем Update ниже
@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('program', 'version', 'release_date', 'is_active', 'download_count')
    list_filter = ('program', 'is_active')
    search_fields = ('version', 'program__name')
    readonly_fields = ('download_count',)  # Теперь поле существует

    fieldsets = (
        (None, {
            'fields': ('program', 'version', 'file', 'is_active', 'download_count')
        }),
        ('Release Info', {
            'fields': ('release_date', 'description'),
            'classes': ('collapse',)
        }),
    )