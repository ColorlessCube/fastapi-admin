/**
 * 时间格式化组合式函数
 * 提供统一的时间格式化功能
 */
import { 
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
} from '../utils/datetime'

/**
 * 时间格式化组合式函数
 * @returns {object} 时间格式化方法集合
 */
export function useDateTime() {
  return {
    // 基础格式化方法
    formatDateTime,
    formatDate,
    formatTime,
    formatRelativeTime,
    formatSmartDateTime,
    formatTimestamp,
    
    // 工具方法
    getTimezoneInfo,
    utcToLocal,
    isToday,
    isYesterday,
    
    // 便捷方法
    /**
     * 格式化创建时间（常用于表格显示）
     * @param {string} utcTimeString - UTC时间字符串
     * @returns {string} 格式化后的时间字符串
     */
    formatCreatedAt: (utcTimeString) => formatDateTime(utcTimeString),
    
    /**
     * 格式化更新时间（常用于表格显示）
     * @param {string} utcTimeString - UTC时间字符串
     * @returns {string} 格式化后的时间字符串
     */
    formatUpdatedAt: (utcTimeString) => formatDateTime(utcTimeString),
    
    /**
     * 格式化列表时间（智能显示）
     * @param {string} utcTimeString - UTC时间字符串
     * @returns {string} 智能格式化的时间字符串
     */
    formatListTime: (utcTimeString) => formatSmartDateTime(utcTimeString),
    
    /**
     * 获取时区显示信息
     * @returns {string} 时区显示字符串
     */
    getTimezoneDisplay: () => {
      const info = getTimezoneInfo()
      return `${info.name} (${info.offsetString})`
    }
  }
}

// 默认导出
export default useDateTime
