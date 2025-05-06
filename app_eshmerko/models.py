# models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    meta_description = models.TextField(verbose_name="Мета-описание")
    content = RichTextField()
    published_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата публикации",
        editable=False  # Добавляем это свойство
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    keywords = models.CharField(max_length=255, blank=True, verbose_name="Ключевые слова")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.id:  # Только при создании новой статьи
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Program(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    download_file = models.FileField(upload_to='programs/', null=True, blank=True)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def increment_download_count(self):
        """Метод для увеличения счетчика скачиваний"""
        self.download_count += 1
        self.save()

    def get_absolute_url(self):
        """Метод для использования в sitemap"""
        return reverse('download_program', kwargs={'program_id': self.id})

class Update(models.Model):
    program = models.ForeignKey(Program, related_name='updates', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.TextField()
    file = models.FileField(upload_to='program_versions/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)  # Добавьте это поле

    def __str__(self):
        return f"Обновление {self.version} для {self.program.name}"

    def increment_download_count(self):
        """Увеличивает счетчик скачиваний"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

    def version_tuple(self):
        """Преобразует строку версии в кортеж чисел (например '1.2.3' -> (1, 2, 3))"""
        try:
            return tuple(map(int, self.version.split('.')))
        except (ValueError, AttributeError):
            return tuple()  # Возвращаем пустой кортеж при ошибках
