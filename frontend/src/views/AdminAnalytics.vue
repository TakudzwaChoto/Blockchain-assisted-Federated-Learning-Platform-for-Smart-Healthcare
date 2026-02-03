<template>
  <div class="admin-analytics">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1>数据分析</h1>
          <p>系统全面数据分析和报告</p>
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

    <!-- Analytics Overview -->
    <div class="analytics-grid">
      <el-card class="analytics-card">
        <template #header>
          <h3>捐赠趋势分析</h3>
        </template>
        <div class="chart-container">
          <div class="mock-chart">
            <div class="chart-header">
              <span>月度捐赠趋势</span>
              <el-select v-model="donationPeriod" size="small" style="width: 120px">
                <el-option label="最近6个月" value="6m" />
                <el-option label="最近1年" value="1y" />
                <el-option label="全部时间" value="all" />
              </el-select>
            </div>
            <div class="chart-content">
              <div class="chart-bars">
                <div class="chart-bar" v-for="(value, index) in donationData" :key="index" 
                     :style="{ height: value + '%' }"
                     :title="`月份 ${index + 1}: ${value} 次捐赠`">
                </div>
              </div>
            </div>
            <div class="chart-stats">
              <div class="stat-item">
                <span class="stat-label">总捐赠次数:</span>
                <span class="stat-value">{{ donationStats.total }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">平均每月:</span>
                <span class="stat-value">{{ donationStats.average }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">增长率:</span>
                <span class="stat-value positive">+{{ donationStats.growth }}%</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="analytics-card">
        <template #header>
          <h3>血型分布</h3>
        </template>
        <div class="chart-container">
          <div class="blood-type-chart">
            <div class="chart-header">
              <span>血型分布统计</span>
            </div>
            <div class="blood-type-grid">
              <div class="blood-type-item" v-for="type in bloodTypeData" :key="type.type">
                <div class="type-circle" :style="{ background: type.color }">
                  <span class="type-percentage">{{ type.percentage }}%</span>
                </div>
                <div class="type-info">
                  <div class="type-name">{{ type.type }}</div>
                  <div class="type-count">{{ type.count }} 人</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="analytics-card">
        <template #header>
          <h3>库存状态</h3>
        </template>
        <div class="chart-container">
          <div class="inventory-chart">
            <div class="chart-header">
              <span>血液库存监控</span>
            </div>
            <div class="inventory-items">
              <div class="inventory-item" v-for="item in inventoryData" :key="item.type">
                <div class="item-header">
                  <span class="item-type">{{ item.type }}</span>
                  <span class="item-status" :class="item.status">{{ item.statusText }}</span>
                </div>
                <div class="item-progress">
                  <el-progress 
                    :percentage="item.percentage" 
                    :color="getProgressColor(item.percentage)"
                    :show-text="false"
                  />
                </div>
                <div class="item-details">
                  <span class="item-amount">{{ item.amount }}ml</span>
                  <span class="item-capacity">容量: {{ item.capacity }}ml</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="analytics-card">
        <template #header>
          <h3>用户活动</h3>
        </template>
        <div class="chart-container">
          <div class="activity-chart">
            <div class="chart-header">
              <span>用户活动统计</span>
            </div>
            <div class="activity-stats">
              <div class="activity-item">
                <div class="activity-icon active-users">
                  <el-icon><User /></el-icon>
                </div>
                <div class="activity-info">
                  <div class="activity-number">{{ userStats.activeUsers }}</div>
                  <div class="activity-label">活跃用户</div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon daily-logins">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="activity-info">
                  <div class="activity-number">{{ userStats.dailyLogins }}</div>
                  <div class="activity-label">今日登录</div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon new-users">
                  <el-icon><Plus /></el-icon>
                </div>
                <div class="activity-info">
                  <div class="activity-number">{{ userStats.newUsers }}</div>
                  <div class="activity-label">新增用户</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Detailed Analytics Table -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <h3>详细数据统计</h3>
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

      <el-table :data="analyticsData" style="width: 100%" v-loading="loading">
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="donations" label="捐赠次数" width="100" />
        <el-table-column prop="donors" label="捐赠人数" width="100" />
        <el-table-column prop="requests" label="申请数量" width="100" />
        <el-table-column prop="processed" label="处理数量" width="100" />
        <el-table-column prop="inventory" label="库存变化" width="120">
          <template #default="{ row }">
            <span :class="row.inventory > 0 ? 'positive' : 'negative'">
              {{ row.inventory > 0 ? '+' : '' }}{{ row.inventory }}ml
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="alerts" label="警报数量" width="100" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Download, User, Clock, Plus } from '@element-plus/icons-vue'

const loading = ref(false)
const donationPeriod = ref('6m')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)

// Mock data
const donationData = ref([65, 80, 45, 90, 75, 85])

const donationStats = reactive({
  total: 440,
  average: 73,
  growth: 12.5
})

const bloodTypeData = ref([
  { type: 'O+', count: 1250, percentage: 45, color: '#f56c6c' },
  { type: 'A+', count: 890, percentage: 30, color: '#409eff' },
  { type: 'B+', count: 520, percentage: 20, color: '#67c23a' },
  { type: 'AB+', count: 180, percentage: 5, color: '#e6a23c' }
])

const inventoryData = ref([
  { type: 'A+', amount: 1250, capacity: 2000, percentage: 62.5, status: 'normal', statusText: '正常' },
  { type: 'B+', amount: 450, capacity: 2000, percentage: 22.5, status: 'low', statusText: '偏低' },
  { type: 'O+', amount: 1890, capacity: 2000, percentage: 94.5, status: 'normal', statusText: '正常' },
  { type: 'AB+', amount: 180, capacity: 2000, percentage: 9, status: 'critical', statusText: '紧急' }
])

const userStats = reactive({
  activeUsers: 156,
  dailyLogins: 89,
  newUsers: 12
})

const analyticsData = ref([
  {
    date: '2024-06-01',
    donations: 45,
    donors: 32,
    requests: 12,
    processed: 11,
    inventory: 1200,
    alerts: 2
  },
  {
    date: '2024-06-02',
    donations: 38,
    donors: 28,
    requests: 8,
    processed: 8,
    inventory: -800,
    alerts: 1
  },
  {
    date: '2024-06-03',
    donations: 52,
    donors: 41,
    requests: 15,
    processed: 14,
    inventory: 1500,
    alerts: 3
  }
])

// Methods
const getProgressColor = (percentage) => {
  if (percentage >= 70) return '#67c23a'
  if (percentage >= 30) return '#e6a23c'
  return '#f56c6c'
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

const viewDetails = (row) => {
  ElMessage.info(`查看 ${row.date} 的详细数据`)
}

const generateReport = () => {
  ElMessage.info('报告生成功能开发中')
}

const exportData = () => {
  ElMessage.info('数据导出功能开发中')
}

onMounted(() => {
  totalRecords.value = analyticsData.value.length
})
</script>

<style scoped>
.admin-analytics {
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

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
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

.chart-container {
  padding: 16px 0;
}

.mock-chart {
  height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-content {
  flex: 1;
  display: flex;
  align-items: flex-end;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
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

.chart-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.stat-value.positive {
  color: #67c23a;
}

.blood-type-chart {
  height: 300px;
}

.blood-type-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding: 20px;
}

.blood-type-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.type-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 12px;
}

.type-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.type-count {
  font-size: 14px;
  color: #666;
}

.inventory-chart {
  height: 300px;
}

.inventory-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
}

.inventory-item {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 16px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-type {
  font-weight: 600;
  color: #333;
}

.item-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
}

.item-status.normal {
  background: #f0f9ff;
  color: #67c23a;
}

.item-status.low {
  background: #fdf6ec;
  color: #e6a23c;
}

.item-status.critical {
  background: #fef0f0;
  color: #f56c6c;
}

.item-progress {
  margin-bottom: 8px;
}

.item-details {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.activity-chart {
  height: 300px;
}

.activity-stats {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 40px 20px;
}

.activity-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.activity-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 12px;
}

.activity-icon.active-users {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.activity-icon.daily-logins {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.activity-icon.new-users {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.activity-number {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.activity-label {
  font-size: 14px;
  color: #666;
}

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

.positive {
  color: #67c23a;
}

.negative {
  color: #f56c6c;
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
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .blood-type-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-stats {
    flex-direction: column;
    gap: 24px;
  }
}
</style>
