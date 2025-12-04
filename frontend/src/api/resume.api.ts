import api from './axios';
import { Resume, PersonalInfo, Education, WorkExperience, Skill, Achievement, Language } from './types';

export const resumeApi = {
  // Resume CRUD
  getResumes: async () => {
    const response = await api.get<Resume[]>('/resumes/');
    return response.data;
  },

  getResume: async (id: number) => {
    const response = await api.get<Resume>(`/resumes/${id}/`);
    return response.data;
  },

  createResume: async (data: { title: string; template?: number }) => {
    const response = await api.post<{ message: string; resume: Resume }>('/resumes/create/', data);
    return response.data;
  },

  updateResume: async (id: number, data: Partial<Resume>) => {
    const response = await api.patch<{ message: string; resume: Resume }>(`/resumes/${id}/update/`, data);
    return response.data;
  },

  deleteResume: async (id: number) => {
    const response = await api.delete(`/resumes/${id}/delete/`);
    return response.data;
  },

  copyResume: async (id: number) => {
    const response = await api.post<{ message: string; resume: Resume }>(`/resumes/${id}/copy/`);
    return response.data;
  },

  setPrimary: async (id: number) => {
    const response = await api.post(`/resumes/${id}/set-primary/`);
    return response.data;
  },

  // Personal Info
  getPersonalInfo: async (resumeId: number) => {
    const response = await api.get<PersonalInfo>(`/resume/${resumeId}/personal-info/`);
    return response.data;
  },

  createPersonalInfo: async (resumeId: number, data: Omit<PersonalInfo, 'id'>) => {
    const response = await api.post(`/resume/${resumeId}/personal-info/`, data);
    return response.data;
  },

  updatePersonalInfo: async (resumeId: number, data: Partial<PersonalInfo>) => {
    const response = await api.patch(`/resume/${resumeId}/personal-info/`, data);
    return response.data;
  },

  // Education
  getEducation: async (resumeId: number) => {
    const response = await api.get<Education[]>(`/resumes/${resumeId}/education/`);
    return response.data;
  },

  createEducation: async (resumeId: number, data: Omit<Education, 'id'>) => {
    const response = await api.post(`/resumes/${resumeId}/education/`, data);
    return response.data;
  },

  updateEducation: async (resumeId: number, id: number, data: Partial<Education>) => {
    const response = await api.patch(`/resumes/${resumeId}/education/${id}/`, data);
    return response.data;
  },

  deleteEducation: async (resumeId: number, id: number) => {
    const response = await api.delete(`/resumes/${resumeId}/education/${id}/`);
    return response.data;
  },

  // Work Experience
  getWorkExperience: async (resumeId: number) => {
    const response = await api.get<WorkExperience[]>(`/resumes/${resumeId}/work-experience/`);
    return response.data;
  },

  createWorkExperience: async (resumeId: number, data: Omit<WorkExperience, 'id'>) => {
    const response = await api.post(`/resumes/${resumeId}/work-experience/`, data);
    return response.data;
  },

  updateWorkExperience: async (resumeId: number, id: number, data: Partial<WorkExperience>) => {
    const response = await api.patch(`/resumes/${resumeId}/work-experience/${id}/`, data);
    return response.data;
  },

  deleteWorkExperience: async (resumeId: number, id: number) => {
    const response = await api.delete(`/resumes/${resumeId}/work-experience/${id}/`);
    return response.data;
  },

  // Skills
  getSkills: async (resumeId: number) => {
    const response = await api.get<Skill[]>(`/resumes/${resumeId}/skills/`);
    return response.data;
  },

  createSkill: async (resumeId: number, data: Omit<Skill, 'id' | 'level_display' | 'category_display'>) => {
    const response = await api.post(`/resumes/${resumeId}/skills/`, data);
    return response.data;
  },

  updateSkill: async (resumeId: number, id: number, data: Partial<Skill>) => {
    const response = await api.patch(`/resumes/${resumeId}/skills/${id}/`, data);
    return response.data;
  },

  deleteSkill: async (resumeId: number, id: number) => {
    const response = await api.delete(`/resumes/${resumeId}/skills/${id}/`);
    return response.data;
  },

  // Achievements
  getAchievements: async (resumeId: number) => {
    const response = await api.get<Achievement[]>(`/resumes/${resumeId}/achievements/`);
    return response.data;
  },

  createAchievement: async (resumeId: number, data: Omit<Achievement, 'id'>) => {
    const response = await api.post(`/resumes/${resumeId}/achievements/`, data);
    return response.data;
  },

  updateAchievement: async (resumeId: number, id: number, data: Partial<Achievement>) => {
    const response = await api.patch(`/resumes/${resumeId}/achievements/${id}/`, data);
    return response.data;
  },

  deleteAchievement: async (resumeId: number, id: number) => {
    const response = await api.delete(`/resumes/${resumeId}/achievements/${id}/`);
    return response.data;
  },

  // Languages
  getLanguages: async (resumeId: number) => {
    const response = await api.get<Language[]>(`/resumes/${resumeId}/languages/`);
    return response.data;
  },

  createLanguage: async (resumeId: number, data: Omit<Language, 'id' | 'proficiency_display'>) => {
    const response = await api.post(`/resumes/${resumeId}/languages/`, data);
    return response.data;
  },

  updateLanguage: async (resumeId: number, id: number, data: Partial<Language>) => {
    const response = await api.patch(`/resumes/${resumeId}/languages/${id}/`, data);
    return response.data;
  },

  deleteLanguage: async (resumeId: number, id: number) => {
    const response = await api.delete(`/resumes/${resumeId}/languages/${id}/`);
    return response.data;
  },

  // Photo
  uploadPhoto: async (resumeId: number, file: File) => {
    const formData = new FormData();
    formData.append('photo', file);
    const response = await api.post(`/resumes/${resumeId}/photo/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  deletePhoto: async (resumeId: number) => {
    const response = await api.delete(`/resumes/${resumeId}/photo/`);
    return response.data;
  },

  // Export
  exportPDF: async (resumeId: number) => {
    const response = await api.get(`/resumes/${resumeId}/export/pdf/`, {
      responseType: 'blob',
    });
    return response.data;
  },

  exportDOCX: async (resumeId: number) => {
    const response = await api.get(`/resumes/${resumeId}/export/docx/`, {
      responseType: 'blob',
    });
    return response.data;
  },
};