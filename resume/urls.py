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
)
from .export_views import (
    ResumeExportPDFView,
    ResumeExportDOCXView,
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
    
    # Экспорт
    path('<int:pk>/export/pdf/', ResumeExportPDFView.as_view(), name='export_pdf'),
    path('<int:pk>/export/docx/', ResumeExportDOCXView.as_view(), name='export_docx'),
]