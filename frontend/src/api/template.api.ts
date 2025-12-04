import api from './axios';
import { Template } from './types';

export const templateApi = {
  // Get all templates
  getTemplates: async () => {
    const response = await api.get<Template[]>('/templates/');
    return response.data;
  },

  // Get single template
  getTemplate: async (id: number) => {
    const response = await api.get<Template>(`/templates/${id}/`);
    return response.data;
  },

  // Search templates
  searchTemplates: async (query: string) => {
    const response = await api.get<{ count: number; results: Template[] }>('/templates/search/', {
      params: { q: query },
    });
    return response.data;
  },

  // Get popular templates
  getPopularTemplates: async (limit: number = 5) => {
    const response = await api.get<{ results: Template[] }>('/templates/popular/', {
      params: { limit },
    });
    return response.data;
  },
};