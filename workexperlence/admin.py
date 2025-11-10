from django.contrib import admin
from .models import WorkExperience


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'start_date', 'end_date', 'is_current', 'resume')
    list_filter = ('is_current', 'start_date', 'resume__user')
    search_fields = ('company', 'position')

