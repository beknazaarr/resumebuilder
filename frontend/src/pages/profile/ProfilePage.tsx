import { useAuthStore } from '@/store/authStore'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { User } from 'lucide-react'

export default function ProfilePage() {
  const { user } = useAuthStore()

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-3xl font-bold">Профиль</h1>
        <p className="text-gray-600 mt-1">Управление вашим аккаунтом</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Личная информация</CardTitle>
          <CardDescription>Обновите данные вашего профиля</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Имя пользователя</label>
            <Input defaultValue={user?.username} disabled />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Email</label>
            <Input defaultValue={user?.email} />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Имя</label>
              <Input defaultValue={user?.first_name} />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Фамилия</label>
              <Input defaultValue={user?.last_name} />
            </div>
          </div>

          <Button>Сохранить изменения</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Изменить пароль</CardTitle>
          <CardDescription>Обновите пароль вашего аккаунта</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Текущий пароль</label>
            <Input type="password" />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Новый пароль</label>
            <Input type="password" />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Подтверждение пароля</label>
            <Input type="password" />
          </div>

          <Button>Изменить пароль</Button>
        </CardContent>
      </Card>
    </div>
  )
}