// js/api.js
const API_BASE_URL = '/api';

function getToken() {
    return localStorage.getItem('access_token');
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
}

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
            const refreshed = await refreshToken();
            if (refreshed) {
                return apiRequest(endpoint, options);
            } else {
                clearTokens();
                window.location.href = '/login.html';
                return null;
            }
        }

        if (response.status === 204) {
            return { message: 'Success' };
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

async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;

    try {
        const response = await fetch(`${API_BASE_URL}/users/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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

const API = {
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
         getViewsStats: (id) => apiRequest(`/resumes/${id}/views-stats/`, {
        method: 'GET'
        }),
        getViewsStats: (id) => apiRequest(`/resumes/${id}/views-stats/`, {
        method: 'GET'
        })
        },
        incrementViews: (id) => apiRequest(`/resumes/${id}/increment-views/`, {
        method: 'POST'
        }),


       exportPDF: async (id) => {
        const token = getToken();
    
        console.log('Export PDF - Token:', token ? 'EXISTS' : 'MISSING');
    
        try {
        const response = await fetch(`${API_BASE_URL}/resumes/${id}/export/pdf/`, {
            method: 'GET',  // ← Должен быть GET, а не POST
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error('Ошибка экспорта');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_${id}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        } catch (error) {
        console.error('Error exporting PDF:', error);
        alert('Ошибка при экспорте PDF: ' + error.message);
        }
        },

        exportDOCX: async (id) => {
        const token = getToken();
        try {
        const response = await fetch(`${API_BASE_URL}/resumes/${id}/export/docx/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Ошибка экспорта');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_${id}.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        } catch (error) {
        console.error('Error exporting DOCX:', error);
        alert('Ошибка при экспорте DOCX');
        }
        },

        // ФОТО
        uploadPhoto: async (resumeId, file) => {
            const formData = new FormData();
            formData.append('photo', file);
            
            const token = getToken();
            const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}/photo/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw error;
            }
            
            return await response.json();
        },

        deletePhoto: async (resumeId) => {
            const token = getToken();
            const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}/photo/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw error;
            }
            
            return await response.json();
        }
    },

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

    achievements: {
        list: (resumeId) => apiRequest(`/resumes/${resumeId}/achievements/`),
        create: (resumeId, data) => apiRequest(`/resumes/${resumeId}/achievements/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (resumeId, id, data) => apiRequest(`/resumes/${resumeId}/achievements/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        delete: (resumeId, id) => apiRequest(`/resumes/${resumeId}/achievements/${id}/`, {
            method: 'DELETE'
        })
    },

    languages: {
        list: (resumeId) => apiRequest(`/resumes/${resumeId}/languages/`),
        create: (resumeId, data) => apiRequest(`/resumes/${resumeId}/languages/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (resumeId, id, data) => apiRequest(`/resumes/${resumeId}/languages/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        delete: (resumeId, id) => apiRequest(`/resumes/${resumeId}/languages/${id}/`, {
            method: 'DELETE'
        })
    },

    templates: {
        list: () => apiRequest('/templates/'),
        get: (id) => apiRequest(`/templates/${id}/`)
    }
};