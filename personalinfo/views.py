from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from resume.models import Resume
from .models import PersonalInfo
from .serializers import PersonalInfoCreateUpdateSerializer


class PersonalInfoCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    """Создание или обновление личной информации в резюме"""
    serializer_class = PersonalInfoCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        resume_id = self.kwargs.get('resume_id')
        resume = get_object_or_404(Resume, pk=resume_id, user=self.request.user)
        return get_object_or_404(PersonalInfo, resume=resume)

    def create(self, request, *args, **kwargs):
        resume_id = self.kwargs.get('resume_id')
        resume = get_object_or_404(Resume, pk=resume_id, user=request.user)
        
        # Проверяем, не существует ли уже PersonalInfo для этого резюме
        if hasattr(resume, 'personal_info'):
            return Response({
                'error': 'Личная информация уже существует. Используйте PUT для обновления.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(resume=resume)
        
        return Response({
            'message': 'Личная информация успешно создана',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Личная информация успешно обновлена',
            'data': serializer.data
        })


class PersonalInfoDeleteView(generics.DestroyAPIView):
    """Удаление личной информации"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        resume_id = self.kwargs.get('resume_id')
        resume = get_object_or_404(Resume, pk=resume_id, user=self.request.user)
        return get_object_or_404(PersonalInfo, resume=resume)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Личная информация удалена'
        }, status=status.HTTP_204_NO_CONTENT)