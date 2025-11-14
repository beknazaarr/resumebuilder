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
    """Детальная информация о шаблоне с HTML и CSS"""
    serializer_class = TemplateDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Админы видят все шаблоны, обычные пользователи - только активные
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = self.perform_create(serializer)
        
        return Response({
            'message': 'Шаблон успешно создан',
            'template': TemplateDetailSerializer(template).data
        }, status=status.HTTP_201_CREATED)


class AdminTemplateUpdateView(generics.UpdateAPIView):
    """Обновление шаблона (только для админов)"""
    queryset = Template.objects.all()
    serializer_class = TemplateCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Шаблон успешно обновлен',
            'template': TemplateDetailSerializer(instance).data
        })


class AdminTemplateDeleteView(generics.DestroyAPIView):
    """Удаление шаблона (только для админов)"""
    queryset = Template.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        template_name = instance.name
        
        # Проверяем, используется ли шаблон в резюме
        resumes_count = instance.resumes.count()
        if resumes_count > 0:
            return Response({
                'error': f'Шаблон "{template_name}" используется в {resumes_count} резюме. Удаление невозможно.',
                'resumes_count': resumes_count
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Шаблон "{template_name}" успешно удален'
        }, status=status.HTTP_204_NO_CONTENT)


class AdminTemplateListView(generics.ListAPIView):
    """Список всех шаблонов для админов (включая неактивные)"""
    queryset = Template.objects.all()
    serializer_class = TemplateDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description', 'created_by__username']
    ordering_fields = ['name', 'created_at', 'updated_at', 'is_active']
    ordering = ['-created_at']