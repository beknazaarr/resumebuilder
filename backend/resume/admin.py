from django.contrib import admin
from resume.models import Resume
from personalinfo.models import PersonalInfo
from education.models import Education
from workexperlence.models import WorkExperience
from skill.models import Skill
from achievement.models import Achievement
from language.models import Language


class PersonalInfoInline(admin.StackedInline):
    """Inline для просмотра личной информации"""
    model = PersonalInfo
    extra = 0
    max_num = 1
    can_delete = False
    readonly_fields = ('full_name', 'phone', 'email', 'address', 'linkedin', 'website', 'summary')
    
    def has_add_permission(self, request, obj=None):
        return False


class EducationInline(admin.TabularInline):
    """Inline для просмотра образования"""
    model = Education
    extra = 0
    can_delete = False
    readonly_fields = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'description', 'order')
    
    def has_add_permission(self, request, obj=None):
        return False


class WorkExperienceInline(admin.TabularInline):
    """Inline для просмотра опыта работы"""
    model = WorkExperience
    extra = 0
    can_delete = False
    readonly_fields = ('company', 'position', 'start_date', 'end_date', 'is_current', 'description', 'order')
    
    def has_add_permission(self, request, obj=None):
        return False


class SkillInline(admin.TabularInline):
    """Inline для просмотра навыков"""
    model = Skill
    extra = 0
    can_delete = False
    readonly_fields = ('name', 'level', 'category', 'order')
    
    def has_add_permission(self, request, obj=None):
        return False


class AchievementInline(admin.TabularInline):
    """Inline для просмотра достижений"""
    model = Achievement
    extra = 0
    can_delete = False
    readonly_fields = ('title', 'description', 'date', 'order')
    
    def has_add_permission(self, request, obj=None):
        return False


class LanguageInline(admin.TabularInline):
    """Inline для просмотра языков"""
    model = Language
    extra = 0
    can_delete = False
    readonly_fields = ('language', 'proficiency_level', 'order')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """
    Админ панель для резюме.
    Админ может только ПРОСМАТРИВАТЬ резюме пользователей.
    Удаление резюме возможно только через управление пользователями.
    """
    list_display = ('title', 'user', 'user_email', 'template', 'is_primary', 'created_at', 'updated_at')
    list_filter = ('is_primary', 'created_at', 'template', 'user__is_active')
    search_fields = ('title', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('user', 'template', 'title', 'photo', 'is_primary', 'created_at', 'updated_at')
    
    inlines = [
        PersonalInfoInline,
        EducationInline,
        WorkExperienceInline,
        SkillInline,
        AchievementInline,
        LanguageInline,
    ]
    
    fieldsets = (
        ('Информация о резюме', {
            'fields': ('user', 'title', 'template', 'is_primary')
        }),
        ('Фотография', {
            'fields': ('photo',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        """Отображение email пользователя"""
        return obj.user.email
    user_email.short_description = 'Email пользователя'
    
    def has_add_permission(self, request):
        """Админ не может создавать резюме через админку"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Админ может только просматривать резюме"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Админ может удалять резюме"""
        return True
    
    def get_readonly_fields(self, request, obj=None):
        """Все поля только для чтения"""
        if obj:
            return self.readonly_fields
        return self.readonly_fields