from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
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
    """Базовый ViewSet для элементов резюме"""
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        resume_id = self.kwargs.get('resume_id')
        return get_object_or_404(Resume, pk=resume_id, user=self.request.user)

    def get_queryset(self):
        resume = self.get_resume()
        return self.queryset.filter(resume=resume)

    def perform_create(self, serializer):
        resume = self.get_resume()
        serializer.save(resume=resume)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': f'{self.model_name} успешно удален'
        }, status=status.HTTP_204_NO_CONTENT)


class EducationViewSet(BaseResumeItemViewSet):
    """CRUD для образования"""
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    model_name = 'Образование'


class WorkExperienceViewSet(BaseResumeItemViewSet):
    """CRUD для опыта работы"""
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    model_name = 'Опыт работы'


class SkillViewSet(BaseResumeItemViewSet):
    """CRUD для навыков"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    model_name = 'Навык'


class AchievementViewSet(BaseResumeItemViewSet):
    """CRUD для достижений"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    model_name = 'Достижение'


class LanguageViewSet(BaseResumeItemViewSet):
    """CRUD для языков"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    model_name = 'Язык'