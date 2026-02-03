<template>
  <div v-if="canAccess">
    <slot />
  </div>
  <div v-else class="access-denied">
    <el-result
      icon="warning"
      title="访问被拒绝"
      :sub-title="message"
    >
      <template #extra>
        <el-button type="primary" @click="$router.push('/user/dashboard')">
          返回个人工作台
        </el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/authStore'

const props = defineProps({
  roles: {
    type: Array,
    default: () => []
  },
  permissions: {
    type: Array,
    default: () => []
  },
  requireAuth: {
    type: Boolean,
    default: true
  },
  fallbackMessage: {
    type: String,
    default: ''
  }
})

const authStore = useAuthStore()

const canAccess = computed(() => {
  // Check if authentication is required
  if (props.requireAuth && !authStore.isAuthenticated) {
    return false
  }

  // Check role requirements
  if (props.roles.length > 0) {
    const hasRequiredRole = props.roles.some(role => authStore.userRole === role)
    if (!hasRequiredRole) {
      return false
    }
  }

  // Check permission requirements
  if (props.permissions.length > 0) {
    const hasRequiredPermission = props.permissions.some(permission => 
      authStore.hasPermission(permission)
    )
    if (!hasRequiredPermission) {
      return false
    }
  }

  return true
})

const message = computed(() => {
  if (props.fallbackMessage) {
    return props.fallbackMessage
  }

  if (!authStore.isAuthenticated && props.requireAuth) {
    return '请先登录以访问此页面'
  }

  if (props.roles.length > 0 && !props.roles.includes(authStore.userRole)) {
    return `您的角色 (${authStore.userRole}) 无权访问此页面`
  }

  if (props.permissions.length > 0) {
    const missingPermissions = props.permissions.filter(permission => 
      !authStore.hasPermission(permission)
    )
    return `您缺少以下权限: ${missingPermissions.join(', ')}`
  }

  return '访问被拒绝'
})
</script>

<style scoped>
.access-denied {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  background: #f5f7fa;
}
</style>
