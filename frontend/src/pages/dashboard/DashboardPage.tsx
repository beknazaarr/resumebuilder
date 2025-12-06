import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/store/authStore'
import { resumeApi } from '@/api/resume.api'
import { FileText, Plus, Edit, TrendingUp, Clock, Star } from 'lucide-react'
import { formatDate } from '@/lib/utils'

export default function DashboardPage() {
  const { user } = useAuthStore()

  const { data: resumes = [], isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: resumeApi.getResumes,
  })

  console.log("resumes =", resumes) // <-- проверка

  // Статистика
  // Извлекаем данные из пагинации DRF
  const items = resumes?.results || [];

// Статистика
  const totalResumes = items.length;
  const primaryResume = items.find(r => r.is_primary);
  const lastUpdated = items.length ? items[0] : null;

// Последние резюме (макс 3)
  const recentResumes = items.slice(0, 3);


  return (
    <div className="space-y-6">
      {/* Приветствие */}
      <div>
        <h1 className="text-3xl font-bold">
          Добро пожаловать, {user?.first_name || user?.username}! 👋
        </h1>
        <p className="text-gray-600 mt-1">
          Управляйте своими резюме и создавайте новые версии для разных вакансий
        </p>
      </div>

      {/* Статистика */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Всего резюме
            </CardTitle>
            <FileText className="h-4 w-4 text-gray-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalResumes}</div>
            <p className="text-xs text-gray-600 mt-1">
              {totalResumes === 0 ? 'Создайте первое резюме' : 'Активных резюме'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Основное резюме
            </CardTitle>
            <Star className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold truncate">
              {primaryResume ? primaryResume.title : '—'}
            </div>
            <p className="text-xs text-gray-600 mt-1">
              {primaryResume ? 'Установлено' : 'Не выбрано'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Последнее обновление
            </CardTitle>
            <Clock className="h-4 w-4 text-gray-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {lastUpdated ? formatDate(lastUpdated.updated_at).split(',')[0] : '—'}
            </div>
            <p className="text-xs text-gray-600 mt-1 truncate">
              {lastUpdated ? lastUpdated.title : 'Нет резюме'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Быстрые действия */}
      <Card>
        <CardHeader>
          <CardTitle>Быстрые действия</CardTitle>
          <CardDescription>Начните работу с резюме</CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link to="/resumes/create">
            <Button className="w-full h-20 flex flex-col items-center justify-center space-y-2">
              <Plus className="w-6 h-6" />
              <span>Создать новое резюме</span>
            </Button>
          </Link>
          
          <Link to="/resumes">
            <Button variant="outline" className="w-full h-20 flex flex-col items-center justify-center space-y-2">
              <Edit className="w-6 h-6" />
              <span>Редактировать резюме</span>
            </Button>
          </Link>
        </CardContent>
      </Card>

      {/* Последние резюме */}
      {recentResumes.length > 0 && (
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Последние резюме</CardTitle>
              <CardDescription>Недавно обновленные резюме</CardDescription>
            </div>
            <Link to="/resumes">
              <Button variant="ghost" size="sm">
                Все резюме
                <TrendingUp className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentResumes.map((resume) => (
              <div
                key={resume.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h3 className="font-medium">{resume.title}</h3>
                    {resume.is_primary && (
                      <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                        Основное
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    Обновлено: {formatDate(resume.updated_at)}
                  </p>
                </div>
                <Link to={`/resumes/${resume.id}/edit`}>
                  <Button variant="outline" size="sm">
                    <Edit className="w-4 h-4 mr-2" />
                    Редактировать
                  </Button>
                </Link>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Нет резюме */}
      {totalResumes === 0 && (
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle className="text-blue-900">🎯 Начните с создания резюме</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-blue-800">
              Создайте своё первое резюме за несколько минут:
            </p>
            <ol className="list-decimal list-inside space-y-2 text-blue-800">
              <li>Нажмите "Создать новое резюме"</li>
              <li>Заполните личную информацию</li>
              <li>Добавьте образование и опыт работы</li>
              <li>Укажите навыки и достижения</li>
              <li>Экспортируйте в PDF или DOCX</li>
            </ol>
            <Link to="/resumes/create">
              <Button className="mt-4">
                <Plus className="w-4 h-4 mr-2" />
                Создать первое резюме
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
