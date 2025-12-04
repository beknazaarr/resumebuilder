// Auth types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_blocked: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
  message: string;
}

// Resume types
export interface Resume {
  id: number;
  title: string;
  template: number | null;
  template_name?: string;
  template_id?: number;
  photo: string | null;
  is_primary: boolean;
  personal_info?: PersonalInfo;
  education: Education[];
  work_experience: WorkExperience[];
  skills: Skill[];
  achievements: Achievement[];
  languages: Language[];
  sections_count?: number;
  completion_percentage?: number;
  created_at: string;
  updated_at: string;
}

export interface PersonalInfo {
  id: number;
  full_name: string;
  phone: string;
  email: string;
  address: string;
  linkedin: string;
  website: string;
  summary: string;
}

export interface Education {
  id: number;
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date: string | null;
  description: string;
  order: number;
}

export interface WorkExperience {
  id: number;
  company: string;
  position: string;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string;
  order: number;
}

export interface Skill {
  id: number;
  name: string;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  level_display: string;
  category: 'technical' | 'soft' | 'language' | 'other';
  category_display: string;
  order: number;
}

export interface Achievement {
  id: number;
  title: string;
  description: string;
  date: string | null;
  order: number;
}

export interface Language {
  id: number;
  language: string;
  proficiency_level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2' | 'native';
  proficiency_display: string;
  order: number;
}

// Template types
export interface Template {
  id: number;
  name: string;
  description: string;
  preview_image: string | null;
  html_structure?: string;
  css_styles?: string;
  is_active: boolean;
  created_by_username?: string;
  created_at: string;
  updated_at: string;
}

// API Response wrapper
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

// Pagination
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}