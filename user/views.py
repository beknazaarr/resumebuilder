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
            'message': 'Пользователь успешно зарегистрирован'
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
                'error': 'Неверные учетные данные'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Проверка блокировки
        if user.is_blocked:
            return Response({
                'error': 'Ваш аккаунт заблокирован. Обратитесь к администратору.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Генерируем токены
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Вход выполнен успешно'
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
                    'error': 'Неверный старый пароль'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Устанавливаем новый пароль
            user.set_password(serializer.data.get('new_password'))
            user.save()
            
            return Response({
                'message': 'Пароль успешно изменен'
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
    ordering_fields = ['created_at', 'username', 'email']
    ordering = ['-created_at']


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Управление конкретным пользователем (только для админов)"""
    queryset = User.objects.all()
    serializer_class = AdminUserManagementSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def destroy(self, request, *args, **kwargs):
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
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Пользователь {username} успешно удален'
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
            
            return Response({
                'message': f'Пользователь {user.username} {"заблокирован" if user.is_blocked else "разблокирован"}',
                'is_blocked': user.is_blocked,
                'user': AdminUserManagementSerializer(user).data
            })
            
        except User.DoesNotExist:
            return Response({
                'error': 'Пользователь не найден'
            }, status=status.HTTP_404_NOT_FOUND)