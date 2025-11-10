from django.db import models


class Skill(models.Model):
    """Навыки"""
    
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('expert', 'Эксперт'),
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'Технические'),
        ('soft', 'Гибкие навыки'),
        ('language', 'Языки'),
        ('other', 'Другое'),
    ]
    
    resume = models.ForeignKey(
        'resume.Resume',
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='Резюме'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название навыка'
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='intermediate',
        verbose_name='Уровень'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='technical',
        verbose_name='Категория'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"