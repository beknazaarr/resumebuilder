import { NavLink } from 'react-router-dom'
import { LayoutDashboard, FileText, Layout, User } from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  {
    name: 'Дашборд',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Мои резюме',
    href: '/resumes',
    icon: FileText,
  },
  {
    name: 'Шаблоны',
    href: '/templates',
    icon: Layout,
  },
  {
    name: 'Профиль',
    href: '/profile',
    icon: User,
  },
]

export default function Sidebar() {
  return (
    <aside className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col lg:pt-16">
      <div className="flex flex-col flex-grow bg-white border-r border-gray-200 pt-5 pb-4 overflow-y-auto">
        <nav className="flex-1 px-4 space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  isActive
                    ? 'bg-primary text-white'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                )
              }
            >
              {({ isActive }) => (
                <>
                  <item.icon
                    className={cn(
                      'mr-3 h-5 w-5 flex-shrink-0',
                      isActive ? 'text-white' : 'text-gray-500 group-hover:text-gray-900'
                    )}
                  />
                  {item.name}
                </>
              )}
            </NavLink>
          ))}
        </nav>
      </div>
    </aside>
  )
}