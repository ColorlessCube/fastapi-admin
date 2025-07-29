import { h } from 'vue'
import {
  User,
  Setting,
  Bell,
  UserFilled,
  Key,
  CircleCheck,
  Lock,
  Grid,
  CircleClose,
  Delete
} from '@element-plus/icons-vue'

// 用户管理表格配置
export function createUserTableConfig(t) {
  
  return {
    title: t('pages.users.title'),
    description: t('pages.users.description'),
    icon: 'User',
    
    toolbar: {
      search: {
        enabled: true,
        placeholder: t('pages.users.searchPlaceholder')
      },
      filters: [
        {
          key: 'role_id',
          type: 'select',
          placeholder: t('pages.users.filterByRole'),
          options: [] // 动态加载
        },
        {
          key: 'is_active',
          type: 'select',
          placeholder: t('pages.users.filterByStatus'),
          options: [
            { label: t('common.active'), value: true },
            { label: t('common.inactive'), value: false }
          ]
        }
      ],
      actions: [
        {
          key: 'add',
          label: t('pages.users.addUser'),
          icon: 'Plus',
          type: 'primary',
          permission: 'user:create'
        }
      ]
    },

    // 多选配置
    selection: {
      enabled: true,
      actions: [
        {
          key: 'batchDelete',
          label: t('table.batchDelete'),
          type: 'danger',
          icon: Delete,
          confirm: t('table.confirmBatchDelete'),
          permission: 'user:delete'
        }
      ]
    },

    statistics: [
      {
        key: 'total',
        label: t('pages.users.totalUsers'),
        icon: UserFilled,
        color: 'blue'
      },
      {
        key: 'active',
        label: t('pages.users.activeUsers'),
        icon: CircleCheck,
        color: 'green'
      },
      {
        key: 'inactive',
        label: t('pages.users.inactiveUsers'),
        icon: CircleClose,
        color: 'orange'
      },
      {
        key: 'roles',
        label: t('pages.users.totalRoles'),
        icon: Lock,
        color: 'purple'
      }
    ],
    
    columns: [
      {
        key: 'username',
        label: t('pages.users.username'),
        sortable: true,
        width: 120
      },
      {
        key: 'email',
        label: t('pages.users.email'),
        sortable: true,
        width: 200
      },
      {
        key: 'full_name',
        label: t('pages.users.fullName'),
        width: 300
      },
      {
        key: 'roles',
        label: t('pages.users.roles'),
        type: 'tags',
        width: 200,
        formatter: (value) => value?.map(r => r.name) || []
      },
      {
        key: 'is_active',
        label: t('pages.users.status'),
        type: 'status',
        width: 100,
        formatter: (value) => value ? t('common.active') : t('common.inactive')
      },
      {
        key: 'created_at',
        label: t('common.createdAt'),
        type: 'datetime',
        sortable: true,
        width: 200
      }
    ],
    
    actions: [
      {
        key: 'edit',
        label: t('common.edit'),
        icon: 'Edit',
        type: 'primary',
        size: 'small',
        permission: 'user:update'
      },
      {
        key: 'delete',
        label: t('common.delete'),
        icon: 'Delete',
        type: 'danger',
        size: 'small',
        permission: 'user:delete',
        confirm: t('pages.users.deleteConfirm')
      }
    ],
    
    pagination: {
      pageSizes: [10, 20, 50, 100],
      defaultPageSize: 20
    }
  }
}

// 角色管理表格配置
export function createRoleTableConfig(t) {
  
  return {
    title: t('pages.roles.title'),
    description: t('pages.roles.description'),
    icon: 'Lock',
    
    toolbar: {
      search: {
        enabled: true,
        placeholder: t('pages.roles.searchPlaceholder')
      },
      actions: [
        {
          key: 'add',
          label: t('pages.roles.addRole'),
          icon: 'Plus',
          type: 'primary',
          permission: 'role:create'
        }
      ]
    },
    
    statistics: [
      {
        key: 'total',
        label: t('pages.roles.totalRoles'),
        icon: Lock,
        color: 'blue'
      },
      {
        key: 'totalPermissions',
        label: t('pages.roles.totalPermissions'),
        icon: Key,
        color: 'green'
      },
      {
        key: 'totalUsers',
        label: t('pages.roles.totalUsers'),
        icon: User,
        color: 'orange'
      }
    ],
    
    columns: [
      {
        key: 'name',
        label: t('pages.roles.roleName'),
        sortable: true,
        width: 150
      },
      {
        key: 'description',
        label: t('common.description'),
        showOverflowTooltip: true
      },
      {
        key: 'permissions',
        label: t('pages.roles.permissions'),
        formatter: (value) => `${value?.length || 0} ${t('pages.roles.permissionCount')}`
      },
      {
        key: 'is_active',
        label: t('pages.roles.status'),
        type: 'status',
        width: 80,
        formatter: (value) => value ? t('common.active') : t('common.inactive')
      },
      {
        key: 'created_at',
        label: t('common.createdAt'),
        type: 'datetime',
        sortable: true,
        width: 200
      }
    ],
    
    actions: [
      {
        key: 'edit',
        label: t('pages.roles.editRole'), // 更改为更明确的标签
        icon: 'Edit',
        type: 'primary',
        size: 'small',
        permission: 'role:update'
      },
      {
        key: 'delete',
        label: t('common.delete'),
        icon: 'Delete',
        type: 'danger',
        size: 'small',
        permission: 'role:delete',
        confirm: t('pages.roles.deleteConfirm')
      }
    ],
    
    pagination: {
      pageSizes: [10, 20, 50, 100],
      defaultPageSize: 20
    }
  }
}

// 系统配置表格配置
export function createSystemConfigTableConfig(t) {
  
  return {
    title: t('pages.systemConfigs.title'),
    description: t('pages.systemConfigs.description'),
    icon: 'Setting',
    
    toolbar: {
      search: {
        enabled: true,
        placeholder: t('pages.systemConfigs.searchPlaceholder')
      },
      filters: [
        {
          key: 'data_type',
          type: 'select',
          placeholder: t('pages.systemConfigs.filterByDataType'),
          options: [
            { label: 'string', value: 'string' },
            { label: 'number', value: 'number' },
            { label: 'boolean', value: 'boolean' },
            { label: 'json', value: 'json' }
          ]
        },
        {
          key: 'is_active',
          type: 'select',
          placeholder: t('pages.systemConfigs.filterByStatus'),
          options: [
            { label: t('common.active'), value: true },
            { label: t('common.inactive'), value: false }
          ]
        }
      ],
      actions: [
        {
          key: 'add',
          label: t('pages.systemConfigs.addConfig'),
          icon: 'Plus',
          type: 'primary',
          permission: 'system:config_create'
        }
      ]
    },
    
    statistics: [
      {
        key: 'total',
        label: t('pages.systemConfigs.totalConfigs'),
        icon: Setting,
        color: 'blue'
      },
      {
        key: 'active',
        label: t('pages.systemConfigs.activeConfigs'),
        icon: CircleCheck,
        color: 'green'
      },
      {
        key: 'system',
        label: t('pages.systemConfigs.systemConfigs'),
        icon: Lock,
        color: 'orange'
      },
      {
        key: 'by_type',
        label: t('pages.systemConfigs.dataTypes'),
        icon: Grid,
        color: 'purple',
        formatter: (value) => Object.keys(value || {}).length
      }
    ],
    
    columns: [
      {
        key: 'key',
        label: t('pages.systemConfigs.configKey'),
        sortable: true,
        width: 200
      },
      {
        key: 'value',
        label: t('pages.systemConfigs.configValue'),
        width: 300,
        showOverflowTooltip: true
      },
      {
        key: 'description',
        label: t('common.description'),
        showOverflowTooltip: true
      },
      {
        key: 'data_type',
        label: t('pages.systemConfigs.dataType'),
        type: 'tags',
        width: 100,
        formatter: (value) => [value]
      },
      {
        key: 'is_active',
        label: t('pages.systemConfigs.status'),
        type: 'status',
        width: 80,
        formatter: (value) => value ? t('common.active') : t('common.inactive')
      },
      {
        key: 'is_system',
        label: t('pages.systemConfigs.isSystem'),
        type: 'boolean',
        width: 100
      },
      {
        key: 'created_at',
        label: t('common.createdAt'),
        type: 'datetime',
        sortable: true,
        width: 180
      }
    ],
    
    actions: [
      {
        key: 'edit',
        label: t('common.edit'),
        icon: 'Edit',
        type: 'primary',
        size: 'small',
        permission: 'system:config_update'
      },
      {
        key: 'delete',
        label: t('common.delete'),
        icon: 'Delete',
        type: 'danger',
        size: 'small',
        permission: 'system:config_delete',
        confirm: t('pages.systemConfigs.deleteConfirm')
      }
    ],
    
    pagination: {
      pageSizes: [10, 20, 50, 100],
      defaultPageSize: 20
    }
  }
}

// 通知配置表格配置
export function createNotificationTableConfig(t) {

  return {
    title: t('pages.notificationClients.title'),
    description: t('pages.notificationClients.description'),
    icon: 'Bell',

    toolbar: {
      search: {
        enabled: true,
        placeholder: t('pages.notificationClients.searchPlaceholder')
      },
      filters: [
        {
          key: 'type',
          type: 'select',
          placeholder: t('pages.notificationClients.filterByType'),
          options: [] // 动态加载
        },
        {
          key: 'enabled',
          type: 'select',
          placeholder: t('pages.notificationClients.filterByStatus'),
          options: [
            { label: t('common.enabled'), value: true },
            { label: t('common.disabled'), value: false }
          ]
        }
      ],
      actions: [
        {
          key: 'add',
          label: t('pages.notificationClients.addClient'),
          icon: 'Plus',
          type: 'primary',
          permission: 'notification:create'
        }
      ]
    },

    statistics: [
      {
        key: 'total',
        label: t('pages.notificationClients.totalClients'),
        icon: Bell,
        color: 'blue'
      },
      {
        key: 'enabled',
        label: t('pages.notificationClients.enabledClients'),
        icon: CircleCheck,
        color: 'green'
      },
      {
        key: 'by_type',
        label: t('pages.notificationClients.clientTypes'),
        icon: Grid,
        color: 'orange',
        formatter: (value) => Object.keys(value || {}).length
      },
      {
        key: 'interactive',
        label: t('pages.notificationClients.interactiveClients'),
        icon: Bell,
        color: 'purple'
      }
    ],

    columns: [
      {
        key: 'name',
        label: t('pages.notificationClients.clientName'),
        sortable: true,
        width: 150
      },
      {
        key: 'type',
        label: t('pages.notificationClients.clientType'),
        type: 'tags',
        width: 120,
        formatter: (value) => [value]
      },
      {
        key: 'enabled',
        label: t('pages.notificationClients.status'),
        type: 'status',
        width: 80,
        formatter: (value) => value ? t('common.enabled') : t('common.disabled')
      },
      {
        key: 'interactive',
        label: t('pages.notificationClients.interactive'),
        type: 'boolean',
        width: 100
      },
      {
        key: 'switches',
        label: t('pages.notificationClients.scenarios'),
        type: 'tags',
        formatter: (value) => {
          if (!value || typeof value !== 'object') return []
          return Object.entries(value)
            .filter(([_, enabled]) => enabled)
            .map(([scenario, _]) => scenario)
        }
      },
      {
        key: 'created_at',
        label: t('common.createdAt'),
        type: 'datetime',
        sortable: true,
        width: 180
      }
    ],

    actions: [
      {
        key: 'test',
        label: t('pages.notificationClients.testClient'),
        icon: 'Play',
        type: 'warning',
        size: 'small',
        permission: 'notification:test'
      },
      {
        key: 'edit',
        label: t('common.edit'),
        icon: 'Edit',
        type: 'primary',
        size: 'small',
        permission: 'notification:update'
      },
      {
        key: 'delete',
        label: t('common.delete'),
        icon: 'Delete',
        type: 'danger',
        size: 'small',
        permission: 'notification:delete',
        confirm: t('pages.notificationClients.deleteConfirm')
      }
    ],

    pagination: {
      pageSizes: [10, 20, 50, 100],
      defaultPageSize: 20
    }
  }
}
