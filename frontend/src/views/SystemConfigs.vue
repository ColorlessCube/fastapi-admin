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
import { createSystemConfigTableConfig } from '../config/tableConfigs.js'
import { createSystemConfigFormConfig, createDefaultFormData } from '../config/formConfigs.js'
import { useAdminTable, createApiHandlers } from '../composables/useAdminTable.js'
import { useI18n } from 'vue-i18n'
import api from '../api'

export default {
  name: 'SystemConfigs',
  components: {
    AdminLayout,
    AdminTable
  },
  setup() {
    const { t } = useI18n()

    // 表格配置 - 使用计算属性响应语言变化
    const tableConfig = computed(() => createSystemConfigTableConfig(t))

    // 表单对话框相关
    const dialogVisible = ref(false)
    const formMode = ref('add')
    const submitting = ref(false)

    // 表单配置
    const formConfig = computed(() => createSystemConfigFormConfig(t))

    // 表单数据
    const formData = reactive(createDefaultFormData(createSystemConfigFormConfig(t)))

    // API处理器
    const apiHandlers = createApiHandlers(api, '/system-configs')

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
      onEdit: handleEdit
    })

    // 添加配置
    async function handleAdd() {
      formMode.value = 'add'
      Object.assign(formData, createDefaultFormData(createSystemConfigFormConfig(t)))
      dialogVisible.value = true
    }

    // 编辑配置
    async function handleEdit(config) {
      formMode.value = 'edit'
      Object.assign(formData, {
        id: config.id,
        key: config.key,
        value: config.value,
        description: config.description,
        data_type: config.data_type,
        is_active: config.is_active,
        is_system: config.is_system
      })
      dialogVisible.value = true
    }

    // 删除配置
    const handleDelete = async (config) => {
      try {
        await api.delete(`/system-configs/${config.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        await handleRefresh()
      } catch (error) {
        console.error('Failed to delete config:', error)
        ElMessage.error(t('messages.deleteFailed'))
      }
    }

    // 表单提交处理
    const handleFormSubmit = async (submitData) => {
      try {
        submitting.value = true

        // 字段名已经与API匹配，直接使用
        const configData = {
          key: submitData.key,
          value: submitData.value,
          description: submitData.description,
          data_type: submitData.data_type,
          is_active: submitData.is_active,
          is_system: submitData.is_system
        }

        // 数据类型转换
        if (configData.data_type === 'number') {
          configData.value = Number(configData.value)
        } else if (configData.data_type === 'boolean') {
          configData.value = configData.value === 'true' || configData.value === true
        } else if (configData.data_type === 'json') {
          try {
            JSON.parse(configData.value) // 验证JSON格式
          } catch (error) {
            ElMessage.error(t('pages.systemConfigs.invalidJson'))
            return
          }
        }

        if (formMode.value === 'edit') {
          configData.id = formData.id
          await api.put(`/system-configs/${configData.id}`, configData)
          ElMessage.success(t('messages.updateSuccess'))
        } else {
          await api.post('/system-configs/', configData)
          ElMessage.success(t('messages.createSuccess'))
        }

        dialogVisible.value = false
        await handleRefresh()
      } catch (error) {
        console.error('Failed to submit config:', error)
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
      Object.assign(formData, createDefaultFormData(createSystemConfigFormConfig(t)))
    }



    // 初始化
    onMounted(async () => {
      await initialize()
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
      handleFormSubmit,
      handleFormCancel,
      handleFormReset
    }
  }
}
</script>



