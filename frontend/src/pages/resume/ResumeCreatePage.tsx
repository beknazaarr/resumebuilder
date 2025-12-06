import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { useMutation, useQuery } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { resumeApi } from '@/api/resume.api'
import { templateApi } from '@/api/template.api'
import { ArrowLeft, FileText, Layout } from 'lucide-react'

const createResumeSchema = z.object({
  title: z.string().min(3, 'Название должно содержать минимум 3 символа'),
  template: z.number().optional(),
  is_primary: z.boolean().optional(),
})

type CreateResumeForm = z.infer<typeof createResumeSchema>

export default function ResumeCreatePage() {
  const navigate = useNavigate()
  const [selectedTemplate, setSelectedTemplate] = useState<number | null>(null)

  const { data: templates, isLoading: templatesLoading } = useQuery({
    queryKey: ['templates'],
    queryFn: templateApi.getTemplates,
  })

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateResumeForm>({
    resolver: zodResolver(createResumeSchema),
    defaultValues: {
      is_primary: false,
    },
  })

  const createResumeMutation = useMutation({
    mutationFn: (data: { title: string; template?: number; is_primary?: boolean }) =>
      resumeApi.createResume(data),
    onSuccess: (data) => {
      toast.success('Резюме успешно создано!')
      // Перенаправляем на страницу редактирования
      navigate(`/resumes/${data.resume.id}/edit`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Ошибка при создании резюме')
    },
  })

  const onSubmit = (data: CreateResumeForm) => {
    createResumeMutation.mutate({
      title: data.title,
      template: selectedTemplate || undefined,
      is_primary: data.is_primary,
    })
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Шапка */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/resumes')}
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Назад
            </Button>
            <h1 className="text-3xl font-bold">Создать новое резюме</h1>
          </div>
          <p className="text-gray-600 mt-1">
            Заполните основную информацию для создания резюме
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Основная информация */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="w-5 h-5 mr-2" />
              Основная информация
            </CardTitle>
            <CardDescription>
              Укажите название резюме и выберите шаблон (по желанию)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Название */}
            <div className="space-y-2">
              <label className="text-sm font-medium">
                Название резюме <span className="text-red-500">*</span>
              </label>
              <Input
                {...register('title')}
                placeholder="Например: Frontend Developer Resume"
                disabled={createResumeMutation.isPending}
              />
              {errors.title && (
                <p className="text-sm text-destructive">{errors.title.message}</p>
              )}
              <p className="text-xs text-gray-600">
                Это название только для вас, оно не будет отображаться в резюме
              </p>
            </div>

            {/* Сделать основным */}
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="is_primary"
                {...register('is_primary')}
                className="w-4 h-4"
                disabled={createResumeMutation.isPending}
              />
              <label htmlFor="is_primary" className="text-sm font-medium cursor-pointer">
                Сделать основным резюме
              </label>
            </div>
          </CardContent>
        </Card>

        {/* Выбор шаблона */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Layout className="w-5 h-5 mr-2" />
              Выбор шаблона (опционально)
            </CardTitle>
            <CardDescription>
              Вы можете выбрать шаблон сейчас или позже
            </CardDescription>
          </CardHeader>
          <CardContent>
            {templatesLoading ? (
              <div className="text-center py-8 text-gray-600">
                Загрузка шаблонов...
              </div>
            ) : templates && templates.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Без шаблона */}
                <div
                  onClick={() => setSelectedTemplate(null)}
                  className={`
                    border-2 rounded-lg p-4 cursor-pointer transition-all
                    ${selectedTemplate === null
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200 hover:border-gray-300'
                    }
                  `}
                >
                  <div className="w-full h-32 bg-gray-100 rounded-md flex items-center justify-center mb-3">
                    <FileText className="w-12 h-12 text-gray-400" />
                  </div>
                  <h3 className="font-medium">Без шаблона</h3>
                  <p className="text-xs text-gray-600 mt-1">
                    Выбрать шаблон позже
                  </p>
                </div>

                {/* Шаблоны */}
                {templates.slice(0, 5).map((template) => (
                  <div
                    key={template.id}
                    onClick={() => setSelectedTemplate(template.id)}
                    className={`
                      border-2 rounded-lg p-4 cursor-pointer transition-all
                      ${selectedTemplate === template.id
                        ? 'border-primary bg-primary/5'
                        : 'border-gray-200 hover:border-gray-300'
                      }
                    `}
                  >
                    {template.preview_image ? (
                      <img
                        src={template.preview_image}
                        alt={template.name}
                        className="w-full h-32 object-cover rounded-md mb-3"
                      />
                    ) : (
                      <div className="w-full h-32 bg-gray-100 rounded-md flex items-center justify-center mb-3">
                        <Layout className="w-12 h-12 text-gray-400" />
                      </div>
                    )}
                    <h3 className="font-medium">{template.name}</h3>
                    <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                      {template.description}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-600">
                Нет доступных шаблонов
              </div>
            )}

            {templates && templates.length > 5 && (
              <div className="mt-4 text-center">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/templates')}
                >
                  Посмотреть все шаблоны ({templates.length})
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Кнопки */}
        <div className="flex items-center justify-between">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/resumes')}
            disabled={createResumeMutation.isPending}
          >
            Отмена
          </Button>
          <Button
            type="submit"
            size="lg"
            disabled={createResumeMutation.isPending}
          >
            {createResumeMutation.isPending ? 'Создание...' : 'Создать резюме'}
          </Button>
        </div>
      </form>
    </div>
  )
}