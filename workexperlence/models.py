from django.db import models


class WorkExperience(models.Model):
    """Опыт работы"""
    resume = models.ForeignKey(
        'resume.Resume',
        on_delete=models.CASCADE,
        related_name='work_experience',
        verbose_name='Резюме'
    )
    company = models.CharField(
        max_length=300,
        verbose_name='Компания'
    )
    position = models.CharField(
        max_length=200,
        verbose_name='Должность'
    )
    start_date = models.DateField(
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата окончания'
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name='Текущее место работы'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание обязанностей'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.company} - {self.position}"