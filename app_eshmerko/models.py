# models.py
from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    download_file = models.FileField(upload_to='programs/', null=True, blank=True)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def increment_download_count(self):
        """Метод для увеличения счетчика скачиваний"""
        self.download_count += 1
        self.save()

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
