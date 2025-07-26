<template>
  <AdminLayout>
    <div class="system-configs-content">
      <div class="page-header">
        <div class="header-content">
          <div class="header-info">
            <h1>{{ $t('pages.systemConfigs.title') }}</h1>
            <p>{{ $t('pages.systemConfigs.description') }}</p>
          </div>
          <div class="header-actions">
            <el-button type="primary" size="large" @click="handleAdd" v-if="pagePermissions.create">
              <el-icon><Plus /></el-icon>
              {{ $t('pages.systemConfigs.addConfig') }}
            </el-button>
          </div>
        </div>
      </div>

      <el-card class="table-card">
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-icon><Setting /></el-icon>
              <span>{{ $t('pages.systemConfigs.configList') }}</span>
            </div>
          </div>
        </template>

        <div class="table-container">
            <el-table
              :data="configs"
              v-loading="loading"
              style="width: 100%"
              :header-cell-style="{ background: 'var(--bg-basic-2)', color: 'var(--text-basic)' }"
            >
              <el-table-column prop="key" :label="$t('pages.systemConfigs.configKey')" min-width="200" show-overflow-tooltip />
              <el-table-column prop="value" :label="$t('pages.systemConfigs.configValue')" min-width="200" show-overflow-tooltip>
                <template #default="scope">
                  <div class="value-display">
                    <span v-if="scope.row.data_type === 'boolean'">
                      <el-tag :type="scope.row.value === 'true' ? 'success' : 'danger'" size="small">
                        {{ scope.row.value === 'true' ? $t('common.yes') : $t('common.no') }}
                      </el-tag>
                    </span>
                    <span v-else-if="scope.row.data_type === 'json'" class="json-value">
                      {{ formatJsonValue(scope.row.value) }}
                    </span>
                    <span v-else>{{ scope.row.value }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="description" :label="$t('pages.systemConfigs.description')" min-width="200" show-overflow-tooltip />
              <el-table-column prop="data_type" :label="$t('pages.systemConfigs.dataType')" min-width="100" align="center">
                <template #default="scope">
                  <el-tag size="small" :type="getDataTypeColor(scope.row.data_type)">
                    {{ scope.row.data_type }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="is_active" :label="$t('pages.users.status')" min-width="80" align="center">
                <template #default="scope">
                  <el-tag :type="scope.row.is_active ? 'success' : 'danger'" size="small">
                    {{ scope.row.is_active ? $t('common.active') : $t('common.inactive') }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="is_system" :label="$t('pages.systemConfigs.isSystem')" min-width="100" align="center">
                <template #default="scope">
                  <el-tag :type="scope.row.is_system ? 'warning' : 'info'" size="small">
                    {{ scope.row.is_system ? $t('common.yes') : $t('common.no') }}
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
                    :disabled="scope.row.is_system"
                    v-if="pagePermissions.delete"
                  >
                    {{ $t('common.delete') }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
        </div>
      </el-card>
    </div>

    <!-- 配置编辑对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        ref="configForm"
        :model="configFormData"
        :rules="configFormRules"
        :label-width="currentLocale === 'zh-CN' ? '100px' : '140px'"
      >
        <el-form-item :label="$t('pages.systemConfigs.configKey')" prop="key">
          <el-input v-model="configFormData.key" :disabled="isEdit" />
        </el-form-item>
        <el-form-item :label="$t('pages.systemConfigs.configValue')" prop="value">
          <el-input
            v-if="configFormData.data_type !== 'json'"
            v-model="configFormData.value"
            :type="configFormData.data_type === 'boolean' ? 'text' : 'text'"
          />
          <el-input
            v-else
            type="textarea"
            :rows="4"
            v-model="configFormData.value"
            :placeholder="$t('pages.systemConfigs.jsonPlaceholder')"
          />
        </el-form-item>
        <el-form-item :label="$t('pages.systemConfigs.description')" prop="description">
          <el-input
            type="textarea"
            :rows="2"
            v-model="configFormData.description"
          />
        </el-form-item>
        <el-form-item :label="$t('pages.systemConfigs.dataType')" prop="data_type">
          <el-select v-model="configFormData.data_type" style="width: 100%">
            <el-option label="string" value="string" />
            <el-option label="integer" value="integer" />
            <el-option label="boolean" value="boolean" />
            <el-option label="json" value="json" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('pages.users.status')">
          <el-switch v-model="configFormData.is_active" />
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
  name: 'SystemConfigs',
  components: {
    AdminLayout
  },
  setup() {
    const { t } = useI18n()
    const currentLocale = ref(getLocale())
    const { getPagePermissions, initPermissions } = usePermissions()
    const configs = ref([])

    // 页面权限 - 使用计算属性使其响应式
    const pagePermissions = computed(() => getPagePermissions('system-configs'))
    const loading = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const submitting = ref(false)
    const configForm = ref()

    const dialogTitle = ref('')
    
    const configFormData = reactive({
      key: '',
      value: '',
      description: '',
      data_type: 'string',
      is_active: true
    })

    const configFormRules = {
      key: [
        { required: true, message: t('validation.required'), trigger: 'blur' }
      ],
      value: [
        { required: true, message: t('validation.required'), trigger: 'blur' }
      ]
    }

    const loadConfigs = async () => {
      loading.value = true
      try {
        const response = await api.get('/system-configs/')
        configs.value = response
      } catch (error) {
        console.error('Failed to load configs:', error)
        ElMessage.error(t('messages.loadFailed'))
      } finally {
        loading.value = false
      }
    }

    const handleAdd = () => {
      isEdit.value = false
      dialogTitle.value = t('pages.systemConfigs.addConfig')
      Object.assign(configFormData, {
        key: '',
        value: '',
        description: '',
        data_type: 'string',
        is_active: true
      })
      dialogVisible.value = true
    }

    const handleEdit = (config) => {
      isEdit.value = true
      dialogTitle.value = t('pages.systemConfigs.editConfig')
      Object.assign(configFormData, {
        id: config.id,
        key: config.key,
        value: config.value,
        description: config.description,
        data_type: config.data_type,
        is_active: config.is_active
      })
      dialogVisible.value = true
    }

    const handleDelete = async (config) => {
      try {
        await ElMessageBox.confirm(
          t('messages.deleteConfirm', { type: t('pages.systemConfigs.title'), name: config.key }), 
          t('common.warning'), 
          {
            confirmButtonText: t('common.confirm'),
            cancelButtonText: t('common.cancel'),
            type: 'warning'
          }
        )
        
        await api.delete(`/system-configs/${config.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        loadConfigs()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(t('messages.deleteFailed'))
        }
      }
    }

    const handleSubmit = async () => {
      try {
        await configForm.value.validate()
        submitting.value = true
        
        if (isEdit.value) {
          await api.put(`/system-configs/${configFormData.id}`, {
            value: configFormData.value,
            description: configFormData.description,
            data_type: configFormData.data_type,
            is_active: configFormData.is_active
          })
          ElMessage.success(t('messages.updateSuccess'))
        } else {
          await api.post('/system-configs/', configFormData)
          ElMessage.success(t('messages.createSuccess'))
        }
        
        dialogVisible.value = false
        loadConfigs()
      } catch (error) {
        console.error('Submit error:', error)
        ElMessage.error(isEdit.value ? t('messages.updateFailed') : t('messages.createFailed'))
      } finally {
        submitting.value = false
      }
    }



    const formatJsonValue = (value) => {
      try {
        const parsed = JSON.parse(value)
        return JSON.stringify(parsed, null, 2).substring(0, 100) + (value.length > 100 ? '...' : '')
      } catch {
        return value
      }
    }

    const getDataTypeColor = (dataType) => {
      const colors = {
        string: 'primary',
        integer: 'success',
        boolean: 'warning',
        json: 'info'
      }
      return colors[dataType] || 'primary'
    }

    onMounted(async () => {
      // 确保权限已初始化
      await initPermissions()
      loadConfigs()
    })

    return {
      configs,
      loading,
      dialogVisible,
      isEdit,
      submitting,
      configForm,
      dialogTitle,
      configFormData,
      configFormRules,
      currentLocale,
      pagePermissions,
      handleAdd,
      handleEdit,
      handleDelete,
      handleSubmit,
      formatDateTime,
      formatRelativeTime,
      formatJsonValue,
      getDataTypeColor
    }
  }
}
</script>

<style scoped>
.system-configs-content {
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
  box-shadow: var(--shadow-1);
  border: 1px solid var(--border-basic-1);
  overflow: hidden;
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

.table-container {
  padding: 0;
}

.value-display {
  max-width: 200px;
  word-break: break-all;
}

.json-value {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: var(--text-alternate);
}

.system-configs-content :deep(.el-table) {
  background-color: var(--bg-basic-1);
}

.system-configs-content :deep(.el-table__row) {
  background-color: var(--bg-basic-1);
}

.system-configs-content :deep(.el-table__row:hover > td) {
  background-color: var(--bg-basic-2) !important;
}

.system-configs-content :deep(.el-form-item__label) {
  color: var(--text-basic);
  font-weight: 500;
}

.system-configs-content :deep(.el-dialog) {
  border-radius: 16px;
}

.system-configs-content :deep(.el-dialog__header) {
  background-color: var(--bg-basic-2);
  border-radius: 16px 16px 0 0;
  padding: 20px 24px;
}

.system-configs-content :deep(.el-dialog__title) {
  color: var(--text-basic);
  font-weight: 600;
}

.system-configs-content :deep(.el-dialog__body) {
  padding: 24px;
}

.system-configs-content :deep(.el-dialog__footer) {
  padding: 16px 24px 24px;
  background-color: var(--bg-basic-2);
  border-radius: 0 0 16px 16px;
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
