<template>
  <div id="app">
    <div v-if="debug" style="background: red; color: white; padding: 20px;">
      DEBUG: App is loading...
    </div>
    <router-view />
    <ToastContainer />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ToastContainer from './components/ToastContainer.vue'

const debug = ref(false)

onMounted(() => {
  console.log('App component mounted')
  debug.value = false
})
</script>

<style>
/* Global styles for professional appearance */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
  color: #303133;
}

#app {
  min-height: 100vh;
}

/* Enhanced KPI Cards */
.kpi-section {
  margin-bottom: 24px;
}

.enhanced-kpi-card {
  position: relative;
  overflow: hidden;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.enhanced-kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.kpi-content {
  text-align: center;
  margin-bottom: 16px;
}

.kpi-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.kpi-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.kpi-change {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.kpi-up .kpi-change {
  color: #67c23a;
}

.kpi-down .kpi-change {
  color: #f56c6c;
}

.kpi-sparkline {
  height: 40px;
  border-radius: 4px;
}

.sparkline {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

/* Charts Section */
.charts-section {
  margin-bottom: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.chart-content {
  padding: 16px 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Smooth transitions */
* {
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

/* Card hover effects */
.el-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* Button improvements */
.el-button {
  font-weight: 500;
}

.el-button--primary {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border: none;
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #66b1ff 0%, #409eff 100%);
}

/* Table improvements */
.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-table th {
  background-color: #f8f9fa !important;
  font-weight: 600;
}

/* Form improvements */
.el-form-item__label {
  font-weight: 500;
  color: #606266;
}

/* Input improvements */
.el-input__inner:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

/* Select improvements */
.el-select .el-input.is-focus .el-input__inner {
  border-color: #409eff;
}

/* Date picker improvements */
.el-date-editor.el-input {
  width: 100%;
}

/* Slider improvements */
.el-slider__runway {
  background-color: #e4e7ed;
}

.el-slider__bar {
  background: linear-gradient(90deg, #409eff 0%, #66b1ff 100%);
}

.el-slider__button {
  border-color: #409eff;
}

/* Card improvements */
.el-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.el-card__header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e4e7ed;
  font-weight: 600;
}

/* Dropdown improvements */
.el-dropdown-menu {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.el-dropdown-menu__item:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

/* Dialog improvements */
.el-dialog {
  border-radius: 12px;
  overflow: hidden;
}

.el-dialog__header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e4e7ed;
}

/* Loading skeleton improvements */
.el-skeleton__item {
  background: linear-gradient(90deg, #f2f2f2 25%, #e6e6e6 50%, #f2f2f2 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Responsive improvements */
@media (max-width: 768px) {
  .el-col {
    margin-bottom: 16px;
  }
  
  .filter-actions {
    flex-direction: column;
    gap: 4px;
  }
  
  .custom-filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .custom-filter-row > * {
    margin-right: 0 !important;
    margin-bottom: 8px;
  }
}

/* Print styles */
@media print {
  .no-print {
    display: none !important;
  }
  
  .el-card {
    box-shadow: none !important;
    border: 1px solid #ccc !important;
  }
  
  .el-button {
    display: none !important;
  }
}
</style>
