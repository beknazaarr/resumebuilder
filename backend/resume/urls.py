from django.urls import path
from .views import (
    ResumeListView,
    ResumeCreateView,
    ResumeDetailView,
    ResumeUpdateView,
    ResumeDeleteView,
    ResumeCopyView,
    ResumeSetPrimaryView,
    ResumePreviewView,
    ResumePublicView,        # ← ДОБАВЬТЕ ЭТО
    ResumeViewsStatsView,    # ← И ЭТО
    ResumeIncrementViewsView,
)
from .export_views import (
    ResumeExportPDFView,
    ResumeExportDOCXView,
)
from .photo_views import (
    ResumePhotoUploadView,
    ResumePhotoInfoView,
)

app_name = 'resume'

urlpatterns = [
    # Основные операции с резюме
    path('', ResumeListView.as_view(), name='list'),
    path('create/', ResumeCreateView.as_view(), name='create'),
    path('<int:pk>/', ResumeDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', ResumeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ResumeDeleteView.as_view(), name='delete'),
    
    # Дополнительные операции
    path('<int:pk>/copy/', ResumeCopyView.as_view(), name='copy'),
    path('<int:pk>/set-primary/', ResumeSetPrimaryView.as_view(), name='set_primary'),
    
    # Предпросмотр
    path('<int:pk>/preview/', ResumePreviewView.as_view(), name='preview'),
    
    # Публичный просмотр и статистика
    path('<int:pk>/public/', ResumePublicView.as_view(), name='public'),
    path('<int:pk>/views-stats/', ResumeViewsStatsView.as_view(), name='views_stats'),
    path('<int:pk>/increment-views/', ResumeIncrementViewsView.as_view(), name='increment_views'),
    
    # Работа с фотографией
    path('<int:pk>/photo/', ResumePhotoUploadView.as_view(), name='photo_upload'),
    path('<int:pk>/photo/info/', ResumePhotoInfoView.as_view(), name='photo_info'),
    
    # Экспорт
    path('<int:pk>/export/pdf/', ResumeExportPDFView.as_view(), name='export_pdf'),
    path('<int:pk>/export/docx/', ResumeExportDOCXView.as_view(), name='export_docx'),
]