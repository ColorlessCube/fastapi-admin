<template>
  <div class="admin-layout">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="sidebarWidth" class="sidebar-container">
        <div class="logo" @click="toggleSidebar">
          <div class="logo-icon">
            <el-icon><Grid /></el-icon>
          </div>
          <div class="logo-text" v-show="!sidebarCollapsed">
            <h3>FastAPI Admin</h3>
            <span>{{ $t('common.system') }}</span>
          </div>
        </div>
        <el-menu
          :default-active="$route.path"
          :default-openeds="defaultOpeneds"
          :collapse="sidebarCollapsed"
          router
          background-color="transparent"
          text-color="var(--sidebar-text)"
          active-text-color="var(--sidebar-text-active)"
        >
          <!-- 仪表盘 - 一级菜单 -->
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>{{ $t('nav.dashboard') }}</span>
          </el-menu-item>

          <!-- 系统管理 - 二级菜单 -->
          <el-sub-menu index="system" v-if="hasSystemMenuAccess">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span>{{ $t('nav.systemManagement') }}</span>
            </template>
            <el-menu-item index="/users" v-if="canAccessPage('users')">
              <el-icon><User /></el-icon>
              <span>{{ $t('nav.userManagement') }}</span>
            </el-menu-item>
            <el-menu-item index="/roles" v-if="canAccessPage('roles')">
              <el-icon><UserFilled /></el-icon>
              <span>{{ $t('nav.roleManagement') }}</span>
            </el-menu-item>
            <el-menu-item index="/system-configs" v-if="canAccessPage('system-configs')">
              <el-icon><Setting /></el-icon>
              <span>{{ $t('nav.systemConfigs') }}</span>
            </el-menu-item>
            <el-menu-item index="/notification-clients" v-if="canAccessPage('notification-clients')">
              <el-icon><Bell /></el-icon>
              <span>{{ $t('nav.notificationClients') }}</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header>
          <div class="header-content">
            <div class="header-left">
              <div class="breadcrumb-container">
                <el-icon class="breadcrumb-icon"><Location /></el-icon>
                <div class="breadcrumb-content">
                  <div class="breadcrumb-path">
                    <span class="breadcrumb-item" v-if="breadcrumbItems.length > 1">
                      {{ breadcrumbItems[0] }}
                    </span>
                    <el-icon v-if="breadcrumbItems.length > 1" class="breadcrumb-separator">
                      <ArrowRight />
                    </el-icon>
                    <span class="breadcrumb-current">
                      {{ breadcrumbItems[breadcrumbItems.length - 1] }}
                    </span>
                  </div>
                  <div class="breadcrumb-description">
                    {{ pageDescription }}
                  </div>
                </div>
              </div>
            </div>
            <div class="header-right">
              <div class="header-actions">
                <div class="notification-btn">
                  <el-icon><Bell /></el-icon>
                </div>
                <el-dropdown @command="handleLanguageChange" class="language-dropdown">
                  <div class="language-btn">
                    <el-icon><Operation /></el-icon>
                    <span>{{ currentLanguage.label }}</span>
                    <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
                  </div>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item
                        v-for="lang in supportedLanguages"
                        :key="lang.value"
                        :command="lang.value"
                        :class="{ 'is-active': currentLocale === lang.value }"
                      >
                        {{ lang.label }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
                <el-dropdown @command="handleCommand" class="user-dropdown">
                  <div class="user-info">
                    <el-avatar :size="40" class="user-avatar" :src="userInfo.avatar">
                      <el-icon><User /></el-icon>
                    </el-avatar>
                    <div class="user-details">
                      <span class="user-name">{{ userInfo.full_name || userInfo.username }}</span>
                      <span class="user-role">{{ $t('common.user') }}</span>
                    </div>
                    <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
                  </div>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="profile">
                        <el-icon><User /></el-icon>
                        {{ $t('nav.profile') }}
                      </el-dropdown-item>
                      <el-dropdown-item divided command="logout">
                        <el-icon><SwitchButton /></el-icon>
                        {{ $t('nav.logout') }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
        </el-header>

        <!-- 主要内容 -->
        <el-main>
          <div class="page-content">
            <slot />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { setLocale, getLocale, getSupportedLocales } from '../i18n'
import { usePermissions } from '../utils/permissions'

export default {
  name: 'AdminLayout',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const { t } = useI18n()
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))

    // 侧边栏状态管理
    const sidebarCollapsed = ref(localStorage.getItem('sidebarCollapsed') === 'true')
    const sidebarWidth = computed(() => sidebarCollapsed.value ? '100px' : '280px')

    // 权限管理
    const { hasPermission, canAccessPage, initPermissions } = usePermissions()

    // 权限加载状态
    const permissionsLoaded = ref(false)

    // 国际化相关
    const currentLocale = ref(getLocale())
    const supportedLanguages = getSupportedLocales()
    const currentLanguage = computed(() => {
      return supportedLanguages.find(lang => lang.value === currentLocale.value) || supportedLanguages[0]
    })

    // 默认展开的菜单
    const defaultOpeneds = ref(['system'])

    // 页面配置 - 使用国际化
    const pageTitle = computed(() => {
      const pathMap = {
        '/': 'pages.dashboard.title',
        '/users': 'pages.users.title',
        '/roles': 'pages.roles.title',
        '/system-configs': 'pages.systemConfigs.title'
      }
      return t(pathMap[route.path] || 'common.system')
    })

    const pageDescription = computed(() => {
      const pathMap = {
        '/': 'pages.dashboard.description',
        '/users': 'pages.users.description',
        '/roles': 'pages.roles.description',
        '/system-configs': 'pages.systemConfigs.description'
      }
      return t(pathMap[route.path] || 'common.welcome')
    })

    const breadcrumbItems = computed(() => {
      const pathMap = {
        '/': [t('nav.dashboard')],
        '/users': [t('nav.systemManagement'), t('nav.userManagement')],
        '/roles': [t('nav.systemManagement'), t('nav.roleManagement')],
        '/system-configs': [t('nav.systemManagement'), t('nav.systemConfigs')]
      }
      return pathMap[route.path] || [t('common.system')]
    })

    // 权限检查计算属性
    const hasSystemMenuAccess = computed(() => {
      return canAccessPage('users') || canAccessPage('roles') || canAccessPage('system-configs')
    })

    // 初始化权限
    onMounted(async () => {
      try {
        await initPermissions()
        permissionsLoaded.value = true
        console.log('Permissions initialized successfully')
      } catch (error) {
        console.error('Failed to initialize permissions:', error)
        permissionsLoaded.value = true // 即使失败也要显示页面
      }
    })

    // 侧边栏切换功能
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('sidebarCollapsed', sidebarCollapsed.value.toString())
    }

    // 语言切换处理
    const handleLanguageChange = (locale) => {
      setLocale(locale)
      currentLocale.value = locale
      ElMessage.success(t('messages.languageChanged'))
    }

    const handleCommand = async (command) => {
      if (command === 'logout') {
        try {
          await ElMessageBox.confirm(t('messages.logoutConfirm'), t('common.warning'), {
            confirmButtonText: t('common.confirm'),
            cancelButtonText: t('common.cancel'),
            type: 'warning'
          })

          localStorage.removeItem('token')
          localStorage.removeItem('user')
          ElMessage.success(t('messages.logoutSuccess'))
          router.push('/login')
        } catch {
          // 用户取消
        }
      } else if (command === 'profile') {
        // 跳转到个人资料页面
        router.push('/profile')
      }
    }

    return {
      userInfo,
      pageTitle,
      pageDescription,
      breadcrumbItems,
      defaultOpeneds,
      currentLocale,
      supportedLanguages,
      currentLanguage,
      // 侧边栏相关
      sidebarCollapsed,
      sidebarWidth,
      toggleSidebar,
      // 权限相关
      hasPermission,
      canAccessPage,
      hasSystemMenuAccess,
      permissionsLoaded,
      handleCommand,
      handleLanguageChange
    }
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  overflow: hidden;
}

.admin-layout :deep(.el-container) {
  height: 100vh;
}

.sidebar-container {
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-1);
  z-index: 100;
  transition: width 0.3s ease;
}

.admin-layout :deep(.el-menu) {
  border-right: none;
  flex: 1;
  overflow-y: auto;
  padding: 12px 0;
}

.admin-layout :deep(.el-menu-item) {
  height: 48px;
  line-height: 48px;
  margin: 4px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.admin-layout :deep(.el-menu-item:hover) {
  background-color: var(--sidebar-item-hover) !important;
  color: var(--sidebar-text-active) !important;
}

.admin-layout :deep(.el-menu-item.is-active) {
  background-color: var(--sidebar-item-active) !important;
  color: var(--sidebar-text-active) !important;
  font-weight: 600;
}

.admin-layout :deep(.el-sub-menu) {
  margin: 4px 16px;
}

.admin-layout :deep(.el-sub-menu__title) {
  height: 48px;
  line-height: 48px;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
  color: var(--sidebar-text) !important;
}

.admin-layout :deep(.el-sub-menu__title:hover) {
  background-color: var(--sidebar-item-hover) !important;
  color: var(--sidebar-text-active) !important;
}

.admin-layout :deep(.el-sub-menu .el-menu-item) {
  height: 44px;
  line-height: 44px;
  margin: 2px 0 2px 20px;
  padding-left: 40px !important;
  background-color: transparent !important;
  border-radius: 8px;
}

.admin-layout :deep(.el-sub-menu .el-menu-item:hover) {
  background-color: var(--sidebar-item-hover) !important;
  color: var(--sidebar-text-active) !important;
}

.admin-layout :deep(.el-sub-menu .el-menu-item.is-active) {
  background-color: var(--sidebar-item-active) !important;
  color: var(--sidebar-text-active) !important;
  font-weight: 600;
}

/* 简化的滚动条样式 */
.admin-layout :deep(.el-menu)::-webkit-scrollbar {
  width: 4px;
}

.admin-layout :deep(.el-menu)::-webkit-scrollbar-thumb {
  background: var(--border-basic-2);
  border-radius: 2px;
}

.logo {
  height: 80px;
  display: flex;
  align-items: center;
  padding: 0 24px;
  background-color: var(--sidebar-bg);
  border-bottom: 1px solid var(--border-basic-1);
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo:hover {
  background-color: var(--sidebar-item-hover);
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  margin-right: 12px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.logo-icon:hover {
  transform: scale(1.05);
}

.logo-text {
  transition: opacity 0.3s ease;
  overflow: hidden;
}

.logo-text h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-basic);
  line-height: 1.2;
  white-space: nowrap;
}

.logo-text span {
  font-size: 12px;
  color: var(--text-alternate);
  font-weight: 400;
  white-space: nowrap;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  z-index: 10;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 24px;
  gap: 24px;
}

.header-left {
  flex: 1;
  display: flex;
  align-items: center;
}

.header-right {
  flex-shrink: 0;
}





.admin-layout :deep(.el-main) {
  background-color: #f0f2f5;
  padding: 0;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.page-content {
  padding: 24px;
  min-height: calc(100vh - 60px);
}

/* 简化的主内容滚动条样式 */
.admin-layout :deep(.el-main)::-webkit-scrollbar {
  width: 6px;
}

.admin-layout :deep(.el-main)::-webkit-scrollbar-thumb {
  background: var(--border-basic-2);
  border-radius: 3px;
}

/* 新增的样式 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background-color: var(--bg-basic-2);
  border: 1px solid var(--border-basic-1);
  color: var(--text-alternate);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
}

.notification-btn:hover {
  background-color: var(--bg-basic-3);
  color: var(--text-basic);
  border-color: var(--border-basic-2);
}

.language-dropdown {
  cursor: pointer;
}

.language-btn {
  display: flex;
  align-items: center;
  padding: 4px 12px 4px 4px;
  border-radius: 12px;
  background-color: var(--bg-basic-2);
  border: 1px solid var(--border-basic-1);
  transition: all 0.3s ease;
  height: 48px;
  min-width: 100px;
  gap: 8px;
}

.language-btn:hover {
  background-color: var(--bg-basic-3);
  border-color: var(--border-basic-2);
}

.language-btn .el-icon:first-child {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--warning-color), var(--warning-light));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  flex-shrink: 0;
}

.language-btn span {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-basic);
  flex: 1;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  padding: 4px 16px 4px 4px;
  border-radius: 12px;
  background-color: var(--bg-basic-2);
  border: 1px solid var(--border-basic-1);
  transition: all 0.3s ease;
  min-width: 200px;
  height: 48px;
}

.user-info:hover {
  background-color: var(--bg-basic-3);
  border-color: var(--border-basic-2);
}

.user-avatar {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  margin-right: 12px;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-basic);
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.user-role {
  font-size: 12px;
  color: var(--text-alternate);
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.dropdown-icon {
  color: var(--text-alternate);
  font-size: 12px;
  margin-left: 8px;
  flex-shrink: 0;
}

/* 下拉菜单样式 */
.admin-layout :deep(.el-dropdown-menu) {
  border-radius: 12px;
  box-shadow: var(--shadow-2);
  border: 1px solid var(--border-basic-1);
  padding: 8px;
}

.admin-layout :deep(.el-dropdown-menu__item) {
  border-radius: 8px;
  padding: 12px 16px;
  margin: 2px 0;
  transition: all 0.3s ease;
}

.admin-layout :deep(.el-dropdown-menu__item:hover) {
  background-color: var(--bg-basic-2);
  color: var(--primary-color);
}

.admin-layout :deep(.el-dropdown-menu__item .el-icon) {
  margin-right: 8px;
}

/* 面包屑样式 */
.breadcrumb-container {
  display: flex;
  align-items: center;
  padding: 4px 16px 4px 4px;
  border-radius: 12px;
  background-color: var(--bg-basic-2);
  border: 1px solid var(--border-basic-1);
  transition: all 0.3s ease;
  height: 48px;
  min-width: 300px;
}

.breadcrumb-container:hover {
  background-color: var(--bg-basic-3);
  border-color: var(--border-basic-2);
}

.breadcrumb-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--info-color), var(--info-light));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  margin-right: 12px;
  flex-shrink: 0;
}

.breadcrumb-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 0;
}

.breadcrumb-path {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-basic);
  line-height: 1.2;
  width: 100%;
}

.breadcrumb-item {
  color: var(--text-alternate);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.breadcrumb-separator {
  margin: 0 6px;
  font-size: 12px;
  color: var(--text-alternate);
  flex-shrink: 0;
}

.breadcrumb-current {
  color: var(--text-basic);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.breadcrumb-description {
  font-size: 12px;
  color: var(--text-alternate);
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  margin-top: 2px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .breadcrumb-description {
    display: none;
  }

  .header-actions {
    gap: 8px;
  }

  .user-info {
    min-width: 120px;
  }

  .notification-btn,
  .language-btn {
    width: 40px;
    height: 40px;
  }

  .language-btn span {
    display: none;
  }
}

@media (max-width: 480px) {
  .breadcrumb-item,
  .breadcrumb-separator {
    display: none;
  }

  .sidebar-container {
    width: 100px !important;
  }

  .logo-text {
    display: none !important;
  }
}
</style>
