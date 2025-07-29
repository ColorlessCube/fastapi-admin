import { createI18n } from 'vue-i18n'
import zhCN from '../locales/zh-CN.js'
import enUS from '../locales/en-US.js'

// 获取默认语言设置
function getDefaultLocale() {
  // 1. 首先检查用户偏好设置
  const userInfo = localStorage.getItem('user')
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo)
      if (user.preferred_language) {
        return user.preferred_language
      }
    } catch (error) {
      console.warn('Failed to parse user info from localStorage:', error)
    }
  }

  // 2. 检查本地存储的语言设置
  const saved = localStorage.getItem('locale')
  if (saved) {
    return saved
  }

  // 3. 使用浏览器语言设置
  const browserLang = navigator.language || navigator.userLanguage
  if (browserLang.startsWith('zh')) {
    return 'zh-CN'
  }
  return 'en-US'
}

const messages = {
  'zh-CN': zhCN,
  'en-US': enUS,
  'en': enUS  // 添加 'en' 作为 'en-US' 的别名，解决 Element Plus 语言包不匹配问题
}

const i18n = createI18n({
  legacy: false, // 使用 Composition API
  locale: getDefaultLocale(),
  fallbackLocale: 'en-US',
  messages,
  globalInjection: true // 全局注入 $t
})

export default i18n

// 切换语言的辅助函数
export async function setLocale(locale) {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
  document.documentElement.lang = locale

  // 如果用户已登录，同步更新用户偏好到服务器
  const token = localStorage.getItem('token')
  const userInfo = localStorage.getItem('user')

  if (token && userInfo) {
    try {
      const user = JSON.parse(userInfo)

      // 更新本地用户信息
      user.preferred_language = locale
      localStorage.setItem('user', JSON.stringify(user))

      // 同步到服务器
      const { default: api } = await import('../api')
      await api.put('/users/me/preferences', {
        preferred_language: locale
      })
    } catch (error) {
      console.warn('Failed to sync language preference to server:', error)
    }
  }
}

// 获取当前语言
export function getLocale() {
  return i18n.global.locale.value
}

// 获取支持的语言列表
export function getSupportedLocales() {
  return [
    { value: 'zh-CN', label: '中文' },
    { value: 'en-US', label: 'English' }
  ]
}
