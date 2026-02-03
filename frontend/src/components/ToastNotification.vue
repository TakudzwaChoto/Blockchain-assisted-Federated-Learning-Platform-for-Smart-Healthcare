<template>
  <transition name="toast" appear>
    <div
      v-if="visible"
      :class="['toast', `toast-${type}`]"
      @click="handleClick"
    >
      <div class="toast-icon">
        <el-icon v-if="type === 'success'"><Check /></el-icon>
        <el-icon v-else-if="type === 'error'"><Close /></el-icon>
        <el-icon v-else-if="type === 'warning'"><Warning /></el-icon>
        <el-icon v-else><InfoFilled /></el-icon>
      </div>
      <div class="toast-content">
        <div class="toast-title" v-if="title">{{ title }}</div>
        <div class="toast-message">{{ message }}</div>
      </div>
      <div class="toast-close" @click.stop="close">
        <el-icon><Close /></el-icon>
      </div>
      <div class="toast-progress" :style="{ width: `${progress}%` }"></div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Check, Close, Warning, InfoFilled } from '@element-plus/icons-vue'

const props = defineProps({
  id: { type: String, required: true },
  type: { type: String, default: 'info', validator: (value) => ['success', 'error', 'warning', 'info'].includes(value) },
  title: { type: String, default: '' },
  message: { type: String, required: true },
  duration: { type: Number, default: 4000 },
  closable: { type: Boolean, default: true },
  onClick: { type: Function, default: null }
})

const emit = defineEmits(['close'])

const visible = ref(true)
const progress = ref(100)
let timer = null
let progressTimer = null

const close = () => {
  visible.value = false
  emit('close', props.id)
}

const handleClick = () => {
  if (props.onClick) {
    props.onClick()
  }
  if (props.closable) {
    close()
  }
}

const startTimer = () => {
  if (props.duration > 0) {
    const interval = 50
    const decrement = (100 / (props.duration / interval))
    
    progressTimer = setInterval(() => {
      progress.value -= decrement
      if (progress.value <= 0) {
        close()
      }
    }, interval)
  }
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
  if (progressTimer) clearInterval(progressTimer)
})
</script>

<style scoped>
.toast {
  position: relative;
  display: flex;
  align-items: flex-start;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 400px;
}

.toast:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.toast-success {
  border-left: 4px solid #67c23a;
}

.toast-error {
  border-left: 4px solid #f56c6c;
}

.toast-warning {
  border-left: 4px solid #e6a23c;
}

.toast-info {
  border-left: 4px solid #409eff;
}

.toast-icon {
  margin-right: 12px;
  font-size: 20px;
}

.toast-success .toast-icon {
  color: #67c23a;
}

.toast-error .toast-icon {
  color: #f56c6c;
}

.toast-warning .toast-icon {
  color: #e6a23c;
}

.toast-info .toast-icon {
  color: #409eff;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: #303133;
}

.toast-message {
  color: #606266;
  font-size: 14px;
  line-height: 1.4;
}

.toast-close {
  margin-left: 12px;
  color: #909399;
  cursor: pointer;
  transition: color 0.3s;
}

.toast-close:hover {
  color: #606266;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: currentColor;
  opacity: 0.3;
  transition: width 0.05s linear;
}

.toast-success .toast-progress {
  color: #67c23a;
}

.toast-error .toast-progress {
  color: #f56c6c;
}

.toast-warning .toast-progress {
  color: #e6a23c;
}

.toast-info .toast-progress {
  color: #409eff;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
