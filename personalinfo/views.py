from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from resume.models import Resume
from .models import PersonalInfo
from .serializers import PersonalInfoCreateUpdateSerializer


class PersonalInfoCreateUpdateView(generics.GenericAPIView):
    """
    Создание или обновление личной информации в резюме
    POST - создание новой записи
    PUT/PATCH - обновление существующей
    """
    serializer_class = PersonalInfoCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_resume(self):
        """Получение резюме пользователя"""
        resume_id = self.kwargs.get('resume_id')
        return get_object_or_404(Resume, pk=resume_id, user=self.request.user)

    def get_object(self):
        """Получение существующей личной информации"""
        resume = self.get_resume()
        return get_object_or_404(PersonalInfo, resume=resume)

    def post(self, request, *args, **kwargs):
        """Создание новой личной информации"""
        resume = self.get_resume()
        
        # Проверяем, не существует ли уже PersonalInfo для этого резюме
        if hasattr(resume, 'personal_info'):
            return Response({
                'error': 'Личная информация уже существует для этого резюме',
                'message': 'Используйте PUT или PATCH для обновления существующих данных',
                'personal_info_id': resume.personal_info.id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        personal_info = serializer.save(resume=resume)
        
        return Response({
            'message': 'Личная информация успешно создана',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """Полное обновление личной информации"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Личная информация успешно обновлена',
            'data': serializer.data
        })
    
    def patch(self, request, *args, **kwargs):
        """Частичное обновление личной информации"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Личная информация успешно обновлена',
            'data': serializer.data
        })
    
    def get(self, request, *args, **kwargs):
        """Получение текущей личной информации"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except:
            return Response({
                'message': 'Личная информация еще не добавлена',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)


class PersonalInfoDeleteView(generics.DestroyAPIView):
    """Удаление личной информации из резюме"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Получение личной информации для удаления"""
        resume_id = self.kwargs.get('resume_id')
        resume = get_object_or_404(Resume, pk=resume_id, user=self.request.user)
        return get_object_or_404(PersonalInfo, resume=resume)

    def destroy(self, request, *args, **kwargs):
        """Удаление записи"""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'message': 'Личная информация успешно удалена'
        }, status=status.HTTP_204_NO_CONTENT)