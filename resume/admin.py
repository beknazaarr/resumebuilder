from django.contrib import admin
from resume.models import Resume
from personalinfo.models import PersonalInfo
from education.models import Education
from workexperlence.models import WorkExperience
from skill.models import Skill
from achievement.models import Achievement
from language.models import Language


class PersonalInfoInline(admin.StackedInline):
    model = PersonalInfo
    extra = 0
    max_num = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 0


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'is_primary', 'created_at', 'updated_at')
    list_filter = ('is_primary', 'created_at', 'template')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [
        PersonalInfoInline,
        EducationInline,
        WorkExperienceInline,
        SkillInline,
        AchievementInline,
        LanguageInline,
    ]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'title', 'template', 'photo', 'is_primary')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
