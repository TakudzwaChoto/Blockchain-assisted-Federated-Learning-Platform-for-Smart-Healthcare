<template>
  <el-card class="real-time-updates">
    <template #header>
      <div class="updates-header">
        <span>
          <el-icon><Timer /></el-icon>
          Real-Time Updates
        </span>
        <div class="update-controls">
          <el-switch
            v-model="autoRefresh"
            active-text="Auto-refresh"
            inactive-text="Manual"
            @change="toggleAutoRefresh"
          />
          <el-select v-model="refreshInterval" size="small" style="width: 120px; margin-left: 12px">
            <el-option label="5s" :value="5000" />
            <el-option label="10s" :value="10000" />
            <el-option label="30s" :value="30000" />
            <el-option label="1m" :value="60000" />
          </el-select>
          <el-button size="small" @click="manualRefresh" :loading="refreshing">
            <el-icon><Refresh /></el-icon>
            Refresh Now
          </el-button>
        </div>
      </div>
    </template>

    <!-- Live Stats -->
    <div class="live-stats">
      <div class="stat-item" v-for="stat in liveStats" :key="stat.name">
        <div class="stat-icon" :style="{ backgroundColor: stat.color }">
          <el-icon>
            <component :is="stat.icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-change" :class="stat.changeClass">
            <el-icon>
              <component :is="stat.changeIcon" />
            </el-icon>
            {{ stat.change }}
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity Feed -->
    <el-divider>Recent Activity</el-divider>
    <div class="activity-feed">
      <div
        v-for="activity in recentActivity"
        :key="activity.id"
        class="activity-item"
        :class="`activity-${activity.type}`"
      >
        <div class="activity-time">
          {{ formatTime(activity.timestamp) }}
        </div>
        <div class="activity-content">
          <div class="activity-icon">
            <el-icon>
              <component :is="getActivityIcon(activity.type)" />
            </el-icon>
          </div>
          <div class="activity-details">
            <div class="activity-title">{{ activity.title }}</div>
            <div class="activity-description">{{ activity.description }}</div>
          </div>
          <div class="activity-badge">
            <el-tag :type="getActivityTagType(activity.type)" size="small">
              {{ activity.type }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- System Status -->
    <el-divider>System Status</el-divider>
    <div class="system-status">
      <div class="status-item" v-for="status in systemStatus" :key="status.name">
        <div class="status-indicator" :class="`status-${status.status}`"></div>
        <div class="status-info">
          <div class="status-name">{{ status.name }}</div>
          <div class="status-details">{{ status.details }}</div>
        </div>
        <div class="status-metrics">
          <div class="metric">
            <span class="metric-label">CPU:</span>
            <span class="metric-value">{{ status.cpu }}%</span>
          </div>
          <div class="metric">
            <span class="metric-label">Memory:</span>
            <span class="metric-value">{{ status.memory }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts & Notifications -->
    <el-divider>Active Alerts</el-divider>
    <div class="alerts-section">
      <div
        v-for="alert in activeAlerts"
        :key="alert.id"
        class="alert-item"
        :class="`alert-${alert.severity}`"
      >
        <div class="alert-icon">
          <el-icon>
            <component :is="getAlertIcon(alert.severity)" />
          </el-icon>
        </div>
        <div class="alert-content">
          <div class="alert-title">{{ alert.title }}</div>
          <div class="alert-description">{{ alert.description }}</div>
          <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
        </div>
        <div class="alert-actions">
          <el-button size="small" @click="dismissAlert(alert.id)">Dismiss</el-button>
          <el-button size="small" type="primary" @click="viewAlert(alert)">View</el-button>
        </div>
      </div>
      
      <el-empty v-if="activeAlerts.length === 0" description="No active alerts" />
    </div>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import {
  Timer,
  Refresh,
  TrendCharts,
  DataAnalysis,
  User,
  Document,
  Setting,
  Warning,
  InfoFilled,
  SuccessFilled,
  CircleCloseFilled,
  Bell
} from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const emit = defineEmits(['data-refreshed', 'alert-selected'])

const notificationStore = useNotificationStore()

const autoRefresh = ref(false)
const refreshInterval = ref(10000)
const refreshing = ref(false)
let refreshTimer = null

const liveStats = ref([
  {
    name: 'donations',
    label: 'Total Donations',
    value: '1,234',
    change: '+12%',
    changeClass: 'positive',
    changeIcon: 'TrendCharts',
    icon: 'Document',
    color: '#409eff'
  },
  {
    name: 'donors',
    label: 'Active Donors',
    value: '892',
    change: '+5%',
    changeClass: 'positive',
    changeIcon: 'TrendCharts',
    icon: 'User',
    color: '#67c23a'
  },
  {
    name: 'processing',
    label: 'Processing Rate',
    value: '98.5%',
    change: '+0.3%',
    changeClass: 'positive',
    changeIcon: 'TrendCharts',
    icon: 'DataAnalysis',
    color: '#e6a23c'
  },
  {
    name: 'errors',
    label: 'Error Rate',
    value: '0.2%',
    change: '-0.1%',
    changeClass: 'negative',
    changeIcon: 'TrendCharts',
    icon: 'Warning',
    color: '#f56c6c'
  }
])

const recentActivity = ref([
  {
    id: 1,
    type: 'donation',
    title: 'New Donation Recorded',
    description: 'Blood type O+ donation from donor #1234',
    timestamp: new Date(Date.now() - 300000)
  },
  {
    id: 2,
    type: 'processing',
    title: 'Batch Processing Completed',
    description: 'Processed 500 records successfully',
    timestamp: new Date(Date.now() - 600000)
  },
  {
    id: 3,
    type: 'validation',
    title: 'Data Validation Alert',
    description: '3 records failed validation checks',
    timestamp: new Date(Date.now() - 900000)
  },
  {
    id: 4,
    type: 'system',
    title: 'System Backup Completed',
    description: 'Daily backup completed successfully',
    timestamp: new Date(Date.now() - 1800000)
  }
])

const systemStatus = ref([
  {
    name: 'API Server',
    status: 'healthy',
    details: 'All endpoints responding normally',
    cpu: 45,
    memory: 62
  },
  {
    name: 'Database',
    status: 'healthy',
    details: 'Connection pool optimal',
    cpu: 28,
    memory: 41
  },
  {
    name: 'Processing Queue',
    status: 'warning',
    details: 'High queue load detected',
    cpu: 78,
    memory: 85
  }
])

const activeAlerts = ref([
  {
    id: 1,
    severity: 'warning',
    title: 'High Processing Queue',
    description: 'Processing queue has 150+ pending items',
    timestamp: new Date(Date.now() - 300000)
  },
  {
    id: 2,
    severity: 'info',
    title: 'Scheduled Maintenance',
    description: 'System maintenance scheduled for 2:00 AM',
    timestamp: new Date(Date.now() - 3600000)
  }
])

const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  return timestamp.toLocaleDateString()
}

const getActivityIcon = (type) => {
  const icons = {
    donation: 'Document',
    processing: 'DataAnalysis',
    validation: 'Warning',
    system: 'Setting'
  }
  return icons[type] || 'InfoFilled'
}

const getActivityTagType = (type) => {
  const types = {
    donation: 'success',
    processing: 'primary',
    validation: 'warning',
    system: 'info'
  }
  return types[type] || 'info'
}

const getAlertIcon = (severity) => {
  const icons = {
    critical: 'CircleCloseFilled',
    error: 'CircleCloseFilled',
    warning: 'Warning',
    info: 'InfoFilled'
  }
  return icons[severity] || 'InfoFilled'
}

const toggleAutoRefresh = (enabled) => {
  if (enabled) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

const startAutoRefresh = () => {
  if (refreshTimer) clearInterval(refreshTimer)
  refreshTimer = setInterval(() => {
    refreshData()
  }, refreshInterval.value)
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

const manualRefresh = async () => {
  await refreshData()
}

const refreshData = async () => {
  refreshing.value = true
  try {
    // Simulate API calls
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update live stats with random changes
    liveStats.value.forEach(stat => {
      const currentValue = parseInt(stat.value.replace(/[^0-9]/g, ''))
      const change = Math.floor(Math.random() * 10) - 5
      stat.value = (currentValue + change).toLocaleString()
      stat.change = change >= 0 ? `+${change}%` : `${change}%`
      stat.changeClass = change >= 0 ? 'positive' : 'negative'
    })
    
    // Add new random activity
    const activityTypes = ['donation', 'processing', 'validation', 'system']
    const randomType = activityTypes[Math.floor(Math.random() * activityTypes.length)]
    const newActivity = {
      id: Date.now(),
      type: randomType,
      title: `New ${randomType} activity`,
      description: `System detected new ${randomType} event`,
      timestamp: new Date()
    }
    
    recentActivity.value.unshift(newActivity)
    if (recentActivity.value.length > 10) {
      recentActivity.value.pop()
    }
    
    emit('data-refreshed')
    notificationStore.success('Data refreshed successfully')
  } catch (error) {
    notificationStore.error('Failed to refresh data')
  } finally {
    refreshing.value = false
  }
}

const dismissAlert = (alertId) => {
  const index = activeAlerts.value.findIndex(alert => alert.id === alertId)
  if (index > -1) {
    activeAlerts.value.splice(index, 1)
    notificationStore.info('Alert dismissed')
  }
}

const viewAlert = (alert) => {
  emit('alert-selected', alert)
}

onMounted(() => {
  // Start with auto-refresh disabled
  refreshData()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.real-time-updates {
  margin-bottom: 20px;
}

.updates-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.update-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.live-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin: 4px 0;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.stat-change.positive {
  color: #67c23a;
}

.stat-change.negative {
  color: #f56c6c;
}

.activity-feed {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 24px;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  background-color: #fafafa;
  border-left: 3px solid #e4e7ed;
}

.activity-donation {
  border-left-color: #67c23a;
}

.activity-processing {
  border-left-color: #409eff;
}

.activity-validation {
  border-left-color: #e6a23c;
}

.activity-system {
  border-left-color: #909399;
}

.activity-time {
  font-size: 12px;
  color: #c0c4cc;
  min-width: 60px;
}

.activity-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.activity-icon {
  font-size: 16px;
  color: #606266;
}

.activity-details {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  margin-bottom: 2px;
  color: #303133;
}

.activity-description {
  font-size: 12px;
  color: #909399;
}

.system-status {
  margin-bottom: 24px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  background-color: #fafafa;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-healthy {
  background-color: #67c23a;
}

.status-warning {
  background-color: #e6a23c;
}

.status-error {
  background-color: #f56c6c;
}

.status-info {
  flex: 1;
}

.status-name {
  font-weight: 500;
  color: #303133;
}

.status-details {
  font-size: 12px;
  color: #909399;
}

.status-metrics {
  display: flex;
  gap: 16px;
}

.metric {
  display: flex;
  gap: 4px;
  font-size: 12px;
}

.metric-label {
  color: #909399;
}

.metric-value {
  font-weight: 500;
  color: #303133;
}

.alerts-section {
  max-height: 300px;
  overflow-y: auto;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  border-left: 4px solid #e4e7ed;
}

.alert-critical {
  border-left-color: #f56c6c;
  background-color: #fef0f0;
}

.alert-error {
  border-left-color: #f56c6c;
  background-color: #fef0f0;
}

.alert-warning {
  border-left-color: #e6a23c;
  background-color: #fdf6ec;
}

.alert-info {
  border-left-color: #409eff;
  background-color: #ecf5ff;
}

.alert-icon {
  font-size: 18px;
  margin-top: 2px;
}

.alert-critical .alert-icon,
.alert-error .alert-icon {
  color: #f56c6c;
}

.alert-warning .alert-icon {
  color: #e6a23c;
}

.alert-info .alert-icon {
  color: #409eff;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: #303133;
}

.alert-description {
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
}

.alert-time {
  font-size: 11px;
  color: #c0c4cc;
}

.alert-actions {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .updates-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .update-controls {
    flex-wrap: wrap;
  }
  
  .live-stats {
    grid-template-columns: 1fr;
  }
  
  .activity-content,
  .status-item,
  .alert-item {
    flex-direction: column;
    text-align: left;
  }
  
  .status-metrics {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
