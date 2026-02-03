<template>
  <div class="donation-analytics">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>捐赠分析</span>
              <div class="header-actions">
                <el-button-group>
                  <el-button :type="timeRange === 'day' ? 'primary' : ''" @click="setTimeRange('day')">日</el-button>
                  <el-button :type="timeRange === 'week' ? 'primary' : ''" @click="setTimeRange('week')">周</el-button>
                  <el-button :type="timeRange === 'month' ? 'primary' : ''" @click="setTimeRange('month')">月</el-button>
                  <el-button :type="timeRange === 'year' ? 'primary' : ''" @click="setTimeRange('year')">年</el-button>
                </el-button-group>
                <el-button type="primary" @click="refreshData" :loading="loading">
                  <el-icon><Refresh /></el-icon>
                  刷新数据
                </el-button>
                <el-button @click="exportData">
                  <el-icon><Download /></el-icon>
                  导出
                </el-button>
              </div>
            </div>
          </template>
          
          <!-- KPI Overview -->
          <el-row :gutter="16" class="kpi-row">
            <el-col :span="6" v-for="kpi in kpis" :key="kpi.id">
              <div class="kpi-card" @click="viewKPIDetails(kpi)">
                <div class="kpi-icon" :style="{ backgroundColor: kpi.color }">
                  <el-icon>
                    <component :is="kpi.icon" />
                  </el-icon>
                </div>
                <div class="kpi-content">
                  <div class="kpi-value" :class="{ 'updating': kpi.updating }">{{ kpi.value }}</div>
                  <div class="kpi-label">{{ kpi.label }}</div>
                  <div class="kpi-change" :class="kpi.trend">
                    <el-icon v-if="kpi.trend === 'up'"><TrendCharts /></el-icon>
                    <el-icon v-else><TrendCharts /></el-icon>
                    {{ kpi.change }}
                  </div>
                  <div class="kpi-progress">
                    <el-progress :percentage="kpi.progress" :color="kpi.color" :show-text="false" />
                  </div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Charts Section -->
          <el-row :gutter="16" style="margin-top: 24px;">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>月度捐赠趋势</span>
                </template>
                <div class="chart-container">
                  <div class="chart-animation">
                    <div v-for="(bar, index) in monthlyData" :key="index" 
                         class="chart-bar" 
                         :style="{ height: bar.value + '%', backgroundColor: bar.color, animationDelay: index * 0.1 + 's' }">
                      <div class="bar-label">{{ bar.month }}</div>
                      <div class="bar-value">{{ bar.donations }}</div>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>血型分布</span>
                </template>
                <div class="blood-type-chart">
                  <div class="wheel-container">
                    <div v-for="type in bloodTypes" :key="type.type" 
                         class="blood-segment" 
                         :style="{ transform: `rotate(${type.angle}deg)`, background: type.color }">
                      <div class="segment-label">{{ type.type }}</div>
                    </div>
                    <div class="wheel-center">
                      <div class="center-value">{{ totalUnits }}</div>
                      <div class="center-label">Total Units</div>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Refresh, TrendCharts, DataAnalysis, User, Document, Download } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

// State
const loading = ref(false)
const timeRange = ref('month')
const totalUnits = ref('2,456')

// Enhanced KPI Data
const kpis = ref([
  {
    id: 'total-donations',
    label: '总捐赠数',
    value: '12,456',
    change: '+12%',
    trend: 'up',
    icon: 'Document',
    color: '#409eff',
    progress: 78,
    updating: false
  },
  {
    id: 'monthly-average',
    label: '月平均',
    value: '1,038',
    change: '+8%',
    trend: 'up',
    icon: 'TrendCharts',
    color: '#67c23a',
    progress: 85,
    updating: false
  },
  {
    id: 'active-donors',
    label: '活跃捐赠者',
    value: '3,892',
    change: '+15%',
    trend: 'up',
    icon: 'User',
    color: '#e6a23c',
    progress: 92,
    updating: false
  },
  {
    id: 'success-rate',
    label: '成功率',
    value: '98.5%',
    change: '+2%',
    trend: 'up',
    icon: 'DataAnalysis',
    color: '#f56c6c',
    progress: 98,
    updating: false
  }
])

// Monthly Data for Chart
const monthlyData = ref([
  { month: 'Jan', donations: '890', value: 75, color: '#409eff' },
  { month: 'Feb', donations: '1,023', value: 85, color: '#67c23a' },
  { month: 'Mar', donations: '945', value: 80, color: '#e6a23c' },
  { month: 'Apr', donations: '1,156', value: 95, color: '#f56c6c' },
  { month: 'May', donations: '1,089', value: 90, color: '#909399' },
  { month: 'Jun', donations: '1,234', value: 100, color: '#409eff' }
])

// Blood Type Data
const bloodTypes = ref([
  { type: 'O+', percentage: 38, color: '#e74c3c', angle: 0 },
  { type: 'A+', percentage: 34, color: '#3498db', angle: 45 },
  { type: 'B+', percentage: 9, color: '#2ecc71', angle: 90 },
  { type: 'AB+', percentage: 3, color: '#9b59b6', angle: 135 },
  { type: 'O-', percentage: 7, color: '#c0392b', angle: 180 },
  { type: 'A-', percentage: 6, color: '#2980b9', angle: 225 },
  { type: 'B-', percentage: 2, color: '#27ae60', angle: 270 },
  { type: 'AB-', percentage: 1, color: '#8e44ad', angle: 315 }
])

// Methods
const setTimeRange = (range) => {
  timeRange.value = range
  refreshData()
  notificationStore.info(`Time range changed to ${range}`)
}

const refreshData = async () => {
  loading.value = true
  
  // Simulate data refresh
  kpis.value.forEach(kpi => {
    kpi.updating = true
  })
  
  setTimeout(() => {
    // Update with new data
    kpis.value.forEach(kpi => {
      kpi.updating = false
      // Simulate small changes in values
      const currentValue = parseInt(kpi.value.replace(/[^0-9]/g, ''))
      const change = Math.floor(Math.random() * 10) - 5
      kpi.value = (currentValue + change).toLocaleString()
    })
    
    loading.value = false
    notificationStore.success('数据刷新成功')
  }, 1500)
}

const exportData = () => {
  // Create export data
  const exportContent = {
    kpis: kpis.value,
    monthlyData: monthlyData.value,
    bloodTypes: bloodTypes.value,
    exportTime: new Date().toISOString()
  }
  
  // Create download link
  const blob = new Blob([JSON.stringify(exportContent, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = window.document.createElement('a')
  link.href = url
  link.download = `donation-analytics-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  notificationStore.success('数据导出成功')
}

const viewKPIDetails = (kpi) => {
  notificationStore.info(`Viewing details for ${kpi.label}: ${kpi.value}`)
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.donation-analytics {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.kpi-row {
  margin-bottom: 24px;
}

.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e4e7ed;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
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
  margin-bottom: 12px;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.kpi-value.updating {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.kpi-label {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.kpi-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.kpi-change.up {
  color: #27ae60;
}

.kpi-change.down {
  color: #e74c3c;
}

.kpi-progress {
  margin-top: 12px;
}

.chart-container {
  height: 300px;
  position: relative;
}

.chart-animation {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 250px;
  padding: 20px;
}

.chart-bar {
  flex: 1;
  border-radius: 4px;
  position: relative;
  animation: growBar 1s ease-out forwards;
  min-height: 20px;
  transition: all 0.3s ease;
}

.chart-bar:hover {
  transform: translateY(-4px);
  filter: brightness(1.1);
}

@keyframes growBar {
  0% { height: 0; }
  100% { height: var(--height); }
}

.bar-label {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: #7f8c8d;
  white-space: nowrap;
}

.bar-value {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  font-weight: 600;
  color: #2c3e50;
  white-space: nowrap;
}

.blood-type-chart {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wheel-container {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  position: relative;
  background: conic-gradient(
    from 0deg,
    #e74c3c 0deg 45deg,
    #3498db 45deg 90deg,
    #2ecc71 90deg 135deg,
    #9b59b6 135deg 180deg,
    #c0392b 180deg 225deg,
    #2980b9 225deg 270deg,
    #27ae60 270deg 315deg,
    #8e44ad 315deg 360deg
  );
}

.blood-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  clip-path: polygon(50% 50%, 50% 0%, 85% 15%);
}

.segment-label {
  position: absolute;
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
}

.wheel-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.center-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
}

.center-label {
  font-size: 0.7rem;
  color: #7f8c8d;
  margin-top: 2px;
}
</style>
