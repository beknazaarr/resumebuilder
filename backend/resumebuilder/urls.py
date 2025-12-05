from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from resume.common_views import (
    EducationViewSet,
    WorkExperienceViewSet,
    SkillViewSet,
    AchievementViewSet,
    LanguageViewSet
)

# Swagger/OpenAPI настройки
schema_view = get_schema_view(
    openapi.Info(
        title="ResumeBuilder API",
        default_version='v1',
        description="API для онлайн-платформы создания резюме",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@resumebuilder.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Router для ViewSets
router = DefaultRouter()

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Swagger документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints - ВАЖНО: все API роуты должны быть ПЕРЕД фронтенд паттерном
    path('api/users/', include('user.urls')),
    path('api/templates/', include('template.urls')),
    path('api/resumes/', include('resume.urls')),
    path('api/', include('personalinfo.urls')),
]

# Динамически добавляем роуты для каждого ViewSet с resume_id
# Education
urlpatterns += [
    path('api/resumes/<int:resume_id>/education/', 
         EducationViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='education-list'),
    path('api/resumes/<int:resume_id>/education/<int:pk>/', 
         EducationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='education-detail'),
]

# Work Experience
urlpatterns += [
    path('api/resumes/<int:resume_id>/work-experience/', 
         WorkExperienceViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='work-experience-list'),
    path('api/resumes/<int:resume_id>/work-experience/<int:pk>/', 
         WorkExperienceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='work-experience-detail'),
]

# Skills
urlpatterns += [
    path('api/resumes/<int:resume_id>/skills/', 
         SkillViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='skill-list'),
    path('api/resumes/<int:resume_id>/skills/<int:pk>/', 
         SkillViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='skill-detail'),
]

# Achievements
urlpatterns += [
    path('api/resumes/<int:resume_id>/achievements/', 
         AchievementViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='achievement-list'),
    path('api/resumes/<int:resume_id>/achievements/<int:pk>/', 
         AchievementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='achievement-detail'),
]

# Languages
urlpatterns += [
    path('api/resumes/<int:resume_id>/languages/', 
         LanguageViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='language-list'),
    path('api/resumes/<int:resume_id>/languages/<int:pk>/', 
         LanguageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='language-detail'),
]

# Media files (для разработки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ВАЖНО: Frontend маршрут должен быть ПОСЛЕДНИМ
# Он перехватывает все остальные запросы и отдаёт index.html
urlpatterns += [
    re_path(r'^(?!api|admin|swagger|redoc|media|static).*$', 
            TemplateView.as_view(template_name='index.html'), 
            name='frontend'),
]