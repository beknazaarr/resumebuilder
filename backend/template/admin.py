from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Управление шаблонами резюме"""
    
    list_display = (
        'name', 
        'preview_thumbnail',
        'is_active', 
        'usage_count',
        'created_by', 
        'created_at', 
        'updated_at'
    )
    
    list_filter = (
        'is_active', 
        'created_at',
        'created_by'
    )
    
    search_fields = (
        'name', 
        'description',
        'created_by__username'
    )
    
    readonly_fields = (
        'created_by',
        'created_at', 
        'updated_at',
        'usage_count',
        'resumes_list',
        'preview_display'
    )
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Превью', {
            'fields': ('preview_image', 'preview_display'),
            'classes': ('collapse',)
        }),
        ('Структура шаблона', {
            'fields': ('html_structure', 'css_styles'),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Использование', {
            'fields': ('usage_count', 'resumes_list'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_thumbnail(self, obj):
        """Миниатюра превью в списке"""
        if obj.preview_image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 60px; border-radius: 4px;" />',
                obj.preview_image.url
            )
        return '-'
    preview_thumbnail.short_description = 'Превью'
    
    def preview_display(self, obj):
        """Полноразмерное превью в детальном виде"""
        if obj.preview_image:
            return format_html(
                '<img src="{}" style="max-width: 400px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.preview_image.url
            )
        return 'Превью не загружено'
    preview_display.short_description = 'Предпросмотр'
    
    def usage_count(self, obj):
        """Количество использований шаблона"""
        count = obj.resumes.count()
        if count > 0:
            url = reverse('admin:resume_resume_changelist') + f'?template__id__exact={obj.id}'
            return format_html(
                '<a href="{}" style="font-weight: bold; color: #417690;">{} резюме</a>',
                url,
                count
            )
        return format_html('<span style="color: #999;">Не используется</span>')
    usage_count.short_description = 'Использование'
    
    def resumes_list(self, obj):
        """Список резюме, использующих этот шаблон"""
        resumes = obj.resumes.select_related('user').all()[:20]  # Показываем первые 20
        total_count = obj.resumes.count()
        
        if not resumes:
            return "Шаблон пока не используется"
        
        html = '<ul style="margin: 0; padding-left: 20px;">'
        for resume in resumes:
            url = reverse('admin:resume_resume_change', args=[resume.id])
            html += f'<li><a href="{url}">{resume.title}</a> ({resume.user.username})</li>'
        html += '</ul>'
        
        if total_count > 20:
            html += f'<p style="color: #999; margin-top: 10px;">... и еще {total_count - 20} резюме</p>'
        
        return format_html(html)
    resumes_list.short_description = 'Список резюме с этим шаблоном'
    
    def save_model(self, request, obj, form, change):
        """Сохранение с автоматическим указанием создателя"""
        if not change:  # Если создается новый шаблон
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Оптимизация запросов"""
        qs = super().get_queryset(request)
        return qs.select_related('created_by').prefetch_related('resumes')
    
    def has_delete_permission(self, request, obj=None):
        """Проверка возможности удаления"""
        if obj and obj.resumes.exists():
            return False  # Нельзя удалить шаблон, который используется
        return super().has_delete_permission(request, obj)
    
    def delete_model(self, request, obj):
        """Удаление с проверкой"""
        if obj.resumes.exists():
            from django.contrib import messages
            messages.error(
                request,
                f'Невозможно удалить шаблон "{obj.name}", так как он используется в {obj.resumes.count()} резюме.'
            )
            return
        super().delete_model(request, obj)
    
    actions = ['activate_templates', 'deactivate_templates', 'duplicate_template']
    
    def activate_templates(self, request, queryset):
        """Массовая активация шаблонов"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано шаблонов: {updated}')
    activate_templates.short_description = 'Активировать выбранные шаблоны'
    
    def deactivate_templates(self, request, queryset):
        """Массовая деактивация шаблонов"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано шаблонов: {updated}')
    deactivate_templates.short_description = 'Деактивировать выбранные шаблоны'
    
    def duplicate_template(self, request, queryset):
        """Дублирование шаблона"""
        for template in queryset:
            template.pk = None
            template.name = f"{template.name} (копия)"
            template.created_by = request.user
            template.is_active = False
            template.save()
        
        count = queryset.count()
        self.message_user(request, f'Создано копий шаблонов: {count}')
    duplicate_template.short_description = 'Дублировать выбранные шаблоны'