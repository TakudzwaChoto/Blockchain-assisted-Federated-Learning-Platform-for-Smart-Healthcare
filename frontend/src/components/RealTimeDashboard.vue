<template>
  <div class="real-time-dashboard">
    <div class="dashboard-header">
      <h3>Real-time Monitoring</h3>
      <div class="live-indicator">
        <span class="live-dot"></span>
        Live
      </div>
    </div>
    
    <div class="metrics-grid">
      <div class="metric-card urgent">
        <div class="metric-icon">
          <el-icon size="24"><Warning /></el-icon>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ urgentBlood }}</div>
          <div class="metric-label">Urgent Blood</div>
        </div>
      </div>
      
      <div class="metric-card available">
        <div class="metric-icon">
          <el-icon size="24"><Monitor /></el-icon>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ availableUnits }}</div>
          <div class="metric-label">Available Units</div>
        </div>
      </div>
      
      <div class="metric-card requests">
        <div class="metric-icon">
          <el-icon size="24"><Document /></el-icon>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ pendingRequests }}</div>
          <div class="metric-label">Pending Requests</div>
        </div>
      </div>
    </div>
    
    <div class="chart-container">
      <div class="chart-header">
        <h4>Blood Trends</h4>
        <div class="chart-controls">
          <el-select v-model="timeRange" size="small">
            <el-option label="24H" value="24h" />
            <el-option label="7D" value="7d" />
            <el-option label="30D" value="30d" />
          </el-select>
        </div>
      </div>
      <div class="chart-area" ref="chartRef"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Monitor, Warning, Document } from '@element-plus/icons-vue'

const chartRef = ref()
const timeRange = ref('24h')

// Real-time data
const urgentBlood = ref(12)
const availableUnits = ref(2847)
const pendingRequests = ref(45)

let intervalId = null

// Simulate real-time data updates
const startRealTimeUpdates = () => {
  intervalId = setInterval(() => {
    urgentBlood.value = Math.max(0, urgentBlood.value + Math.floor(Math.random() * 5) - 2)
    availableUnits.value = Math.max(0, availableUnits.value + Math.floor(Math.random() * 20) - 10)
    pendingRequests.value = Math.max(0, pendingRequests.value + Math.floor(Math.random() * 3) - 1)
  }, 3000)
}

onMounted(() => {
  startRealTimeUpdates()
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.real-time-dashboard {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #67c23a;
  font-weight: 600;
}

.live-dot {
  width: 8px;
  height: 8px;
  background: #67c23a;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-card.urgent {
  background: linear-gradient(135deg, #ff6b6b, #ff4757);
  color: white;
}

.metric-card.available {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: white;
}

.metric-card.requests {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 14px;
  opacity: 0.9;
}

.chart-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-area {
  height: 300px;
  background: white;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}
</style>
