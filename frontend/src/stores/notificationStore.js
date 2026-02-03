import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref([])
  let nextId = 1

  const addNotification = (options) => {
    const id = `notification-${nextId++}`
    const notification = {
      id,
      type: 'info',
      title: '',
      duration: 4000,
      closable: true,
      ...options
    }

    notifications.value.push(notification)
    return id
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const success = (message, options = {}) => {
    return addNotification({ type: 'success', message, ...options })
  }

  const error = (message, options = {}) => {
    return addNotification({ type: 'error', message, duration: 6000, ...options })
  }

  const warning = (message, options = {}) => {
    return addNotification({ type: 'warning', message, ...options })
  }

  const info = (message, options = {}) => {
    return addNotification({ type: 'info', message, ...options })
  }

  const clear = () => {
    notifications.value = []
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    success,
    error,
    warning,
    info,
    clear
  }
})
