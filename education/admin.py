from django.contrib import admin
from .models import Education


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'resume')
    list_filter = ('degree', 'start_date', 'resume__user')
    search_fields = ('institution', 'field_of_study')
