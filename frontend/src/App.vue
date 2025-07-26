<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* CSS 变量定义 - 参考 ngx-admin 配色 */
:root {
  /* 主色调 */
  --primary-color: #3366ff;
  --primary-light: #598bff;
  --primary-dark: #274bdb;

  /* 成功色 */
  --success-color: #00d68f;
  --success-light: #40e4a6;
  --success-dark: #00b373;

  /* 信息色 */
  --info-color: #0095ff;
  --info-light: #40b3ff;
  --info-dark: #006fd6;

  /* 警告色 */
  --warning-color: #ffaa00;
  --warning-light: #ffbb33;
  --warning-dark: #cc8800;

  /* 危险色 */
  --danger-color: #ff3d71;
  --danger-light: #ff708d;
  --danger-dark: #cc1f5b;

  /* 背景色 */
  --bg-basic-1: #ffffff;
  --bg-basic-2: #f7f9fc;
  --bg-basic-3: #edf1f7;
  --bg-basic-4: #e4e9f2;

  /* 文字色 */
  --text-basic: #2e3a59;
  --text-alternate: #a4abb3;
  --text-control: #73777f;
  --text-disabled: #c5cee0;
  --text-hint: #8f9bb3;

  /* 边框色 */
  --border-basic-1: #edf1f7;
  --border-basic-2: #e4e9f2;
  --border-basic-3: #c5cee0;
  --border-basic-4: #a4abb3;

  /* 阴影 */
  --shadow-1: 0 2px 12px 0 rgba(25, 50, 75, 0.2);
  --shadow-2: 0 4px 20px 0 rgba(25, 50, 75, 0.1);
  --shadow-3: 0 8px 30px 0 rgba(25, 50, 75, 0.08);

  /* 侧边栏 */
  --sidebar-bg: #ffffff;
  --sidebar-text: #2e3a59;
  --sidebar-text-active: #3366ff;
  --sidebar-item-hover: #f7f9fc;
  --sidebar-item-active: #edf4ff;

  /* 顶部栏 */
  --header-bg: #ffffff;
  --header-text: #2e3a59;
  --header-border: #edf1f7;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: var(--bg-basic-2);
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-basic);
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-basic-2);
}

/* Element Plus 主题覆盖 */
.el-container {
  height: 100vh !important;
  background-color: var(--bg-basic-2);
}

.el-aside {
  height: 100vh !important;
  background-color: var(--sidebar-bg) !important;
  border-right: 1px solid var(--border-basic-1);
  box-shadow: var(--shadow-1);
}

.el-main {
  height: calc(100vh - 70px) !important;
  overflow-y: auto !important;
  background-color: var(--bg-basic-2);
  padding: 24px;
}

.el-header {
  background-color: var(--header-bg) !important;
  border-bottom: 1px solid var(--header-border) !important;
  box-shadow: var(--shadow-2) !important;
  height: 70px !important;
  line-height: 70px !important;
}

/* 卡片样式 */
.el-card {
  border: 1px solid var(--border-basic-1);
  box-shadow: var(--shadow-2);
  border-radius: 12px;
  background-color: var(--bg-basic-1);
}

.el-card__header {
  background-color: var(--bg-basic-1);
  border-bottom: 1px solid var(--border-basic-1);
  padding: 20px 24px;
}

.el-card__body {
  padding: 24px;
}

/* 按钮样式 */
.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: #ffffff;
}

.el-button--primary:hover {
  background-color: var(--primary-light);
  border-color: var(--primary-light);
}

.el-button--success {
  background-color: var(--success-color);
  border-color: var(--success-color);
}

.el-button--success:hover {
  background-color: var(--success-light);
  border-color: var(--success-light);
}

.el-button--warning {
  background-color: var(--warning-color);
  border-color: var(--warning-color);
}

.el-button--warning:hover {
  background-color: var(--warning-light);
  border-color: var(--warning-light);
}

.el-button--danger {
  background-color: var(--danger-color);
  border-color: var(--danger-color);
}

.el-button--danger:hover {
  background-color: var(--danger-light);
  border-color: var(--danger-light);
}

/* 表格样式 */
.el-table {
  background-color: var(--bg-basic-1);
  border: 1px solid var(--border-basic-1);
  border-radius: 12px;
  overflow: hidden;
}

.el-table th.el-table__cell {
  background-color: var(--bg-basic-2);
  color: var(--text-basic);
  font-weight: 600;
  border-bottom: 1px solid var(--border-basic-1);
}

.el-table td.el-table__cell {
  border-bottom: 1px solid var(--border-basic-1);
}

.el-table__row:hover > td {
  background-color: var(--bg-basic-2) !important;
}

/* 表单样式 */
.el-input__wrapper {
  border: 1px solid var(--border-basic-2);
  border-radius: 8px;
  background-color: var(--bg-basic-1);
}

.el-input__wrapper:hover {
  border-color: var(--border-basic-3);
}

.el-input__wrapper.is-focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(51, 102, 255, 0.1);
}

/* 标签样式 */
.el-tag {
  border-radius: 6px;
  font-weight: 500;
}

.el-tag--success {
  background-color: rgba(0, 214, 143, 0.1);
  border-color: var(--success-color);
  color: var(--success-dark);
}

.el-tag--danger {
  background-color: rgba(255, 61, 113, 0.1);
  border-color: var(--danger-color);
  color: var(--danger-dark);
}

.el-tag--info {
  background-color: rgba(164, 171, 179, 0.1);
  border-color: var(--text-alternate);
  color: var(--text-control);
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: var(--bg-basic-3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: var(--border-basic-3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--border-basic-4);
}

/* Firefox 滚动条 */
* {
  scrollbar-width: thin;
  scrollbar-color: var(--border-basic-3) var(--bg-basic-3);
}

/* 对话框样式 */
.el-dialog {
  border-radius: 12px;
  box-shadow: var(--shadow-3);
}

.el-dialog__header {
  background-color: var(--bg-basic-1);
  border-bottom: 1px solid var(--border-basic-1);
  padding: 20px 24px;
}

.el-dialog__body {
  padding: 24px;
}

/* 消息提示样式 */
.el-message {
  border-radius: 8px;
  box-shadow: var(--shadow-2);
}

.el-message--success {
  background-color: rgba(0, 214, 143, 0.1);
  border-color: var(--success-color);
  color: var(--success-dark);
}

.el-message--error {
  background-color: rgba(255, 61, 113, 0.1);
  border-color: var(--danger-color);
  color: var(--danger-dark);
}

.el-message--warning {
  background-color: rgba(255, 170, 0, 0.1);
  border-color: var(--warning-color);
  color: var(--warning-dark);
}

.el-message--info {
  background-color: rgba(0, 149, 255, 0.1);
  border-color: var(--info-color);
  color: var(--info-dark);
}

/* 自定义 MessageBox 样式 */
.el-message-box {
  border-radius: 16px !important;
  box-shadow: var(--shadow-3) !important;
  border: 1px solid var(--border-basic-1) !important;
  background-color: var(--bg-basic-1) !important;
}

.el-message-box__header {
  background-color: var(--bg-basic-1) !important;
  border-bottom: 1px solid var(--border-basic-1) !important;
  padding: 20px 24px 16px 24px !important;
  border-radius: 16px 16px 0 0 !important;
}

.el-message-box__title {
  color: var(--text-basic) !important;
  font-size: 18px !important;
  font-weight: 600 !important;
}

.el-message-box__content {
  padding: 16px 24px 20px 24px !important;
  color: var(--text-basic) !important;
}

.el-message-box__message {
  font-size: 14px !important;
  line-height: 1.6 !important;
  color: var(--text-basic) !important;
}

.el-message-box__btns {
  padding: 16px 24px 24px 24px !important;
  border-top: 1px solid var(--border-basic-1) !important;
  background-color: var(--bg-basic-1) !important;
  border-radius: 0 0 16px 16px !important;
}

.el-message-box__btns .el-button {
  border-radius: 8px !important;
  font-weight: 500 !important;
  padding: 10px 20px !important;
}

.el-message-box__btns .el-button--primary {
  background-color: var(--primary-color) !important;
  border-color: var(--primary-color) !important;
}

.el-message-box__btns .el-button--primary:hover {
  background-color: var(--primary-light) !important;
  border-color: var(--primary-light) !important;
}

.el-message-box__btns .el-button--default {
  background-color: var(--bg-basic-2) !important;
  border-color: var(--border-basic-2) !important;
  color: var(--text-basic) !important;
}

.el-message-box__btns .el-button--default:hover {
  background-color: var(--bg-basic-3) !important;
  border-color: var(--border-basic-3) !important;
}

/* 警告图标样式 */
.el-message-box__status.el-icon {
  color: var(--warning-color) !important;
  font-size: 24px !important;
}

/* 遮罩层样式 */
.el-overlay {
  background-color: rgba(0, 0, 0, 0.3) !important;
  backdrop-filter: blur(4px) !important;
}
</style>
