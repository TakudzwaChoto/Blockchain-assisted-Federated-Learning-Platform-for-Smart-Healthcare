import { defineStore } from 'pinia'
import mockDB from '../services/mockDatabase'

const LS_KEY = 'bde.auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),

  getters: {
    userRole: (state) => state.user?.role || null,
    isAdmin: (state) => state.user?.role === 'admin',
    isUser: (state) => state.user?.role === 'user',
    isDoctor: (state) => state.user?.role === 'doctor',
    isGovernment: (state) => state.user?.role === 'government'
  },

  actions: {
    login(credentials) {
      try {
        // Use mock database to find user
        const foundUser = mockDB.findUser(credentials.username, credentials.password)
        
        if (foundUser) {
          // Check if role matches (if provided)
          if (credentials.role && foundUser.role !== credentials.role) {
            return { success: false, error: '账户类型不匹配' }
          }

          // Update last login
          const data = mockDB.getData()
          const userIndex = data.users.findIndex(u => u.id === foundUser.id)
          if (userIndex > -1) {
            data.users[userIndex].lastLogin = new Date()
            data.users[userIndex].loginCount = (data.users[userIndex].loginCount || 0) + 1
            mockDB.saveData(data)
          }

          this.user = foundUser
          this.token = `mock-token-${foundUser.id}-${Date.now()}`
          this.isAuthenticated = true
          this.save()

          return { success: true, user: foundUser }
        } else {
          return { success: false, error: '用户名或密码错误' }
        }
      } catch (error) {
        console.error('Login error:', error)
        return { success: false, error: '登录失败，请稍后重试' }
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem(LS_KEY)
    },

    save() {
      const payload = {
        user: this.user,
        token: this.token,
        isAuthenticated: this.isAuthenticated
      }
      localStorage.setItem(LS_KEY, JSON.stringify(payload))
    },

    load() {
      try {
        const raw = localStorage.getItem(LS_KEY)
        if (!raw) return
        const parsed = JSON.parse(raw)
        this.$patch(parsed)
      } catch (error) {
        console.warn('Failed to load auth state:', error)
        this.logout()
      }
    },

    hasPermission(permission) {
      return this.user?.permissions?.includes(permission) || false
    },

    // Add new user (for registration)
    addUser(userData) {
      try {
        // Check if username already exists
        const existingUser = mockDB.findUserByUsername(userData.username)
        if (existingUser) {
          throw new Error('用户名已存在')
        }

        // Add user to mock database
        const newUser = mockDB.addUser(userData)
        return { success: true, user: newUser }
      } catch (error) {
        console.error('Add user error:', error)
        return { success: false, error: error.message }
      }
    },

    canAccessResource(resourceId) {
      if (this.isAdmin) return true
      if (this.isUser && this.user?.assignedData?.includes(resourceId)) return true
      return false
    }
  }
})
