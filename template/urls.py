from django.urls import path
from .views import (
    TemplateListView,
    TemplateDetailView,
    AdminTemplateCreateView,
    AdminTemplateUpdateView,
    AdminTemplateDeleteView,
    AdminTemplateListView,
)

app_name = 'template'

urlpatterns = [
    # Публичные эндпоинты
    path('', TemplateListView.as_view(), name='list'),
    path('<int:pk>/', TemplateDetailView.as_view(), name='detail'),
    
    # Админ эндпоинты
    path('admin/', AdminTemplateListView.as_view(), name='admin_list'),
    path('admin/create/', AdminTemplateCreateView.as_view(), name='admin_create'),
    path('admin/<int:pk>/update/', AdminTemplateUpdateView.as_view(), name='admin_update'),
    path('admin/<int:pk>/delete/', AdminTemplateDeleteView.as_view(), name='admin_delete'),
]