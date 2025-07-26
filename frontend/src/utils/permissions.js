/**
 * 前端权限管理工具
 */
import { ref, computed } from 'vue'
import api from '../api'

// 用户权限状态
const userPermissions = ref([])
const userInfo = ref(null)

/**
 * 权限管理类
 */
class PermissionManager {
  constructor() {
    this.permissions = userPermissions
    this.user = userInfo
  }

  /**
   * 初始化用户权限
   */
  async initPermissions() {
    try {
      // 从localStorage获取用户信息
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        this.user.value = JSON.parse(storedUser)
      }

      // 获取用户权限列表
      if (this.user.value) {
        try {
          const response = await api.get('/auth/me/permissions')
          this.permissions.value = response.permissions || []
          console.log('User permissions loaded:', this.permissions.value.length, 'permissions')
        } catch (apiError) {
          console.error('Failed to load user permissions from API:', apiError)
          // 权限加载失败时，不给任何权限，严格按照数据库分配
          this.permissions.value = []
        }
      }
    } catch (error) {
      console.error('Failed to initialize permissions:', error)
      this.permissions.value = []
    }
  }

  /**
   * 检查用户是否有指定权限
   * @param {string} permission 权限代码，如 'user:read'
   * @returns {boolean}
   */
  hasPermission(permission) {
    try {
      // 严格按照数据库中的权限分配检查，不给超级用户特殊待遇
      return this.permissions.value.some(p => p.code === permission)
    } catch (error) {
      console.error('Error checking permission:', error)
      return false
    }
  }

  /**
   * 检查用户是否有任意一个权限
   * @param {string[]} permissions 权限代码数组
   * @returns {boolean}
   */
  hasAnyPermission(permissions) {
    return permissions.some(permission => this.hasPermission(permission))
  }

  /**
   * 检查用户是否有所有权限
   * @param {string[]} permissions 权限代码数组
   * @returns {boolean}
   */
  hasAllPermissions(permissions) {
    return permissions.every(permission => this.hasPermission(permission))
  }

  /**
   * 检查用户是否可以访问页面
   * @param {string} page 页面标识
   * @returns {boolean}
   */
  canAccessPage(page) {
    try {
      const pagePermissions = {
        'dashboard': ['dashboard:read'],
        'users': ['user:read'],
        'roles': ['role:read'],
        'permissions': ['permission:read'],
        'system-configs': ['system:config_read']
      }

      const requiredPermissions = pagePermissions[page]
      if (!requiredPermissions) {
        return true // 未定义权限要求的页面默认可访问
      }

      return this.hasAnyPermission(requiredPermissions)
    } catch (error) {
      console.error('Error checking page access:', error)
      return false
    }
  }

  /**
   * 获取页面可用的操作权限
   * @param {string} page 页面标识
   * @returns {object} 操作权限对象
   */
  getPagePermissions(page) {
    const permissions = {
      users: {
        read: this.hasPermission('user:read'),
        create: this.hasPermission('user:create'),
        update: this.hasPermission('user:update'),
        delete: this.hasPermission('user:delete')
      },
      roles: {
        read: this.hasPermission('role:read'),
        create: this.hasPermission('role:create'),
        update: this.hasPermission('role:update'),
        delete: this.hasPermission('role:delete'),
        assignPermission: this.hasPermission('role:assign_permission')
      },
      permissions: {
        read: this.hasPermission('permission:read'),
        create: this.hasPermission('permission:create'),
        update: this.hasPermission('permission:update'),
        delete: this.hasPermission('permission:delete')
      },
      'system-configs': {
        read: this.hasPermission('system:config_read'),
        create: this.hasPermission('system:config_create'),
        update: this.hasPermission('system:config_update'),
        delete: this.hasPermission('system:config_delete')
      }
    }

    return permissions[page] || {}
  }

  /**
   * 清除权限数据
   */
  clearPermissions() {
    this.permissions.value = []
    this.user.value = null
  }

  /**
   * 获取用户信息
   */
  getUserInfo() {
    return this.user.value
  }

  /**
   * 获取用户权限列表
   */
  getUserPermissions() {
    return this.permissions.value
  }
}

// 创建全局权限管理器实例
const permissionManager = new PermissionManager()

/**
 * 权限检查组合式函数
 */
export function usePermissions() {
  return {
    // 权限检查方法
    hasPermission: (permission) => {
      try {
        return permissionManager.hasPermission(permission)
      } catch (error) {
        console.error('Error in hasPermission:', error)
        return false
      }
    },
    hasAnyPermission: (permissions) => {
      try {
        return permissionManager.hasAnyPermission(permissions)
      } catch (error) {
        console.error('Error in hasAnyPermission:', error)
        return false
      }
    },
    hasAllPermissions: (permissions) => {
      try {
        return permissionManager.hasAllPermissions(permissions)
      } catch (error) {
        console.error('Error in hasAllPermissions:', error)
        return false
      }
    },
    canAccessPage: (page) => {
      try {
        return permissionManager.canAccessPage(page)
      } catch (error) {
        console.error('Error in canAccessPage:', error)
        return true // 默认允许访问
      }
    },
    getPagePermissions: (page) => {
      try {
        return permissionManager.getPagePermissions(page)
      } catch (error) {
        console.error('Error in getPagePermissions:', error)
        return {}
      }
    },

    // 响应式数据
    userPermissions: computed(() => {
      try {
        return permissionManager.getUserPermissions()
      } catch (error) {
        console.error('Error getting user permissions:', error)
        return []
      }
    }),
    userInfo: computed(() => {
      try {
        return permissionManager.getUserInfo()
      } catch (error) {
        console.error('Error getting user info:', error)
        return null
      }
    }),

    // 管理方法
    initPermissions: async () => {
      try {
        await permissionManager.initPermissions()
      } catch (error) {
        console.error('Error initializing permissions:', error)
      }
    },
    clearPermissions: () => {
      try {
        permissionManager.clearPermissions()
      } catch (error) {
        console.error('Error clearing permissions:', error)
      }
    }
  }
}

// 导出权限管理器实例
export default permissionManager

// 权限指令，用于v-permission
export const permissionDirective = {
  mounted(el, binding) {
    const { value } = binding
    if (value && !permissionManager.hasPermission(value)) {
      el.style.display = 'none'
    }
  },
  updated(el, binding) {
    const { value } = binding
    if (value && !permissionManager.hasPermission(value)) {
      el.style.display = 'none'
    } else {
      el.style.display = ''
    }
  }
}
