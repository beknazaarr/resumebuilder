from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Resume
from .serializers import (
    ResumeListSerializer,
    ResumeDetailSerializer,
    ResumeCreateUpdateSerializer
)


class ResumeListView(generics.ListAPIView):
    """Список всех резюме текущего пользователя"""
    serializer_class = ResumeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_primary', 'template']
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-updated_at']

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeCreateView(generics.CreateAPIView):
    """Создание нового резюме"""
    serializer_class = ResumeCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        resume = serializer.save()
        
        return Response({
            'message': 'Резюме успешно создано',
            'resume': ResumeDetailSerializer(resume).data
        }, status=status.HTTP_201_CREATED)


class ResumeDetailView(generics.RetrieveAPIView):
    """Детальная информация о резюме"""
    serializer_class = ResumeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumePreviewView(APIView):
    """Предпросмотр резюме в реальном времени (возвращает HTML)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        # Получаем шаблон
        if not resume.template:
            return Response({
                'error': 'Для резюме не выбран шаблон'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Формируем данные для предпросмотра
        context = {
            'resume': resume,
            'personal_info': getattr(resume, 'personal_info', None),
            'education': resume.education.all(),
            'work_experience': resume.work_experience.all(),
            'skills': resume.skills.all(),
            'achievements': resume.achievements.all(),
            'languages': resume.languages.all(),
        }
        
        # Возвращаем HTML и CSS
        return Response({
            'html': resume.template.html_structure,
            'css': resume.template.css_styles,
            'data': ResumeDetailSerializer(resume).data
        })


class ResumeUpdateView(generics.UpdateAPIView):
    """Обновление резюме"""
    serializer_class = ResumeCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Резюме успешно обновлено',
            'resume': ResumeDetailSerializer(instance).data
        })


class ResumeDeleteView(generics.DestroyAPIView):
    """Удаление резюме"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        resume_title = instance.title
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Резюме "{resume_title}" успешно удалено'
        }, status=status.HTTP_204_NO_CONTENT)


class ResumeCopyView(APIView):
    """Копирование существующего резюме"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        original_resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        # Создаем копию резюме
        new_resume = Resume.objects.create(
            user=request.user,
            template=original_resume.template,
            title=f"{original_resume.title} (копия)",
            photo=original_resume.photo,
            is_primary=False
        )
        
        # Копируем личную информацию
        if hasattr(original_resume, 'personal_info'):
            original_info = original_resume.personal_info
            from personalinfo.models import PersonalInfo
            PersonalInfo.objects.create(
                resume=new_resume,
                full_name=original_info.full_name,
                phone=original_info.phone,
                email=original_info.email,
                address=original_info.address,
                linkedin=original_info.linkedin,
                website=original_info.website,
                summary=original_info.summary
            )
        
        # Копируем образование
        for edu in original_resume.education.all():
            from education.models import Education
            Education.objects.create(
                resume=new_resume,
                institution=edu.institution,
                degree=edu.degree,
                field_of_study=edu.field_of_study,
                start_date=edu.start_date,
                end_date=edu.end_date,
                description=edu.description,
                order=edu.order
            )
        
        # Копируем опыт работы
        for work in original_resume.work_experience.all():
            from workexperlence.models import WorkExperience
            WorkExperience.objects.create(
                resume=new_resume,
                company=work.company,
                position=work.position,
                start_date=work.start_date,
                end_date=work.end_date,
                is_current=work.is_current,
                description=work.description,
                order=work.order
            )
        
        # Копируем навыки
        for skill in original_resume.skills.all():
            from skill.models import Skill
            Skill.objects.create(
                resume=new_resume,
                name=skill.name,
                level=skill.level,
                category=skill.category,
                order=skill.order
            )
        
        # Копируем достижения
        for achievement in original_resume.achievements.all():
            from achievement.models import Achievement
            Achievement.objects.create(
                resume=new_resume,
                title=achievement.title,
                description=achievement.description,
                date=achievement.date,
                order=achievement.order
            )
        
        # Копируем языки
        for lang in original_resume.languages.all():
            from language.models import Language
            Language.objects.create(
                resume=new_resume,
                language=lang.language,
                proficiency_level=lang.proficiency_level,
                order=lang.order
            )
        
        return Response({
            'message': f'Резюме "{original_resume.title}" успешно скопировано',
            'resume': ResumeDetailSerializer(new_resume).data
        }, status=status.HTTP_201_CREATED)


class ResumeSetPrimaryView(APIView):
    """Установить резюме как основное"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        # Снимаем флаг is_primary со всех резюме пользователя
        Resume.objects.filter(user=request.user).update(is_primary=False)
        
        # Устанавливаем текущее резюме как основное
        resume.is_primary = True
        resume.save()
        
        return Response({
            'message': f'Резюме "{resume.title}" установлено как основное',
            'resume': ResumeListSerializer(resume).data
        })