# ResumeBuilder API - Полная документация

## 🚀 Установка и запуск

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
mkdir -p media/resumes/photos media/templates/previews templates/resume
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

---

## 📚 API Документация

### Swagger UI
- **URL**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

---

## 🔐 Аутентификация

### Регистрация
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "Иван",
    "last_name": "Иванов"
}
```

**Ответ:**
```json
{
    "user": {...},
    "refresh": "refresh_token_here",
    "access": "access_token_here",
    "message": "Регистрация прошла успешно"
}
```

### Авторизация
```http
POST /api/users/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepass123"
}
```

### Обновление токена
```http
POST /api/users/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

---

## 👤 Профиль пользователя

### Получить профиль
```http
GET /api/users/profile/
Authorization: Bearer {access_token}
```

### Обновить профиль
```http
PUT /api/users/profile/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "username": "newusername",
    "email": "newemail@example.com",
    "first_name": "Новое",
    "last_name": "Имя"
}
```

### Сменить пароль
```http
POST /api/users/change-password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "old_password": "oldpass123",
    "new_password": "newpass456",
    "new_password2": "newpass456"
}
```

---

## 📄 Шаблоны

### Список всех шаблонов
```http
GET /api/templates/
```

### Поиск шаблонов
```http
GET /api/templates/search/?q=классический&sort=popular
```

**Параметры:**
- `q` - текстовый поиск
- `sort` - сортировка: `name`, `-name`, `created_at`, `-created_at`, `popular`, `-popular`
- `is_active` - фильтр по активности (только для админов)

### Популярные шаблоны
```http
GET /api/templates/popular/?limit=5
```

### Детали шаблона
```http
GET /api/templates/{id}/
```

### Создать шаблон (админ)
```http
POST /api/templates/admin/create/
Authorization: Bearer {admin_access_token}
Content-Type: multipart/form-data

{
    "name": "Классический",
    "description": "Стандартный шаблон",
    "html_structure": "<html>...</html>",
    "css_styles": "body {...}",
    "preview_image": [файл],
    "is_active": true
}
```

### Статистика шаблонов (админ)
```http
GET /api/templates/admin/stats/
Authorization: Bearer {admin_access_token}
```

### Массовые операции (админ)
```http
POST /api/templates/admin/bulk-operations/
Authorization: Bearer {admin_access_token}
Content-Type: application/json

{
    "action": "activate",  // или "deactivate", "delete"
    "template_ids": [1, 2, 3]
}
```

---

## 📝 Резюме

### Список резюме
```http
GET /api/resumes/
Authorization: Bearer {access_token}
```

**Параметры фильтрации:**
- `is_primary=true` - только основное резюме
- `template=1` - резюме с определенным шаблоном
- `search=название` - поиск по названию
- `ordering=-created_at` - сортировка

### Создать резюме
```http
POST /api/resumes/create/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "title": "Мое резюме",
    "template": 1,
    "is_primary": false
}
```

### Детали резюме
```http
GET /api/resumes/{id}/
Authorization: Bearer {access_token}
```

### Обновить резюме
```http
PUT /api/resumes/{id}/update/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "title": "Новое название",
    "template": 2
}
```

### Копировать резюме
```http
POST /api/resumes/{id}/copy/
Authorization: Bearer {access_token}
```

### Установить как основное
```http
POST /api/resumes/{id}/set-primary/
Authorization: Bearer {access_token}
```

### Предпросмотр резюме
```http
GET /api/resumes/{id}/preview/
Authorization: Bearer {access_token}
```

**Ответ:**
```json
{
    "html": "полный HTML резюме",
    "css": "CSS стили",
    "data": {...}
}
```

### Удалить резюме
```http
DELETE /api/resumes/{id}/delete/
Authorization: Bearer {access_token}
```

---

## 📸 Работа с фотографией

### Загрузить фото
```http
POST /api/resumes/{id}/photo/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

photo: [файл изображения]
```

**Требования:**
- Форматы: JPEG, JPG, PNG, WEBP
- Максимальный размер: 5MB
- Изображение автоматически оптимизируется до 800x800px

**Ответ:**
```json
{
    "message": "Фотография успешно загружена",
    "photo_url": "/media/resumes/photos/photo.jpg",
    "resume": {...}
}
```

### Информация о фото
```http
GET /api/resumes/{id}/photo/info/
Authorization: Bearer {access_token}
```

**Ответ:**
```json
{
    "has_photo": true,
    "photo_url": "/media/resumes/photos/photo.jpg",
    "file_name": "photo.jpg",
    "file_size": 245678,
    "file_size_mb": 0.23,
    "dimensions": {
        "width": 800,
        "height": 800
    },
    "format": "JPEG"
}
```

### Удалить фото
```http
DELETE /api/resumes/{id}/photo/
Authorization: Bearer {access_token}
```

---

## 📋 Личная информация

### Создать/обновить
```http
POST /api/resume/{resume_id}/personal-info/
Authorization: Bearer {access_token}
Content-Type: application/json

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

### Получить
```http
GET /api/resume/{resume_id}/personal-info/
Authorization: Bearer {access_token}
```

### Удалить
```http
DELETE /api/resume/{resume_id}/personal-info/delete/
Authorization: Bearer {access_token}
```

---

## 🎓 Образование

### Список
```http
GET /api/resumes/{resume_id}/education/
Authorization: Bearer {access_token}
```

### Добавить
```http
POST /api/resumes/{resume_id}/education/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "institution": "КГТУ им. Раззакова",
    "degree": "Бакалавр",
    "field_of_study": "Программная инженерия",
    "start_date": "2018-09-01",
    "end_date": "2022-06-30",
    "description": "Специализация в разработке ПО",
    "order": 0
}
```

### Обновить
```http
PUT /api/resumes/{resume_id}/education/{id}/
Authorization: Bearer {access_token}
```

### Удалить
```http
DELETE /api/resumes/{resume_id}/education/{id}/
Authorization: Bearer {access_token}
```

---

## 💼 Опыт работы

### Список
```http
GET /api/resumes/{resume_id}/work-experience/
Authorization: Bearer {access_token}
```

### Добавить
```http
POST /api/resumes/{resume_id}/work-experience/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "company": "Tech Company",
    "position": "Senior Developer",
    "start_date": "2022-07-01",
    "end_date": null,
    "is_current": true,
    "description": "Разработка веб-приложений на Django/React",
    "order": 0
}
```

**Примечание:** Если `is_current=true`, поле `end_date` должно быть `null`

---

## ⚡ Навыки

### Добавить
```http
POST /api/resumes/{resume_id}/skills/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "Python",
    "level": "advanced",
    "category": "technical",
    "order": 0
}
```

**Уровни:**
- `beginner` - Начальный
- `intermediate` - Средний
- `advanced` - Продвинутый
- `expert` - Эксперт

**Категории:**
- `technical` - Технические
- `soft` - Гибкие навыки
- `language` - Языки программирования
- `other` - Другое

### Получить по категориям
```http
GET /api/resumes/{resume_id}/skills/by_category/
Authorization: Bearer {access_token}
```

---

## 🏆 Достижения

### Добавить
```http
POST /api/resumes/{resume_id}/achievements/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "title": "Победитель хакатона",
    "description": "1 место в национальном хакатоне по разработке",
    "date": "2023-05-15",
    "order": 0
}
```

---

## 🌍 Языки

### Добавить
```http
POST /api/resumes/{resume_id}/languages/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "language": "Английский",
    "proficiency_level": "B2",
    "order": 0
}
```

**Уровни:**
- `A1` - Начальный
- `A2` - Элементарный
- `B1` - Средний
- `B2` - Выше среднего
- `C1` - Продвинутый
- `C2` - Владение в совершенстве
- `native` - Родной

---

## 📥 Экспорт

### Экспорт в PDF
```http
GET /api/resumes/{id}/export/pdf/
Authorization: Bearer {access_token}
```

Скачивает файл `{название_резюме}.pdf`

### Экспорт в DOCX
```http
GET /api/resumes/{id}/export/docx/
Authorization: Bearer {access_token}
```

Скачивает файл `{название_резюме}.docx`

---

## 👨‍💼 Администрирование

### Список пользователей
```http
GET /api/users/admin/users/
Authorization: Bearer {admin_access_token}
```

**Фильтры:**
- `is_blocked=true`
- `is_active=false`
- `is_staff=true`
- `search=username`
- `ordering=-created_at`

### Детали пользователя
```http
GET /api/users/admin/users/{id}/
Authorization: Bearer {admin_access_token}
```

### Обновить пользователя
```http
PUT /api/users/admin/users/{id}/
Authorization: Bearer {admin_access_token}
Content-Type: application/json

{
    "is_blocked": true,
    "is_active": false
}
```

### Блокировка/разблокировка
```http
POST /api/users/admin/users/{id}/block/
Authorization: Bearer {admin_access_token}
```

Переключает статус блокировки пользователя

### Удалить пользователя
```http
DELETE /api/users/admin/users/{id}/
Authorization: Bearer {admin_access_token}
```

**Примечание:** Удаляются также все резюме пользователя

---

## 🔄 Полный сценарий использования

### 1. Регистрация и авторизация
```bash
# Регистрация
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Сохраните access_token из ответа
```

### 2. Создание резюме
```bash
curl -X POST http://localhost:8000/api/resumes/create/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Резюме Software Engineer",
    "template": 1,
    "is_primary": true
  }'

# Сохраните resume_id
```

### 3. Загрузка фотографии
```bash
curl -X POST http://localhost:8000/api/resumes/{resume_id}/photo/ \
  -H "Authorization: Bearer {access_token}" \
  -F "photo=@/path/to/photo.jpg"
```

### 4. Добавление личной информации
```bash
curl -X POST http://localhost:8000/api/resume/{resume_id}/personal-info/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "phone": "+996555123456",
    "email": "john@example.com",
    "address": "Bishkek, Kyrgyzstan",
    "linkedin": "https://linkedin.com/in/johndoe",
    "summary": "Experienced software engineer..."
  }'
```

### 5. Добавление опыта работы
```bash
curl -X POST http://localhost:8000/api/resumes/{resume_id}/work-experience/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Tech Corp",
    "position": "Senior Developer",
    "start_date": "2020-01-01",
    "is_current": true,
    "description": "Developing web applications"
  }'
```

### 6. Добавление навыков
```bash
curl -X POST http://localhost:8000/api/resumes/{resume_id}/skills/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python",
    "level": "expert",
    "category": "technical"
  }'
```

### 7. Предпросмотр
```bash
curl -X GET http://localhost:8000/api/resumes/{resume_id}/preview/ \
  -H "Authorization: Bearer {access_token}"
```

### 8. Экспорт в PDF
```bash
curl -X GET http://localhost:8000/api/resumes/{resume_id}/export/pdf/ \
  -H "Authorization: Bearer {access_token}" \
  --output resume.pdf
```

---

## 📁 Структура проекта

```
resumebuilder/
├── achievement/          # Достижения
├── education/            # Образование
├── language/             # Языки
├── personalinfo/         # Личная информация
├── resume/               # Резюме
│   ├── export_utils.py   # Утилиты экспорта
│   ├── export_views.py   # Views экспорта
│   ├── photo_views.py    # Views для фото (НОВОЕ)
│   ├── common_views.py   # Общие CRUD views
│   └── serializers.py    # Сериализаторы
├── skill/                # Навыки
├── template/             # Шаблоны
│   ├── advanced_views.py # Расширенный поиск (НОВОЕ)
│   └── views.py          # Основные views
├── user/                 # Пользователи
├── workexperlence/       # Опыт работы
├── resumebuilder/        # Настройки проекта
├── templates/            # HTML шаблоны
│   └── resume/
│       ├── pdf_template.html
│       └── preview_template.html (ОБНОВЛЕНО)
├── media/                # Медиа файлы
│   ├── resumes/photos/   # Фотографии
│   └── templates/previews/ # Превью шаблонов
└── requirements.txt
```

---

## ✅ Реализованные функции

### Для пользователей:
- ✅ Регистрация и авторизация (JWT)
- ✅ Управление профилем
- ✅ Смена пароля
- ✅ Создание/редактирование резюме
- ✅ Множественные версии резюме
- ✅ Копирование резюме
- ✅ Установка основного резюме
- ✅ Загрузка и оптимизация фотографий
- ✅ Добавление всех секций (образование, опыт, навыки и т.д.)
- ✅ Предпросмотр в реальном времени
- ✅ Экспорт в PDF/DOCX
- ✅ Поиск и фильтрация шаблонов

### Для администраторов:
- ✅ Управление пользователями
- ✅ Блокировка/разблокировка
- ✅ Удаление аккаунтов
- ✅ Управление шаблонами
- ✅ Статистика по шаблонам
- ✅ Массовые операции над шаблонами

---

## 🔒 Безопасность

- JWT аутентификация с refresh токенами
- Валидация всех входных данных
- Проверка прав доступа
- Оптимизация и валидация загружаемых изображений
- Защита от SQL injection (Django ORM)
- CORS настройки

### В продакшене:
```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['yourdomain.com']
CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']
```

---

## 🐛 Известные ограничения

1. Максимальный размер фото: 5MB
2. Поддерживаемые форматы фото: JPEG, PNG, WEBP
3. Шаблоны, используемые в резюме, нельзя удалить
4. Суперпользователь не может быть заблокирован

---

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи Django: `python manage.py runserver --verbosity 2`
2. Проверьте миграции: `python manage.py showmigrations`
3. Откройте Swagger UI для интерактивного тестирования

---

## 📝 Changelog

### v1.0 (текущая версия)
- ✅ Базовый функционал резюме
- ✅ Аутентификация JWT
- ✅ Экспорт PDF/DOCX
- ✅ Загрузка фотографий с оптимизацией
- ✅ Расширенный поиск шаблонов
- ✅ Предпросмотр в реальном времени
- ✅ Административная панель

---

## 🚀 Следующие шаги

Возможные улучшения:
- Email подтверждение при регистрации
- Сброс пароля через email
- Более сложные шаблоны с конструктором
- Экспорт в другие форматы (HTML, JSON)
- API для интеграции с другими сервисами
- Версионирование резюме