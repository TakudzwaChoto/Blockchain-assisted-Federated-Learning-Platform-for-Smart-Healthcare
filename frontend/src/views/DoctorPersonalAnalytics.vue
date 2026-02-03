<template>
  <div class="personal-analytics">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">个人分析</h1>
          <p class="page-subtitle">查看个人工作绩效和数据分析</p>
        </div>
        <div class="header-actions">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="updateAnalytics"
            style="margin-right: 16px"
          />
          <el-button @click="exportReport">
            <el-icon><Download /></el-icon>
            导出报告
          </el-button>
        </div>
      </div>
    </div>

    <!-- Performance Summary -->
    <div class="performance-summary">
      <el-card class="summary-card">
        <template #header>
          <h3>工作绩效概览</h3>
        </template>
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-icon patients">
              <el-icon size="32"><User /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-number">{{ performance.totalPatients }}</div>
              <div class="summary-label">管理患者</div>
              <div class="summary-trend" :class="getTrendClass(performance.patientsTrend)">
                <el-icon><ArrowUp v-if="performance.patientsTrend > 0" /><ArrowDown v-else /></el-icon>
                {{ Math.abs(performance.patientsTrend) }}%
              </div>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon requests">
              <el-icon size="32"><Document /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-number">{{ performance.totalRequests }}</div>
              <div class="summary-label">输血申请</div>
              <div class="summary-trend" :class="getTrendClass(performance.requestsTrend)">
                <el-icon><ArrowUp v-if="performance.requestsTrend > 0" /><ArrowDown v-else /></el-icon>
                {{ Math.abs(performance.requestsTrend) }}%
              </div>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon transfusions">
              <el-icon size="32"><Box /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-number">{{ performance.totalTransfusions }}</div>
              <div class="summary-label">完成输血</div>
              <div class="summary-trend" :class="getTrendClass(performance.transfusionsTrend)">
                <el-icon><ArrowUp v-if="performance.transfusionsTrend > 0" /><ArrowDown v-else /></el-icon>
                {{ Math.abs(performance.transfusionsTrend) }}%
              </div>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon efficiency">
              <el-icon size="32"><TrendCharts /></el-icon>
            </div>
            <div class="summary-info">
              <div class="summary-number">{{ performance.efficiency }}%</div>
              <div class="summary-label">工作效率</div>
              <div class="summary-trend" :class="getTrendClass(performance.efficiencyTrend)">
                <el-icon><ArrowUp v-if="performance.efficiencyTrend > 0" /><ArrowDown v-else /></el-icon>
                {{ Math.abs(performance.efficiencyTrend) }}%
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <div class="charts-grid">
        <!-- Monthly Trends -->
        <el-card class="chart-card">
          <template #header>
            <h3>月度工作趋势</h3>
          </template>
          <div class="chart-container">
            <div class="chart-placeholder">
              <div class="mock-chart">
                <div class="chart-bar" v-for="(value, index) in monthlyData" :key="index" :style="{ height: `${value}%` }"></div>
              </div>
              <div class="chart-labels">
                <span v-for="(month, index) in chartMonths" :key="index">{{ month }}</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Blood Type Distribution -->
        <el-card class="chart-card">
          <template #header>
            <h3>血型使用分布</h3>
          </template>
          <div class="chart-container">
            <div class="blood-type-chart">
              <div class="distribution-item" v-for="type in bloodTypeData" :key="type.type">
                <div class="type-info">
                  <span class="type-name">{{ type.type }}</span>
                  <span class="type-count">{{ type.count }}次</span>
                  <span class="type-percentage">{{ type.percentage }}%</span>
                </div>
                <div class="type-bar">
                  <div class="bar-fill" :style="{ width: `${type.percentage}%` }"></div>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Urgency Distribution -->
        <el-card class="chart-card">
          <template #header>
            <h3>紧急程度分布</h3>
          </template>
          <div class="chart-container">
            <div class="urgency-chart">
              <div class="urgency-item" v-for="urgency in urgencyData" :key="urgency.level">
                <div class="urgency-label">{{ urgency.level }}</div>
                <div class="urgency-count">{{ urgency.count }}</div>
                <div class="urgency-bar">
                  <div class="bar-fill" :style="{ width: `${urgency.percentage}%` }" :class="urgency.class"></div>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Response Time -->
        <el-card class="chart-card">
          <template #header>
            <h3>响应时间分析</h3>
          </template>
          <div class="chart-container">
            <div class="response-time-chart">
              <div class="response-item" v-for="time in responseTimeData" :key="time.metric">
                <div class="response-label">{{ time.metric }}</div>
                <div class="response-value">{{ time.value }}分钟</div>
                <div class="response-bar">
                  <div class="bar-fill" :style="{ width: `${time.percentage}%` }"></div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- Detailed Analytics -->
    <div class="detailed-analytics">
      <el-row :gutter="24">
        <!-- Patient Statistics -->
        <el-col :span="12">
          <el-card class="analytics-card">
            <template #header>
              <h3>患者统计</h3>
            </template>
            <div class="patient-stats">
              <div class="stat-row">
                <span class="stat-label">新增患者</span>
                <span class="stat-value">{{ patientStats.newPatients }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">活跃患者</span>
                <span class="stat-value">{{ patientStats.activePatients }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">平均年龄</span>
                <span class="stat-value">{{ patientStats.averageAge }}岁</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">男女比例</span>
                <span class="stat-value">{{ patientStats.genderRatio }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">血型分布</span>
                <div class="blood-type-mini">
                  <span v-for="type in patientStats.bloodTypeDistribution" :key="type.type" class="mini-tag">
                    {{ type.type }}: {{ type.count }}
                  </span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- Workload Analysis -->
        <el-col :span="12">
          <el-card class="analytics-card">
            <template #header>
              <h3>工作量分析</h3>
            </template>
            <div class="workload-stats">
              <div class="stat-row">
                <span class="stat-label">日均处理申请</span>
                <span class="stat-value">{{ workloadStats.dailyRequests }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">平均处理时间</span>
                <span class="stat-value">{{ workloadStats.averageProcessTime }}分钟</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">成功率</span>
                <span class="stat-value">{{ workloadStats.successRate }}%</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">加班时长</span>
                <span class="stat-value">{{ workloadStats.overtimeHours }}小时</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">工作满意度</span>
                <el-rate v-model="workloadStats.satisfaction" disabled show-score />
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- Activity Timeline -->
    <div class="activity-section">
      <el-card class="activity-card">
        <template #header>
          <div class="activity-header">
            <h3>工作活动时间线</h3>
            <el-select v-model="activityFilter" placeholder="筛选类型" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option label="患者管理" value="patient" />
              <el-option label="输血申请" value="request" />
              <el-option label="输血完成" value="transfusion" />
              <el-option label="系统操作" value="system" />
            </el-select>
          </div>
        </template>
        <div class="activity-timeline">
          <el-timeline>
            <el-timeline-item
              v-for="activity in filteredActivities"
              :key="activity.id"
              :timestamp="formatDateTime(activity.timestamp)"
              :type="getTimelineType(activity.type)"
            >
              <div class="timeline-content">
                <div class="activity-header">
                  <span class="activity-title">{{ activity.title }}</span>
                  <el-tag :type="getActivityTagType(activity.type)" size="small">
                    {{ getActivityTypeText(activity.type) }}
                  </el-tag>
                </div>
                <div class="activity-description">{{ activity.description }}</div>
                <div class="activity-details" v-if="activity.details">
                  <el-descriptions :column="2" size="small">
                    <el-descriptions-item 
                      v-for="(value, key) in activity.details" 
                      :key="key"
                      :label="key"
                    >
                      {{ value }}
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  User, Document, Box, TrendCharts, Download, ArrowUp, ArrowDown 
} from '@element-plus/icons-vue'
import dataService from '../services/dataService'

// Reactive data
const loading = ref(false)
const dateRange = ref([])
const activityFilter = ref('')

// Performance data
const performance = reactive({
  totalPatients: 156,
  patientsTrend: 12.5,
  totalRequests: 89,
  requestsTrend: -5.2,
  totalTransfusions: 67,
  transfusionsTrend: 8.7,
  efficiency: 94,
  efficiencyTrend: 3.1
})

// Chart data
const monthlyData = ref([65, 78, 90, 81, 56, 95, 88, 72, 85, 91, 76, 84])
const chartMonths = ref(['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'])

const bloodTypeData = ref([
  { type: 'A+', count: 34, percentage: 35 },
  { type: 'B+', count: 28, percentage: 29 },
  { type: 'O+', count: 25, percentage: 26 },
  { type: 'AB+', count: 10, percentage: 10 }
])

const urgencyData = ref([
  { level: '常规', count: 45, percentage: 50, class: 'normal' },
  { level: '紧急', count: 30, percentage: 34, class: 'urgent' },
  { level: '非常紧急', count: 14, percentage: 16, class: 'critical' }
])

const responseTimeData = ref([
  { metric: '申请审核', value: 15, percentage: 30 },
  { metric: '血型匹配', value: 8, percentage: 16 },
  { metric: '血液准备', value: 25, percentage: 50 },
  { metric: '输血执行', value: 45, percentage: 90 }
])

// Patient statistics
const patientStats = reactive({
  newPatients: 23,
  activePatients: 156,
  averageAge: 42,
  genderRatio: '1:1.2',
  bloodTypeDistribution: [
    { type: 'A+', count: 45 },
    { type: 'B+', count: 38 },
    { type: 'O+', count: 52 },
    { type: 'AB+', count: 21 }
  ]
})

// Workload statistics
const workloadStats = reactive({
  dailyRequests: 7.4,
  averageProcessTime: 28,
  successRate: 96,
  overtimeHours: 12,
  satisfaction: 4.5
})

// Activities data
const activities = ref([
  {
    id: 1,
    type: 'patient',
    title: '新增患者',
    description: '添加患者张三到管理系统',
    timestamp: new Date('2024-01-20 09:30'),
    details: {
      '患者姓名': '张三',
      '血型': 'A+',
      '年龄': '45岁'
    }
  },
  {
    id: 2,
    type: 'request',
    title: '提交输血申请',
    description: '为患者李四申请400ml O型血',
    timestamp: new Date('2024-01-20 10:15'),
    details: {
      '申请编号': 'REQ001',
      '紧急程度': '紧急',
      '申请量': '400ml'
    }
  },
  {
    id: 3,
    type: 'transfusion',
    title: '完成输血',
    description: '患者王五输血治疗完成',
    timestamp: new Date('2024-01-20 14:20'),
    details: {
      '患者姓名': '王五',
      '血型': 'B+',
      '输血量': '300ml'
    }
  },
  {
    id: 4,
    type: 'system',
    title: '系统更新',
    description: '输血协议已更新',
    timestamp: new Date('2024-01-20 16:00'),
    details: {
      '版本号': 'v2.1.0',
      '更新内容': '输血安全协议'
    }
  }
])

// Computed properties
const filteredActivities = computed(() => {
  if (!activityFilter.value) return activities.value
  return activities.value.filter(activity => activity.type === activityFilter.value)
})

// Methods
const getTrendClass = (trend) => {
  return trend > 0 ? 'trend-up' : 'trend-down'
}

const getTimelineType = (type) => {
  const types = {
    'patient': 'primary',
    'request': 'warning',
    'transfusion': 'success',
    'system': 'info'
  }
  return types[type] || 'info'
}

const getActivityTagType = (type) => {
  const types = {
    'patient': 'primary',
    'request': 'warning',
    'transfusion': 'success',
    'system': 'info'
  }
  return types[type] || 'info'
}

const getActivityTypeText = (type) => {
  const texts = {
    'patient': '患者管理',
    'request': '输血申请',
    'transfusion': '输血完成',
    'system': '系统操作'
  }
  return texts[type] || type
}

const formatDateTime = (date) => {
  return new Date(date).toLocaleString('zh-CN')
}

const updateAnalytics = () => {
  ElMessage.info('更新分析数据')
  // In real app, this would fetch new data based on date range
}

const exportReport = () => {
  ElMessage.success('报告导出成功')
}

// Load data on mount
onMounted(() => {
  // Initialize with current month date range
  const now = new Date()
  const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
  const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  
  dateRange.value = [
    firstDay.toISOString().split('T')[0],
    lastDay.toISOString().split('T')[0]
  ]
})
</script>

<style scoped>
.personal-analytics {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* Header Styles */
.page-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.title-section p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.header-actions {
  display: flex;
  align-items: center;
}

/* Performance Summary */
.performance-summary {
  margin-bottom: 24px;
}

.summary-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.summary-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.summary-icon.patients { background: linear-gradient(135deg, #667eea, #764ba2); }
.summary-icon.requests { background: linear-gradient(135deg, #f093fb, #f5576c); }
.summary-icon.transfusions { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.summary-icon.efficiency { background: linear-gradient(135deg, #fa709a, #fee140); }

.summary-info {
  flex: 1;
}

.summary-number {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.summary-label {
  color: #666;
  font-size: 14px;
  margin-top: 4px;
}

.summary-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  margin-top: 4px;
}

.trend-up {
  color: #67c23a;
}

.trend-down {
  color: #f56c6c;
}

/* Charts Section */
.charts-section {
  margin-bottom: 24px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.chart-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin: 0;
  color: #333;
}

.chart-container {
  height: 250px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.chart-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px 0;
}

.mock-chart {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 180px;
  width: 100%;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  transition: height 0.3s ease;
}

.chart-labels {
  display: flex;
  justify-content: space-around;
  margin-top: 12px;
  font-size: 12px;
  color: #666;
}

/* Blood Type Chart */
.blood-type-chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.type-info {
  width: 120px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.type-count {
  color: #666;
}

.type-percentage {
  color: #667eea;
  font-weight: 600;
}

.type-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* Urgency Chart */
.urgency-chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.urgency-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.urgency-label {
  width: 80px;
  font-weight: 600;
  color: #333;
}

.urgency-count {
  width: 40px;
  text-align: center;
  color: #666;
}

.urgency-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.urgency-bar .bar-fill.normal { background: linear-gradient(90deg, #67c23a, #85ce61); }
.urgency-bar .bar-fill.urgent { background: linear-gradient(90deg, #e6a23c, #ebb563); }
.urgency-bar .bar-fill.critical { background: linear-gradient(90deg, #f56c6c, #f78989); }

/* Response Time Chart */
.response-time-chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.response-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.response-label {
  width: 100px;
  font-weight: 600;
  color: #333;
}

.response-value {
  width: 60px;
  text-align: center;
  color: #667eea;
  font-weight: 600;
}

.response-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

/* Detailed Analytics */
.detailed-analytics {
  margin-bottom: 24px;
}

.analytics-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.analytics-card h3 {
  margin: 0;
  color: #333;
}

.patient-stats,
.workload-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.stat-value {
  color: #333;
  font-weight: 600;
}

.blood-type-mini {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.mini-tag {
  background: #f0f0f0;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

/* Activity Timeline */
.activity-section {
  margin-bottom: 24px;
}

.activity-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-header h3 {
  margin: 0;
  color: #333;
}

.activity-timeline {
  max-height: 500px;
  overflow-y: auto;
}

.timeline-content {
  padding-left: 20px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.activity-title {
  font-weight: 600;
  color: #333;
}

.activity-description {
  color: #666;
  margin-bottom: 8px;
}

.activity-details {
  margin-top: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .distribution-item,
  .urgency-item,
  .response-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .type-info,
  .urgency-label,
  .response-label {
    width: auto;
  }
}
</style>
