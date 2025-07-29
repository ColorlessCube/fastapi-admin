<template>
  <div class="admin-table-cell">
    <!-- 文本类型 -->
    <span v-if="!column.type || column.type === 'text'">
      {{ formattedValue }}
    </span>

    <!-- 状态类型 -->
    <el-tag 
      v-else-if="column.type === 'status'"
      :type="getStatusType(value)"
      size="small"
    >
      {{ formattedValue }}
    </el-tag>

    <!-- 标签数组类型 -->
    <div v-else-if="column.type === 'tags'" class="tags-container">
      <el-tag
        v-for="(tag, index) in getTagsArray()"
        :key="index"
        size="small"
        :type="getTagType(tag, index)"
        style="margin-right: 4px; margin-bottom: 2px;"
      >
        {{ tag }}
      </el-tag>
    </div>

    <!-- 日期时间类型 -->
    <div v-else-if="column.type === 'datetime'" class="datetime-container">
      <div class="datetime-main">{{ formatDateTime(value) }}</div>
      <div class="datetime-relative">{{ formatRelativeTime(value) }}</div>
    </div>

    <!-- 数字类型 -->
    <span v-else-if="column.type === 'number'" class="number-value">
      {{ formatNumber(value) }}
    </span>

    <!-- 布尔类型 -->
    <el-tag 
      v-else-if="column.type === 'boolean'"
      :type="value ? 'success' : 'info'"
      size="small"
    >
      {{ value ? $t('common.yes') : $t('common.no') }}
    </el-tag>

    <!-- JSON类型 -->
    <div v-else-if="column.type === 'json'" class="json-container">
      <el-popover
        placement="top"
        :width="300"
        trigger="hover"
        :content="formatJson(value)"
      >
        <template #reference>
          <el-tag size="small" type="info">JSON</el-tag>
        </template>
      </el-popover>
    </div>

    <!-- 链接类型 -->
    <el-link 
      v-else-if="column.type === 'link'"
      :href="getLinkHref()"
      :type="column.linkType || 'primary'"
      target="_blank"
    >
      {{ formattedValue }}
    </el-link>

    <!-- 图片类型 -->
    <el-image
      v-else-if="column.type === 'image'"
      :src="value"
      :style="{ width: column.imageWidth || '40px', height: column.imageHeight || '40px' }"
      fit="cover"
      :preview-src-list="[value]"
    />

    <!-- 进度条类型 -->
    <el-progress
      v-else-if="column.type === 'progress'"
      :percentage="getProgressValue()"
      :status="getProgressStatus()"
      :stroke-width="6"
    />

    <!-- 自定义渲染 -->
    <div v-else-if="column.type === 'custom'">
      <slot :name="`column-${column.key}`" :row="row" :value="value" :column="column">
        {{ formattedValue }}
      </slot>
    </div>

    <!-- 默认文本 -->
    <span v-else>
      {{ formattedValue }}
    </span>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { formatDateTime, formatRelativeTime } from '../utils/datetime'

export default {
  name: 'AdminTableCell',
  props: {
    value: {
      type: [String, Number, Boolean, Array, Object],
      default: null
    },
    column: {
      type: Object,
      required: true
    },
    row: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const { t } = useI18n()

    // 格式化后的值
    const formattedValue = computed(() => {
      if (props.value === null || props.value === undefined) {
        return props.column.defaultValue || '-'
      }

      if (props.column.formatter && typeof props.column.formatter === 'function') {
        return props.column.formatter(props.value, props.row)
      }

      return props.value
    })

    // 获取状态类型
    const getStatusType = (value) => {
      if (props.column.statusMap) {
        return props.column.statusMap[value] || 'info'
      }
      
      // 默认状态映射
      if (typeof value === 'boolean') {
        return value ? 'success' : 'danger'
      }
      
      if (typeof value === 'string') {
        const lowerValue = value.toLowerCase()
        if (['active', 'enabled', 'success', '活跃', '启用', '成功'].includes(lowerValue)) {
          return 'success'
        }
        if (['inactive', 'disabled', 'error', '非活跃', '禁用', '错误'].includes(lowerValue)) {
          return 'danger'
        }
        if (['pending', 'warning', '待处理', '警告'].includes(lowerValue)) {
          return 'warning'
        }
      }
      
      return 'info'
    }

    // 获取标签数组
    const getTagsArray = () => {
      if (Array.isArray(formattedValue.value)) {
        return formattedValue.value
      }
      if (typeof formattedValue.value === 'string') {
        return formattedValue.value.split(',').map(s => s.trim()).filter(Boolean)
      }
      return []
    }

    // 获取标签类型
    const getTagType = (tag, index) => {
      if (props.column.tagTypes && props.column.tagTypes[tag]) {
        return props.column.tagTypes[tag]
      }
      
      // 循环使用不同颜色
      const types = ['', 'success', 'info', 'warning', 'danger']
      return types[index % types.length]
    }

    // 格式化数字
    const formatNumber = (value) => {
      if (typeof value !== 'number') return value
      
      if (props.column.numberFormat) {
        return new Intl.NumberFormat(props.column.numberFormat.locale || 'zh-CN', 
          props.column.numberFormat.options || {}
        ).format(value)
      }
      
      return value.toLocaleString()
    }

    // 格式化JSON
    const formatJson = (value) => {
      try {
        if (typeof value === 'string') {
          return JSON.stringify(JSON.parse(value), null, 2)
        }
        return JSON.stringify(value, null, 2)
      } catch {
        return String(value)
      }
    }

    // 获取链接地址
    const getLinkHref = () => {
      if (props.column.linkHref) {
        if (typeof props.column.linkHref === 'function') {
          return props.column.linkHref(props.value, props.row)
        }
        return props.column.linkHref
      }
      return props.value
    }

    // 获取进度值
    const getProgressValue = () => {
      if (typeof props.value === 'number') {
        return Math.min(100, Math.max(0, props.value))
      }
      return 0
    }

    // 获取进度状态
    const getProgressStatus = () => {
      const value = getProgressValue()
      if (value >= 100) return 'success'
      if (value >= 80) return ''
      if (value >= 60) return 'warning'
      return 'exception'
    }

    return {
      formattedValue,
      getStatusType,
      getTagsArray,
      getTagType,
      formatNumber,
      formatJson,
      getLinkHref,
      getProgressValue,
      getProgressStatus,
      formatDateTime,
      formatRelativeTime,
      t
    }
  }
}
</script>

<style scoped>
.admin-table-cell {
  display: flex;
  align-items: center;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.datetime-container {
  display: flex;
  flex-direction: column;
}

.datetime-main {
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.datetime-relative {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 2px;
}

.number-value {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-weight: 500;
}

.json-container {
  cursor: pointer;
}
</style>
