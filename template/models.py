from django.db import models
from django.conf import settings


class Template(models.Model):
    """Шаблон резюме"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название шаблона'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    preview_image = models.ImageField(
        upload_to='templates/previews/',
        blank=True,
        null=True,
        verbose_name='Превью шаблона'
    )
    html_structure = models.TextField(
        verbose_name='HTML структура'
    )
    css_styles = models.TextField(
        verbose_name='CSS стили'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_templates',
        verbose_name='Создал'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['-created_at']

    def __str__(self):
        return self.name