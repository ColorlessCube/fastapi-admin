<template>
  <el-dialog
    :model-value="visible"
    :width="config.width || '600px'"
    :show-close="false"
    class="form-dialog"
    @update:model-value="$emit('update:visible', $event)"
    @close="handleCancel"
  >
    <template #header>
      <div class="form-dialog-header">
        <div class="header-left">
          <div class="form-avatar">
            <el-icon>
              <component :is="config.icon" />
            </el-icon>
          </div>
          <div class="header-info">
            <h3 class="form-title">{{ computedTitle }}</h3>
            <p class="form-description">{{ config.description }}</p>
          </div>
        </div>
        <div class="header-right">
          <el-button 
            type="info" 
            :icon="Close" 
            circle 
            size="small"
            @click="handleCancel"
          />
        </div>
      </div>
    </template>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="auto"
    >
      <template v-for="field in visibleFields" :key="field.field">
        <!-- 文本输入框 -->
        <el-form-item
          v-if="field.type === 'input'"
          :label="field.label"
          :prop="field.field"
        >
          <el-input
            v-model="formData[field.field]"
            :placeholder="field.placeholder"
            :disabled="field.disabled"
            v-bind="field.props"
          />
        </el-form-item>

        <!-- 多行文本 -->
        <el-form-item
          v-else-if="field.type === 'textarea'"
          :label="field.label"
          :prop="field.field"
        >
          <el-input
            v-model="formData[field.field]"
            type="textarea"
            :placeholder="field.placeholder"
            :disabled="field.disabled"
            v-bind="field.props"
          />
        </el-form-item>

        <!-- 下拉选择 -->
        <el-form-item
          v-else-if="field.type === 'select'"
          :label="field.label"
          :prop="field.field"
        >
          <el-select
            v-model="formData[field.field]"
            :placeholder="field.placeholder"
            :disabled="field.disabled"
            v-bind="field.props"
          >
            <el-option
              v-for="option in getFieldOptions(field)"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>

        <!-- 开关 -->
        <el-form-item
          v-else-if="field.type === 'switch'"
          :label="field.label"
          :prop="field.field"
        >
          <el-switch
            v-model="formData[field.field]"
            :disabled="field.disabled"
            v-bind="field.props"
          />
        </el-form-item>

        <!-- 复选框组 -->
        <el-form-item
          v-else-if="field.type === 'checkbox-group'"
          :label="field.label"
          :prop="field.field"
        >
          <el-checkbox-group
            v-model="formData[field.field]"
            :disabled="field.disabled"
            v-bind="field.props"
          >
            <el-checkbox
              v-for="option in getFieldOptions(field)"
              :key="option.value"
              :label="option.value"
            >
              {{ option.label }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <!-- 数字输入 -->
        <el-form-item
          v-else-if="field.type === 'number'"
          :label="field.label"
          :prop="field.field"
        >
          <el-input-number
            v-model="formData[field.field]"
            :placeholder="field.placeholder"
            :disabled="field.disabled"
            v-bind="field.props"
          />
        </el-form-item>

        <!-- 自定义插槽 -->
        <el-form-item
          v-else-if="field.type === 'slot'"
          :label="field.label"
          :prop="field.field"
          :class="{ 'full-width-slot': field.fullWidth }"
        >
          <slot :name="field.field" :field="field" :form-data="formData" />
        </el-form-item>
      </template>
    </el-form>

    <template #footer>
      <div class="form-dialog-footer">
        <div class="footer-info">
          <el-icon><InfoFilled /></el-icon>
          <span>{{ config.footerNote || t('common.formNote') }}</span>
        </div>
        <div class="footer-actions">
          <el-button 
            size="large"
            @click="handleCancel"
          >
            {{ config.cancelText || t('common.cancel') }}
          </el-button>
          <el-button 
            type="primary" 
            size="large"
            @click="handleSubmit" 
            :loading="loading"
            :icon="Check"
          >
            {{ config.submitText || t('common.confirm') }}
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  Close,
  Check,
  InfoFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  config: {
    type: Object,
    required: true
  },
  formData: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'add' // add, edit
  }
})

const emit = defineEmits(['update:visible', 'submit', 'cancel', 'reset'])

const { t } = useI18n()
const formRef = ref()

// 计算标题
const computedTitle = computed(() => {
  if (typeof props.config.title === 'function') {
    return props.config.title(props.mode, props.formData)
  }
  return props.config.title
})

// 计算可见字段
const visibleFields = computed(() => {
  return props.config.fields?.filter(field => {
    if (typeof field.visible === 'function') {
      return field.visible(props.formData, props.mode)
    }
    return field.visible !== false
  }) || []
})

// 计算表单验证规则
const formRules = computed(() => {
  const rules = {}
  visibleFields.value.forEach(field => {
    if (field.rules) {
      rules[field.field] = field.rules
    } else if (field.required) {
      rules[field.field] = [
        { required: true, message: `${field.label} is required`, trigger: 'blur' }
      ]
    }
  })
  return rules
})

// 获取字段选项
const getFieldOptions = (field) => {
  if (typeof field.options === 'function') {
    return field.options(props.formData, props.mode)
  }
  return field.options || []
}

// 处理提交
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    emit('submit', { ...props.formData })
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}

// 处理取消
const handleCancel = () => {
  emit('cancel')
  emit('update:visible', false)
}

// 重置表单
const resetForm = () => {
  nextTick(() => {
    formRef.value?.resetFields()
    emit('reset')
  })
}

// 监听对话框显示状态
watch(() => props.visible, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})

defineExpose({
  resetForm,
  validate: () => formRef.value?.validate(),
  clearValidate: () => formRef.value?.clearValidate()
})
</script>

<style scoped>
/* 表单对话框样式 */
:deep(.form-dialog) {
  border-radius: 12px;
  box-shadow: var(--shadow-3);
  border: 1px solid var(--border-basic-1);
  overflow: hidden;
}

:deep(.form-dialog .el-dialog__header) {
  padding: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-bottom: none;
  border-radius: 12px;
}

:deep(.form-dialog .el-dialog__body) {
  padding: 24px 32px;
  background-color: var(--bg-basic-1);
  border-radius: 0;
}

:deep(.form-dialog .el-dialog__footer) {
  padding: 0;
  background-color: var(--bg-basic-1);
  border-top: 1px solid var(--border-basic-1);
  border-radius: 0;
}

/* 对话框头部 */
.form-dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  border-radius: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.form-avatar {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.header-info {
  flex: 1;
}

.form-title {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-description {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 400;
  line-height: 1.5;
}

.header-right .el-button {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
}

.header-right .el-button:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

/* 表单样式优化 */
:deep(.form-dialog .el-form) {
  margin-top: 8px;
}

:deep(.form-dialog .el-form-item) {
  margin-bottom: 24px;
}

:deep(.form-dialog .el-form-item__label) {
  font-weight: 500;
  color: var(--text-basic);
}

:deep(.form-dialog .el-input__wrapper) {
  border-radius: 6px;
}

:deep(.form-dialog .el-textarea__inner) {
  border-radius: 6px;
}

:deep(.form-dialog .el-select) {
  width: 100%;
}

:deep(.form-dialog .el-select .el-input__wrapper) {
  border-radius: 6px;
}

/* 全宽插槽样式 */
:deep(.form-dialog .full-width-slot) {
  margin-bottom: 0;
}

:deep(.form-dialog .full-width-slot .el-form-item__content) {
  width: 100%;
  margin-left: 0 !important;
}

:deep(.form-dialog .full-width-slot .el-form-item__label) {
  display: none;
}

/* 对话框底部 */
.form-dialog-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 32px;
  background: var(--bg-basic-1);
  border-top: 1px solid var(--border-basic-1);
}

.footer-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-alternate);
  font-size: 13px;
  flex: 1;
  text-align: left;
  margin-right: 24px;
}

.footer-info .el-icon {
  color: var(--info-color);
}

.footer-actions {
  display: flex;
  gap: 12px;
}

.footer-actions .el-button {
  border-radius: 6px;
  font-weight: 500;
  padding: 12px 24px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-dialog-header {
    padding: 20px 24px;
  }
  
  .form-title {
    font-size: 20px;
  }
  
  :deep(.form-dialog .el-dialog__body) {
    padding: 20px 24px;
  }
  
  .form-dialog-footer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    padding: 20px 24px;
  }
  
  .footer-actions {
    justify-content: stretch;
  }
  
  .footer-actions .el-button {
    flex: 1;
  }
}
</style>
