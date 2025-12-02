from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from resume.models import Resume
from education.models import Education
from workexperlence.models import WorkExperience
from skill.models import Skill
from achievement.models import Achievement
from language.models import Language
from resume.serializers import (
    EducationSerializer,
    WorkExperienceSerializer,
    SkillSerializer,
    AchievementSerializer,
    LanguageSerializer
)


class BaseResumeItemViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet для элементов резюме
    Содержит общую логику для всех связанных с резюме сущностей
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Отключаем пагинацию для элементов резюме

    def get_resume(self):
        """Получение резюме пользователя по ID"""
        resume_id = self.kwargs.get('resume_id')
        return get_object_or_404(Resume, pk=resume_id, user=self.request.user)

    def get_queryset(self):
        """Получение queryset элементов конкретного резюме"""
        resume = self.get_resume()
        return self.queryset.filter(resume=resume).order_by('order', '-id')

    def perform_create(self, serializer):
        """Создание нового элемента с привязкой к резюме"""
        resume = self.get_resume()
        serializer.save(resume=resume)

    def create(self, request, *args, **kwargs):
        """Создание с кастомным ответом"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': f'{self.model_name} успешно добавлен',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Обновление с кастомным ответом"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': f'{self.model_name} успешно обновлен',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """Удаление с кастомным ответом"""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'message': f'{self.model_name} успешно удален'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def reorder(self, request, resume_id=None):
        """
        Массовое изменение порядка элементов
        Ожидает: {"items": [{"id": 1, "order": 0}, {"id": 2, "order": 1}, ...]}
        """
        items_data = request.data.get('items', [])
        
        if not items_data:
            return Response({
                'error': 'Необходимо передать список элементов с их новым порядком'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        resume = self.get_resume()
        updated_count = 0
        
        for item_data in items_data:
            item_id = item_data.get('id')
            new_order = item_data.get('order')
            
            if item_id is not None and new_order is not None:
                try:
                    item = self.queryset.get(id=item_id, resume=resume)
                    item.order = new_order
                    item.save(update_fields=['order'])
                    updated_count += 1
                except self.queryset.model.DoesNotExist:
                    pass
        
        return Response({
            'message': f'Порядок обновлен для {updated_count} элементов',
            'updated_count': updated_count
        })


class EducationViewSet(BaseResumeItemViewSet):
    """CRUD операции для образования"""
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    model_name = 'Образование'


class WorkExperienceViewSet(BaseResumeItemViewSet):
    """CRUD операции для опыта работы"""
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    model_name = 'Опыт работы'


class SkillViewSet(BaseResumeItemViewSet):
    """CRUD операции для навыков"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    model_name = 'Навык'
    
    @action(detail=False, methods=['get'])
    def by_category(self, request, resume_id=None):
        """Получить навыки, сгруппированные по категориям"""
        resume = self.get_resume()
        skills = Skill.objects.filter(resume=resume).order_by('category', 'order')
        
        # Группируем по категориям
        grouped_skills = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in grouped_skills:
                grouped_skills[category] = []
            grouped_skills[category].append(SkillSerializer(skill).data)
        
        return Response(grouped_skills)


class AchievementViewSet(BaseResumeItemViewSet):
    """CRUD операции для достижений"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    model_name = 'Достижение'


class LanguageViewSet(BaseResumeItemViewSet):
    """CRUD операции для языков"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    model_name = 'Язык'