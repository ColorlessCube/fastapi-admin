export default {
  // Common
  common: {
    confirm: 'Confirm',
    cancel: 'Cancel',
    save: 'Save',
    edit: 'Edit',
    delete: 'Delete',
    add: 'Add',
    search: 'Search',
    loading: 'Loading...',
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Info',
    yes: 'Yes',
    no: 'No',
    active: 'Active',
    inactive: 'Inactive',
    operation: 'Operation',
    refresh: 'Refresh',
    back: 'Back',
    next: 'Next',
    previous: 'Previous',
    submit: 'Submit',
    reset: 'Reset',
    close: 'Close',
    system: 'Management System',
    welcome: 'Welcome to Management System',
    user: 'User',
    pleaseSelect: 'Please select'
  },

  // Navigation and Menu
  nav: {
    dashboard: 'Dashboard',
    systemManagement: 'System Management',
    userManagement: 'User Management',
    roleManagement: 'Role Management',
    systemConfigs: 'System Configs',
    logout: 'Logout',
    profile: 'Profile'
  },

  // Page titles and descriptions
  pages: {
    dashboard: {
      title: 'Dashboard',
      description: 'System overview and key metrics',
      welcome: 'Welcome back!',
      welcomeDesc: 'This is your management dashboard where you can view system overview and key metrics.',
      quickActions: 'Quick Actions',
      quickActionsDesc: 'Quick access to common functions',
      systemInfo: 'System Information',
      version: 'System Version',
      backend: 'Backend Framework',
      frontend: 'Frontend Framework',
      database: 'Database',
      auth: 'Authentication',
      systemVersion: 'System Version',
      currentVersion: 'Current Version',
      systemUptime: 'System Uptime',
      runningTime: 'Running Time',
      systemStatus: 'System Status',
      serviceHealth: 'Service Health',
      lastUpdate: 'Last Update',
      systemUpdate: 'System Update Time',
      techStack: 'Technology Stack',
      environmentInfo: 'Environment Info',
      browserInfo: 'Browser',
      screenResolution: 'Screen Resolution',
      language: 'Language',
      timezone: 'Timezone',
      onlineTime: 'Online Time',
      lastLogin: 'Last Login',
      loginCount: 'Login Count',
      refreshPage: 'Refresh Page',
      clearCache: 'Clear Cache',
      exportData: 'Export Data',
      viewLogs: 'View Logs',
      cacheCleared: 'Cache cleared successfully',
      dataExported: 'Data exported successfully',
      logsInConsole: 'Logs output to console',
      security: 'Security'
    },
    users: {
      title: 'User Management',
      description: 'Manage system user accounts and permission assignments',
      userList: 'User List',
      addUser: 'Add User',
      editUser: 'Edit User',
      deleteUser: 'Delete User',
      username: 'Username',
      email: 'Email',
      fullName: 'Full Name',
      password: 'Password',
      roles: 'Roles',
      status: 'Status',
      activeUsers: 'Active Users',
      createdAt: 'Created At',
      updatedAt: 'Updated At',
      noRoles: 'No Roles',
      preferences: 'Preferences',
      preferredLanguage: 'Preferred Language',
      timezone: 'Timezone',
      selectTimezone: 'Please select timezone'
    },
    roles: {
      title: 'Role Management',
      description: 'Manage system roles and permission configurations',
      roleList: 'Role List',
      addRole: 'Add Role',
      editRole: 'Edit Role',
      deleteRole: 'Delete Role',
      roleName: 'Role Name',
      roleDescription: 'Role Description',
      permissions: 'Permissions',
      assignPermissions: 'Assign Permissions',
      permissionAssignment: 'Permission Assignment',
      permissionGroups: 'Permission Groups',
      savePermissions: 'Save Permissions',
      permissionCount: 'permissions',
      assignPermissionsTo: 'Assign permissions to role "{roleName}"',
      selectPermissions: 'Select pages and functions this role can access'
    },
    login: {
      title: 'FastAPI Admin',
      subtitle: 'Modern Management System',
      username: 'Please enter username',
      password: 'Please enter password',
      loginBtn: 'Login Now',
      loggingIn: 'Logging in...',
      demoAccounts: 'Demo Accounts:',
      adminAccount: 'Admin: admin / admin123',
      userAccount: 'User: user / user123'
    },
    systemConfigs: {
      title: 'System Configs',
      description: 'Manage system runtime configuration parameters',
      configList: 'Config List',
      addConfig: 'Add Config',
      editConfig: 'Edit Config',
      configKey: 'Config Key',
      configValue: 'Config Value',
      dataType: 'Data Type',
      isSystem: 'System Config',
      jsonPlaceholder: 'Please enter valid JSON format data'
    },
    profile: {
      title: 'Profile',
      description: 'Manage your personal information and preferences',
      basicInfo: 'Basic Information',
      preferences: 'Preferences',
      changePassword: 'Change Password',
      loginHistory: 'Login History',
      language: 'Preferred Language',
      timezone: 'Timezone',
      selectTimezone: 'Please select timezone',
      currentPassword: 'Current Password',
      newPassword: 'New Password',
      confirmPassword: 'Confirm Password',
      enterCurrentPassword: 'Please enter current password',
      enterNewPassword: 'Please enter new password',
      confirmNewPassword: 'Please confirm new password',
      lastLogin: 'Last Login',
      loginCount: 'Login Count',
      lastLoginIP: 'Last Login IP',
      accountCreated: 'Account Created'
    }
  },

  // Statistics
  stats: {
    totalUsers: 'Total Users',
    totalRoles: 'Total Roles',
    totalPermissions: 'Total Permissions',
    activeUsers: 'Active Users'
  },

  // Form validation
  validation: {
    required: 'This field is required',
    email: 'Please enter a valid email address',
    minLength: 'Length cannot be less than {min} characters',
    maxLength: 'Length cannot exceed {max} characters'
  },

  // Messages
  messages: {
    loginSuccess: 'Login successful',
    loginFailed: 'Login failed, please check username and password',
    logoutConfirm: 'Are you sure you want to logout?',
    logoutSuccess: 'Logged out successfully',
    deleteConfirm: 'Are you sure you want to delete {type} "{name}"?',
    deleteSuccess: 'Deleted successfully',
    deleteFailed: 'Delete failed',
    saveSuccess: 'Saved successfully',
    saveFailed: 'Save failed',
    updateSuccess: 'Updated successfully',
    updateFailed: 'Update failed',
    createSuccess: 'Created successfully',
    createFailed: 'Create failed',
    loadFailed: 'Load failed',
    profileUpdateSuccess: 'Profile updated successfully',
    profileUpdateFailed: 'Update failed, please try again',
    permissionAssignSuccess: 'Permissions assigned successfully',
    permissionAssignFailed: 'Permission assignment failed',
    cannotDeleteSelf: 'Cannot delete yourself',
    hasUsersAssociated: 'Roles with associated users cannot be deleted',
    languageChanged: 'Language changed successfully',
    preferencesUpdated: 'Preferences updated successfully',
    passwordChanged: 'Password changed successfully',
    currentPasswordIncorrect: 'Current password is incorrect',
    passwordChangeFailed: 'Failed to change password'
  },

  // Form validation
  validation: {
    emailRequired: 'Please enter email',
    emailInvalid: 'Invalid email format',
    currentPasswordRequired: 'Please enter current password',
    newPasswordRequired: 'Please enter new password',
    passwordMinLength: 'Password must be at least 6 characters',
    confirmPasswordRequired: 'Please confirm new password',
    passwordMismatch: 'Passwords do not match'
  },

  // Permissions
  permissions: {
    dashboard: {
      read: 'View Dashboard'
    },
    user: {
      read: 'View User List',
      create: 'Create User',
      update: 'Update User',
      delete: 'Delete User'
    },
    role: {
      read: 'View Role List',
      create: 'Create Role',
      update: 'Update Role',
      delete: 'Delete Role',
      assignPermission: 'Assign Role Permissions'
    },
    permission: {
      read: 'View Permission List',
      create: 'Create Permission',
      update: 'Update Permission',
      delete: 'Delete Permission'
    },
    system: {
      settings: 'System Settings',
      logs: 'View System Logs'
    }
  }
}
