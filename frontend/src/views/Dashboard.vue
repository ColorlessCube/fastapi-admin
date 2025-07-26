<template>
  <AdminLayout>
    <div class="dashboard-content">
      <!-- 欢迎区域 -->
      <div class="welcome-section">
        <div class="welcome-content">
          <h1>{{ $t('pages.dashboard.welcome') }}</h1>
          <p>{{ $t('pages.dashboard.welcomeDesc') }}</p>
          <div class="timezone-info">
            <el-icon><Clock /></el-icon>
            <span>{{ currentTime }}</span>
            <span class="timezone">{{ timezoneDisplay }}</span>
          </div>
        </div>
      </div>

      <!-- 系统信息卡片 -->
      <div class="stats-section">
        <el-row :gutter="24">
          <el-col :span="6">
            <div class="stat-card primary">
              <div class="stat-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ systemInfo.version }}</div>
                <div class="stat-label">{{ $t('pages.dashboard.systemVersion') }}</div>
                <div class="stat-description">{{ $t('pages.dashboard.currentVersion') }}</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card success">
              <div class="stat-icon">
                <el-icon><Timer /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ systemInfo.uptime }}</div>
                <div class="stat-label">{{ $t('pages.dashboard.systemUptime') }}</div>
                <div class="stat-description">{{ $t('pages.dashboard.runningTime') }}</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card warning">
              <div class="stat-icon">
                <el-icon><Connection /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ systemInfo.status }}</div>
                <div class="stat-label">{{ $t('pages.dashboard.systemStatus') }}</div>
                <div class="stat-description">{{ $t('pages.dashboard.serviceHealth') }}</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card info">
              <div class="stat-icon">
                <el-icon><Calendar /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ systemInfo.lastUpdate }}</div>
                <div class="stat-label">{{ $t('pages.dashboard.lastUpdate') }}</div>
                <div class="stat-description">{{ $t('pages.dashboard.systemUpdate') }}</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 详细信息区域 -->
      <div class="info-section">
        <el-row :gutter="24">
          <!-- 系统技术栈 -->
          <el-col :span="12">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon><Setting /></el-icon>
                  <span>{{ $t('pages.dashboard.techStack') }}</span>
                </div>
              </template>
              <div class="tech-stack">
                <div class="tech-item">
                  <div class="tech-icon backend">
                    <el-icon><Server /></el-icon>
                  </div>
                  <div class="tech-content">
                    <div class="tech-title">{{ $t('pages.dashboard.backend') }}</div>
                    <div class="tech-desc">FastAPI + SQLAlchemy + Alembic</div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="tech-icon frontend">
                    <el-icon><Monitor /></el-icon>
                  </div>
                  <div class="tech-content">
                    <div class="tech-title">{{ $t('pages.dashboard.frontend') }}</div>
                    <div class="tech-desc">Vue 3 + Element Plus + Vite</div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="tech-icon database">
                    <el-icon><Coin /></el-icon>
                  </div>
                  <div class="tech-content">
                    <div class="tech-title">{{ $t('pages.dashboard.database') }}</div>
                    <div class="tech-desc">SQLite + 权限管理</div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="tech-icon security">
                    <el-icon><Lock /></el-icon>
                  </div>
                  <div class="tech-content">
                    <div class="tech-title">{{ $t('pages.dashboard.security') }}</div>
                    <div class="tech-desc">JWT Token + RBAC</div>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>

          <!-- 环境信息 -->
          <el-col :span="12">
            <el-card class="info-card">
              <template #header>
                <div class="card-header">
                  <el-icon><InfoFilled /></el-icon>
                  <span>{{ $t('pages.dashboard.environmentInfo') }}</span>
                </div>
              </template>
              <div class="env-info">
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.browserInfo') }}</span>
                  <span class="env-value">{{ browserInfo.name }} {{ browserInfo.version }}</span>
                </div>
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.screenResolution') }}</span>
                  <span class="env-value">{{ browserInfo.resolution }}</span>
                </div>
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.language') }}</span>
                  <span class="env-value">{{ browserInfo.language }}</span>
                </div>
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.timezone') }}</span>
                  <span class="env-value">{{ timezoneDisplay }}</span>
                </div>
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.onlineTime') }}</span>
                  <span class="env-value">{{ onlineTime }}</span>
                </div>
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.lastLogin') }}</span>
                  <span class="env-value">{{ userLastLogin }}</span>
                </div>
                <div class="env-item">
                  <span class="env-label">{{ $t('pages.dashboard.loginCount') }}</span>
                  <span class="env-value">{{ userLoginCount }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 快捷操作区域 -->
      <div class="quick-actions-section">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <el-icon><Operation /></el-icon>
              <span>{{ $t('pages.dashboard.quickActions') }}</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button-group>
              <el-button type="primary" @click="refreshPage">
                <el-icon><Refresh /></el-icon>
                {{ $t('pages.dashboard.refreshPage') }}
              </el-button>
              <el-button type="success" @click="clearCache">
                <el-icon><Delete /></el-icon>
                {{ $t('pages.dashboard.clearCache') }}
              </el-button>
              <el-button type="warning" @click="exportData">
                <el-icon><Download /></el-icon>
                {{ $t('pages.dashboard.exportData') }}
              </el-button>
              <el-button type="info" @click="viewLogs">
                <el-icon><Document /></el-icon>
                {{ $t('pages.dashboard.viewLogs') }}
              </el-button>
            </el-button-group>
          </div>
        </el-card>
      </div>
          </div>
  </AdminLayout>
</template>

<script>
import { reactive, ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useDateTime } from '../composables/useDateTime'
import AdminLayout from '../components/AdminLayout.vue'
import api from '../api'

export default {
  name: 'Dashboard',
  components: {
    AdminLayout
  },
  setup() {
    const { t } = useI18n()
    const { formatDateTime, getTimezoneDisplay } = useDateTime()

    // 系统信息
    const systemInfo = reactive({
      version: 'v1.0.0',
      uptime: '0天',
      status: '正常',
      lastUpdate: '今天'
    })

    // 浏览器信息
    const browserInfo = reactive({
      name: '',
      version: '',
      resolution: '',
      language: ''
    })

    // 时间显示
    const currentTime = ref('')
    const timezoneDisplay = ref('')
    const onlineTime = ref('0分钟')
    let timeInterval = null
    let sessionStartTime = Date.now() // 当前会话开始时间

    // 用户信息
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    const userLastLogin = ref('--')
    const userLoginCount = ref('--')

    // 初始化系统信息
    const initSystemInfo = () => {
      // 计算系统运行时间（模拟）
      const startDate = new Date('2025-01-01')
      const now = new Date()
      const diffTime = Math.abs(now - startDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      systemInfo.uptime = `${diffDays}天`

      // 设置最后更新时间
      systemInfo.lastUpdate = formatDateTime(now.toISOString()).split(' ')[0]
    }

    // 初始化浏览器信息
    const initBrowserInfo = () => {
      const ua = navigator.userAgent

      // 检测浏览器
      if (ua.includes('Chrome')) {
        browserInfo.name = 'Chrome'
        const match = ua.match(/Chrome\/(\d+)/)
        browserInfo.version = match ? match[1] : 'Unknown'
      } else if (ua.includes('Firefox')) {
        browserInfo.name = 'Firefox'
        const match = ua.match(/Firefox\/(\d+)/)
        browserInfo.version = match ? match[1] : 'Unknown'
      } else if (ua.includes('Safari')) {
        browserInfo.name = 'Safari'
        const match = ua.match(/Version\/(\d+)/)
        browserInfo.version = match ? match[1] : 'Unknown'
      } else {
        browserInfo.name = 'Unknown'
        browserInfo.version = 'Unknown'
      }

      // 屏幕分辨率
      browserInfo.resolution = `${screen.width}x${screen.height}`

      // 语言 - 优先使用用户偏好语言
      browserInfo.language = userInfo.value.preferred_language || navigator.language || 'zh-CN'
    }

    // 初始化用户信息
    const initUserInfo = () => {
      if (userInfo.value.last_login_at) {
        userLastLogin.value = formatDateTime(userInfo.value.last_login_at)
      }

      if (userInfo.value.login_count) {
        userLoginCount.value = userInfo.value.login_count + ' 次'
      }

      // 如果用户有时区偏好，使用用户的时区
      if (userInfo.value.timezone) {
        timezoneDisplay.value = userInfo.value.timezone
      }
    }

    // 更新时间显示
    const updateTime = () => {
      const now = new Date()
      currentTime.value = formatDateTime(now.toISOString())
      timezoneDisplay.value = getTimezoneDisplay()

      // 计算在线时长：从上次登录时间到现在
      if (userInfo.value.last_login_at) {
        const lastLoginTime = new Date(userInfo.value.last_login_at + 'Z') // 确保是UTC时间
        const onlineMilliseconds = now.getTime() - lastLoginTime.getTime()
        const onlineMinutes = Math.floor(onlineMilliseconds / (1000 * 60))

        if (onlineMinutes < 1) {
          onlineTime.value = '刚刚登录'
        } else if (onlineMinutes < 60) {
          onlineTime.value = `${onlineMinutes}分钟`
        } else if (onlineMinutes < 1440) { // 小于24小时
          const hours = Math.floor(onlineMinutes / 60)
          const minutes = onlineMinutes % 60
          onlineTime.value = minutes > 0 ? `${hours}小时${minutes}分钟` : `${hours}小时`
        } else { // 超过24小时
          const days = Math.floor(onlineMinutes / 1440)
          const hours = Math.floor((onlineMinutes % 1440) / 60)
          onlineTime.value = hours > 0 ? `${days}天${hours}小时` : `${days}天`
        }
      } else {
        // 如果没有上次登录时间，使用会话开始时间
        const sessionMinutes = Math.floor((Date.now() - sessionStartTime) / (1000 * 60))
        if (sessionMinutes < 60) {
          onlineTime.value = `${sessionMinutes}分钟`
        } else {
          const hours = Math.floor(sessionMinutes / 60)
          const minutes = sessionMinutes % 60
          onlineTime.value = minutes > 0 ? `${hours}小时${minutes}分钟` : `${hours}小时`
        }
      }
    }

    // 启动时间更新
    const startTimeUpdate = () => {
      updateTime()
      timeInterval = setInterval(updateTime, 1000) // 每秒更新
    }

    // 停止时间更新
    const stopTimeUpdate = () => {
      if (timeInterval) {
        clearInterval(timeInterval)
        timeInterval = null
      }
    }

    // 快捷操作方法
    const refreshPage = () => {
      window.location.reload()
    }

    const clearCache = () => {
      localStorage.clear()
      sessionStorage.clear()
      ElMessage.success(t('pages.dashboard.cacheCleared'))
    }

    const exportData = () => {
      const data = {
        timestamp: new Date().toISOString(),
        systemInfo: systemInfo,
        browserInfo: browserInfo,
        userAgent: navigator.userAgent
      }

      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `system-info-${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)

      ElMessage.success(t('pages.dashboard.dataExported'))
    }

    const viewLogs = () => {
      console.log('System Info:', systemInfo)
      console.log('Browser Info:', browserInfo)
      console.log('Performance:', performance.now())
      ElMessage.info(t('pages.dashboard.logsInConsole'))
    }

    onMounted(() => {
      initSystemInfo()
      initUserInfo()
      initBrowserInfo()
      startTimeUpdate()
    })

    onUnmounted(() => {
      stopTimeUpdate()
    })

    return {
      systemInfo,
      browserInfo,
      currentTime,
      timezoneDisplay,
      onlineTime,
      userLastLogin,
      userLoginCount,
      formatDateTime,
      refreshPage,
      clearCache,
      exportData,
      viewLogs
    }
  }
}
</script>

<style scoped>
.dashboard-content {
  background-color: transparent;
}

.welcome-section {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-content h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
}

.welcome-content p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.timezone-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  font-size: 14px;
  opacity: 0.9;
}

.timezone-info .el-icon {
  font-size: 16px;
}

.timezone {
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.welcome-actions .el-button {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
}

.welcome-actions .el-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.stats-section {
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-basic-1);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-2);
  border: 1px solid var(--border-basic-1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-3);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
}

.stat-card.primary::before {
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
}

.stat-card.success::before {
  background: linear-gradient(90deg, var(--success-color), var(--success-light));
}

.stat-card.warning::before {
  background: linear-gradient(90deg, var(--warning-color), var(--warning-light));
}

.stat-card.info::before {
  background: linear-gradient(90deg, var(--info-color), var(--info-light));
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  margin-bottom: 16px;
}

.stat-card.primary .stat-icon {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
}

.stat-card.success .stat-icon {
  background: linear-gradient(135deg, var(--success-color), var(--success-light));
}

.stat-card.warning .stat-icon {
  background: linear-gradient(135deg, var(--warning-color), var(--warning-light));
}

.stat-card.info .stat-icon {
  background: linear-gradient(135deg, var(--info-color), var(--info-light));
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-basic);
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-alternate);
  margin-bottom: 8px;
}

.stat-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: var(--success-color);
  font-weight: 600;
}

.stat-trend .el-icon {
  margin-right: 4px;
  font-size: 14px;
}

.stat-description {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 4px;
}

/* 信息区域样式 */
.info-section {
  margin: 24px 0;
}

.info-card {
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-basic);
}

/* 技术栈样式 */
.tech-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tech-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: var(--bg-basic-2);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.tech-item:hover {
  background-color: var(--bg-basic-3);
  transform: translateX(4px);
}

.tech-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.tech-icon.backend {
  background: linear-gradient(135deg, #409eff, #67c23a);
}

.tech-icon.frontend {
  background: linear-gradient(135deg, #e6a23c, #f56c6c);
}

.tech-icon.database {
  background: linear-gradient(135deg, #909399, #606266);
}

.tech-icon.security {
  background: linear-gradient(135deg, #f56c6c, #e6a23c);
}

.tech-content {
  flex: 1;
}

.tech-title {
  font-weight: 600;
  color: var(--text-basic);
  margin-bottom: 4px;
}

.tech-desc {
  font-size: 13px;
  color: var(--text-alternate);
}

/* 环境信息样式 */
.env-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.env-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-light);
}

.env-item:last-child {
  border-bottom: none;
}

.env-label {
  font-weight: 500;
  color: var(--text-basic);
}

.env-value {
  color: var(--text-alternate);
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
}

/* 快捷操作样式 */
.quick-actions-section {
  margin: 24px 0;
}

.quick-actions {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.quick-actions .el-button-group .el-button {
  padding: 12px 20px;
  font-weight: 500;
}

.quick-actions .el-button-group .el-button .el-icon {
  margin-right: 6px;
}
</style>
