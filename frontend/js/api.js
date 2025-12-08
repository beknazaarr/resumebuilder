// js/api.js
const API_BASE_URL = '/api';

// Получить токен из localStorage
function getToken() {
    return localStorage.getItem('access_token');
}

// Установить токены
function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

// Удалить токены
function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
}

// Базовый fetch с обработкой токена
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Токен истек, попробуем обновить
            const refreshed = await refreshToken();
            if (refreshed) {
                // Повторяем запрос с новым токеном
                return apiRequest(endpoint, options);
            } else {
                // Не удалось обновить токен, разлогиниваем
                clearTokens();
                window.location.href = '/login.html';
                return null;
            }
        }

        const data = await response.json();
        
        if (!response.ok) {
            throw data;
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Обновление токена
async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    
    if (!refresh) return false;

    try {
        const response = await fetch(`${API_BASE_URL}/users/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        }
        return false;
    } catch (error) {
        console.error('Refresh token error:', error);
        return false;
    }
}

// API методы
const API = {
    // Авторизация
    auth: {
        register: (data) => apiRequest('/users/register/', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        login: (data) => apiRequest('/users/login/', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        getProfile: () => apiRequest('/users/profile/'),
        
        updateProfile: (data) => apiRequest('/users/profile/', {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        
        changePassword: (data) => apiRequest('/users/change-password/', {
            method: 'POST',
            body: JSON.stringify(data)
        })
    },

    // Резюме
    resumes: {
        list: () => apiRequest('/resumes/'),
        
        get: (id) => apiRequest(`/resumes/${id}/`),
        
        create: (data) => apiRequest('/resumes/create/', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        update: (id, data) => apiRequest(`/resumes/${id}/update/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        
        delete: (id) => apiRequest(`/resumes/${id}/delete/`, {
            method: 'DELETE'
        }),
        
        copy: (id) => apiRequest(`/resumes/${id}/copy/`, {
            method: 'POST'
        }),
        
        setPrimary: (id) => apiRequest(`/resumes/${id}/set-primary/`, {
            method: 'POST'
        }),
        
        exportPDF: (id) => {
            const token = getToken();
            window.open(`${API_BASE_URL}/resumes/${id}/export/pdf/`, '_blank');
        },
        
        exportDOCX: (id) => {
            const token = getToken();
            window.open(`${API_BASE_URL}/resumes/${id}/export/docx/`, '_blank');
        }
    },

    // Личная информация
    personalInfo: {
        get: (resumeId) => apiRequest(`/resumes/${resumeId}/personal-info/`),
        
        createOrUpdate: (resumeId, data) => apiRequest(`/resumes/${resumeId}/personal-info/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        update: (resumeId, data) => apiRequest(`/resumes/${resumeId}/personal-info/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        })
    },

    // Образование
    education: {
        list: (resumeId) => apiRequest(`/resumes/${resumeId}/education/`),
        
        create: (resumeId, data) => apiRequest(`/resumes/${resumeId}/education/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        update: (resumeId, id, data) => apiRequest(`/resumes/${resumeId}/education/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        
        delete: (resumeId, id) => apiRequest(`/resumes/${resumeId}/education/${id}/`, {
            method: 'DELETE'
        })
    },

    // Опыт работы
    workExperience: {
        list: (resumeId) => apiRequest(`/resumes/${resumeId}/work-experience/`),
        
        create: (resumeId, data) => apiRequest(`/resumes/${resumeId}/work-experience/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        update: (resumeId, id, data) => apiRequest(`/resumes/${resumeId}/work-experience/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        
        delete: (resumeId, id) => apiRequest(`/resumes/${resumeId}/work-experience/${id}/`, {
            method: 'DELETE'
        })
    },

    // Навыки
    skills: {
        list: (resumeId) => apiRequest(`/resumes/${resumeId}/skills/`),
        
        create: (resumeId, data) => apiRequest(`/resumes/${resumeId}/skills/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        
        update: (resumeId, id, data) => apiRequest(`/resumes/${resumeId}/skills/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        
        delete: (resumeId, id) => apiRequest(`/resumes/${resumeId}/skills/${id}/`, {
            method: 'DELETE'
        })
    },

    // Шаблоны
    templates: {
        list: () => apiRequest('/templates/'),
        
        get: (id) => apiRequest(`/templates/${id}/`)
    }
};