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
    >
      <!-- 角色表单中的权限选择插槽 -->
      <template #permissions>
        <div class="role-permission-tree-container">
          <div class="tree-header">
            <div class="tree-actions">
              <el-button
                  size="small"
                  type="primary"
                  :icon="Plus"
                  @click="expandAllInForm"
              >
                {{ $t('pages.roles.expandAll') }}
              </el-button>
              <el-button
                  size="small"
                  type="info"
                  :icon="Minus"
                  @click="collapseAllInForm"
              >
                {{ $t('pages.roles.collapseAll') }}
              </el-button>
            </div>
          </div>

          <div class="permission-tree">
            <el-tree
                ref="roleFormPermissionTree"
                :data="permissionTreeData"
                :props="{ children: 'children', label: 'label' }"
                show-checkbox
                node-key="id"
                :default-checked-keys="formData.permissions"
                :default-expanded-keys="defaultExpandedKeys"
                @check="handleFormPermissionCheck"
                class="custom-tree"
            />
          </div>
        </div>
      </template>
    </AdminTable>



  </AdminLayout>
</template>
<script>
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {
  Plus,
  Minus
} from '@element-plus/icons-vue'
import AdminLayout from '../components/AdminLayout.vue'
import AdminTable from '../components/AdminTable.vue'
import FormDialog from '../components/FormDialog.vue'
import {createRoleTableConfig} from '../config/tableConfigs.js'
import {createRoleFormConfig, createDefaultFormData} from '../config/formConfigs.js'
import {useAdminTable, createApiHandlers} from '../composables/useAdminTable.js'
import {useI18n} from 'vue-i18n'
import api from '../api'

export default {
  name: 'Roles',
  components: {
    AdminLayout,
    AdminTable,
    FormDialog
  },
  setup() {
    const {t} = useI18n()

    // 表格配置 - 使用计算属性响应语言变化
    const tableConfig = computed(() => createRoleTableConfig(t))

    // 表单对话框相关
    const dialogVisible = ref(false)
    const formMode = ref('add')
    const submitting = ref(false)

    // 权限相关数据
    const roleFormPermissionTree = ref(null) // 角色表单中的权限树
    const selectedPermissions = ref([])
    const permissionTreeData = ref([])

    // 表单配置
    const formConfig = computed(() => createRoleFormConfig(t))

    // 表单数据
    const formData = reactive({
      ...createDefaultFormData(createRoleFormConfig(t)),
      permissions: [] // 添加权限字段
    })

    // API处理器
    const apiHandlers = createApiHandlers(api, '/roles')

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

    // 添加角色
    async function handleAdd() {
      formMode.value = 'add'
      Object.assign(formData, {
        ...createDefaultFormData(createRoleFormConfig(t)),
        permissions: []
      })
      // 加载权限数据用于表单
      await loadPermissions()
      dialogVisible.value = true
    }

    // 编辑角色
    async function handleEdit(role) {
      formMode.value = 'edit'

      // 加载权限数据
      await loadPermissions()

      // 加载角色的权限
      await loadRolePermissions(role.id)

      Object.assign(formData, {
        id: role.id,
        name: role.name,
        description: role.description,
        isActive: role.is_active,
        permissions: selectedPermissions.value // 设置当前角色的权限
      })

      dialogVisible.value = true
    }

    // 删除角色
    const handleDelete = async (role) => {
      try {
        await api.delete(`/roles/${role.id}`)
        ElMessage.success(t('messages.deleteSuccess'))
        await handleRefresh()
      } catch (error) {
        console.error('Failed to delete role:', error)
        ElMessage.error(t('messages.deleteFailed'))
      }
    }



    // 加载权限树
    const loadPermissions = async () => {
      try {
        const response = await api.get('/permissions/')
        const permissions = response.data || response || []

        // 构建权限树结构
        const resourceMap = {}
        permissions.forEach(permission => {
          if (!resourceMap[permission.resource]) {
            resourceMap[permission.resource] = {
              id: permission.resource,
              label: permission.resource,
              children: []
            }
          }
          resourceMap[permission.resource].children.push({
            id: permission.id,
            label: `${permission.name} (${permission.action})`,
            description: permission.description
          })
        })

        permissionTreeData.value = Object.values(resourceMap)
      } catch (error) {
        console.error('Failed to load permissions:', error)
        ElMessage.error(t('messages.loadFailed'))
      }
    }

    // 加载角色权限
    const loadRolePermissions = async (roleId) => {
      try {
        const response = await api.get(`/roles/${roleId}/permissions`)
        const permissions = response.data || response || []
        selectedPermissions.value = permissions.map(p => p.id)
      } catch (error) {
        console.error('Failed to load role permissions:', error)
      }
    }



    // 角色表单中的权限选择处理
    const handleFormPermissionCheck = (data, checked) => {
      if (roleFormPermissionTree.value) {
        const checkedKeys = roleFormPermissionTree.value.getCheckedKeys()
        // 只保存叶子节点（实际权限）的ID
        formData.permissions = checkedKeys.filter(id => typeof id === 'number')
      }
    }

    // 角色表单中展开所有节点
    const expandAllInForm = () => {
      if (roleFormPermissionTree.value) {
        const allKeys = []
        permissionTreeData.value.forEach(category => {
          allKeys.push(category.id)
          if (category.children) {
            category.children.forEach(child => {
              allKeys.push(child.id)
            })
          }
        })
        allKeys.forEach(key => {
          const node = roleFormPermissionTree.value.getNode(key)
          if (node) {
            node.expand()
          }
        })
      }
    }

    // 角色表单中折叠所有节点
    const collapseAllInForm = () => {
      if (roleFormPermissionTree.value) {
        permissionTreeData.value.forEach(category => {
          const node = roleFormPermissionTree.value.getNode(category.id)
          if (node) {
            node.collapse()
          }
        })
      }
    }

    // 表单提交处理
    const handleFormSubmit = async (submitData) => {
      try {
        submitting.value = true

        // 转换字段名以匹配API
        const roleData = {
          name: submitData.name,
          description: submitData.description,
          is_active: submitData.isActive
        }

        if (formMode.value === 'edit') {
          roleData.id = formData.id
          await api.put(`/roles/${roleData.id}`, roleData)

          // 更新权限
          if (submitData.permissions !== undefined) {
            await api.put(`/roles/${roleData.id}/permissions`, {
              permission_ids: submitData.permissions
            })
          }

          ElMessage.success(t('messages.updateSuccess'))
        } else {
          // 创建角色
          const response = await api.post('/roles/', roleData)
          const newRole = response.data || response

          // 如果有选择权限，则分配权限
          if (submitData.permissions && submitData.permissions.length > 0) {
            await api.put(`/roles/${newRole.id}/permissions`, {
              permission_ids: submitData.permissions
            })
          }

          ElMessage.success(t('messages.createSuccess'))
        }

        dialogVisible.value = false
        await handleRefresh()
      } catch (error) {
        console.error('Failed to submit role:', error)
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
      Object.assign(formData, {
        ...createDefaultFormData(createRoleFormConfig(t)),
        permissions: []
      })
    }




    // 默认展开的节点
    const defaultExpandedKeys = computed(() => {
      return permissionTreeData.value.map(item => item.id)
    })



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
      handleFormReset,

      // 权限管理相关
      roleFormPermissionTree,
      selectedPermissions,
      permissionTreeData,
      defaultExpandedKeys,
      handleFormPermissionCheck,
      expandAllInForm,
      collapseAllInForm,

      // 图标
      Plus,
      Minus
    }
  }
}
</script>

<style scoped>

/* 权限树容器 */
.permission-tree-container {
  background: var(--bg-basic-1);
  border-radius: 12px;
  border: 1px solid var(--border-basic-1);
  margin: 0;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  width: 100%;
  min-height: 400px;
}

/* 角色表单中的权限树容器 */
.role-permission-tree-container {
  background: var(--bg-basic-1);
  border-radius: 12px;
  border: 1px solid var(--border-basic-1);
  margin: 0;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  width: 100%;
  min-height: 300px;
}

.tree-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: var(--bg-basic-2);
  border-bottom: 1px solid var(--border-basic-1);
}

.tree-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-basic);
}

.tree-actions {
  display: flex;
  gap: 8px;
}

.tree-actions .el-button {
  border-radius: 6px;
  font-weight: 500;
}

/* 权限树 */
.permission-tree {
  padding: 28px 32px 32px;
  height: 350px;
  overflow-y: auto;
  background: var(--bg-basic-1);
}

/* 自定义树样式 */
:deep(.custom-tree .el-tree-node) {
  margin-bottom: 4px;
}

:deep(.custom-tree .el-tree-node__content) {
  height: 44px;
  padding: 0 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

:deep(.custom-tree .el-tree-node__content:hover) {
  background-color: var(--bg-basic-2);
  border-color: var(--border-basic-2);
}

:deep(.custom-tree .el-tree-node__expand-icon) {
  color: var(--text-alternate);
  font-size: 14px;
}

:deep(.custom-tree .el-tree-node__expand-icon.expanded) {
  color: var(--primary-color);
}

:deep(.custom-tree .el-checkbox) {
  margin-right: 12px;
}

:deep(.custom-tree .el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

:deep(.custom-tree .el-checkbox__input.is-indeterminate .el-checkbox__inner) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

:deep(.custom-tree .el-tree-node__label) {
  font-size: 14px;
  color: var(--text-basic);
  font-weight: 500;
}

/* 父级节点样式 */
:deep(.custom-tree > .el-tree-node > .el-tree-node__content) {
  background: linear-gradient(90deg, var(--bg-basic-2), var(--bg-basic-1));
  border: 1px solid var(--border-basic-1);
  font-weight: 600;
}

:deep(.custom-tree > .el-tree-node > .el-tree-node__content:hover) {
  background: linear-gradient(90deg, var(--bg-basic-3), var(--bg-basic-2));
  border-color: var(--primary-color);
}

:deep(.custom-tree > .el-tree-node > .el-tree-node__content .el-tree-node__label) {
  color: var(--primary-color);
  font-weight: 600;
  font-size: 15px;
}

/* 子级节点样式 */
:deep(.custom-tree .el-tree-node__children .el-tree-node__content) {
  margin-left: 24px;
  background: var(--bg-basic-1);
}

:deep(.custom-tree .el-tree-node__children .el-tree-node__content .el-tree-node__label) {
  color: var(--text-control);
  font-weight: 500;
  font-size: 13px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .tree-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .tree-actions {
    width: 100%;
    justify-content: stretch;
  }

  .tree-actions .el-button {
    flex: 1;
  }

  .permission-tree {
    padding: 24px 20px;
  }
}

/* 滚动条样式 */
.permission-tree::-webkit-scrollbar {
  width: 6px;
}

.permission-tree::-webkit-scrollbar-track {
  background: var(--bg-basic-3);
  border-radius: 3px;
}

.permission-tree::-webkit-scrollbar-thumb {
  background: var(--border-basic-3);
  border-radius: 3px;
}

.permission-tree::-webkit-scrollbar-thumb:hover {
  background: var(--border-basic-4);
}
</style>

