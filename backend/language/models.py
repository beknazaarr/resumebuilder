from django.db import models


class Language(models.Model):
    """Языки"""
    
    PROFICIENCY_CHOICES = [
        ('A1', 'A1 - Начальный'),
        ('A2', 'A2 - Элементарный'),
        ('B1', 'B1 - Средний'),
        ('B2', 'B2 - Выше среднего'),
        ('C1', 'C1 - Продвинутый'),
        ('C2', 'C2 - Владение в совершенстве'),
        ('native', 'Родной'),
    ]
    
    resume = models.ForeignKey(
        'resume.Resume',
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name='Резюме'
    )
    language = models.CharField(
        max_length=100,
        verbose_name='Язык'
    )
    proficiency_level = models.CharField(
        max_length=10,
        choices=PROFICIENCY_CHOICES,
        verbose_name='Уровень владения'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'
        ordering = ['order']

    def __str__(self):
        return f"{self.language} ({self.get_proficiency_level_display()})"