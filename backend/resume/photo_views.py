from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from .models import Resume
from .serializers import ResumeDetailSerializer


class ResumePhotoUploadView(APIView):
    """
    Загрузка и обновление фотографии резюме
    POST - загрузить новую фотографию
    DELETE - удалить текущую фотографию
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Загрузка фотографии"""
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        # Проверяем наличие файла
        if 'photo' not in request.FILES:
            return Response({
                'error': 'Файл фотографии не предоставлен',
                'detail': 'Используйте поле "photo" для загрузки изображения'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        photo_file = request.FILES['photo']
        
        # Проверяем размер файла (максимум 5MB)
        max_size = 5 * 1024 * 1024  # 5MB в байтах
        if photo_file.size > max_size:
            return Response({
                'error': 'Размер файла слишком большой',
                'detail': f'Максимальный размер файла: 5MB. Ваш файл: {round(photo_file.size / 1024 / 1024, 2)}MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем формат файла
        allowed_formats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if photo_file.content_type not in allowed_formats:
            return Response({
                'error': 'Неподдерживаемый формат файла',
                'detail': 'Поддерживаемые форматы: JPEG, JPG, PNG, WEBP',
                'received': photo_file.content_type
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Открываем изображение с помощью Pillow
            img = Image.open(photo_file)
            
            # Конвертируем в RGB если необходимо
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Изменяем размер изображения (макс 800x800, сохраняя пропорции)
            max_dimension = 800
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Сохраняем оптимизированное изображение в BytesIO
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Создаем новый InMemoryUploadedFile
            optimized_photo = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{photo_file.name.split('.')[0]}_optimized.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
            
            # Удаляем старое фото если существует
            if resume.photo:
                resume.photo.delete(save=False)
            
            # Сохраняем новое фото
            resume.photo = optimized_photo
            resume.save()
            
            return Response({
                'message': 'Фотография успешно загружена и оптимизирована',
                'photo_url': resume.photo.url,
                'resume': ResumeDetailSerializer(resume).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Ошибка при обработке изображения',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """Удаление фотографии"""
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        if not resume.photo:
            return Response({
                'message': 'У резюме нет фотографии для удаления'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Удаляем файл фотографии
        resume.photo.delete(save=False)
        resume.photo = None
        resume.save()
        
        return Response({
            'message': 'Фотография успешно удалена',
            'resume': ResumeDetailSerializer(resume).data
        }, status=status.HTTP_200_OK)


class ResumePhotoInfoView(APIView):
    """Получение информации о текущей фотографии"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        """Получить информацию о фотографии"""
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        if not resume.photo:
            return Response({
                'has_photo': False,
                'message': 'У резюме нет фотографии'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Открываем изображение для получения информации
            with Image.open(resume.photo.path) as img:
                width, height = img.size
                format_name = img.format
            
            return Response({
                'has_photo': True,
                'photo_url': resume.photo.url,
                'file_name': resume.photo.name.split('/')[-1],
                'file_size': resume.photo.size,
                'file_size_mb': round(resume.photo.size / 1024 / 1024, 2),
                'dimensions': {
                    'width': width,
                    'height': height
                },
                'format': format_name
            })
        except Exception as e:
            return Response({
                'error': 'Ошибка при получении информации о фото',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)