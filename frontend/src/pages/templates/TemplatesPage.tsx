import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { templateApi } from '@/api/template.api'
import { Layout } from 'lucide-react'

export default function TemplatesPage() {
  const { data: templates, isLoading } = useQuery({
    queryKey: ['templates'],
    queryFn: templateApi.getTemplates,
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Шаблоны резюме</h1>
        <p className="text-gray-600 mt-1">Выберите шаблон для своего резюме</p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Загрузка...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates?.map((template) => (
            <Card key={template.id} className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                {template.preview_image ? (
                  <img
                    src={template.preview_image}
                    alt={template.name}
                    className="w-full h-48 object-cover rounded-md mb-4"
                  />
                ) : (
                  <div className="w-full h-48 bg-gray-100 rounded-md mb-4 flex items-center justify-center">
                    <Layout className="w-12 h-12 text-gray-400" />
                  </div>
                )}
                <CardTitle>{template.name}</CardTitle>
                <CardDescription className="line-clamp-2">
                  {template.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}