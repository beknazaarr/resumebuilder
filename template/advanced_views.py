from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Template
from .serializers import TemplateListSerializer, TemplateDetailSerializer


class TemplateSearchView(APIView):
    """
    Расширенный поиск шаблонов с множественными фильтрами
    
    Query параметры:
    - q: текстовый поиск по названию и описанию
    - is_active: фильтр по активности (true/false)
    - created_by: поиск по создателю
    - sort: сортировка (name, -name, created_at, -created_at, popular, -popular)
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Начальный queryset
        queryset = Template.objects.all()
        
        # Если не админ, показываем только активные
        if not (request.user.is_authenticated and request.user.is_staff):
            queryset = queryset.filter(is_active=True)
        
        # Текстовый поиск
        search_query = request.query_params.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Фильтр по активности (только для админов)
        is_active = request.query_params.get('is_active')
        if is_active and request.user.is_staff:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        # Фильтр по создателю (только для админов)
        created_by = request.query_params.get('created_by')
        if created_by and request.user.is_staff:
            queryset = queryset.filter(created_by__username__icontains=created_by)
        
        # Добавляем аннотацию с количеством использований
        queryset = queryset.annotate(usage_count=Count('resumes'))
        
        # Сортировка
        sort_param = request.query_params.get('sort', '-created_at')
        
        sort_mapping = {
            'name': 'name',
            '-name': '-name',
            'created_at': 'created_at',
            '-created_at': '-created_at',
            'popular': '-usage_count',
            '-popular': 'usage_count',
        }
        
        sort_field = sort_mapping.get(sort_param, '-created_at')
        queryset = queryset.order_by(sort_field)
        
        # Сериализация
        serializer = TemplateListSerializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'results': serializer.data,
            'search_query': search_query,
            'sort': sort_param
        })


class TemplatePopularView(APIView):
    """Получить самые популярные шаблоны"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 5))
        
        # Только активные шаблоны для обычных пользователей
        queryset = Template.objects.filter(is_active=True)
        
        # Аннотируем количество использований и сортируем
        queryset = queryset.annotate(
            usage_count=Count('resumes')
        ).order_by('-usage_count')[:limit]
        
        serializer = TemplateListSerializer(queryset, many=True)
        
        # Добавляем статистику использования
        results = []
        for template_data, template_obj in zip(serializer.data, queryset):
            template_data['usage_count'] = template_obj.usage_count
            results.append(template_data)
        
        return Response({
            'message': f'Топ {limit} популярных шаблонов',
            'results': results
        })


class TemplateStatsView(APIView):
    """Статистика по шаблонам"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Общая статистика
        total_templates = Template.objects.count()
        active_templates = Template.objects.filter(is_active=True).count()
        inactive_templates = total_templates - active_templates
        
        # Самый популярный шаблон
        most_popular = Template.objects.annotate(
            usage_count=Count('resumes')
        ).order_by('-usage_count').first()
        
        most_popular_data = None
        if most_popular:
            most_popular_data = {
                'id': most_popular.id,
                'name': most_popular.name,
                'usage_count': most_popular.resumes.count()
            }
        
        # Неиспользуемые шаблоны
        unused_templates = Template.objects.annotate(
            usage_count=Count('resumes')
        ).filter(usage_count=0).count()
        
        # Статистика по создателям
        creators_stats = {}
        for template in Template.objects.select_related('created_by').all():
            if template.created_by:
                username = template.created_by.username
                if username not in creators_stats:
                    creators_stats[username] = {
                        'count': 0,
                        'active': 0
                    }
                creators_stats[username]['count'] += 1
                if template.is_active:
                    creators_stats[username]['active'] += 1
        
        return Response({
            'total_templates': total_templates,
            'active_templates': active_templates,
            'inactive_templates': inactive_templates,
            'unused_templates': unused_templates,
            'most_popular': most_popular_data,
            'creators_stats': creators_stats
        })


class TemplateBulkOperationsView(APIView):
    """Массовые операции над шаблонами (только для админов)"""
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        """
        Массовые операции:
        - action: 'activate', 'deactivate', 'delete'
        - template_ids: список ID шаблонов
        """
        action = request.data.get('action')
        template_ids = request.data.get('template_ids', [])
        
        if not action or not template_ids:
            return Response({
                'error': 'Необходимо указать action и template_ids'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем шаблоны
        templates = Template.objects.filter(id__in=template_ids)
        
        if not templates.exists():
            return Response({
                'error': 'Шаблоны не найдены'
            }, status=status.HTTP_404_NOT_FOUND)
        
        updated_count = 0
        errors = []
        
        if action == 'activate':
            updated_count = templates.update(is_active=True)
            message = f'Активировано шаблонов: {updated_count}'
            
        elif action == 'deactivate':
            updated_count = templates.update(is_active=False)
            message = f'Деактивировано шаблонов: {updated_count}'
            
        elif action == 'delete':
            # Проверяем, не используются ли шаблоны
            for template in templates:
                if template.resumes.exists():
                    errors.append({
                        'template_id': template.id,
                        'name': template.name,
                        'error': f'Используется в {template.resumes.count()} резюме'
                    })
                else:
                    template.delete()
                    updated_count += 1
            
            message = f'Удалено шаблонов: {updated_count}'
        else:
            return Response({
                'error': 'Неизвестное действие. Доступны: activate, deactivate, delete'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': message,
            'updated_count': updated_count,
            'errors': errors if errors else None
        })