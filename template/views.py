from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Template
from .serializers import (
    TemplateListSerializer,
    TemplateDetailSerializer,
    TemplateCreateUpdateSerializer
)


class TemplateListView(generics.ListAPIView):
    """Список всех активных шаблонов"""
    serializer_class = TemplateListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Обычные пользователи видят только активные шаблоны
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Template.objects.all()
        return Template.objects.filter(is_active=True)


class TemplateDetailView(generics.RetrieveAPIView):
    """Детальная информация о шаблоне"""
    serializer_class = TemplateDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Template.objects.all()
        return Template.objects.filter(is_active=True)


class AdminTemplateCreateView(generics.CreateAPIView):
    """Создание нового шаблона (только для админов)"""
    queryset = Template.objects.all()
    serializer_class = TemplateCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AdminTemplateUpdateView(generics.UpdateAPIView):
    """Обновление шаблона (только для админов)"""
    queryset = Template.objects.all()
    serializer_class = TemplateCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminTemplateDeleteView(generics.DestroyAPIView):
    """Удаление шаблона (только для админов)"""
    queryset = Template.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Проверяем, используется ли шаблон
        if instance.resumes.exists():
            return Response({
                'error': f'Шаблон используется в {instance.resumes.count()} резюме. Удаление невозможно.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response({
            'message': 'Шаблон успешно удален'
        }, status=status.HTTP_204_NO_CONTENT)


class AdminTemplateListView(generics.ListAPIView):
    """Список всех шаблонов для админов"""
    queryset = Template.objects.all()
    serializer_class = TemplateDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']