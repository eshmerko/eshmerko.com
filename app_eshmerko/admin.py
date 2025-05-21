from django.contrib import admin
from django.db import models
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Program, Update, Article, Project, ProjectImage, Testimonial, ProjectCategory, ProgramLaunch
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.utils import timezone
# --- CKEditor Forms ---
class ProgramAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Program
        fields = '__all__'

class ProjectAdminForm(forms.ModelForm):
    short_description = forms.CharField(widget=CKEditorWidget())
    full_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Project
        fields = '__all__'

# --- Article ---
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
        if obj:
            return self.readonly_fields + ('published_date',)
        return self.readonly_fields

# --- Program ---
class UpdateInline(admin.TabularInline):
    model = Update
    extra = 1

class ProgramAdmin(admin.ModelAdmin):
    form = ProgramAdminForm
    list_display = ('name', 'display_description', 'download_count')
    inlines = [UpdateInline]

    def display_description(self, obj):
        return strip_tags(obj.description)[:50] + "..." if obj.description else ""
    display_description.short_description = 'Описание'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(Program, ProgramAdmin)

# --- Update ---
@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('program', 'version', 'release_date', 'is_active', 'download_count')
    list_filter = ('program', 'is_active')
    search_fields = ('version', 'program__name')
    readonly_fields = ('download_count',)

    fieldsets = (
        (None, {
            'fields': ('program', 'version', 'file', 'is_active', 'download_count')
        }),
        ('Release Info', {
            'fields': ('release_date', 'description'),
            'classes': ('collapse',)
        }),
    )

# --- ProjectCategory ---
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# --- Project ---
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;" />')
        return "-"
    image_preview.short_description = "Превью"

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'category', 'completion_date', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, TestimonialInline]

# --- ProjectImage ---
@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'order', 'image_preview')
    list_filter = ('project',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 60px;" />')
        return "-"
    image_preview.short_description = "Превью"


# --- Testimonial ---
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'company')
    list_filter = ('project',)
    search_fields = ('author', 'text')

# ⭐⭐⭐⭐⭐ Добавляем новый класс для ProgramLaunch ⭐⭐⭐⭐⭐
@admin.register(ProgramLaunch)
class ProgramLaunchAdmin(admin.ModelAdmin):
    list_display = (
        'app_name', 
        'app_version', 
        'install_id_short',
        'launch_count', 
        'first_launch',
        'last_launch',
        'days_since_last_launch',
        'is_active'
    )
    list_filter = (
        'app_name',
        'system_platform',
        ('first_launch', admin.DateFieldListFilter),
    )
    search_fields = ('install_id', 'app_name', 'app_version')
    readonly_fields = ('install_id', 'first_launch', 'last_launch')
    ordering = ('-last_launch',)
    date_hierarchy = 'first_launch'
    list_per_page = 50

    fieldsets = (
        (None, {
            'fields': (
                'install_id', 
                'app_name', 
                'app_version',
                'launch_count'
            )
        }),
        ('Системная информация', {
            'fields': (
                'system_platform',
                'python_version',
            ),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': (
                'first_launch',
                'last_launch',
            ),
            'classes': ('collapse',)
        }),
    )

    def install_id_short(self, obj):
        return str(obj.install_id)[:8] + '...'
    install_id_short.short_description = 'ID установки'

    def days_since_last_launch(self, obj):
        delta = timezone.now() - obj.last_launch
        return f"{delta.days} дней назад"
    days_since_last_launch.short_description = 'Последняя активность'

    def is_active(self, obj):
        delta = timezone.now() - obj.last_launch
        return delta.days <= 30
    is_active.boolean = True
    is_active.short_description = 'Активная установка'

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions