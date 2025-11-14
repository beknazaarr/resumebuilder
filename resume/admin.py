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
    can_delete = False


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    can_delete = True


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 0
    can_delete = True


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    can_delete = True


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 0
    can_delete = True


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0
    can_delete = True


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'is_primary', 'created_at', 'updated_at')
    list_filter = ('is_primary', 'created_at', 'template', 'user')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'user')
    
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
    
    def has_add_permission(self, request):
        # Админ не может создавать резюме через админку
        return False
    
    def has_change_permission(self, request, obj=None):
        # Админ может только просматривать, но не редактировать
        return True
    
    def has_delete_permission(self, request, obj=None):
        # Админ не может удалять резюме через админку
        # Только через управление пользователем
        return False