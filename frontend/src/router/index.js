import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'
import Roles from '../views/Roles.vue'
import SystemConfigs from '../views/SystemConfigs.vue'
import NotificationClients from '../views/NotificationClients.vue'
import Profile from '../views/Profile.vue'
import permissionManager from '../utils/permissions'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: { requiresAuth: true, requiredPermission: 'user:read' }
  },
  {
    path: '/roles',
    name: 'Roles',
    component: Roles,
    meta: { requiresAuth: true, requiredPermission: 'role:read' }
  },
  {
    path: '/system-configs',
    name: 'SystemConfigs',
    component: SystemConfigs,
    meta: { requiresAuth: true, requiredPermission: 'system:config_read' }
  },
  {
    path: '/notification-clients',
    name: 'NotificationClients',
    component: NotificationClients,
    meta: { requiresAuth: true, requiredPermission: 'notification:read' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  // 检查是否需要登录
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  // 如果已登录访问登录页，重定向到首页
  if (to.path === '/login' && token) {
    next('/')
    return
  }

  // 检查权限要求
  if (to.meta.requiredPermission) {
    // 临时简化：如果用户已登录就允许访问，权限检查由页面组件处理
    console.log(`Route ${to.path} requires permission ${to.meta.requiredPermission}`)
    if (token && user) {
      next()
      return
    } else {
      console.warn(`Access denied to ${to.path}: user not logged in`)
      next('/login')
      return
    }
  }

  next()
})

export default router
