/**
 * 时间格式化工具
 * 将UTC时间转换为本地时间并格式化显示
 */

/**
 * 将UTC时间字符串转换为本地时间
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {Date} 本地时间Date对象
 */
export function utcToLocal(utcTimeString) {
  if (!utcTimeString) return null

  // 如果时间字符串没有时区信息，假设它是UTC时间并添加Z后缀
  let timeString = utcTimeString
  if (!timeString.endsWith('Z') && !timeString.includes('+') && !timeString.includes('-', 10)) {
    timeString = timeString + 'Z'
  }

  // 创建Date对象，JavaScript会自动处理UTC到本地时间的转换
  const date = new Date(timeString)

  // 检查日期是否有效
  if (isNaN(date.getTime())) {
    console.warn('Invalid date string:', utcTimeString)
    return null
  }

  return date
}

/**
 * 格式化时间为本地时间字符串
 * @param {string} utcTimeString - UTC时间字符串
 * @param {object} options - 格式化选项
 * @returns {string} 格式化后的本地时间字符串
 */
export function formatDateTime(utcTimeString, options = {}) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return '--'
  
  const defaultOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false // 使用24小时制
  }
  
  const formatOptions = { ...defaultOptions, ...options }
  
  try {
    return localDate.toLocaleString(navigator.language, formatOptions)
  } catch (error) {
    console.warn('Error formatting date:', error)
    return localDate.toLocaleString()
  }
}

/**
 * 格式化日期（不包含时间）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 格式化后的本地日期字符串
 */
export function formatDate(utcTimeString) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return '--'
  
  try {
    return localDate.toLocaleDateString(navigator.language, {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (error) {
    console.warn('Error formatting date:', error)
    return localDate.toLocaleDateString()
  }
}

/**
 * 格式化时间（不包含日期）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 格式化后的本地时间字符串
 */
export function formatTime(utcTimeString) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return '--'
  
  try {
    return localDate.toLocaleTimeString(navigator.language, {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    })
  } catch (error) {
    console.warn('Error formatting time:', error)
    return localDate.toLocaleTimeString()
  }
}

/**
 * 格式化相对时间（如：2小时前）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 相对时间字符串
 */
export function formatRelativeTime(utcTimeString) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return '--'
  
  const now = new Date()
  const diffMs = now.getTime() - localDate.getTime()
  const diffSeconds = Math.floor(diffMs / 1000)
  const diffMinutes = Math.floor(diffSeconds / 60)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)
  
  if (diffSeconds < 60) {
    return '刚刚'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}分钟前`
  } else if (diffHours < 24) {
    return `${diffHours}小时前`
  } else if (diffDays < 7) {
    return `${diffDays}天前`
  } else {
    return formatDate(utcTimeString)
  }
}

/**
 * 获取时区信息
 * @returns {object} 时区信息
 */
export function getTimezoneInfo() {
  const date = new Date()
  const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
  const offset = -date.getTimezoneOffset() / 60
  const offsetString = offset >= 0 ? `+${offset}` : `${offset}`
  
  return {
    timeZone,
    offset,
    offsetString: `UTC${offsetString}`,
    name: timeZone.split('/').pop()
  }
}

/**
 * 格式化时间戳
 * @param {number} timestamp - 时间戳（毫秒）
 * @returns {string} 格式化后的时间字符串
 */
export function formatTimestamp(timestamp) {
  if (!timestamp) return '--'
  
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return '--'
  
  try {
    return date.toLocaleString(navigator.language, {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    })
  } catch (error) {
    console.warn('Error formatting timestamp:', error)
    return date.toLocaleString()
  }
}

/**
 * 检查是否为今天
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {boolean} 是否为今天
 */
export function isToday(utcTimeString) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return false
  
  const today = new Date()
  return localDate.toDateString() === today.toDateString()
}

/**
 * 检查是否为昨天
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {boolean} 是否为昨天
 */
export function isYesterday(utcTimeString) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return false
  
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  return localDate.toDateString() === yesterday.toDateString()
}

/**
 * 智能时间格式化（根据时间远近选择不同格式）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 智能格式化的时间字符串
 */
export function formatSmartDateTime(utcTimeString) {
  const localDate = utcToLocal(utcTimeString)
  if (!localDate) return '--'
  
  if (isToday(utcTimeString)) {
    return `今天 ${formatTime(utcTimeString)}`
  } else if (isYesterday(utcTimeString)) {
    return `昨天 ${formatTime(utcTimeString)}`
  } else {
    return formatDateTime(utcTimeString)
  }
}

// 默认导出常用的格式化函数
export default {
  formatDateTime,
  formatDate,
  formatTime,
  formatRelativeTime,
  formatSmartDateTime,
  formatTimestamp,
  getTimezoneInfo,
  utcToLocal,
  isToday,
  isYesterday
}
