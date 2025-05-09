from django.contrib import admin
from django.db import models
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Program, Update, Article, Project, ProjectImage, Testimonial
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

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
