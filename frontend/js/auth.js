// js/auth.js

// Проверка авторизации
function isAuthenticated() {
    return !!localStorage.getItem('access_token');
}

// Получить данные пользователя
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Сохранить данные пользователя
function setCurrentUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// Защита страницы (требует авторизацию)
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login.html';
    }
}

// Выход
function logout() {
    clearTokens();
    window.location.href = '/index.html';
}

// Обновить UI в зависимости от статуса авторизации
function updateAuthUI() {
    const user = getCurrentUser();
    const authButtons = document.getElementById('authButtons');
    const userMenu = document.getElementById('userMenu');

    if (user && authButtons && userMenu) {
        authButtons.style.display = 'none';
        userMenu.style.display = 'flex';
        document.getElementById('userName').textContent = user.username;
    }
}