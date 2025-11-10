from django.contrib import admin
from .models import PersonalInfo


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'resume')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('resume__user',)
