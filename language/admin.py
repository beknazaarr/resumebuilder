from django.contrib import admin
from .models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'proficiency_level', 'resume')
    list_filter = ('proficiency_level', 'resume__user')
    search_fields = ('language',)