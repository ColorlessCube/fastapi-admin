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
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'

import AdminLayout from '../components/AdminLayout.vue'
import AdminTable from '../components/AdminTable.vue'
import { createNotificationTableConfig } from '../config/tableConfigs.js'
import { createNotificationClientFormConfig, createDefaultFormData } from '../config/formConfigs.js'
import { useAdminTable, createApiHandlers, updateConfigOptions } from '../composables/useAdminTable.js'
import { useI18n } from 'vue-i18n'
import api from '../api'

export default {
  name: 'NotificationClients',
  components: {
    AdminLayout,
    AdminTable
  },
  setup() {
    const { t } = useI18n()

    // 表格配置 - 使用计算属性响应语言变化
    const tableConfig = computed(() => createNotificationTableConfig(t))

    // 表单对话框相关
    const dialogVisible = ref(false)
    const formMode = ref('add')
    const submitting = ref(false)

    // 表单配置
    const formConfig = computed(() => createNotificationClientFormConfig(t))

    // 表单数据
    const formData = reactive(createDefaultFormData(createNotificationClientFormConfig(t)))

    // 测试客户端
    const handleTest = async (client) => {
      try {
        await api.post(`/notification-clients/${client.id}/test`)
        ElMessage.success(t('pages.notificationClients.testSuccess'))
      } catch (error) {
        console.error('Failed to test client:', error)
        ElMessage.error(t('pages.notificationClients.testFailed'))
      }
    }

    // API处理器
    const apiHandlers = createApiHandlers(api, '/notification-clients')

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
      onTest: handleTest
    })

    // 加载通知类型
    const loadNotificationTypes = async () => {
      try {
        const response = await api.get('/notification-clients/types')
        notificationTypes.value = response.data || response || []

        // 更新表格配置中的类型选项
        await updateConfigOptions(tableConfig.value, api)
      } catch (error) {
        console.error('Failed to load notification types:', error)
      }
    }

    // 加载通知场景
    const loadNotificationScenarios = async () => {
      try {
        const response = await api.get('/notification-clients/scenarios')
        notificationScenarios.value = response.data || response || []
      } catch (error) {
        console.error('Failed to load notification scenarios:', error)
      }
    }

    // 添加客户端
    async function handleAdd() {
      formMode.value = 'add'
      Object.assign(formData, createDefaultFormData(createNotificationClientFormConfig(t)))
      dialogVisible.value = true
    }

    // 编辑客户端
    async function handleEdit(client) {
      formMode.value = 'edit'

      // 先重置表单数据，避免残留数据
      Object.assign(formData, createDefaultFormData(createNotificationClientFormConfig(t)))

      // 处理switches字段的不同格式
      let switchesValue = []
      if (client.switches) {
        if (Array.isArray(client.switches)) {
          // 如果是数组，直接使用
          switchesValue = client.switches
        } else if (typeof client.switches === 'string') {
          try {
            // 尝试解析JSON字符串
            switchesValue = JSON.parse(client.switches)
          } catch {
            // 如果不是JSON，尝试按逗号分割
            switchesValue = client.switches.split(',').map(s => s.trim()).filter(s => s)
          }
        }
      }

      // 然后设置编辑数据
      Object.assign(formData, {
        id: client.id,
        name: client.name,
        type: client.type,
        description: client.description,
        config: typeof client.config === 'object' ? JSON.stringify(client.config, null, 2) : client.config,
        enabled: client.enabled,
        interactive: client.interactive,
        switches: switchesValue
      })

      // 使用nextTick确保数据更新后再显示对话框
      await nextTick()
      dialogVisible.value = true
    }

    // 删除客户端
    const handleDelete = async (client) => {
      try {
        await api.delete(`/notification-clients/${client.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        await handleRefresh()
      } catch (error) {
        console.error('Failed to delete client:', error)
        ElMessage.error(t('messages.deleteFailed'))
      }
    }

    // 处理类型变更
    const handleTypeChange = (type) => {
      const typeConfig = notificationTypes.value.find(t => t.typeKey === type)
      selectedTypeConfig.value = typeConfig

      // 重置配置
      clientFormData.config = {}
      if (typeConfig?.fields) {
        typeConfig.fields.forEach(field => {
          clientFormData.config[field.key] = field.default || ''
        })
      }
    }

    // 表单提交处理
    const handleFormSubmit = async (submitData) => {
      try {
        submitting.value = true

        // 字段名已经与API匹配，直接使用
        const clientData = {
          name: submitData.name,
          type: submitData.type,
          description: submitData.description,
          config: submitData.config,
          enabled: submitData.enabled,
          interactive: submitData.interactive || false,
          switches: submitData.switches || []
        }

        // 验证config字段的JSON格式（如果有值）
        if (clientData.config && clientData.config.trim()) {
          try {
            JSON.parse(clientData.config)
          } catch (error) {
            ElMessage.error(t('pages.notificationClients.invalidConfig'))
            return
          }
        }

        if (formMode.value === 'edit') {
          clientData.id = formData.id
          await api.put(`/notification-clients/${clientData.id}`, clientData)
          ElMessage.success(t('messages.updateSuccess'))
        } else {
          await api.post('/notification-clients/', clientData)
          ElMessage.success(t('messages.createSuccess'))
        }

        dialogVisible.value = false
        await handleRefresh()
      } catch (error) {
        console.error('Failed to submit client:', error)
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
      Object.assign(formData, createDefaultFormData(createNotificationClientFormConfig(t)))
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


