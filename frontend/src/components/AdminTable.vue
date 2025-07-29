<template>
  <div class="admin-table">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-info">
          <el-icon><component :is="config.icon || 'Grid'" /></el-icon>
          <div class="header-text">
            <div class="breadcrumb">
              <span>{{ $t('menu.systemManagement') }}</span>
              <el-icon><ArrowRight /></el-icon>
              <span>{{ config.title }}</span>
            </div>
            <p class="description">{{ config.description }}</p>
          </div>
        </div>
        <div class="header-actions">
          <el-button
            v-for="action in config.toolbar?.actions || []"
            :key="action.key"
            :type="action.type || 'default'"
            v-show="!action.permission || hasPermission(action.permission)"
            @click="handleHeaderAction(action)"
          >
            <el-icon v-if="action.icon"><component :is="action.icon" /></el-icon>
            {{ action.label }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="action-bar" v-if="config.toolbar">
      <div class="search-section">
        <!-- 搜索框 -->
        <el-input
          v-if="config.toolbar.search?.enabled"
          v-model="searchKeyword"
          :placeholder="config.toolbar.search.placeholder"
          style="width: 300px"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <!-- 筛选器 -->
        <template v-for="filter in config.toolbar.filters || []" :key="filter.key">
          <el-select
            v-if="filter.type === 'select'"
            v-model="filterValues[filter.key]"
            :placeholder="filter.placeholder"
            style="width: 150px; margin-left: 10px"
            clearable
            @change="handleFilter"
          >
            <el-option
              v-for="option in filter.options"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </template>
      </div>

      <div class="button-section">
        <el-button @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          {{ $t('common.refresh') }}
        </el-button>
      </div>
    </div>

    <!-- 批量操作栏 -->
    <div
      class="batch-actions"
      v-if="config.selection?.enabled && selectedRows.length > 0"
    >
      <div class="batch-info">
        <span>{{ $t('table.selectedItems', { count: selectedRows.length }) }}</span>
      </div>
      <div class="batch-buttons">
        <el-button
          v-for="action in config.selection.actions"
          :key="action.key"
          :type="action.type || 'default'"
          :danger="action.danger"
          @click="handleBatchAction(action)"
        >
          <el-icon v-if="action.icon"><component :is="action.icon" /></el-icon>
          {{ action.label }}
        </el-button>
        <el-button @click="clearSelection">{{ $t('table.clearSelection') }}</el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section" v-if="config.statistics?.length">
      <el-row :gutter="20">
        <el-col 
          v-for="stat in config.statistics" 
          :key="stat.key"
          :span="24 / config.statistics.length"
        >
          <div class="stat-card">
            <div class="stat-icon" :class="stat.color">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{
                stat.formatter
                  ? stat.formatter(statistics[stat.key])
                  : (statistics[stat.key] || 0)
              }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 表格卡片 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <div class="card-title">
            <el-icon><component :is="config.icon || 'Grid'" /></el-icon>
            <span>{{ config.tableTitle || config.title }}</span>
          </div>
          <div class="card-extra">
            <span class="total-count">{{ $t('common.total') }}: {{ total }}</span>
          </div>
        </div>
      </template>

      <div class="table-container">
        <el-table
          :data="data"
          v-loading="loading"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <!-- 选择列 -->
          <el-table-column
            v-if="config.selection?.enabled && config.selection?.actions?.length"
            type="selection"
            width="55"
          />
          
          <!-- 数据列 -->
          <el-table-column
            v-for="column in config.columns"
            :key="column.key"
            :prop="column.key"
            :label="column.label"
            :width="column.width"
            :sortable="column.sortable"
            :show-overflow-tooltip="column.showOverflowTooltip !== false"
          >
            <template #default="{ row }">
              <AdminTableCell
                :value="getColumnValue(row, column)"
                :column="column"
                :row="row"
              />
            </template>
          </el-table-column>

          <!-- 操作列 -->
          <el-table-column 
            v-if="config.actions?.length"
            :label="$t('common.operation')" 
            :width="config.actionWidth || 'auto'"
            fixed="right"
          >
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button
                  v-for="action in config.actions"
                  :key="action.key"
                  :type="action.type || 'primary'"
                  :size="action.size || 'small'"
                  v-show="!action.permission || hasPermission(action.permission)"
                  @click="handleAction(action, row)"
                >
                  <el-icon v-if="action.icon"><component :is="action.icon" /></el-icon>
                  {{ action.label }}
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-section">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="config.pagination?.pageSizes || [10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>

    <!-- 通用表单对话框 -->
    <FormDialog
      v-if="formConfig"
      v-model:visible="formDialogVisible"
      :config="formConfig"
      :form-data="formData"
      :loading="formLoading"
      :mode="formMode"
      @submit="handleFormSubmit"
      @cancel="handleFormCancel"
      @reset="handleFormReset"
    >
      <!-- 自定义字段插槽 -->
      <template v-for="(_, name) in $slots" :key="name" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps" />
      </template>
    </FormDialog>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import FormDialog from './FormDialog.vue'
import { 
  Search, Refresh, ArrowRight, Grid
} from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'
import { usePermissions } from '../utils/permissions'
import AdminTableCell from './AdminTableCell.vue'

export default {
  name: 'AdminTable',
  components: {
    AdminTableCell,
    FormDialog,
    Search,
    Refresh,
    ArrowRight,
    Grid
  },
  props: {
    config: {
      type: Object,
      required: true
    },
    data: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    total: {
      type: Number,
      default: 0
    },
    statistics: {
      type: Object,
      default: () => ({})
    },
    // 表单对话框配置
    formConfig: {
      type: Object,
      default: null
    },
    // 表单对话框显示状态
    showFormDialog: {
      type: Boolean,
      default: false
    },
    // 表单数据
    formData: {
      type: Object,
      default: () => ({})
    },
    // 表单加载状态
    formLoading: {
      type: Boolean,
      default: false
    },
    // 表单模式 (add/edit)
    formMode: {
      type: String,
      default: 'add'
    }
  },
  emits: [
    'search',
    'filter',
    'page-change',
    'selection-change',
    'action',
    'refresh',
    // 表单相关事件
    'form-submit',
    'form-cancel',
    'form-reset',
    'update:showFormDialog',
    'update:formData'
  ],
  setup(props, { emit }) {
    const { t } = useI18n()
    const { hasPermission } = usePermissions()

    // 响应式数据
    const searchKeyword = ref('')
    const filterValues = reactive({})
    const selectedRows = ref([])
    const currentPage = ref(1)
    const pageSize = ref(props.config.pagination?.defaultPageSize || 20)

    // 表单对话框相关状态
    const formDialogVisible = ref(false)

    // 搜索处理（防抖）
    let searchTimer = null
    const handleSearch = () => {
      clearTimeout(searchTimer)
      searchTimer = setTimeout(() => {
        currentPage.value = 1
        emitSearchFilter()
      }, 300)
    }

    // 筛选处理
    const handleFilter = () => {
      currentPage.value = 1
      emitSearchFilter()
    }

    // 发送搜索和筛选事件
    const emitSearchFilter = () => {
      const params = {
        keyword: searchKeyword.value,
        filters: { ...filterValues },
        page: currentPage.value,
        pageSize: pageSize.value
      }
      emit('search', params)
    }

    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      emitPageChange()
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
      emitPageChange()
    }

    const emitPageChange = () => {
      const params = {
        keyword: searchKeyword.value,
        filters: { ...filterValues },
        page: currentPage.value,
        pageSize: pageSize.value
      }
      emit('page-change', params)
    }

    // 选择处理
    const handleSelectionChange = (selection) => {
      selectedRows.value = selection
      emit('selection-change', selection)
    }

    // 批量操作处理
    const handleBatchAction = async (action) => {
      if (action.confirm) {
        try {
          await ElMessageBox.confirm(
            action.confirm.replace('{count}', selectedRows.value.length),
            t('common.confirm'),
            { type: 'warning' }
          )
        } catch {
          return
        }
      }
      emit('action', { action: action.key, row: null, rows: selectedRows.value })
    }

    // 清除选择
    const clearSelection = () => {
      selectedRows.value = []
      emit('selection-change', [])
    }

    // 头部操作处理
    const handleHeaderAction = async (action) => {
      if (action.confirm) {
        try {
          await ElMessageBox.confirm(action.confirm, t('common.confirm'), {
            type: 'warning'
          })
        } catch {
          return
        }
      }
      emit('action', { action: action.key, row: null, rows: selectedRows.value })
    }

    // 表格行操作处理
    const handleAction = async (action, row) => {
      if (action.confirm) {
        try {
          await ElMessageBox.confirm(action.confirm, t('common.confirm'), {
            type: 'warning'
          })
        } catch {
          return
        }
      }
      emit('action', { action: action.key, row, rows: selectedRows.value })
    }

    // 刷新
    const handleRefresh = () => {
      emit('refresh')
    }

    // 获取列值
    const getColumnValue = (row, column) => {
      const keys = column.key.split('.')
      let value = row
      for (const key of keys) {
        value = value?.[key]
      }
      return value
    }

    // 表单对话框处理方法
    const handleFormSubmit = (formData) => {
      emit('form-submit', formData)
    }

    const handleFormCancel = () => {
      emit('form-cancel')
      formDialogVisible.value = false
    }

    const handleFormReset = () => {
      emit('form-reset')
    }

    // 监听表单对话框显示状态
    watch(() => props.showFormDialog, (newVal) => {
      formDialogVisible.value = newVal
    })

    watch(formDialogVisible, (newVal) => {
      emit('update:showFormDialog', newVal)
    })

    return {
      searchKeyword,
      filterValues,
      selectedRows,
      currentPage,
      pageSize,
      handleSearch,
      handleFilter,
      handleSizeChange,
      handleCurrentChange,
      handleSelectionChange,
      handleBatchAction,
      clearSelection,
      handleHeaderAction,
      handleAction,
      handleRefresh,
      getColumnValue,
      hasPermission,
      t,
      // 表单对话框相关
      formDialogVisible,
      handleFormSubmit,
      handleFormCancel,
      handleFormReset
    }
  }
}
</script>

<style scoped>
.admin-table {
  padding: 20px;
}

/* 页面头部 */
.page-header {
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  display: flex;
  align-items: center;
}

.header-info .el-icon {
  font-size: 32px;
  margin-right: 16px;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.breadcrumb {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}

.breadcrumb .el-icon {
  margin: 0 8px;
  font-size: 14px;
}

.description {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .el-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .el-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

/* 操作栏 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-section {
  display: flex;
  align-items: center;
}

.button-section {
  display: flex;
  gap: 10px;
}

/* 统计卡片 */
.stats-section {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  color: #fff;
}

.stat-icon.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.green {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.orange {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.purple {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-icon.red {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

/* 表格卡片 */
.table-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.card-title .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.card-extra {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.total-count {
  font-weight: 500;
}

/* 表格容器 */
.table-container {
  margin-top: 16px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-buttons .el-button {
  padding: 4px 8px;
}

/* 批量操作 */
.batch-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 20px;
}

.batch-info {
  color: #495057;
  font-size: 14px;
  font-weight: 500;
}

.batch-buttons {
  display: flex;
  gap: 8px;
}

.batch-buttons .el-button {
  padding: 6px 12px;
  font-size: 13px;
}

/* 分页 */
.pagination-section {
  margin-top: 24px;
  padding: 20px;
  display: flex;
  justify-content: center;
  border-top: 1px solid #ebeef5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-table {
    padding: 10px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .action-bar {
    flex-direction: column;
    gap: 16px;
  }

  .search-section {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }

  .search-section .el-input,
  .search-section .el-select {
    width: 100% !important;
    margin-left: 0 !important;
  }
}
</style>
