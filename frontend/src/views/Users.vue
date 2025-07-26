<template>
  <AdminLayout>
    <div class="users-content">
      <div class="page-header">
        <div class="header-content">
          <div class="header-info">
            <h1>{{ $t('pages.users.title') }}</h1>
            <p>{{ $t('pages.users.description') }}</p>
          </div>
          <div class="header-actions">
            <el-button type="primary" size="large" @click="handleAdd" v-if="pagePermissions.create">
              <el-icon><Plus /></el-icon>
              {{ $t('pages.users.addUser') }}
            </el-button>
          </div>
        </div>
      </div>

      <el-card class="table-card">
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-icon><User /></el-icon>
              <span>{{ $t('pages.users.userList') }}</span>
            </div>
          </div>
        </template>
              
              <el-table
                :data="users"
                v-loading="loading"
                style="width: 100%"
              >
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="username" :label="$t('pages.users.username')" min-width="120" />
                <el-table-column prop="email" :label="$t('pages.users.email')" min-width="180" show-overflow-tooltip />
                <el-table-column prop="full_name" :label="$t('pages.users.fullName')" min-width="120" show-overflow-tooltip />
                <el-table-column prop="roles" :label="$t('pages.users.roles')" min-width="160">
                  <template #default="scope">
                    <div class="roles-container">
                      <el-tag
                        v-for="role in scope.row.roles"
                        :key="role.id"
                        size="small"
                        class="role-tag"
                      >
                        {{ role.name }}
                      </el-tag>
                      <span v-if="!scope.row.roles || scope.row.roles.length === 0" class="text-gray">
                        {{ $t('pages.users.noRoles') }}
                      </span>
                    </div>
                  </template>
                </el-table-column>

                <el-table-column prop="is_active" :label="$t('pages.users.status')" min-width="80" align="center">
                  <template #default="scope">
                    <el-tag :type="scope.row.is_active ? 'success' : 'danger'" size="small">
                      {{ scope.row.is_active ? $t('common.active') : $t('common.inactive') }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="created_at" :label="$t('pages.users.createdAt')" min-width="160" show-overflow-tooltip>
                  <template #default="scope">
                    <div class="datetime-display">
                      <div class="datetime-main">{{ formatDateTime(scope.row.created_at) }}</div>
                      <div class="datetime-relative">{{ formatRelativeTime(scope.row.created_at) }}</div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="updated_at" :label="$t('pages.users.updatedAt')" min-width="160" show-overflow-tooltip>
                  <template #default="scope">
                    <div class="datetime-display">
                      <div class="datetime-main">{{ formatDateTime(scope.row.updated_at) }}</div>
                      <div class="datetime-relative">{{ formatRelativeTime(scope.row.updated_at) }}</div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column :label="$t('common.operation')" min-width="160" fixed="right">
                  <template #default="scope">
                    <el-button
                      type="primary"
                      size="small"
                      @click="handleEdit(scope.row)"
                      v-if="pagePermissions.update"
                    >
                      {{ $t('common.edit') }}
                    </el-button>
                    <el-button
                      type="danger"
                      size="small"
                      @click="handleDelete(scope.row)"
                      :disabled="scope.row.id === userInfo.id"
                      v-if="pagePermissions.delete"
                    >
                      {{ $t('common.delete') }}
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
    
    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="userForm"
        :model="userFormData"
        :rules="userFormRules"
        :label-width="currentLocale === 'zh-CN' ? '80px' : '120px'"
      >
        <el-form-item :label="$t('pages.users.username')" prop="username">
          <el-input v-model="userFormData.username" />
        </el-form-item>
        <el-form-item :label="$t('pages.users.email')" prop="email">
          <el-input v-model="userFormData.email" />
        </el-form-item>
        <el-form-item :label="$t('pages.users.fullName')" prop="full_name">
          <el-input v-model="userFormData.full_name" />
        </el-form-item>
        <el-form-item :label="$t('pages.users.password')" prop="password" v-if="!isEdit">
          <el-input type="password" v-model="userFormData.password" />
        </el-form-item>
        <el-form-item :label="$t('pages.users.roles')">
          <el-select
            v-model="userFormData.role_ids"
            multiple
            :placeholder="$t('common.pleaseSelect')"
            style="width: 100%"
          >
            <el-option
              v-for="role in roles"
              :key="role.id"
              :label="role.name"
              :value="role.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('pages.users.status')">
          <el-switch v-model="userFormData.is_active" />
        </el-form-item>

        <!-- 偏好设置 -->
        <el-divider>{{ $t('pages.users.preferences') }}</el-divider>

        <el-form-item :label="$t('pages.users.preferredLanguage')">
          <el-select v-model="userFormData.preferred_language" style="width: 100%">
            <el-option
              v-for="lang in languageOptions"
              :key="lang.value"
              :label="lang.label"
              :value="lang.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item :label="$t('pages.users.timezone')">
          <el-select
            v-model="userFormData.timezone"
            filterable
            clearable
            style="width: 100%"
            :placeholder="$t('pages.users.selectTimezone')"
          >
            <el-option
              v-for="tz in timezoneOptions"
              :key="tz.value"
              :label="tz.label"
              :value="tz.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ $t('common.confirm') }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </AdminLayout>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { getLocale } from '../i18n'
import { usePermissions } from '../utils/permissions'
import { formatDateTime, formatRelativeTime } from '../utils/datetime'
import AdminLayout from '../components/AdminLayout.vue'
import api from '../api'

export default {
  name: 'Users',
  components: {
    AdminLayout
  },
  setup() {
    const { t } = useI18n()
    const currentLocale = ref(getLocale())
    const { getPagePermissions, initPermissions } = usePermissions()
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))

    // 页面权限 - 使用计算属性使其响应式
    const pagePermissions = computed(() => getPagePermissions('users'))
    const users = ref([])
    const roles = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const submitting = ref(false)
    const userForm = ref()
    
    const userFormData = reactive({
      id: null,
      username: '',
      email: '',
      full_name: '',
      password: '',
      is_active: true,
      role_ids: [],
      preferred_language: 'zh-CN',
      timezone: ''
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
    
    const userFormRules = {
      username: [
        { required: true, message: t('validation.required'), trigger: 'blur' }
      ],
      email: [
        { required: true, message: t('validation.required'), trigger: 'blur' },
        { type: 'email', message: t('validation.email'), trigger: 'blur' }
      ],
      password: [
        { required: true, message: t('validation.required'), trigger: 'blur' },
        { min: 6, message: t('validation.minLength', { min: 6 }), trigger: 'blur' }
      ]
    }
    
    const dialogTitle = ref('')
    
    const loadUsers = async () => {
      try {
        loading.value = true
        users.value = await api.get('/users/')
      } catch (error) {
        console.error('Failed to load users:', error)
        ElMessage.error(t('messages.loadFailed'))
      } finally {
        loading.value = false
      }
    }

    const loadRoles = async () => {
      try {
        roles.value = await api.get('/roles/')
      } catch (error) {
        console.error('Failed to load roles:', error)
        ElMessage.error(t('messages.loadFailed'))
      }
    }
    
    const handleAdd = async () => {
      isEdit.value = false
      dialogTitle.value = t('pages.users.addUser')

      // 确保角色数据已加载
      if (roles.value.length === 0) {
        await loadRoles()
      }

      resetForm()
      dialogVisible.value = true
    }
    
    const handleEdit = async (user) => {
      isEdit.value = true
      dialogTitle.value = t('pages.users.editUser')

      // 确保角色数据已加载
      if (roles.value.length === 0) {
        await loadRoles()
      }

      Object.assign(userFormData, {
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        is_active: user.is_active,
        password: '',
        role_ids: user.roles?.map(role => role.id) || [],
        preferred_language: user.preferred_language || 'zh-CN',
        timezone: user.timezone || ''
      })
      dialogVisible.value = true
    }
    
    const handleDelete = async (user) => {
      try {
        await ElMessageBox.confirm(
          t('messages.deleteConfirm', { type: t('pages.users.title'), name: user.username }),
          t('common.warning'),
          {
            confirmButtonText: t('common.confirm'),
            cancelButtonText: t('common.cancel'),
            type: 'warning'
          }
        )

        await api.delete(`/users/${user.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        loadUsers()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Delete user error:', error)
          ElMessage.error(t('messages.deleteFailed'))
        }
      }
    }
    
    const handleSubmit = async () => {
      try {
        await userForm.value.validate()
        submitting.value = true
        
        if (isEdit.value) {
          // 编辑用户
          const updateData = {
            username: userFormData.username,
            email: userFormData.email,
            full_name: userFormData.full_name,
            is_active: userFormData.is_active,
            preferred_language: userFormData.preferred_language,
            timezone: userFormData.timezone,
            role_ids: userFormData.role_ids
          }
          await api.put(`/users/${userFormData.id}`, updateData)
          ElMessage.success(t('messages.updateSuccess'))
        } else {
          // 添加用户
          await api.post('/users/', userFormData)
          ElMessage.success(t('messages.createSuccess'))
        }

        dialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('Submit error:', error)
        ElMessage.error(isEdit.value ? t('messages.updateFailed') : t('messages.createFailed'))
      } finally {
        submitting.value = false
      }
    }
    
    const resetForm = () => {
      Object.assign(userFormData, {
        id: null,
        username: '',
        email: '',
        full_name: '',
        password: '',
        is_active: true,
        role_ids: [],
        preferred_language: 'zh-CN',
        timezone: ''
      })
    }
    

    

    
    onMounted(async () => {
      // 确保权限已初始化
      await initPermissions()
      loadUsers()
      loadRoles()
    })
    
    return {
      userInfo,
      users,
      roles,
      loading,
      dialogVisible,
      isEdit,
      submitting,
      userForm,
      userFormData,
      userFormRules,
      dialogTitle,
      pagePermissions,
      currentLocale,
      languageOptions,
      timezoneOptions,
      handleAdd,
      handleEdit,
      handleDelete,
      handleSubmit,
      formatDateTime,
      formatRelativeTime
    }
  }
}
</script>

<style scoped>
.users-content {
  background-color: transparent;
}

.page-header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  color: white;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
}

.header-info p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.header-actions .el-button {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
}

.header-actions .el-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.table-card {
  border-radius: 16px;
  box-shadow: var(--shadow-2);
  border: 1px solid var(--border-basic-1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-basic);
}

.card-title .el-icon {
  margin-right: 8px;
  font-size: 20px;
  color: var(--primary-color);
}

.text-gray {
  color: var(--text-alternate);
  font-size: 12px;
}

/* 表格样式优化 */
.users-content :deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
}

.users-content :deep(.el-table th.el-table__cell) {
  background-color: var(--bg-basic-2);
  color: var(--text-basic);
  font-weight: 600;
  border-bottom: 1px solid var(--border-basic-1);
}

.users-content :deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid var(--border-basic-1);
}

.users-content :deep(.el-table__row:hover > td) {
  background-color: var(--bg-basic-2) !important;
}

/* 按钮样式优化 */
.users-content :deep(.el-button--small) {
  border-radius: 8px;
  font-weight: 500;
}

/* 标签样式优化 */
.users-content :deep(.el-tag) {
  border-radius: 8px;
  font-weight: 500;
  border: none;
}

/* 对话框样式优化 */
.users-content :deep(.el-dialog) {
  border-radius: 16px;
  box-shadow: var(--shadow-3);
}

.users-content :deep(.el-dialog__header) {
  background-color: var(--bg-basic-1);
  border-bottom: 1px solid var(--border-basic-1);
  border-radius: 16px 16px 0 0;
}

.users-content :deep(.el-form-item__label) {
  color: var(--text-basic);
  font-weight: 500;
}

/* 角色标签容器 */
.roles-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}

.role-tag {
  margin: 0;
  white-space: nowrap;
}

/* 时间显示样式 */
.datetime-display {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.datetime-main {
  font-size: 13px;
  color: var(--text-basic);
  font-weight: 500;
}

.datetime-relative {
  font-size: 11px;
  color: var(--text-alternate);
  opacity: 0.8;
}
</style>
