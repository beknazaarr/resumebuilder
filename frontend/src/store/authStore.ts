import { create } from 'zustand'
import { authApi } from '@/api/auth.api'
import { User, RegisterRequest } from '@/api/types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (username: string, password: string) => {
    const response = await authApi.login({ username, password })
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
    set({ user: response.user, isAuthenticated: true })
  },

  register: async (data: RegisterRequest) => {
    const response = await authApi.register(data)
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
    set({ user: response.user, isAuthenticated: true })
  },

  logout: () => {
    authApi.logout()
    set({ user: null, isAuthenticated: false })
  },

  checkAuth: async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        const user = await authApi.getProfile()
        set({ user, isAuthenticated: true, isLoading: false })
      } else {
        set({ isLoading: false })
      }
    } catch (error) {
      set({ isLoading: false })
    }
  },
}))