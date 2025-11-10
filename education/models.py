from django.db import models


class Education(models.Model):
    """Образование"""
    resume = models.ForeignKey(
        'resume.Resume',
        on_delete=models.CASCADE,
        related_name='education',
        verbose_name='Резюме'
    )
    institution = models.CharField(
        max_length=300,
        verbose_name='Учебное заведение'
    )
    degree = models.CharField(
        max_length=200,
        verbose_name='Степень/Квалификация'
    )
    field_of_study = models.CharField(
        max_length=200,
        verbose_name='Специальность'
    )
    start_date = models.DateField(
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата окончания'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.institution} - {self.degree}"