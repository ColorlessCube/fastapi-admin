<template>
  <AdminLayout>
    <AdminTable
      :config="tableConfig"
      :data="data"
      :loading="loading"
      :total="total"
      :statistics="statistics"
      :form-config="formConfig"
      :show-form-dialog="dialogVisible"
      :form-data="formData"
      :form-loading="submitting"
      :form-mode="formMode"
      @search="handleSearch"
      @page-change="handlePageChange"
      @selection-change="handleSelectionChange"
      @action="handleAction"
      @refresh="handleRefresh"
      @form-submit="handleFormSubmit"
      @form-cancel="handleFormCancel"
      @form-reset="handleFormReset"
      @update:show-form-dialog="dialogVisible = $event"
    />

  </AdminLayout>
</template>


<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import AdminLayout from '../components/AdminLayout.vue'
import AdminTable from '../components/AdminTable.vue'
import { createUserTableConfig } from '../config/tableConfigs.js'
import { useAdminTable, createApiHandlers, updateConfigOptions } from '../composables/useAdminTable.js'
import { createUserFormConfig, createDefaultFormData } from '../config/formConfigs.js'
import { useI18n } from 'vue-i18n'
import api from '../api'

export default {
  name: 'Users',
  components: {
    AdminLayout,
    AdminTable
  },
  setup() {
    const { t } = useI18n()

    // 表格配置 - 使用计算属性响应语言变化
    const tableConfig = computed(() => createUserTableConfig(t))

    // 表单对话框相关
    const dialogVisible = ref(false)
    const formMode = ref('add')
    const submitting = ref(false)
    const roles = ref([])

    // 表单配置
    const formConfig = computed(() => {
      const config = createUserFormConfig(t)
      // 动态更新角色选项
      config.fields = config.fields.map(field => {
        if (field.field === 'roleIds') {
          return {
            ...field,
            options: roles.value.map(role => ({
              label: role.name,
              value: role.id
            }))
          }
        }
        return field
      })
      return config
    })

    // 表单数据
    const formData = reactive(createDefaultFormData(createUserFormConfig(t)))



    // 批量删除用户
    const handleBatchDelete = async (users) => {
      try {
        const userIds = users.map(user => user.id)
        await api.post('/users/batch-delete', { user_ids: userIds })
        ElMessage.success(t('messages.batchDeleteSuccess', { count: users.length }))
        await handleRefresh()
      } catch (error) {
        console.error('Failed to batch delete users:', error)
        ElMessage.error(t('messages.batchDeleteFailed'))
      }
    }

    // API处理器
    const apiHandlers = createApiHandlers(api, '/users')

    // 使用通用表格组合函数
    const {
      loading,
      data,
      total,
      statistics,
      selectedRows,
      handleSearch,
      handlePageChange,
      handleSelectionChange,
      handleAction,
      handleRefresh,
      initialize
    } = useAdminTable({
      ...apiHandlers,
      config: tableConfig,
      onAdd: handleAdd,
      onEdit: handleEdit,
      onBatchDelete: handleBatchDelete
    })

    // 加载角色列表
    const loadRoles = async () => {
      try {
        const response = await api.get('/roles/')
        roles.value = response.data || response || []

        // 更新表格配置中的角色选项
        await updateConfigOptions(tableConfig.value, api)
      } catch (error) {
        console.error('Failed to load roles:', error)
      }
    }

    // 添加用户
    async function handleAdd() {
      formMode.value = 'add'
      Object.assign(formData, createDefaultFormData(createUserFormConfig(t)))
      dialogVisible.value = true
    }

    // 编辑用户
    async function handleEdit(user) {
      formMode.value = 'edit'
      Object.assign(formData, {
        id: user.id, // 保存ID用于更新
        username: user.username,
        email: user.email,
        fullName: user.full_name,
        roleIds: user.roles?.map(r => r.id) || [],
        isActive: user.is_active
      })
      dialogVisible.value = true
    }

    // 删除用户
    const handleDelete = async (user) => {
      try {
        await api.delete(`/users/${user.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        await handleRefresh()
      } catch (error) {
        console.error('Failed to delete user:', error)
        ElMessage.error(t('messages.deleteFailed'))
      }
    }

    // 表单提交处理
    const handleFormSubmit = async (submitData) => {
      try {
        submitting.value = true

        // 转换字段名以匹配API
        const userData = {
          username: submitData.username,
          email: submitData.email,
          full_name: submitData.fullName,
          role_ids: submitData.roleIds,
          is_active: submitData.isActive
        }

        if (formMode.value === 'edit') {
          userData.id = formData.id
          await api.put(`/users/${userData.id}`, userData)
          ElMessage.success(t('messages.updateSuccess'))
        } else {
          userData.password = submitData.password
          await api.post('/users/', userData)
          ElMessage.success(t('messages.createSuccess'))
        }

        dialogVisible.value = false
        await handleRefresh()
      } catch (error) {
        console.error('Failed to submit user:', error)
        ElMessage.error(t('messages.submitFailed'))
      } finally {
        submitting.value = false
      }
    }

    // 表单取消处理
    const handleFormCancel = () => {
      dialogVisible.value = false
    }

    // 表单重置处理
    const handleFormReset = () => {
      Object.assign(formData, createDefaultFormData(createUserFormConfig(t)))
    }



    // 初始化
    onMounted(async () => {
      await Promise.all([
        loadRoles(),
        initialize()
      ])
    })

    return {
      // 表格相关
      tableConfig,
      loading,
      data,
      total,
      statistics,
      selectedRows,
      handleSearch,
      handlePageChange,
      handleSelectionChange,
      handleAction,
      handleRefresh,

      // 表单对话框相关
      formConfig,
      dialogVisible,
      formMode,
      formData,
      submitting,
      roles,
      handleFormSubmit,
      handleFormCancel,
      handleFormReset,
      handleAdd
    }
  }
}
</script>


