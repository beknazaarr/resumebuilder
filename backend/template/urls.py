from django.urls import path
from .views import (
    TemplateListView,
    TemplateDetailView,
    AdminTemplateCreateView,
    AdminTemplateUpdateView,
    AdminTemplateDeleteView,
    AdminTemplateListView,
)
from .advanced_views import (
    TemplateSearchView,
    TemplatePopularView,
    TemplateStatsView,
    TemplateBulkOperationsView,
)

app_name = 'template'

urlpatterns = [
    # Публичные эндпоинты
    path('', TemplateListView.as_view(), name='list'),
    path('<int:pk>/', TemplateDetailView.as_view(), name='detail'),
    
    # Расширенный поиск и фильтрация
    path('search/', TemplateSearchView.as_view(), name='search'),
    path('popular/', TemplatePopularView.as_view(), name='popular'),
    
    # Админ эндпоинты
    path('admin/', AdminTemplateListView.as_view(), name='admin_list'),
    path('admin/create/', AdminTemplateCreateView.as_view(), name='admin_create'),
    path('admin/<int:pk>/update/', AdminTemplateUpdateView.as_view(), name='admin_update'),
    path('admin/<int:pk>/delete/', AdminTemplateDeleteView.as_view(), name='admin_delete'),
    path('admin/stats/', TemplateStatsView.as_view(), name='admin_stats'),
    path('admin/bulk-operations/', TemplateBulkOperationsView.as_view(), name='admin_bulk_operations'),
]