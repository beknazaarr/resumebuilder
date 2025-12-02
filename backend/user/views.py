from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    AdminUserManagementSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Генерируем JWT токены
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Регистрация прошла успешно. Добро пожаловать!'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """Авторизация пользователя"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Валидация входных данных
        if not username or not password:
            return Response({
                'error': 'Необходимо указать username и password'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Аутентификация
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                'error': 'Неверное имя пользователя или пароль'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Проверка активности аккаунта
        if not user.is_active:
            return Response({
                'error': 'Ваш аккаунт деактивирован. Обратитесь к администратору.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Проверка блокировки
        if user.is_blocked:
            return Response({
                'error': 'Ваш аккаунт заблокирован. Обратитесь к администратору для разблокировки.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Генерируем токены
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': f'Добро пожаловать, {user.first_name or user.username}!'
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля пользователя"""
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserProfileUpdateSerializer
    
    def update(self, request, *args, **kwargs):
        """Обновление профиля с кастомным ответом"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Профиль успешно обновлен',
            'user': UserSerializer(instance).data
        })


class ChangePasswordView(APIView):
    """Изменение пароля пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Проверяем старый пароль
            if not user.check_password(serializer.data.get('old_password')):
                return Response({
                    'error': 'Неверный текущий пароль'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Проверяем, что новый пароль отличается от старого
            if serializer.data.get('old_password') == serializer.data.get('new_password'):
                return Response({
                    'error': 'Новый пароль должен отличаться от текущего'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Устанавливаем новый пароль
            user.set_password(serializer.data.get('new_password'))
            user.save()
            
            return Response({
                'message': 'Пароль успешно изменен. Используйте новый пароль для входа.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserListView(generics.ListAPIView):
    """Список всех пользователей (только для админов)"""
    queryset = User.objects.all()
    serializer_class = AdminUserManagementSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_blocked', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username', 'email', 'last_login']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Оптимизация запросов с подсчетом резюме"""
        return User.objects.prefetch_related('resumes')


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Управление конкретным пользователем (только для админов)"""
    queryset = User.objects.all()
    serializer_class = AdminUserManagementSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        """Обновление пользователя с проверками"""
        instance = self.get_object()
        
        # Запрещаем изменять статус суперпользователя
        if instance.is_superuser and not request.user.is_superuser:
            return Response({
                'error': 'Вы не можете изменять данные суперпользователя'
            }, status=status.HTTP_403_FORBIDDEN)
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': f'Данные пользователя {instance.username} успешно обновлены',
            'user': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя с проверками"""
        instance = self.get_object()
        
        # Запрещаем удалять самого себя
        if instance.id == request.user.id:
            return Response({
                'error': 'Вы не можете удалить свой собственный аккаунт'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Запрещаем удалять суперпользователей
        if instance.is_superuser:
            return Response({
                'error': 'Нельзя удалить суперпользователя'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        username = instance.username
        resumes_count = instance.resumes.count()
        
        # Удаляем пользователя (резюме удалятся автоматически по CASCADE)
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Пользователь {username} и его {resumes_count} резюме успешно удалены'
        }, status=status.HTTP_204_NO_CONTENT)


class AdminBlockUserView(APIView):
    """Блокировка/разблокировка пользователя (только для админов)"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            
            # Запрещаем блокировать самого себя
            if user.id == request.user.id:
                return Response({
                    'error': 'Вы не можете заблокировать свой собственный аккаунт'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Запрещаем блокировать суперпользователей
            if user.is_superuser:
                return Response({
                    'error': 'Нельзя заблокировать суперпользователя'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Переключаем статус блокировки
            user.is_blocked = not user.is_blocked
            user.save()
            
            action = "заблокирован" if user.is_blocked else "разблокирован"
            
            return Response({
                'message': f'Пользователь {user.username} успешно {action}',
                'is_blocked': user.is_blocked,
                'user': AdminUserManagementSerializer(user).data
            })
            
        except User.DoesNotExist:
            return Response({
                'error': 'Пользователь не найден'
            }, status=status.HTTP_404_NOT_FOUND)