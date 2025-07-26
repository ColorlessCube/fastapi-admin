export default {
  // 通用
  common: {
    confirm: '确定',
    cancel: '取消',
    save: '保存',
    edit: '编辑',
    delete: '删除',
    add: '添加',
    search: '搜索',
    loading: '加载中...',
    success: '成功',
    error: '错误',
    warning: '警告',
    info: '信息',
    yes: '是',
    no: '否',
    active: '激活',
    inactive: '禁用',
    operation: '操作',
    refresh: '刷新',
    back: '返回',
    next: '下一步',
    previous: '上一步',
    submit: '提交',
    reset: '重置',
    close: '关闭',
    system: '管理系统',
    welcome: '欢迎使用管理系统',
    user: '用户',
    pleaseSelect: '请选择'
  },

  // 导航和菜单
  nav: {
    dashboard: '仪表盘',
    systemManagement: '系统管理',
    userManagement: '用户管理',
    roleManagement: '角色管理',
    systemConfigs: '系统配置',
    logout: '退出登录',
    profile: '个人资料'
  },

  // 页面标题和描述
  pages: {
    dashboard: {
      title: '仪表盘',
      description: '系统概览和关键指标',
      welcome: '欢迎回来！',
      welcomeDesc: '这里是您的管理仪表盘，您可以查看系统概览和关键指标。',
      quickActions: '快速操作',
      quickActionsDesc: '常用功能快速入口',
      systemInfo: '系统信息',
      version: '系统版本',
      backend: '后端框架',
      frontend: '前端框架',
      database: '数据库',
      auth: '认证方式',
      systemVersion: '系统版本',
      currentVersion: '当前版本',
      systemUptime: '运行时间',
      runningTime: '系统运行时间',
      systemStatus: '系统状态',
      serviceHealth: '服务健康状态',
      lastUpdate: '最后更新',
      systemUpdate: '系统更新时间',
      techStack: '技术栈',
      environmentInfo: '环境信息',
      browserInfo: '浏览器',
      screenResolution: '屏幕分辨率',
      language: '语言',
      timezone: '时区',
      onlineTime: '在线时长',
      lastLogin: '最后登录',
      loginCount: '登录次数',
      refreshPage: '刷新页面',
      clearCache: '清除缓存',
      exportData: '导出数据',
      viewLogs: '查看日志',
      cacheCleared: '缓存已清除',
      dataExported: '数据已导出',
      logsInConsole: '日志已输出到控制台',
      security: '安全认证'
    },
    users: {
      title: '用户管理',
      description: '管理系统用户账号和权限分配',
      userList: '用户列表',
      addUser: '添加用户',
      editUser: '编辑用户',
      deleteUser: '删除用户',
      username: '用户名',
      email: '邮箱',
      fullName: '姓名',
      password: '密码',
      roles: '角色',
      status: '状态',
      activeUsers: '活跃用户',
      createdAt: '创建时间',
      updatedAt: '更新时间',
      noRoles: '无角色',
      preferences: '偏好设置',
      preferredLanguage: '首选语言',
      timezone: '时区',
      selectTimezone: '请选择时区'
    },
    roles: {
      title: '角色管理',
      description: '管理系统角色和权限配置',
      roleList: '角色列表',
      addRole: '添加角色',
      editRole: '编辑角色',
      deleteRole: '删除角色',
      roleName: '角色名称',
      roleDescription: '角色描述',
      permissions: '权限',
      assignPermissions: '分配权限',
      permissionAssignment: '权限分配',
      permissionGroups: '权限分组',
      savePermissions: '保存权限',
      permissionCount: '个权限',
      assignPermissionsTo: '为角色 "{roleName}" 分配权限',
      selectPermissions: '选择该角色可以访问的页面和功能'
    },
    login: {
      title: 'FastAPI Admin',
      subtitle: '现代化管理系统',
      username: '请输入用户名',
      password: '请输入密码',
      loginBtn: '立即登录',
      loggingIn: '登录中...',
      demoAccounts: '演示账号：',
      adminAccount: '管理员: admin / admin123',
      userAccount: '普通用户: user / user123'
    },
    systemConfigs: {
      title: '系统配置',
      description: '管理系统运行时配置参数',
      configList: '配置列表',
      addConfig: '添加配置',
      editConfig: '编辑配置',
      configKey: '配置键',
      configValue: '配置值',
      dataType: '数据类型',
      isSystem: '系统配置',
      jsonPlaceholder: '请输入有效的JSON格式数据'
    },
    profile: {
      title: '个人资料',
      description: '管理您的个人信息和偏好设置',
      basicInfo: '基本信息',
      preferences: '偏好设置',
      changePassword: '修改密码',
      loginHistory: '登录历史',
      language: '首选语言',
      timezone: '时区',
      selectTimezone: '请选择时区',
      currentPassword: '当前密码',
      newPassword: '新密码',
      confirmPassword: '确认密码',
      enterCurrentPassword: '请输入当前密码',
      enterNewPassword: '请输入新密码',
      confirmNewPassword: '请确认新密码',
      lastLogin: '最后登录',
      loginCount: '登录次数',
      lastLoginIP: '最后登录IP',
      accountCreated: '账户创建时间'
    }
  },

  // 统计信息
  stats: {
    totalUsers: '总用户数',
    totalRoles: '角色数量',
    totalPermissions: '权限数量',
    activeUsers: '活跃用户'
  },

  // 表单验证
  validation: {
    required: '此字段为必填项',
    email: '请输入有效的邮箱地址',
    minLength: '长度不能少于 {min} 个字符',
    maxLength: '长度不能超过 {max} 个字符'
  },

  // 消息提示
  messages: {
    loginSuccess: '登录成功',
    loginFailed: '登录失败，请检查用户名和密码',
    logoutConfirm: '确定要退出登录吗？',
    logoutSuccess: '已退出登录',
    deleteConfirm: '确定要删除{type} "{name}" 吗？',
    deleteSuccess: '删除成功',
    deleteFailed: '删除失败',
    saveSuccess: '保存成功',
    saveFailed: '保存失败',
    updateSuccess: '更新成功',
    updateFailed: '更新失败',
    createSuccess: '创建成功',
    createFailed: '创建失败',
    loadFailed: '加载失败',
    profileUpdateSuccess: '个人资料更新成功',
    profileUpdateFailed: '更新失败，请重试',
    permissionAssignSuccess: '权限分配成功',
    permissionAssignFailed: '权限分配失败',
    cannotDeleteSelf: '无法删除自己',
    hasUsersAssociated: '有用户关联的角色无法删除',
    languageChanged: '语言切换成功',
    preferencesUpdated: '偏好设置更新成功',
    passwordChanged: '密码修改成功',
    currentPasswordIncorrect: '当前密码不正确',
    passwordChangeFailed: '密码修改失败'
  },

  // 表单验证
  validation: {
    emailRequired: '请输入邮箱',
    emailInvalid: '邮箱格式不正确',
    currentPasswordRequired: '请输入当前密码',
    newPasswordRequired: '请输入新密码',
    passwordMinLength: '密码长度至少6位',
    confirmPasswordRequired: '请确认新密码',
    passwordMismatch: '两次输入的密码不一致'
  },

  // 权限相关
  permissions: {
    dashboard: {
      read: '查看仪表盘'
    },
    user: {
      read: '查看用户列表',
      create: '创建用户',
      update: '更新用户',
      delete: '删除用户'
    },
    role: {
      read: '查看角色列表',
      create: '创建角色',
      update: '更新角色',
      delete: '删除角色',
      assignPermission: '分配角色权限'
    },
    permission: {
      read: '查看权限列表',
      create: '创建权限',
      update: '更新权限',
      delete: '删除权限'
    },
    system: {
      settings: '系统设置',
      logs: '查看系统日志'
    }
  }
}
