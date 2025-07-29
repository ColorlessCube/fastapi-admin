import {
  User,
  Operation,
  Setting,
  Bell,
  UserFilled
} from '@element-plus/icons-vue'

// 创建用户表单配置的函数
export const createUserFormConfig = (t) => ({
  icon: User,
  width: '600px',
  title: (mode) => mode === 'add' ? t('pages.users.addUser') : t('pages.users.editUser'),
  description: t('pages.users.formDescription'),
  footerNote: t('pages.users.formNote'),
  fields: [
    {
      field: 'username',
      type: 'input',
      label: t('pages.users.username'),
      required: true,
      placeholder: t('pages.users.usernamePlaceholder'),
      rules: [
        { required: true, message: t('pages.users.usernameRequired'), trigger: 'blur' },
        { min: 3, max: 20, message: t('pages.users.usernameLength'), trigger: 'blur' }
      ]
    },
    {
      field: 'email',
      type: 'input',
      label: t('pages.users.email'),
      required: true,
      placeholder: t('pages.users.emailPlaceholder'),
      rules: [
        { required: true, message: t('pages.users.emailRequired'), trigger: 'blur' },
        { type: 'email', message: t('pages.users.emailFormat'), trigger: 'blur' }
      ]
    },
    {
      field: 'fullName',
      type: 'input',
      label: t('pages.users.fullName'),
      required: true,
      placeholder: t('pages.users.fullNamePlaceholder'),
      rules: [
        { required: true, message: t('pages.users.fullNameRequired'), trigger: 'blur' }
      ]
    },
    {
      field: 'password',
      type: 'input',
      label: t('pages.users.password'),
      required: true,
      placeholder: t('pages.users.passwordPlaceholder'),
      visible: (formData, mode) => mode === 'add', // 只在添加模式显示
      props: {
        type: 'password',
        showPassword: true
      },
      rules: [
        { required: true, message: t('pages.users.passwordRequired'), trigger: 'blur' },
        { min: 6, message: t('pages.users.passwordLength'), trigger: 'blur' }
      ]
    },
    {
      field: 'roleIds',
      type: 'select',
      label: t('pages.users.roles'),
      placeholder: t('pages.users.selectRoles'),
      props: {
        multiple: true,
        clearable: true
      },
      options: (formData, mode) => {
        // 这里可以从外部传入或者通过API获取
        return []
      }
    },
    {
      field: 'isActive',
      type: 'switch',
      label: t('pages.users.status'),
      props: {
        activeText: t('common.active'),
        inactiveText: t('common.inactive')
      }
    }
  ]
})

// 创建角色表单配置的函数
export const createRoleFormConfig = (t) => ({
  icon: Operation,
  width: '900px', // 增加宽度以容纳权限树
  title: (mode) => mode === 'add' ? t('pages.roles.addRole') : t('pages.roles.editRole'),
  description: t('pages.roles.formDescription'),
  footerNote: t('pages.roles.formNote'),
  fields: [
    {
      field: 'name',
      type: 'input',
      label: t('pages.roles.roleName'),
      required: true,
      placeholder: t('pages.roles.roleNamePlaceholder'),
      rules: [
        { required: true, message: t('pages.roles.roleNameRequired'), trigger: 'blur' },
        { min: 2, max: 50, message: t('pages.roles.roleNameLength'), trigger: 'blur' }
      ]
    },
    {
      field: 'description',
      type: 'textarea',
      label: t('common.description'),
      placeholder: t('pages.roles.descriptionPlaceholder'),
      props: {
        rows: 3,
        maxlength: 200,
        showWordLimit: true
      }
    },
    {
      field: 'isActive',
      type: 'switch',
      label: t('pages.roles.status'),
      props: {
        activeText: t('common.active'),
        inactiveText: t('common.inactive')
      }
    },
    {
      field: 'permissions',
      type: 'slot',
      label: t('pages.roles.permissions'),
      fullWidth: true
      // 在添加和编辑模式下都显示
    }
  ]
})

// 创建系统配置表单配置的函数
export const createSystemConfigFormConfig = (t) => ({
  icon: Setting,
  width: '700px',
  title: (mode) => mode === 'add' ? t('pages.systemConfigs.addConfig') : t('pages.systemConfigs.editConfig'),
  description: t('pages.systemConfigs.formDescription'),
  footerNote: t('pages.systemConfigs.formNote'),
  fields: [
    {
      field: 'key',
      type: 'input',
      label: t('pages.systemConfigs.configKey'),
      required: true,
      placeholder: t('pages.systemConfigs.configKeyPlaceholder'),
      rules: [
        { required: true, message: t('pages.systemConfigs.configKeyRequired'), trigger: 'blur' },
        { min: 2, max: 100, message: t('pages.systemConfigs.configKeyLength'), trigger: 'blur' }
      ]
    },
    {
      field: 'value',
      type: 'textarea',
      label: t('pages.systemConfigs.configValue'),
      required: true,
      placeholder: t('pages.systemConfigs.configValuePlaceholder'),
      props: {
        rows: 3,
        maxlength: 1000,
        showWordLimit: true
      },
      rules: [
        { required: true, message: t('pages.systemConfigs.configValueRequired'), trigger: 'blur' }
      ]
    },
    {
      field: 'description',
      type: 'textarea',
      label: t('common.description'),
      placeholder: t('pages.systemConfigs.descriptionPlaceholder'),
      props: {
        rows: 2,
        maxlength: 500,
        showWordLimit: true
      }
    },
    {
      field: 'data_type',
      type: 'select',
      label: t('pages.systemConfigs.dataType'),
      required: true,
      placeholder: t('pages.systemConfigs.dataTypePlaceholder'),
      options: [
        { label: 'String', value: 'string' },
        { label: 'Number', value: 'number' },
        { label: 'Boolean', value: 'boolean' },
        { label: 'JSON', value: 'json' }
      ],
      rules: [
        { required: true, message: t('pages.systemConfigs.dataTypeRequired'), trigger: 'change' }
      ]
    },
    {
      field: 'is_system',
      type: 'switch',
      label: t('pages.systemConfigs.isSystem'),
      props: {
        activeText: t('common.yes'),
        inactiveText: t('common.no')
      }
    },
    {
      field: 'is_active',
      type: 'switch',
      label: t('common.status'),
      props: {
        activeText: t('common.active'),
        inactiveText: t('common.inactive')
      }
    }
  ]
})

// 创建通知客户端表单配置的函数
export const createNotificationClientFormConfig = (t) => ({
  icon: Bell,
  width: '800px',
  title: (mode) => mode === 'add' ? t('pages.notificationClients.addClient') : t('pages.notificationClients.editClient'),
  description: t('pages.notificationClients.formDescription'),
  footerNote: t('pages.notificationClients.formNote'),
  fields: [
    {
      field: 'name',
      type: 'input',
      label: t('pages.notificationClients.clientName'),
      required: true,
      placeholder: t('pages.notificationClients.clientNamePlaceholder'),
      rules: [
        { required: true, message: t('pages.notificationClients.clientNameRequired'), trigger: 'blur' },
        { min: 2, max: 100, message: t('pages.notificationClients.clientNameLength'), trigger: 'blur' }
      ]
    },
    {
      field: 'type',
      type: 'select',
      label: t('pages.notificationClients.notificationType'),
      required: true,
      placeholder: t('pages.notificationClients.notificationTypePlaceholder'),
      options: [
        { label: t('pages.notificationClients.typeEmail'), value: 'email' },
        { label: t('pages.notificationClients.typeSms'), value: 'sms' },
        { label: t('pages.notificationClients.typePush'), value: 'push' },
        { label: t('pages.notificationClients.typeWebhook'), value: 'webhook' }
      ],
      rules: [
        { required: true, message: t('pages.notificationClients.notificationTypeRequired'), trigger: 'change' }
      ]
    },
    {
      field: 'description',
      type: 'textarea',
      label: t('common.description'),
      placeholder: t('pages.notificationClients.descriptionPlaceholder'),
      props: {
        rows: 3,
        maxlength: 500,
        showWordLimit: true
      }
    },
    {
      field: 'config',
      type: 'textarea',
      label: t('pages.notificationClients.configuration'),
      placeholder: t('pages.notificationClients.configurationPlaceholder'),
      props: {
        rows: 4,
        maxlength: 2000,
        showWordLimit: true
      }
    },
    {
      field: 'enabled',
      type: 'switch',
      label: t('common.status'),
      props: {
        activeText: t('common.enabled'),
        inactiveText: t('common.disabled')
      }
    },
    {
      field: 'interactive',
      type: 'switch',
      label: t('pages.notificationClients.supportsInteraction'),
      props: {
        activeText: t('common.yes'),
        inactiveText: t('common.no')
      }
    },
    {
      field: 'switches',
      type: 'checkbox-group',
      label: t('pages.notificationClients.scenarios'),
      options: [
        { label: t('pages.notificationClients.scenarioLogin'), value: 'login' },
        { label: t('pages.notificationClients.scenarioRegister'), value: 'register' },
        { label: t('pages.notificationClients.scenarioPasswordReset'), value: 'password_reset' },
        { label: t('pages.notificationClients.scenarioSystemAlert'), value: 'system_alert' },
        { label: t('pages.notificationClients.scenarioUserAction'), value: 'user_action' }
      ]
    }
  ]
})

// 创建权限管理表单配置的函数
export const createPermissionFormConfig = (t, roleName) => ({
  icon: UserFilled,
  width: '900px',
  title: roleName,
  description: t('pages.roles.permissionDescription'),
  footerNote: t('pages.roles.permissionChangeNote'),
  submitText: t('common.confirm'),
  cancelText: t('common.cancel'),
  fields: [
    {
      field: 'permissionTree',
      type: 'slot',
      label: '', // 移除标签文字
      fullWidth: true // 撑满容器
    }
  ]
})

// 获取表单配置的辅助函数
export function getFormConfig(type, t) {
  const configCreators = {
    users: createUserFormConfig,
    roles: createRoleFormConfig,
    systemConfigs: createSystemConfigFormConfig,
    notificationClients: createNotificationClientFormConfig,
    permissions: createPermissionFormConfig
  }

  const creator = configCreators[type]
  return creator ? creator(t) : null
}

// 创建默认表单数据的辅助函数
export function createDefaultFormData(config) {
  const defaultData = {}
  
  config.fields?.forEach(field => {
    switch (field.type) {
      case 'switch':
        defaultData[field.field] = field.props?.defaultValue ?? true
        break
      case 'checkbox-group':
        defaultData[field.field] = []
        break
      case 'select':
        if (field.props?.multiple) {
          defaultData[field.field] = []
        } else {
          defaultData[field.field] = field.props?.defaultValue ?? ''
        }
        break
      case 'number':
        defaultData[field.field] = field.props?.defaultValue ?? 0
        break
      default:
        defaultData[field.field] = field.props?.defaultValue ?? ''
    }
  })
  
  return defaultData
}
