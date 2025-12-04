import api from './axios';
import { LoginRequest, RegisterRequest, AuthResponse, User } from './types';

export const authApi = {
  // Регистрация
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/users/register/', data);
    return response.data;
  },

  // Вход
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/users/login/', data);
    return response.data;
  },

  // Получить профиль
  getProfile: async (): Promise<User> => {
    const response = await api.get<User>('/users/profile/');
    return response.data;
  },

  // Обновить профиль
  updateProfile: async (data: Partial<User>): Promise<{ message: string; user: User }> => {
    const response = await api.patch<{ message: string; user: User }>('/users/profile/', data);
    return response.data;
  },

  // Изменить пароль
  changePassword: async (data: {
    old_password: string;
    new_password: string;
    new_password2: string;
  }): Promise<{ message: string }> => {
    const response = await api.post<{ message: string }>('/users/change-password/', data);
    return response.data;
  },

  // Выход (очистка токенов на клиенте)
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};