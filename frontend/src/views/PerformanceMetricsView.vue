<template>
  <div class="performance-metrics">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>绩效指标</span>
              <div class="header-actions">
                <el-button type="primary" @click="refreshMetrics">
                  <el-icon><Refresh /></el-icon>
                  刷新指标
                </el-button>
                <el-button @click="exportMetrics">
                  <el-icon><Download /></el-icon>
                  导出
                </el-button>
              </div>
            </div>
          </template>

          <!-- Key Performance Indicators -->
          <el-row :gutter="16" class="kpi-section">
            <el-col :span="6" v-for="kpi in kpis" :key="kpi.id">
              <div class="kpi-card" :class="kpi.trend">
                <div class="kpi-header">
                  <div class="kpi-title">{{ kpi.title }}</div>
                  <div class="kpi-icon" :style="{ backgroundColor: kpi.color }">
                    <el-icon>
                      <component :is="kpi.icon" />
                    </el-icon>
                  </div>
                </div>
                <div class="kpi-value">{{ kpi.value }}</div>
                <div class="kpi-change">
                  <el-icon v-if="kpi.trend === 'up'"><TrendCharts /></el-icon>
                  <el-icon v-else-if="kpi.trend === 'down'"><TrendCharts /></el-icon>
                  <span>{{ kpi.change }}</span>
                </div>
                <div class="kpi-sparkline">
                  <div class="sparkline" :style="{ background: kpi.sparkline }"></div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Performance Charts -->
          <el-divider>绩效趋势</el-divider>
          <el-row :gutter="16">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>收集效率</span>
                </template>
                <div class="chart-placeholder">
                  <el-empty description="效率趋势图将在此处显示" />
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>处理时间</span>
                </template>
                <div class="chart-placeholder">
                  <el-empty description="处理时间图表将在此处显示" />
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- Department Performance -->
          <el-divider>部门绩效</el-divider>
          <el-table :data="departmentPerformance" style="width: 100%">
            <el-table-column prop="department" label="部门" />
            <el-table-column prop="target" label="目标" width="100" />
            <el-table-column prop="actual" label="实际" width="100" />
            <el-table-column prop="performance" label="绩效%" width="120">
              <template #default="{ row }">
                <el-progress :percentage="Math.min(100, row.performance)" :color="getPerformanceColor(row.performance)" />
              </template>
            </el-table-column>
            <el-table-column prop="rating" label="评级" width="100">
              <template #default="{ row }">
                <el-tag :type="getRatingType(row.rating)">
                  {{ row.rating }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="trend" label="趋势" width="100">
              <template #default="{ row }">
                <el-tag :type="getTrendType(row.trend)">
                  {{ row.trend }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>

          <!-- System Metrics -->
          <el-divider>System Metrics</el-divider>
          <el-row :gutter="16">
            <el-col :span="8" v-for="metric in systemMetrics" :key="metric.id">
              <div class="system-metric-card">
                <div class="metric-header">
                  <div class="metric-title">{{ metric.title }}</div>
                  <div class="metric-status" :class="metric.status.toLowerCase()">
                    {{ metric.status }}
                  </div>
                </div>
                <div class="metric-value">{{ metric.value }}</div>
                <div class="metric-description">{{ metric.description }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Refresh, Download, TrendCharts, DataAnalysis, User, Document } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const kpis = ref([
  {
    id: 'efficiency',
    title: 'Collection Efficiency',
    value: '94.5%',
    change: '+2.3%',
    trend: 'up',
    icon: 'TrendCharts',
    color: '#409eff',
    sparkline: 'linear-gradient(135deg, #409eff 0%, #66b1ff 100%)'
  },
  {
    id: 'processing',
    title: 'Processing Time',
    value: '12.3 min',
    change: '-1.2 min',
    trend: 'up',
    icon: 'DataAnalysis',
    color: '#67c23a',
    sparkline: 'linear-gradient(135deg, #67c23a 0%, #85ce61 100%)'
  },
  {
    id: 'satisfaction',
    title: 'Donor Satisfaction',
    value: '4.7/5.0',
    change: '+0.2',
    trend: 'up',
    icon: 'User',
    color: '#e6a23c',
    sparkline: 'linear-gradient(135deg, #e6a23c 0%, #ebb563 100%)'
  },
  {
    id: 'compliance',
    title: 'Compliance Rate',
    value: '98.7%',
    change: '+0.5%',
    trend: 'up',
    icon: 'Document',
    color: '#f56c6c',
    sparkline: 'linear-gradient(135deg, #f56c6c 0%, #f78989 100%)'
  }
])

const departmentPerformance = ref([
  {
    department: 'Collection Center A',
    target: 500,
    actual: 523,
    performance: 104.6,
    rating: 'Excellent',
    trend: 'Improving'
  },
  {
    department: 'Collection Center B',
    target: 300,
    actual: 287,
    performance: 95.7,
    rating: 'Good',
    trend: 'Stable'
  },
  {
    department: 'Mobile Unit 1',
    target: 200,
    actual: 156,
    performance: 78.0,
    rating: 'Fair',
    trend: 'Declining'
  }
])

const systemMetrics = ref([
  {
    id: 'uptime',
    title: 'System Uptime',
    value: '99.8%',
    status: 'Healthy',
    description: 'Last 30 days'
  },
  {
    id: 'response',
    title: 'Response Time',
    value: '1.2s',
    status: 'Good',
    description: 'Average response'
  },
  {
    id: 'throughput',
    title: 'Daily Throughput',
    value: '2,456',
    status: 'Optimal',
    description: 'Records processed'
  }
])

const getPerformanceColor = (performance) => {
  if (performance >= 100) return '#67c23a'
  if (performance >= 90) return '#409eff'
  if (performance >= 80) return '#e6a23c'
  return '#f56c6c'
}

const getRatingType = (rating) => {
  switch (rating) {
    case 'Excellent': return 'success'
    case 'Good': return 'primary'
    case 'Fair': return 'warning'
    case 'Poor': return 'danger'
    default: return 'info'
  }
}

const getTrendType = (trend) => {
  switch (trend) {
    case 'Improving': return 'success'
    case 'Stable': return 'primary'
    case 'Declining': return 'danger'
    default: return 'info'
  }
}

const refreshMetrics = () => {
  notificationStore.success('Performance metrics refreshed')
}

const exportMetrics = () => {
  notificationStore.success('指标导出成功')
}
</script>

<style scoped>
.performance-metrics {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.kpi-section {
  margin-bottom: 32px;
}

.kpi-card {
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
  position: relative;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.kpi-title {
  font-weight: 600;
  color: #303133;
}

.kpi-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 8px;
}

.kpi-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 12px;
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

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.system-metric-card {
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

.system-metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.metric-title {
  font-weight: 600;
  color: #303133;
}

.metric-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.metric-status.healthy {
  background: #f0f9ff;
  color: #409eff;
}

.metric-status.good {
  background: #f0f9ff;
  color: #67c23a;
}

.metric-status.optimal {
  background: #f0f9ff;
  color: #e6a23c;
}

.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.metric-description {
  font-size: 12px;
  color: #606266;
}
</style>
