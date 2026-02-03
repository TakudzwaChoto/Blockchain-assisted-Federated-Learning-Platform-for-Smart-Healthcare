<template>
  <teleport to="body">
    <div class="toast-container">
      <ToastNotification
        v-for="notification in notifications"
        :key="notification.id"
        v-bind="notification"
        @close="removeNotification"
      />
    </div>
  </teleport>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useNotificationStore } from '../stores/notificationStore'
import ToastNotification from './ToastNotification.vue'

const notificationStore = useNotificationStore()
const { notifications } = storeToRefs(notificationStore)
const { removeNotification } = notificationStore
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: none;
}

.toast-container > * {
  pointer-events: auto;
}
</style>
