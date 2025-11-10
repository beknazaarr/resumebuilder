from django.contrib import admin
from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'resume')
    list_filter = ('date', 'resume__user')
    search_fields = ('title', 'description')


