<template>
  <div class="theme-switcher">
    <el-switch
      v-model="isDark"
      :active-icon="Moon"
      :inactive-icon="Sunny"
      active-color="#667eea"
      inactive-color="#f39c12"
      @change="toggleTheme"
    />
    <span class="theme-label">{{ isDark ? 'Dark Mode' : 'Light Mode' }}</span>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Moon, Sunny } from '@element-plus/icons-vue'
const isDark = ref(false)

const toggleTheme = (value) => {
  if (value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<style scoped>
.theme-switcher {
  display: flex;
  align-items: center;
  gap: 8px;
}

.theme-label {
  font-size: 14px;
  color: var(--text-color);
}
</style>
