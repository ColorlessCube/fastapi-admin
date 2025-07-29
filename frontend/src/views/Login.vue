<template>
  <div class="login-container">
    <div class="login-background">
      <div class="bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- 语言切换按钮 -->
    <div class="language-switcher">
      <el-dropdown @command="handleLanguageChange">
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
    </div>

    <div class="login-content">
      <div class="login-card">
        <div class="login-header">
          <div class="logo">
            <div class="logo-icon">
              <el-icon><Grid /></el-icon>
            </div>
            <div class="logo-text">
              <h1>{{ $t('pages.login.title') }}</h1>
              <p>{{ $t('pages.login.subtitle') }}</p>
            </div>
          </div>
        </div>

        <div class="login-form">
          <el-form
            ref="loginForm"
            :model="loginData"
            :rules="rules"
            label-width="0"
          >
            <el-form-item prop="username">
              <div class="input-wrapper">
                <el-icon class="input-icon"><User /></el-icon>
                <el-input
                  v-model="loginData.username"
                  :placeholder="$t('pages.login.username')"
                  size="large"
                  class="custom-input"
                />
              </div>
            </el-form-item>

            <el-form-item prop="password">
              <div class="input-wrapper">
                <el-icon class="input-icon"><Lock /></el-icon>
                <el-input
                  v-model="loginData.password"
                  type="password"
                  :placeholder="$t('pages.login.password')"
                  size="large"
                  class="custom-input"
                  @keyup.enter="handleLogin"
                />
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="login-button"
                :loading="loading"
                @click="handleLogin"
              >
                <span v-if="!loading">{{ $t('pages.login.loginBtn') }}</span>
                <span v-else>{{ $t('pages.login.loggingIn') }}</span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="login-footer">
            <div class="demo-accounts">
              <p>{{ $t('pages.login.demoAccounts') }}</p>
              <div class="account-tags">
                <el-tag class="account-tag" @click="fillAccount('admin')">
                  {{ $t('pages.login.adminAccount') }}
                </el-tag>
                <el-tag class="account-tag" @click="fillAccount('user')">
                  {{ $t('pages.login.userAccount') }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { setLocale, getLocale, getSupportedLocales } from '../i18n'
import api from '../api'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const { t } = useI18n()
    const loginForm = ref()
    const loading = ref(false)

    // 国际化相关
    const currentLocale = ref(getLocale())
    const supportedLanguages = getSupportedLocales()
    const currentLanguage = computed(() => {
      return supportedLanguages.find(lang => lang.value === currentLocale.value) || supportedLanguages[0]
    })
    
    const loginData = reactive({
      username: '',
      password: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const fillAccount = (type) => {
      if (type === 'admin') {
        loginData.username = 'admin'
        loginData.password = 'admin123'
      } else if (type === 'user') {
        loginData.username = 'user'
        loginData.password = 'user123'
      }
    }

    // 语言切换处理
    const handleLanguageChange = (locale) => {
      setLocale(locale)
      currentLocale.value = locale
      ElMessage.success(t('messages.languageChanged'))
    }

    const handleLogin = async () => {
      try {
        await loginForm.value.validate()
        loading.value = true

        const response = await api.post('/auth/login', loginData)

        localStorage.setItem('token', response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))

        ElMessage.success(t('messages.loginSuccess'))
        router.push('/')
      } catch (error) {
        console.error('Login error:', error)
        ElMessage.error(t('messages.loginFailed'))
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginForm,
      loginData,
      rules,
      loading,
      currentLocale,
      supportedLanguages,
      currentLanguage,
      fillAccount,
      handleLogin,
      handleLanguageChange
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.bg-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
  animation: float 8s ease-in-out infinite reverse;
}

.shape-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  left: 10%;
  animation: float 10s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.login-content {
  position: relative;
  z-index: 10;
}

.login-card {
  width: 420px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
}

.login-header {
  padding: 40px 40px 20px 40px;
  text-align: center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
  margin-bottom: 16px;
  box-shadow: 0 8px 20px rgba(51, 102, 255, 0.3);
}

.logo-text h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-basic);
}

.logo-text p {
  margin: 0;
  font-size: 16px;
  color: var(--text-alternate);
}

.login-form {
  padding: 20px 40px 40px 40px;
}

.input-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-alternate);
  font-size: 18px;
  z-index: 10;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid var(--border-basic-2);
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  height: 52px;
  padding-left: 48px;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: var(--border-basic-3);
  background-color: rgba(255, 255, 255, 0.9);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(51, 102, 255, 0.1);
  background-color: rgba(255, 255, 255, 1);
}

.login-form :deep(.el-input__inner) {
  padding-left: 48px;
  font-size: 16px;
  color: var(--text-basic);
}

.login-button {
  width: 100%;
  height: 52px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border: none;
  box-shadow: 0 8px 20px rgba(51, 102, 255, 0.3);
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(51, 102, 255, 0.4);
}

.login-footer {
  margin-top: 24px;
  text-align: center;
}

.demo-accounts p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: var(--text-alternate);
  font-weight: 500;
}

.account-tags {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.account-tag {
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  background-color: rgba(51, 102, 255, 0.1);
  border: 1px solid rgba(51, 102, 255, 0.2);
  color: var(--primary-color);
  font-size: 13px;
  transition: all 0.3s ease;
}

.account-tag:hover {
  background-color: rgba(51, 102, 255, 0.15);
  border-color: rgba(51, 102, 255, 0.3);
  transform: translateY(-1px);
}

/* 语言切换按钮样式 */
.language-switcher {
  position: absolute;
  top: 24px;
  right: 24px;
  z-index: 20;
}

.language-switcher .language-btn {
  display: flex;
  align-items: center;
  padding: 8px 16px 8px 8px;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  cursor: pointer;
  gap: 8px;
  min-width: 100px;
}

.language-switcher .language-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.language-switcher .language-btn .el-icon:first-child {
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

.language-switcher .language-btn span {
  font-size: 14px;
  font-weight: 500;
  color: white;
  flex: 1;
}

.language-switcher .dropdown-icon {
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  flex-shrink: 0;
}

/* 下拉菜单样式 */
.language-switcher :deep(.el-dropdown-menu) {
  border-radius: 12px;
  box-shadow: var(--shadow-2);
  border: 1px solid var(--border-basic-1);
  padding: 8px;
  backdrop-filter: blur(20px);
}

.language-switcher :deep(.el-dropdown-menu__item) {
  border-radius: 8px;
  padding: 12px 16px;
  margin: 2px 0;
  transition: all 0.3s ease;
}

.language-switcher :deep(.el-dropdown-menu__item:hover) {
  background-color: var(--bg-basic-2);
  color: var(--primary-color);
}

.language-switcher :deep(.el-dropdown-menu__item.is-active) {
  background-color: var(--primary-color);
  color: white;
}
</style>
