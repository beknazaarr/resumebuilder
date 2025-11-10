from django.contrib import admin
from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category', 'resume')
    list_filter = ('level', 'category', 'resume__user')
    search_fields = ('name',)