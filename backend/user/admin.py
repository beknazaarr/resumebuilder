from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Управление пользователями"""
    
    list_display = (
        'username', 
        'email', 
        'full_name_display', 
        'resumes_count',
        'is_staff', 
        'is_blocked', 
        'is_active',
        'created_at'
    )
    
    list_filter = (
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'is_blocked', 
        'created_at',
        'date_joined'
    )
    
    search_fields = (
        'username', 
        'email', 
        'first_name', 
        'last_name'
    )
    
    ordering = ('-created_at',)
    
    readonly_fields = (
        'created_at',
        'updated_at', 
        'date_joined',
        'last_login',
        'resumes_count',
        'resumes_list'
    )
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('is_blocked', 'created_at', 'updated_at')
        }),
        ('Статистика', {
            'fields': ('resumes_count', 'resumes_list'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name_display(self, obj):
        """Отображение полного имени"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return "-"
    full_name_display.short_description = 'Полное имя'
    
    def resumes_count(self, obj):
        """Количество резюме пользователя"""
        count = obj.resumes.count()
        if count > 0:
            url = reverse('admin:resume_resume_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}">{} резюме</a>', url, count)
        return "0 резюме"
    resumes_count.short_description = 'Резюме'
    
    def resumes_list(self, obj):
        """Список резюме пользователя"""
        resumes = obj.resumes.all()
        if not resumes:
            return "Нет резюме"
        
        html = '<ul>'
        for resume in resumes:
            url = reverse('admin:resume_resume_change', args=[resume.id])
            primary = ' <strong>(Основное)</strong>' if resume.is_primary else ''
            html += f'<li><a href="{url}">{resume.title}</a>{primary} - {resume.updated_at.strftime("%d.%m.%Y")}</li>'
        html += '</ul>'
        
        return format_html(html)
    resumes_list.short_description = 'Список резюме'
    
    def get_queryset(self, request):
        """Оптимизация запросов"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('resumes')
    
    actions = ['block_users', 'unblock_users', 'activate_users', 'deactivate_users']
    
    def block_users(self, request, queryset):
        """Массовая блокировка пользователей"""
        # Исключаем суперпользователей и текущего пользователя
        users_to_block = queryset.exclude(is_superuser=True).exclude(id=request.user.id)
        updated = users_to_block.update(is_blocked=True)
        self.message_user(request, f'Заблокировано пользователей: {updated}')
    block_users.short_description = 'Заблокировать выбранных пользователей'
    
    def unblock_users(self, request, queryset):
        """Массовая разблокировка пользователей"""
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f'Разблокировано пользователей: {updated}')
    unblock_users.short_description = 'Разблокировать выбранных пользователей'
    
    def activate_users(self, request, queryset):
        """Массовая активация пользователей"""
        users_to_activate = queryset.exclude(id=request.user.id)
        updated = users_to_activate.update(is_active=True)
        self.message_user(request, f'Активировано пользователей: {updated}')
    activate_users.short_description = 'Активировать выбранных пользователей'
    
    def deactivate_users(self, request, queryset):
        """Массовая деактивация пользователей"""
        # Исключаем суперпользователей и текущего пользователя
        users_to_deactivate = queryset.exclude(is_superuser=True).exclude(id=request.user.id)
        updated = users_to_deactivate.update(is_active=False)
        self.message_user(request, f'Деактивировано пользователей: {updated}')
    deactivate_users.short_description = 'Деактивировать выбранных пользователей'
    
    def has_delete_permission(self, request, obj=None):
        """Проверка прав на удаление"""
        if obj:
            # Нельзя удалить себя или суперпользователя
            if obj.id == request.user.id or obj.is_superuser:
                return False
        return super().has_delete_permission(request, obj)