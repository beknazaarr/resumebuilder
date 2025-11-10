# ResumeBuilder API

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Создание БД PostgreSQL

```sql
CREATE DATABASE resumebuilder_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE resumebuilder_db TO postgres;
```

### 3. Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Создание папок для медиа

```bash
mkdir media
mkdir media/resumes
mkdir media/resumes/photos
mkdir media/templates
mkdir media/templates/previews
```

### 6. Создание папки для шаблонов

```bash
mkdir -p templates/resume
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

## API Endpoints

### Документация
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

### Аутентификация

#### Регистрация
```
POST /api/users/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "Иван",
    "last_name": "Иванов"
}
```

#### Авторизация
```
POST /api/users/login/
{
    "username": "testuser",
    "password": "securepassword123"
}
```

Ответ:
```json
{
    "user": {...},
    "refresh": "refresh_token",
    "access": "access_token"
}
```

#### Обновление токена
```
POST /api/users/token/refresh/
{
    "refresh": "refresh_token"
}
```

### Профиль пользователя

#### Получить/обновить профиль
```
GET/PUT /api/users/profile/
Authorization: Bearer {access_token}
```

#### Сменить пароль
```
POST /api/users/change-password/
Authorization: Bearer {access_token}
{
    "old_password": "oldpass",
    "new_password": "newpass123",
    "new_password2": "newpass123"
}
```

### Шаблоны

#### Список шаблонов
```
GET /api/templates/
```

#### Детали шаблона
```
GET /api/templates/{id}/
```

#### Создать шаблон (только админ)
```
POST /api/templates/admin/create/
Authorization: Bearer {access_token}
{
    "name": "Классический",
    "description": "Стандартный шаблон резюме",
    "html_structure": "<html>...</html>",
    "css_styles": "body { ... }",
    "is_active": true
}
```

### Резюме

#### Список резюме
```
GET /api/resumes/
Authorization: Bearer {access_token}
```

#### Создать резюме
```
POST /api/resumes/create/
Authorization: Bearer {access_token}
{
    "title": "Мое резюме",
    "template": 1,
    "is_primary": false
}
```

#### Детали резюме
```
GET /api/resumes/{id}/
Authorization: Bearer {access_token}
```

#### Обновить резюме
```
PUT /api/resumes/{id}/update/
Authorization: Bearer {access_token}
```

#### Удалить резюме
```
DELETE /api/resumes/{id}/delete/
Authorization: Bearer {access_token}
```

#### Копировать резюме
```
POST /api/resumes/{id}/copy/
Authorization: Bearer {access_token}
```

#### Установить как основное
```
POST /api/resumes/{id}/set-primary/
Authorization: Bearer {access_token}
```

### Личная информация

#### Создать/обновить личную информацию
```
POST/PUT /api/resume/{resume_id}/personal-info/
Authorization: Bearer {access_token}
{
    "full_name": "Иван Иванов",
    "phone": "+996555123456",
    "email": "ivan@example.com",
    "address": "Бишкек, Кыргызстан",
    "linkedin": "https://linkedin.com/in/ivan",
    "website": "https://ivan.dev",
    "summary": "Опытный разработчик..."
}
```

### Образование

#### Список образования
```
GET /api/resumes/{resume_id}/education/
Authorization: Bearer {access_token}
```

#### Добавить образование
```
POST /api/resumes/{resume_id}/education/
Authorization: Bearer {access_token}
{
    "institution": "КГТУ им. Раззакова",
    "degree": "Бакалавр",
    "field_of_study": "Программная инженерия",
    "start_date": "2018-09-01",
    "end_date": "2022-06-30",
    "description": "Специализация...",
    "order": 0
}
```

#### Обновить образование
```
PUT /api/resumes/{resume_id}/education/{id}/
Authorization: Bearer {access_token}
```

#### Удалить образование
```
DELETE /api/resumes/{resume_id}/education/{id}/
Authorization: Bearer {access_token}
```

### Опыт работы

#### Список опыта работы
```
GET /api/resumes/{resume_id}/work-experience/
Authorization: Bearer {access_token}
```

#### Добавить опыт работы
```
POST /api/resumes/{resume_id}/work-experience/
Authorization: Bearer {access_token}
{
    "company": "Tech Company",
    "position": "Senior Developer",
    "start_date": "2022-07-01",
    "end_date": null,
    "is_current": true,
    "description": "Разработка веб-приложений...",
    "order": 0
}
```

### Навыки

#### Добавить навык
```
POST /api/resumes/{resume_id}/skills/
Authorization: Bearer {access_token}
{
    "name": "Python",
    "level": "advanced",
    "category": "technical",
    "order": 0
}
```

Уровни: `beginner`, `intermediate`, `advanced`, `expert`
Категории: `technical`, `soft`, `language`, `other`

### Достижения

#### Добавить достижение
```
POST /api/resumes/{resume_id}/achievements/
Authorization: Bearer {access_token}
{
    "title": "Победитель хакатона",
    "description": "1 место в национальном хакатоне",
    "date": "2023-05-15",
    "order": 0
}
```

### Языки

#### Добавить язык
```
POST /api/resumes/{resume_id}/languages/
Authorization: Bearer {access_token}
{
    "language": "Английский",
    "proficiency_level": "B2",
    "order": 0
}
```

Уровни: `A1`, `A2`, `B1`, `B2`, `C1`, `C2`, `native`

### Экспорт

#### Экспорт в PDF
```
GET /api/resumes/{id}/export/pdf/
Authorization: Bearer {access_token}
```

#### Экспорт в DOCX
```
GET /api/resumes/{id}/export/docx/
Authorization: Bearer {access_token}
```

### Админ панель

#### Список пользователей
```
GET /api/users/admin/users/
Authorization: Bearer {admin_access_token}
```

#### Управление пользователем
```
GET/PUT/DELETE /api/users/admin/users/{id}/
Authorization: Bearer {admin_access_token}
```

#### Блокировка пользователя
```
POST /api/users/admin/users/{id}/block/
Authorization: Bearer {admin_access_token}
```

## Тестирование

### Пример полного сценария

1. Регистрация
2. Авторизация (получение токена)
3. Создание резюме
4. Добавление личной информации
5. Добавление образования
6. Добавление опыта работы
7. Добавление навыков
8. Добавление достижений
9. Добавление языков
10. Просмотр полного резюме
11. Экспорт в PDF/DOCX

### Использование Postman

1. Импортируйте коллекцию из Swagger
2. Настройте переменную окружения `access_token`
3. После авторизации сохраните токен в переменную
4. Используйте `{{access_token}}` в заголовках

## Структура проекта

```
resumebuilder/
├── achievement/        # Достижения
├── education/          # Образование
├── language/           # Языки
├── personalinfo/       # Личная информация
├── resume/            # Резюме
│   ├── export_utils.py
│   ├── export_views.py
│   ├── common_views.py
│   └── serializers.py
├── skill/             # Навыки
├── template/          # Шаблоны
├── user/              # Пользователи
├── workexperlence/    # Опыт работы
├── resumebuilder/     # Настройки проекта
├── templates/         # HTML шаблоны
│   └── resume/
│       └── pdf_template.html
├── media/             # Медиа файлы
└── requirements.txt
```

## Дополнительные замечания

1. Все запросы (кроме регистрации, авторизации и просмотра шаблонов) требуют JWT токен
2. Пользователь может видеть только свои резюме
3. При установке резюме как основное, у других резюме флаг `is_primary` снимается автоматически
4. При копировании резюме копируются все связанные данные
5. Админ может управлять всеми пользователями и шаблонами

## Безопасность

- Используйте сильные пароли
- В продакшене смените SECRET_KEY
- Настройте CORS для конкретных доменов
- Используйте HTTPS
- Настройте rate limiting для API