from django.db import models


class Achievement(models.Model):
    """Достижения"""
    resume = models.ForeignKey(
        'resume.Resume',
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Резюме'
    )
    title = models.CharField(
        max_length=300,
        verbose_name='Название достижения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата получения'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['order', '-date']

    def __str__(self):
        return self.title