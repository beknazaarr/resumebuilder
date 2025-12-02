from django.db import models


class PersonalInfo(models.Model):
    """Личная информация в резюме"""
    resume = models.OneToOneField(
        'resume.Resume',
        on_delete=models.CASCADE,
        related_name='personal_info',
        verbose_name='Резюме'
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name='ФИО'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Email'
    )
    address = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Адрес'
    )
    linkedin = models.URLField(
        blank=True,
        verbose_name='LinkedIn'
    )
    website = models.URLField(
        blank=True,
        verbose_name='Веб-сайт'
    )
    summary = models.TextField(
        blank=True,
        verbose_name='О себе'
    )

    class Meta:
        verbose_name = 'Личная информация'
        verbose_name_plural = 'Личная информация'

    def __str__(self):
        return f"Личная информация - {self.full_name}"