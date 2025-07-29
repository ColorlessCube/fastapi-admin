import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { usePermissions } from '../utils/permissions'

/**
 * 通用管理表格组合函数
 * @param {Object} options 配置选项
 * @param {Function} options.loadData 加载数据的函数
 * @param {Function} options.loadStatistics 加载统计信息的函数
 * @param {Function} options.deleteItem 删除项目的函数
 * @param {Object} options.config 表格配置
 */
export function useAdminTable(options) {
  const { t } = useI18n()
  const { initPermissions } = usePermissions()

  // 响应式数据
  const loading = ref(false)
  const data = ref([])
  const total = ref(0)
  const statistics = ref({})
  const selectedRows = ref([])

  // 搜索和分页参数
  const searchParams = reactive({
    keyword: '',
    filters: {},
    page: 1,
    pageSize: computed(() => options.config?.value?.pagination?.defaultPageSize || options.config?.pagination?.defaultPageSize || 20).value
  })

  // 加载数据
  const loadData = async (params = {}) => {
    loading.value = true
    try {
      const queryParams = {
        skip: (params.page - 1) * params.pageSize,
        limit: params.pageSize,
        ...params.filters
      }
      
      if (params.keyword) {
        queryParams.keyword = params.keyword
      }

      const response = await options.loadData(queryParams)
      
      if (response.data) {
        data.value = response.data
        total.value = response.total || 0
      } else {
        // 兼容旧格式
        data.value = response || []
        total.value = data.value.length
      }
    } catch (error) {
      console.error('Failed to load data:', error)
      ElMessage.error(t('messages.loadFailed'))
      data.value = []
      total.value = 0
    } finally {
      loading.value = false
    }
  }

  // 加载统计信息
  const loadStatistics = async () => {
    if (!options.loadStatistics) return
    
    try {
      const response = await options.loadStatistics()
      statistics.value = response.data || response || {}
    } catch (error) {
      console.error('Failed to load statistics:', error)
      // 如果统计接口失败，计算本地统计
      calculateLocalStatistics()
    }
  }

  // 计算本地统计（降级方案）
  const calculateLocalStatistics = () => {
    const total = data.value.length
    const active = data.value.filter(item => item.is_active).length
    const inactive = total - active
    
    statistics.value = {
      total,
      active,
      inactive,
      ...statistics.value
    }
  }

  // 搜索处理
  const handleSearch = (params) => {
    Object.assign(searchParams, params)
    loadData(searchParams)
  }

  // 分页处理
  const handlePageChange = (params) => {
    Object.assign(searchParams, params)
    loadData(searchParams)
  }

  // 选择处理
  const handleSelectionChange = (selection) => {
    selectedRows.value = selection
  }

  // 操作处理
  const handleAction = async (actionData) => {
    const { action, row, rows } = actionData
    
    try {
      switch (action) {
        case 'add':
          await handleAdd()
          break
        case 'edit':
          await handleEdit(row)
          break
        case 'delete':
          await handleDelete(row)
          break
        case 'permissions':
          await handlePermissions(row)
          break
        default:
          // 触发自定义事件
          if (options.onAction) {
            await options.onAction(action, row, rows)
          }
          break
      }
    } catch (error) {
      console.error(`Action ${action} failed:`, error)
      ElMessage.error(t('messages.operationFailed'))
    }
  }

  // 添加处理
  const handleAdd = async () => {
    if (options.onAdd) {
      await options.onAdd()
    }
  }

  // 编辑处理
  const handleEdit = async (row) => {
    if (options.onEdit) {
      await options.onEdit(row)
    }
  }

  // 删除处理
  const handleDelete = async (row) => {
    if (options.deleteItem) {
      await options.deleteItem(row.id)
      ElMessage.success(t('messages.deleteSuccess'))
      await refreshData()
    }
  }

  // 权限处理
  const handlePermissions = async (row) => {
    if (options.onPermissions) {
      await options.onPermissions(row)
    }
  }

  // 批量删除处理
  const handleBatchDelete = async (rows) => {
    if (options.onBatchDelete) {
      await options.onBatchDelete(rows)
    }
  }

  // 刷新数据
  const handleRefresh = () => {
    refreshData()
  }

  // 刷新数据（内部方法）
  const refreshData = async () => {
    await Promise.all([
      loadData(searchParams),
      loadStatistics()
    ])
  }

  // 初始化
  const initialize = async () => {
    await initPermissions()
    await refreshData()
  }

  // 导出的方法和数据
  return {
    // 响应式数据
    loading,
    data,
    total,
    statistics,
    selectedRows,
    searchParams,

    // 方法
    loadData,
    loadStatistics,
    handleSearch,
    handlePageChange,
    handleSelectionChange,
    handleAction,
    handleRefresh,
    refreshData,
    initialize,

    // 单独的操作方法（供外部调用）
    handleAdd,
    handleEdit,
    handleDelete,
    handlePermissions
  }
}

/**
 * 创建标准的API调用函数
 * @param {Object} api API对象
 * @param {string} endpoint 端点路径
 */
export function createApiHandlers(api, endpoint) {
  return {
    loadData: (params) => api.get(`${endpoint}/`, { params }),
    loadStatistics: () => api.get(`${endpoint}/statistics`),
    deleteItem: (id) => api.delete(`${endpoint}/${id}`)
  }
}

/**
 * 为角色筛选器加载选项
 * @param {Object} api API对象
 */
export async function loadRoleOptions(api) {
  try {
    const response = await api.get('/roles/')
    const roles = response.data || response || []
    return roles.map(role => ({
      label: role.name,
      value: role.id
    }))
  } catch (error) {
    console.error('Failed to load roles:', error)
    return []
  }
}

/**
 * 为通知类型筛选器加载选项
 * @param {Object} api API对象
 */
export async function loadNotificationTypeOptions(api) {
  try {
    const response = await api.get('/notification-clients/types')
    const types = response.data || response || []
    return types.map(type => ({
      label: type,
      value: type
    }))
  } catch (error) {
    console.error('Failed to load notification types:', error)
    return []
  }
}

/**
 * 更新表格配置中的动态选项
 * @param {Object} config 表格配置
 * @param {Object} api API对象
 */
export async function updateConfigOptions(config, api) {
  if (!config.toolbar?.filters) return config

  for (const filter of config.toolbar.filters) {
    if (filter.key === 'role_id' && filter.options.length === 0) {
      filter.options = await loadRoleOptions(api)
    }
    if (filter.key === 'type' && filter.options.length === 0) {
      filter.options = await loadNotificationTypeOptions(api)
    }
  }

  return config
}
