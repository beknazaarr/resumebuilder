import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { resumeApi } from '@/api/resume.api'
import { templateApi } from '@/api/template.api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  FileText, 
  Plus, 
  TrendingUp, 
  Layout, 
  Clock,
  ArrowRight,
  Star
} from 'lucide-react'

export default function DashboardPage() {
  const { data: resumes, isLoading: resumesLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: resumeApi.getResumes,
  })

  const { data: templates, isLoading: templatesLoading } = useQuery({
    queryKey: ['templates', 'popular'],
    queryFn: () => templateApi.getPopularTemplates(3),
  })

  const stats = [
    {
      title: 'Всего резюме',
      value: resumes?.length || 0,
      icon: FileText,
      description: 'Создано резюме',
      color: 'bg-blue-500'
    },
    {
      title: 'Активных',
      value: resumes?.filter(r => !r.is_primary).length || 0,
      icon: TrendingUp,
      description: 'Резюме в работе',
      color: 'bg-green-500'
    },
    {
      title: 'Шаблонов',
      value: templates?.results?.length || 0,
      icon: Layout,
      description: 'Доступно шаблонов',
      color: 'bg-purple-500'
    }
  ]

  const recentResumes = resumes?.slice(0, 3) || []

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Дашборд</h1>
          <p className="text-gray-600 mt-1">
            Добро пожаловать! Создавайте профессиональные резюме
          </p>
        </div>
        <Link to="/resumes/create">
          <Button size="lg" className="shadow-lg">
            <Plus className="w-5 h-5 mr-2" />
            Создать резюме
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    {stat.title}
                  </p>
                  <h3 className="text-3xl font-bold mt-2">{stat.value}</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    {stat.description}
                  </p>
                </div>
                <div className={`${stat.color} p-4 rounded-full`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Resumes */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Последние резюме</CardTitle>
                <CardDescription>Ваши недавно созданные резюме</CardDescription>
              </div>
              <Link to="/resumes">
                <Button variant="ghost" size="sm">
                  Все резюме
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {resumesLoading ? (
              <div className="text-center py-8 text-gray-500">Загрузка...</div>
            ) : recentResumes.length === 0 ? (
              <div className="text-center py-8">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-600 mb-4">Резюме пока нет</p>
                <Link to="/resumes/create">
                  <Button size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    Создать первое резюме
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {recentResumes.map((resume) => (
                  <Link
                    key={resume.id}
                    to={`/resumes/${resume.id}/edit`}
                    className="block"
                  >
                    <div className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors">
                      <div className="flex items-center space-x-3">
                        <div className="p-2 bg-blue-50 rounded">
                          <FileText className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium">{resume.title}</p>
                          <div className="flex items-center text-sm text-gray-500 mt-1">
                            <Clock className="w-3 h-3 mr-1" />
                            {new Date(resume.updated_at).toLocaleDateString('ru-RU')}
                          </div>
                        </div>
                      </div>
                      {resume.is_primary && (
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                          Основное
                        </span>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Popular Templates */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Популярные шаблоны</CardTitle>
                <CardDescription>Начните с готового шаблона</CardDescription>
              </div>
              <Link to="/templates">
                <Button variant="ghost" size="sm">
                  Все шаблоны
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {templatesLoading ? (
              <div className="text-center py-8 text-gray-500">Загрузка...</div>
            ) : (
              <div className="space-y-3">
                {templates?.results?.map((template) => (
                  <div
                    key={template.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-purple-50 rounded">
                        <Layout className="w-5 h-5 text-purple-600" />
                      </div>
                      <div>
                        <p className="font-medium">{template.name}</p>
                        <p className="text-sm text-gray-500 line-clamp-1">
                          {template.description}
                        </p>
                      </div>
                    </div>
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Быстрые действия</CardTitle>
          <CardDescription>Начните работу с резюме</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link to="/resumes/create">
              <div className="p-6 border-2 border-dashed rounded-lg hover:border-primary hover:bg-primary/5 transition-all cursor-pointer text-center">
                <Plus className="w-8 h-8 text-primary mx-auto mb-3" />
                <h4 className="font-semibold mb-1">Создать с нуля</h4>
                <p className="text-sm text-gray-600">
                  Начните с пустого резюме
                </p>
              </div>
            </Link>

            <Link to="/templates">
              <div className="p-6 border-2 border-dashed rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-all cursor-pointer text-center">
                <Layout className="w-8 h-8 text-purple-600 mx-auto mb-3" />
                <h4 className="font-semibold mb-1">Выбрать шаблон</h4>
                <p className="text-sm text-gray-600">
                  Используйте готовый дизайн
                </p>
              </div>
            </Link>

            <Link to="/resumes">
              <div className="p-6 border-2 border-dashed rounded-lg hover:border-green-500 hover:bg-green-50 transition-all cursor-pointer text-center">
                <FileText className="w-8 h-8 text-green-600 mx-auto mb-3" />
                <h4 className="font-semibold mb-1">Мои резюме</h4>
                <p className="text-sm text-gray-600">
                  Продолжить редактирование
                </p>
              </div>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Tips */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
        <CardContent className="p-6">
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-blue-500 rounded-full">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h4 className="font-semibold text-lg mb-2">
                Советы по созданию резюме
              </h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Используйте четкую структуру и профессиональный язык</li>
                <li>• Указывайте конкретные достижения с цифрами</li>
                <li>• Адаптируйте резюме под каждую вакансию</li>
                <li>• Проверьте орфографию и грамматику</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}