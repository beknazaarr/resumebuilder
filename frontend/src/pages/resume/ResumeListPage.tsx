import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText, Plus, Edit, Copy, Trash2 } from 'lucide-react'
import { resumeApi } from '@/api/resume.api'

export default function ResumeListPage() {
  const { data: resumes, isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: resumeApi.getResumes,
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Мои резюме</h1>
          <p className="text-gray-600 mt-1">Управляйте своими резюме</p>
        </div>
        <Link to="/resumes/create">
          <Button size="lg">
            <Plus className="w-5 h-5 mr-2" />
            Создать резюме
          </Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Загрузка...</div>
      ) : !resumes || resumes.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Нет резюме</h3>
            <p className="text-gray-600 mb-6">Создайте свое первое резюме</p>
            <Link to="/resumes/create">
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Создать резюме
              </Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resumes.map((resume) => (
            <Card key={resume.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="truncate">{resume.title}</span>
                  {resume.is_primary && (
                    <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded ml-2">
                      Основное
                    </span>
                  )}
                </CardTitle>
                <CardDescription>
                  Обновлено: {new Date(resume.updated_at).toLocaleDateString('ru-RU')}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {resume.personal_info && (
                  <div className="text-sm text-gray-600">
                    <p className="font-medium">{resume.personal_info.full_name}</p>
                    <p>{resume.personal_info.email}</p>
                  </div>
                )}
                
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>Заполнено: {resume.completion_percentage || 0}%</span>
                  <span>{resume.sections_count || 0} секций</span>
                </div>

                <div className="flex space-x-2">
                  <Link to={`/resumes/${resume.id}/edit`} className="flex-1">
                    <Button variant="outline" className="w-full" size="sm">
                      <Edit className="w-4 h-4 mr-2" />
                      Редактировать
                    </Button>
                  </Link>
                  <Button variant="ghost" size="sm">
                    <Copy className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm">
                    <Trash2 className="w-4 h-4 text-destructive" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}