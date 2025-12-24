from django.db import models
from django.conf import settings


class Resume(models.Model):
    """Резюме пользователя"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='Пользователь'
    )
    template = models.ForeignKey(
        'template.Template',
        on_delete=models.SET_NULL,
        null=True,
        related_name='resumes',
        verbose_name='Шаблон'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название версии'
    )
    photo = models.ImageField(
        upload_to='resumes/photos/',
        blank=True,
        null=True,
        verbose_name='Фотография'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Основное резюме'
    )
    
    # ← ДОБАВЬТЕ ЭТО ПОЛЕ
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров'
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
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    # ← ДОБАВЬТЕ ЭТОТ МЕТОД
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])