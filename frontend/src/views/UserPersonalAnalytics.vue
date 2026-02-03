<template>
  <div class="user-personal-analytics">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1>个人数据分析</h1>
          <p>查看您的个人工作数据分析</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="generateReport">
            <el-icon><Document /></el-icon>
            生成报告
          </el-button>
          <el-button @click="exportData">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
        </div>
      </div>
    </div>

    <!-- Personal Overview -->
    <div class="overview-grid">
      <el-card class="overview-card">
        <template #header>
          <h3>本月工作概览</h3>
        </template>
        <div class="overview-content">
          <div class="overview-stats">
            <div class="stat-item">
              <div class="stat-number">{{ monthlyStats.newDonors }}</div>
              <div class="stat-label">新增捐赠者</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ monthlyStats.processedRequests }}</div>
              <div class="stat-label">处理申请</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ monthlyStats.recordedDonations }}</div>
              <div class="stat-label">记录捐赠</div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <template #header>
          <h3>工作效率</h3>
        </template>
        <div class="overview-content">
          <div class="efficiency-metrics">
            <div class="metric-item">
              <div class="metric-label">平均处理时间</div>
              <div class="metric-value">{{ efficiencyStats.avgProcessTime }}分钟</div>
            </div>
            <div class="metric-item">
              <div class="metric-label">完成率</div>
              <div class="metric-value">{{ efficiencyStats.completionRate }}%</div>
            </div>
            <div class="metric-item">
              <div class="metric-label">满意度评分</div>
              <div class="metric-value">{{ efficiencyStats.satisfaction }}/5.0</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <el-card class="chart-card">
        <template #header>
          <h3>捐赠者管理趋势</h3>
        </template>
        <div class="chart-container">
          <div class="chart-header">
            <span>月度新增捐赠者</span>
            <el-select v-model="donorChartPeriod" size="small" style="width: 120px">
              <el-option label="最近6个月" value="6m" />
              <el-option label="最近1年" value="1y" />
            </el-select>
          </div>
          <div class="chart-content">
            <div class="chart-bars">
              <div class="chart-bar" v-for="(value, index) in donorChartData" :key="index" 
                   :style="{ height: value + '%' }"
                   :title="`月份 ${index + 1}: ${value} 人`">
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <h3>申请处理统计</h3>
        </template>
        <div class="chart-container">
          <div class="chart-header">
            <span>申请处理状态分布</span>
          </div>
          <div class="chart-content">
            <div class="pie-chart">
              <div class="pie-segments">
                <div class="pie-segment approved" style="flex: 65">
                  <div class="segment-label">已批准 65%</div>
                </div>
                <div class="pie-segment pending" style="flex: 25">
                  <div class="segment-label">待处理 25%</div>
                </div>
                <div class="pie-segment rejected" style="flex: 10">
                  <div class="segment-label">已拒绝 10%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <h3>血型分布</h3>
        </template>
        <div class="chart-container">
          <div class="chart-header">
            <span>管理捐赠者血型分布</span>
          </div>
          <div class="chart-content">
            <div class="blood-type-bars">
              <div class="blood-type-bar" v-for="type in bloodTypeData" :key="type.type">
                <div class="type-info">
                  <span class="type-name">{{ type.type }}</span>
                  <span class="type-count">{{ type.count }}人</span>
                </div>
                <div class="type-progress">
                  <div class="progress-bar" :style="{ width: (type.count / maxDonorCount * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <h3>工作负载分析</h3>
        </template>
        <div class="chart-container">
          <div class="chart-header">
            <span>每日工作活动分布</span>
          </div>
          <div class="chart-content">
            <div class="activity-heatmap">
              <div class="heatmap-row" v-for="(day, dayIndex) in weeklyData" :key="dayIndex">
                <div class="day-label">{{ day.day }}</div>
                <div class="hour-bars">
                  <div class="hour-bar" v-for="(hour, hourIndex) in day.hours" :key="hourIndex"
                       :class="getActivityLevel(hour)"
                       :title="`${day.day} ${hourIndex}:00 - ${hourIndex + 1}:00: ${hour} 次活动`">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Detailed Data Table -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <h3>详细工作记录</h3>
          <div class="table-controls">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="small"
              @change="handleDateChange"
            />
            <el-button size="small" @click="refreshData">刷新</el-button>
          </div>
        </div>
      </template>

      <el-table :data="workRecords" style="width: 100%" v-loading="loading">
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="type" label="工作类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getWorkTypeColor(row.type)" size="small">
              {{ getWorkTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="工作描述" min-width="200" />
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column prop="duration" label="耗时" width="100">
          <template #default="{ row }">
            {{ row.duration }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetails(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="totalRecords"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Download } from '@element-plus/icons-vue'

const loading = ref(false)
const donorChartPeriod = ref('6m')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)

// Statistics data
const monthlyStats = reactive({
  newDonors: 12,
  processedRequests: 28,
  recordedDonations: 45
})

const efficiencyStats = reactive({
  avgProcessTime: 15,
  completionRate: 92,
  satisfaction: 4.6
})

// Chart data
const donorChartData = ref([8, 12, 15, 10, 18, 14])

const bloodTypeData = ref([
  { type: 'A+', count: 25 },
  { type: 'B+', count: 18 },
  { type: 'O+', count: 32 },
  { type: 'AB+', count: 8 }
])

const weeklyData = ref([
  {
    day: '周一',
    hours: [2, 3, 5, 8, 12, 15, 18, 20, 16, 12, 8, 5]
  },
  {
    day: '周二',
    hours: [1, 4, 6, 9, 14, 17, 19, 18, 14, 10, 6, 3]
  },
  {
    day: '周三',
    hours: [3, 5, 7, 10, 13, 16, 20, 17, 13, 9, 5, 2]
  },
  {
    day: '周四',
    hours: [2, 4, 6, 8, 11, 14, 18, 19, 15, 11, 7, 4]
  },
  {
    day: '周五',
    hours: [1, 3, 5, 7, 10, 13, 16, 21, 17, 13, 9, 6]
  }
])

// Work records data
const workRecords = ref([
  {
    date: '2024-06-20',
    type: 'donor',
    description: '新增捐赠者王小明',
    quantity: 1,
    duration: 15,
    status: 'completed'
  },
  {
    date: '2024-06-20',
    type: 'request',
    description: '处理输血申请REQ-2024-001',
    quantity: 1,
    duration: 20,
    status: 'completed'
  },
  {
    date: '2024-06-19',
    type: 'donation',
    description: '记录李小红血液捐赠',
    quantity: 1,
    duration: 10,
    status: 'completed'
  },
  {
    date: '2024-06-19',
    type: 'donor',
    description: '更新捐赠者张小华信息',
    quantity: 1,
    duration: 8,
    status: 'completed'
  }
])

// Computed properties
const maxDonorCount = computed(() => 
  Math.max(...bloodTypeData.value.map(type => type.count))
)

// Methods
const getWorkTypeColor = (type) => {
  const colors = {
    donor: 'primary',
    request: 'success',
    donation: 'warning',
    other: 'info'
  }
  return colors[type] || 'info'
}

const getWorkTypeText = (type) => {
  const texts = {
    donor: '捐赠者管理',
    request: '申请处理',
    donation: '捐赠记录',
    other: '其他'
  }
  return texts[type] || type
}

const getStatusColor = (status) => {
  const colors = {
    completed: 'success',
    pending: 'warning',
    failed: 'danger'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    completed: '已完成',
    pending: '进行中',
    failed: '失败'
  }
  return texts[status] || status
}

const getActivityLevel = (value) => {
  if (value >= 15) return 'high'
  if (value >= 8) return 'medium'
  return 'low'
}

const handleDateChange = () => {
  refreshData()
}

const refreshData = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('数据已刷新')
  }, 1000)
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}

const viewDetails = (record) => {
  ElMessage.info(`查看工作记录详情: ${record.description}`)
}

const generateReport = () => {
  ElMessage.info('个人报告生成功能开发中')
}

const exportData = () => {
  ElMessage.info('数据导出功能开发中')
}

onMounted(() => {
  totalRecords.value = workRecords.value.length
})
</script>

<style scoped>
.user-personal-analytics {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

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
  font-weight: 700;
}

.title-section p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.overview-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.overview-card h3 {
  margin: 0;
  color: #333;
}

.overview-content {
  padding: 20px 0;
}

.overview-stats {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.efficiency-metrics {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.metric-label {
  font-size: 14px;
  color: #666;
}

.metric-value {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
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
  padding: 16px 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-content {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 150px;
  width: 100%;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.chart-bar:hover {
  opacity: 0.8;
}

.pie-chart {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.pie-segments {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.pie-segment {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.pie-segment.approved { background: #67c23a; }
.pie-segment.pending { background: #e6a23c; }
.pie-segment.rejected { background: #f56c6c; }

.blood-type-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.blood-type-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-info {
  width: 80px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.type-count {
  color: #666;
}

.type-progress {
  flex: 1;
  height: 20px;
  background: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.activity-heatmap {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.heatmap-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.day-label {
  width: 40px;
  font-size: 12px;
  color: #666;
  text-align: right;
}

.hour-bars {
  display: flex;
  gap: 2px;
  flex: 1;
}

.hour-bar {
  flex: 1;
  height: 20px;
  border-radius: 2px;
  cursor: pointer;
}

.hour-bar.low { background: #e8f5e8; }
.hour-bar.medium { background: #fff3cd; }
.hour-bar.high { background: #f8d7da; }

.table-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header h3 {
  margin: 0;
  color: #333;
}

.table-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .overview-stats {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
