<template>
  <AdminLayout>
    <div class="profile-container">
      <div class="profile-header">
        <h1>{{ $t('pages.profile.title') }}</h1>
        <p>{{ $t('pages.profile.description') }}</p>
      </div>

      <el-row :gutter="24">
        <!-- 基本信息 -->
        <el-col :span="12">
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <el-icon><User /></el-icon>
                <span>{{ $t('pages.profile.basicInfo') }}</span>
              </div>
            </template>
            
            <el-form
              ref="profileForm"
              :model="profileFormData"
              :rules="profileFormRules"
              label-width="120px"
              @submit.prevent="handleUpdateProfile"
            >
              <el-form-item :label="$t('pages.users.username')" prop="username">
                <el-input v-model="profileFormData.username" disabled />
              </el-form-item>
              
              <el-form-item :label="$t('pages.users.email')" prop="email">
                <el-input v-model="profileFormData.email" />
              </el-form-item>
              
              <el-form-item :label="$t('pages.users.fullName')" prop="full_name">
                <el-input v-model="profileFormData.full_name" />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleUpdateProfile" :loading="updating">
                  {{ $t('common.save') }}
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- 偏好设置 -->
        <el-col :span="12">
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <el-icon><Setting /></el-icon>
                <span>{{ $t('pages.profile.preferences') }}</span>
              </div>
            </template>
            
            <el-form
              ref="preferencesForm"
              :model="preferencesFormData"
              label-width="120px"
              @submit.prevent="handleUpdatePreferences"
            >
              <el-form-item :label="$t('pages.profile.language')">
                <el-select v-model="preferencesFormData.preferred_language" style="width: 100%">
                  <el-option
                    v-for="lang in languageOptions"
                    :key="lang.value"
                    :label="lang.label"
                    :value="lang.value"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item :label="$t('pages.profile.timezone')">
                <el-select
                  v-model="preferencesFormData.timezone"
                  filterable
                  style="width: 100%"
                  :placeholder="$t('pages.profile.selectTimezone')"
                >
                  <el-option
                    v-for="tz in timezoneOptions"
                    :key="tz.value"
                    :label="tz.label"
                    :value="tz.value"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleUpdatePreferences" :loading="updatingPreferences">
                  {{ $t('common.save') }}
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>

      <!-- 密码修改 -->
      <el-row :gutter="24" style="margin-top: 24px;">
        <el-col :span="12">
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <el-icon><Lock /></el-icon>
                <span>{{ $t('pages.profile.changePassword') }}</span>
              </div>
            </template>
            
            <el-form
              ref="passwordForm"
              :model="passwordFormData"
              :rules="passwordFormRules"
              label-width="120px"
              @submit.prevent="handleChangePassword"
            >
              <el-form-item :label="$t('pages.profile.currentPassword')" prop="current_password">
                <el-input
                  v-model="passwordFormData.current_password"
                  type="password"
                  show-password
                  :placeholder="$t('pages.profile.enterCurrentPassword')"
                />
              </el-form-item>
              
              <el-form-item :label="$t('pages.profile.newPassword')" prop="new_password">
                <el-input
                  v-model="passwordFormData.new_password"
                  type="password"
                  show-password
                  :placeholder="$t('pages.profile.enterNewPassword')"
                />
              </el-form-item>
              
              <el-form-item :label="$t('pages.profile.confirmPassword')" prop="confirm_password">
                <el-input
                  v-model="passwordFormData.confirm_password"
                  type="password"
                  show-password
                  :placeholder="$t('pages.profile.confirmNewPassword')"
                />
              </el-form-item>
              
              <el-form-item>
                <el-button type="danger" @click="handleChangePassword" :loading="changingPassword">
                  {{ $t('pages.profile.changePassword') }}
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- 登录历史 -->
        <el-col :span="12">
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <el-icon><Clock /></el-icon>
                <span>{{ $t('pages.profile.loginHistory') }}</span>
              </div>
            </template>
            
            <div class="login-info">
              <div class="info-item">
                <span class="info-label">{{ $t('pages.profile.lastLogin') }}:</span>
                <span class="info-value">{{ userLastLogin }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">{{ $t('pages.profile.loginCount') }}:</span>
                <span class="info-value">{{ userLoginCount }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">{{ $t('pages.profile.lastLoginIP') }}:</span>
                <span class="info-value">{{ userLastLoginIP }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">{{ $t('pages.profile.accountCreated') }}:</span>
                <span class="info-value">{{ userCreatedAt }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </AdminLayout>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { formatDateTime } from '../utils/datetime'
import { setLocale } from '../i18n'
import AdminLayout from '../components/AdminLayout.vue'
import api from '../api'

export default {
  name: 'Profile',
  components: {
    AdminLayout
  },
  setup() {
    const { t } = useI18n()
    
    // 表单引用
    const profileForm = ref(null)
    const preferencesForm = ref(null)
    const passwordForm = ref(null)
    
    // 加载状态
    const updating = ref(false)
    const updatingPreferences = ref(false)
    const changingPassword = ref(false)
    
    // 用户信息
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    const userLastLogin = ref('--')
    const userLoginCount = ref('--')
    const userLastLoginIP = ref('--')
    const userCreatedAt = ref('--')
    
    // 基本信息表单
    const profileFormData = reactive({
      username: '',
      email: '',
      full_name: ''
    })
    
    // 偏好设置表单
    const preferencesFormData = reactive({
      preferred_language: 'zh-CN',
      timezone: ''
    })
    
    // 密码修改表单
    const passwordFormData = reactive({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })
    
    // 语言选项
    const languageOptions = [
      { label: '中文', value: 'zh-CN' },
      { label: 'English', value: 'en-US' }
    ]
    
    // 时区选项
    const timezoneOptions = [
      { label: 'Asia/Shanghai (UTC+8)', value: 'Asia/Shanghai' },
      { label: 'America/New_York (UTC-5)', value: 'America/New_York' },
      { label: 'Europe/London (UTC+0)', value: 'Europe/London' },
      { label: 'Asia/Tokyo (UTC+9)', value: 'Asia/Tokyo' },
      { label: 'Australia/Sydney (UTC+11)', value: 'Australia/Sydney' },
      { label: 'America/Los_Angeles (UTC-8)', value: 'America/Los_Angeles' },
      { label: 'Europe/Paris (UTC+1)', value: 'Europe/Paris' }
    ]
    
    // 表单验证规则
    const profileFormRules = {
      email: [
        { required: true, message: t('validation.emailRequired'), trigger: 'blur' },
        { type: 'email', message: t('validation.emailInvalid'), trigger: 'blur' }
      ]
    }
    
    const passwordFormRules = {
      current_password: [
        { required: true, message: t('validation.currentPasswordRequired'), trigger: 'blur' }
      ],
      new_password: [
        { required: true, message: t('validation.newPasswordRequired'), trigger: 'blur' },
        { min: 6, message: t('validation.passwordMinLength'), trigger: 'blur' }
      ],
      confirm_password: [
        { required: true, message: t('validation.confirmPasswordRequired'), trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== passwordFormData.new_password) {
              callback(new Error(t('validation.passwordMismatch')))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }
    
    // 初始化用户信息
    const initUserInfo = () => {
      if (userInfo.value.id) {
        profileFormData.username = userInfo.value.username || ''
        profileFormData.email = userInfo.value.email || ''
        profileFormData.full_name = userInfo.value.full_name || ''

        preferencesFormData.preferred_language = userInfo.value.preferred_language || 'zh-CN'
        preferencesFormData.timezone = userInfo.value.timezone || ''

        userLastLogin.value = userInfo.value.last_login_at ? formatDateTime(userInfo.value.last_login_at) : '--'
        userLoginCount.value = userInfo.value.login_count ? userInfo.value.login_count + ' 次' : '--'
        userLastLoginIP.value = userInfo.value.last_login_ip || '--'
        userCreatedAt.value = userInfo.value.created_at ? formatDateTime(userInfo.value.created_at) : '--'
      }
    }

    // 更新基本信息
    const handleUpdateProfile = async () => {
      if (!profileForm.value) return

      try {
        await profileForm.value.validate()
        updating.value = true

        const response = await api.put('/users/me', {
          email: profileFormData.email,
          full_name: profileFormData.full_name
        })

        // 更新本地用户信息
        const updatedUser = { ...userInfo.value, ...response }
        userInfo.value = updatedUser
        localStorage.setItem('user', JSON.stringify(updatedUser))

        ElMessage.success(t('messages.updateSuccess'))
      } catch (error) {
        console.error('Update profile error:', error)
        ElMessage.error(t('messages.updateFailed'))
      } finally {
        updating.value = false
      }
    }

    // 更新偏好设置
    const handleUpdatePreferences = async () => {
      try {
        updatingPreferences.value = true

        const response = await api.put('/users/me/preferences', {
          preferred_language: preferencesFormData.preferred_language,
          timezone: preferencesFormData.timezone
        })

        // 更新本地用户信息
        const updatedUser = { ...userInfo.value, ...response }
        userInfo.value = updatedUser
        localStorage.setItem('user', JSON.stringify(updatedUser))

        // 如果语言发生变化，立即应用
        if (preferencesFormData.preferred_language !== userInfo.value.preferred_language) {
          await setLocale(preferencesFormData.preferred_language)
        }

        ElMessage.success(t('messages.preferencesUpdated'))
      } catch (error) {
        console.error('Update preferences error:', error)
        ElMessage.error(t('messages.updateFailed'))
      } finally {
        updatingPreferences.value = false
      }
    }

    // 修改密码
    const handleChangePassword = async () => {
      if (!passwordForm.value) return

      try {
        await passwordForm.value.validate()
        changingPassword.value = true

        await api.put('/users/me/password', {
          current_password: passwordFormData.current_password,
          new_password: passwordFormData.new_password
        })

        // 清空表单
        passwordFormData.current_password = ''
        passwordFormData.new_password = ''
        passwordFormData.confirm_password = ''

        ElMessage.success(t('messages.passwordChanged'))
      } catch (error) {
        console.error('Change password error:', error)
        if (error.response?.status === 400) {
          ElMessage.error(t('messages.currentPasswordIncorrect'))
        } else {
          ElMessage.error(t('messages.passwordChangeFailed'))
        }
      } finally {
        changingPassword.value = false
      }
    }

    onMounted(() => {
      initUserInfo()
    })

    return {
      profileForm,
      preferencesForm,
      passwordForm,
      updating,
      updatingPreferences,
      changingPassword,
      userLastLogin,
      userLoginCount,
      userLastLoginIP,
      userCreatedAt,
      profileFormData,
      preferencesFormData,
      passwordFormData,
      languageOptions,
      timezoneOptions,
      profileFormRules,
      passwordFormRules,
      formatDateTime,
      handleUpdateProfile,
      handleUpdatePreferences,
      handleChangePassword
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 24px;
}

.profile-header {
  margin-bottom: 24px;
}

.profile-header h1 {
  margin: 0 0 8px 0;
  color: var(--text-basic);
}

.profile-header p {
  margin: 0;
  color: var(--text-alternate);
}

.profile-card {
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-basic);
}

.login-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: var(--text-basic);
}

.info-value {
  color: var(--text-alternate);
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
}
</style>
