<template>
  <AdminLayout>
    <div class="roles-content">
      <div class="page-header">
        <div class="header-content">
          <div class="header-info">
            <h1>{{ $t('pages.roles.title') }}</h1>
            <p>{{ $t('pages.roles.description') }}</p>
          </div>
          <div class="header-actions">
            <el-button type="primary" size="large" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              {{ $t('pages.roles.addRole') }}
            </el-button>
          </div>
        </div>
      </div>

      <el-card class="table-card">
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-icon><UserFilled /></el-icon>
              <span>{{ $t('pages.roles.roleList') }}</span>
            </div>
          </div>
        </template>
        
        <el-table
          :data="roles"
          v-loading="loading"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" :label="$t('pages.roles.roleName')" min-width="120" />
          <el-table-column prop="description" :label="$t('pages.roles.roleDescription')" min-width="150" show-overflow-tooltip />
          <el-table-column prop="permissions" :label="$t('pages.roles.permissions')" min-width="140" align="center">
            <template #default="scope">
              <el-tag type="info" size="small">
                {{ scope.row.permissions?.length || 0 }} {{ $t('pages.roles.permissionCount') }}
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
          <el-table-column :label="$t('common.operation')" min-width="240" fixed="right">
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
                type="warning"
                size="small"
                @click="handlePermissions(scope.row)"
                v-if="pagePermissions.assignPermission"
              >
                {{ $t('pages.roles.permissions') }}
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(scope.row)"
                v-if="pagePermissions.delete"
              >
                {{ $t('common.delete') }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
    <!-- 添加/编辑角色对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="roleForm"
        :model="roleFormData"
        :rules="roleFormRules"
        :label-width="currentLocale === 'zh-CN' ? '80px' : '120px'"
      >
        <el-form-item :label="$t('pages.roles.roleName')" prop="name">
          <el-input v-model="roleFormData.name" />
        </el-form-item>
        <el-form-item :label="$t('pages.roles.roleDescription')" prop="description">
          <el-input
            type="textarea"
            :rows="3"
            v-model="roleFormData.description"
          />
        </el-form-item>
        <el-form-item :label="$t('pages.users.status')">
          <el-switch v-model="roleFormData.is_active" />
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
    
    <!-- 权限分配对话框 -->
    <el-dialog
      :title="$t('pages.roles.assignPermissions')"
      v-model="permissionDialogVisible"
      width="800px"
    >
      <div class="permission-assignment">
        <div class="permission-header">
          <h4>{{ $t('pages.roles.assignPermissionsTo', { roleName: currentRole?.name }) }}</h4>
          <p>{{ $t('pages.roles.selectPermissions') }}</p>
        </div>
        
        <el-divider />
        
        <div class="permission-groups">
          <div v-for="group in permissionGroups" :key="group.resource" class="permission-group">
            <h5>{{ group.title }}</h5>
            <el-checkbox-group v-model="selectedPermissions">
              <el-checkbox
                v-for="permission in group.permissions"
                :key="permission.id"
                :value="permission.id"
              >
                {{ permission.name }}
                <span class="permission-desc">{{ permission.description }}</span>
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="permissionDialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="handleSavePermissions" :loading="savingPermissions">
            {{ $t('pages.roles.savePermissions') }}
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
import { formatDateTime, formatRelativeTime } from '../utils/datetime'
import { usePermissions } from '../utils/permissions'
import AdminLayout from '../components/AdminLayout.vue'
import api from '../api'

export default {
  name: 'Roles',
  components: {
    AdminLayout
  },
  setup() {
    const { t } = useI18n()
    const currentLocale = ref(getLocale())
    const { getPagePermissions, initPermissions } = usePermissions()
    const roles = ref([])

    // 页面权限 - 使用计算属性使其响应式
    const pagePermissions = computed(() => getPagePermissions('roles'))
    const permissions = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const permissionDialogVisible = ref(false)
    const isEdit = ref(false)
    const submitting = ref(false)
    const savingPermissions = ref(false)
    const roleForm = ref()
    const currentRole = ref(null)
    const selectedPermissions = ref([])
    
    const roleFormData = reactive({
      id: null,
      name: '',
      description: '',
      is_active: true
    })
    
    const roleFormRules = {
      name: [
        { required: true, message: t('validation.required'), trigger: 'blur' }
      ]
    }
    
    const dialogTitle = ref('')
    
    // 权限分组
    const permissionGroups = ref([])
    
    const loadRoles = async () => {
      try {
        loading.value = true
        roles.value = await api.get('/roles/')
      } catch (error) {
        console.error('Failed to load roles:', error)
        ElMessage.error(t('messages.loadFailed'))
      } finally {
        loading.value = false
      }
    }
    
    const loadPermissions = async () => {
      try {
        permissions.value = await api.get('/permissions/')
        groupPermissions()
      } catch (error) {
        console.error('Failed to load permissions:', error)
        ElMessage.error(t('messages.loadFailed'))
      }
    }
    
    const groupPermissions = () => {
      const groups = {}
      permissions.value.forEach(permission => {
        if (!groups[permission.resource]) {
          groups[permission.resource] = {
            resource: permission.resource,
            title: getResourceTitle(permission.resource),
            permissions: []
          }
        }
        groups[permission.resource].permissions.push(permission)
      })
      permissionGroups.value = Object.values(groups)
    }
    
    const getResourceTitle = (resource) => {
      const titles = {
        dashboard: t('nav.dashboard'),
        user: t('nav.userManagement'),
        role: t('nav.roleManagement'),
        permission: t('pages.roles.permissions'),
        system: t('nav.systemManagement'),
        permission_test: t('pages.roles.permissions')
      }
      return titles[resource] || resource
    }


    
    const handleAdd = () => {
      isEdit.value = false
      dialogTitle.value = t('pages.roles.addRole')
      resetForm()
      dialogVisible.value = true
    }
    
    const handleEdit = (role) => {
      isEdit.value = true
      dialogTitle.value = t('pages.roles.editRole')
      Object.assign(roleFormData, {
        id: role.id,
        name: role.name,
        description: role.description,
        is_active: role.is_active
      })
      dialogVisible.value = true
    }
    
    const handlePermissions = (role) => {
      currentRole.value = role
      selectedPermissions.value = role.permissions?.map(p => p.id) || []
      permissionDialogVisible.value = true
    }
    
    const handleDelete = async (role) => {
      try {
        await ElMessageBox.confirm(
          t('messages.deleteConfirm', { type: t('pages.roles.title'), name: role.name }),
          t('common.warning'),
          {
            confirmButtonText: t('common.confirm'),
            cancelButtonText: t('common.cancel'),
            type: 'warning'
          }
        )

        await api.delete(`/roles/${role.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        loadRoles()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(t('messages.deleteFailed'))
        }
      }
    }
    
    const handleSubmit = async () => {
      try {
        await roleForm.value.validate()
        submitting.value = true
        
        if (isEdit.value) {
          await api.put(`/roles/${roleFormData.id}`, roleFormData)
          ElMessage.success(t('messages.updateSuccess'))
        } else {
          await api.post('/roles/', roleFormData)
          ElMessage.success(t('messages.createSuccess'))
        }

        dialogVisible.value = false
        loadRoles()
      } catch (error) {
        console.error('Submit error:', error)
        ElMessage.error(isEdit.value ? t('messages.updateFailed') : t('messages.createFailed'))
      } finally {
        submitting.value = false
      }
    }
    
    const handleSavePermissions = async () => {
      try {
        savingPermissions.value = true
        // 发送正确的数据格式
        await api.put(`/roles/${currentRole.value.id}/permissions`, {
          permission_ids: selectedPermissions.value
        })
        ElMessage.success(t('messages.permissionAssignSuccess'))
        permissionDialogVisible.value = false
        loadRoles()
      } catch (error) {
        console.error('Save permissions error:', error)
        ElMessage.error(t('messages.permissionAssignFailed'))
      } finally {
        savingPermissions.value = false
      }
    }
    
    const resetForm = () => {
      Object.assign(roleFormData, {
        id: null,
        name: '',
        description: '',
        is_active: true
      })
    }

    onMounted(async () => {
      // 确保权限已初始化
      await initPermissions()
      loadRoles()
      loadPermissions()
    })
    
    return {
      roles,
      permissions,
      loading,
      dialogVisible,
      permissionDialogVisible,
      isEdit,
      submitting,
      savingPermissions,
      roleForm,
      currentRole,
      selectedPermissions,
      roleFormData,
      roleFormRules,
      dialogTitle,
      permissionGroups,
      pagePermissions,
      handleAdd,
      handleEdit,
      handlePermissions,
      handleDelete,
      handleSubmit,
      handleSavePermissions,
      formatDateTime,
      formatRelativeTime
    }
  }
}
</script>

<style scoped>
.roles-content {
  background-color: transparent;
}

.page-header {
  background: linear-gradient(135deg, var(--success-color), var(--success-light));
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
  color: var(--success-color);
}

.permission-assignment {
  max-height: 500px;
  overflow-y: auto;
  padding: 16px;
}

.permission-header h4 {
  margin: 0 0 8px 0;
  color: var(--text-basic);
  font-size: 18px;
  font-weight: 600;
}

.permission-header p {
  margin: 0;
  color: var(--text-alternate);
  font-size: 14px;
}

.permission-groups {
  padding: 16px 0;
}

.permission-group {
  margin-bottom: 24px;
  padding: 16px;
  background-color: var(--bg-basic-2);
  border-radius: 12px;
  border: 1px solid var(--border-basic-1);
}

.permission-group h5 {
  margin: 0 0 12px 0;
  color: var(--primary-color);
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.permission-group h5::before {
  content: '';
  width: 4px;
  height: 16px;
  background-color: var(--primary-color);
  border-radius: 2px;
  margin-right: 8px;
}

.permission-group .el-checkbox {
  display: block;
  margin: 8px 0;
  line-height: 1.5;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.permission-group .el-checkbox:hover {
  background-color: var(--bg-basic-1);
}

.permission-desc {
  color: var(--text-alternate);
  font-size: 12px;
  margin-left: 8px;
  opacity: 0.8;
}

/* 表格样式优化 */
.roles-content :deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
}

.roles-content :deep(.el-table th.el-table__cell) {
  background-color: var(--bg-basic-2);
  color: var(--text-basic);
  font-weight: 600;
  border-bottom: 1px solid var(--border-basic-1);
}

.roles-content :deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid var(--border-basic-1);
}

.roles-content :deep(.el-table__row:hover > td) {
  background-color: var(--bg-basic-2) !important;
}

/* 对话框样式优化 */
.roles-content :deep(.el-dialog) {
  border-radius: 16px;
  box-shadow: var(--shadow-3);
}

.roles-content :deep(.el-dialog__header) {
  background-color: var(--bg-basic-1);
  border-bottom: 1px solid var(--border-basic-1);
  border-radius: 16px 16px 0 0;
}

/* 复选框样式优化 */
.roles-content :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.roles-content :deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: var(--primary-color);
  font-weight: 500;
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
