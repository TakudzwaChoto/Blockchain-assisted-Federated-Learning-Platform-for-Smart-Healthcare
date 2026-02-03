<template>
  <div class="government-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <div class="welcome-section">
          <h1>政府监管仪表板</h1>
          <p>血液管理监管与政策协调平台</p>
        </div>
        <div class="header-stats">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ totalInstitutions }}</div>
              <div class="stat-label">监管机构</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ complianceRate }}%</div>
              <div class="stat-label">合规率</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ activeAlerts }}</div>
              <div class="stat-label">活跃警报</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="content-grid">
        <!-- Regulatory Oversight -->
        <div class="dashboard-card oversight-card">
          <div class="card-header">
            <h3>监管概览</h3>
            <el-button type="primary" @click="$router.push('/government/oversight')">
              详细查看
            </el-button>
          </div>
          <div class="card-content">
            <div class="oversight-metrics">
              <div class="metric-item">
                <div class="metric-label">血液安全标准</div>
                <div class="metric-value">
                  <el-progress :percentage="95" color="#67c23a" />
                </div>
              </div>
              <div class="metric-item">
                <div class="metric-label">质量控制合规</div>
                <div class="metric-value">
                  <el-progress :percentage="88" color="#e6a23c" />
                </div>
              </div>
              <div class="metric-item">
                <div class="metric-label">应急响应能力</div>
                <div class="metric-value">
                  <el-progress :percentage="92" color="#409eff" />
                </div>
              </div>
            </div>
            <div class="recent-inspections">
              <h4>近期检查</h4>
              <div class="inspection-list">
                <div v-for="inspection in recentInspections" :key="inspection.id" class="inspection-item">
                  <div class="inspection-info">
                    <div class="inspection-name">{{ inspection.institution }}</div>
                    <div class="inspection-date">{{ inspection.date }}</div>
                  </div>
                  <div class="inspection-status" :class="inspection.status">
                    {{ inspection.statusText }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Policy Compliance -->
        <div class="dashboard-card policy-card">
          <div class="card-header">
            <h3>政策合规</h3>
            <el-button type="primary" @click="$router.push('/government/policy')">
              政策管理
            </el-button>
          </div>
          <div class="card-content">
            <div class="policy-summary">
              <div class="summary-item">
                <div class="summary-icon">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="summary-content">
                  <div class="summary-title">现行政策</div>
                  <div class="summary-value">{{ activePolicies }} 项</div>
                </div>
              </div>
              <div class="summary-item">
                <div class="summary-icon">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="summary-content">
                  <div class="summary-title">待审核</div>
                  <div class="summary-value">{{ pendingPolicies }} 项</div>
                </div>
              </div>
            </div>
            <div class="policy-updates">
              <h4>最新政策更新</h4>
              <div class="update-list">
                <div v-for="update in policyUpdates" :key="update.id" class="update-item">
                  <div class="update-title">{{ update.title }}</div>
                  <div class="update-date">{{ update.date }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Emergency Coordination -->
        <div class="dashboard-card emergency-card">
          <div class="card-header">
            <h3>应急协调</h3>
            <el-button type="danger" @click="$router.push('/government/emergency')">
              应急中心
            </el-button>
          </div>
          <div class="card-content">
            <div class="emergency-status">
              <div class="status-indicator" :class="emergencyStatus.level">
                <div class="status-dot"></div>
                <div class="status-text">{{ emergencyStatus.text }}</div>
              </div>
            </div>
            <div class="emergency-resources">
              <h4>应急资源</h4>
              <div class="resource-grid">
                <div class="resource-item">
                  <div class="resource-label">血液储备</div>
                  <div class="resource-value">{{ emergencyResources.bloodReserve }} 单位</div>
                </div>
                <div class="resource-item">
                  <div class="resource-label">运输车辆</div>
                  <div class="resource-value">{{ emergencyResources.vehicles }} 辆</div>
                </div>
                <div class="resource-item">
                  <div class="resource-label">医疗人员</div>
                  <div class="resource-value">{{ emergencyResources.staff }} 人</div>
                </div>
                <div class="resource-item">
                  <div class="resource-label">合作机构</div>
                  <div class="resource-value">{{ emergencyResources.partners }} 家</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Regional Statistics -->
        <div class="dashboard-card stats-card">
          <div class="card-header">
            <h3>区域统计</h3>
            <el-button @click="refreshStats">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
          <div class="card-content">
            <div class="region-selector">
              <el-select v-model="selectedRegion" @change="updateRegionStats">
                <el-option label="全国" value="national" />
                <el-option label="北京市" value="beijing" />
                <el-option label="上海市" value="shanghai" />
                <el-option label="广东省" value="guangdong" />
              </el-select>
            </div>
            <div class="region-stats">
              <div class="stat-row">
                <div class="stat-item">
                  <div class="stat-label">年采血量</div>
                  <div class="stat-value">{{ regionStats.annualCollection }} 万袋</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">年用血量</div>
                  <div class="stat-value">{{ regionStats.annualUsage }} 万袋</div>
                </div>
              </div>
              <div class="stat-row">
                <div class="stat-item">
                  <div class="stat-label">库存充足率</div>
                  <div class="stat-value">{{ regionStats.inventoryRate }}%</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">应急响应时间</div>
                  <div class="stat-value">{{ regionStats.responseTime }} 分钟</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  DataAnalysis, 
  TrendCharts, 
  Warning, 
  Document, 
  Clock, 
  Refresh 
} from '@element-plus/icons-vue'

// Reactive data
const totalInstitutions = ref(156)
const complianceRate = ref(94.5)
const activeAlerts = ref(3)
const activePolicies = ref(28)
const pendingPolicies = ref(5)
const selectedRegion = ref('national')

const recentInspections = ref([
  {
    id: 1,
    institution: '北京协和医院',
    date: '2024-06-20',
    status: 'pass',
    statusText: '通过'
  },
  {
    id: 2,
    institution: '上海瑞金医院',
    date: '2024-06-18',
    status: 'warning',
    statusText: '警告'
  },
  {
    id: 3,
    institution: '广州中山医院',
    date: '2024-06-15',
    status: 'fail',
    statusText: '不通过'
  }
])

const policyUpdates = ref([
  {
    id: 1,
    title: '血液安全管理条例修订',
    date: '2024-06-15'
  },
  {
    id: 2,
    title: '应急血液调配预案',
    date: '2024-06-10'
  },
  {
    id: 3,
    title: '血液质量检测标准更新',
    date: '2024-06-05'
  }
])

const emergencyStatus = ref({
  level: 'normal',
  text: '正常状态'
})

const emergencyResources = ref({
  bloodReserve: 12500,
  vehicles: 45,
  staff: 128,
  partners: 23
})

const regionStats = ref({
  annualCollection: 285.6,
  annualUsage: 276.3,
  inventoryRate: 96.8,
  responseTime: 12
})

// Methods
const refreshStats = () => {
  // Simulate data refresh
  console.log('Refreshing statistics...')
}

const updateRegionStats = (region) => {
  // Simulate region-specific data update
  const statsMap = {
    national: { annualCollection: 285.6, annualUsage: 276.3, inventoryRate: 96.8, responseTime: 12 },
    beijing: { annualCollection: 45.2, annualUsage: 43.8, inventoryRate: 97.2, responseTime: 8 },
    shanghai: { annualCollection: 38.7, annualUsage: 37.5, inventoryRate: 95.8, responseTime: 10 },
    guangdong: { annualCollection: 52.3, annualUsage: 50.1, inventoryRate: 96.5, responseTime: 15 }
  }
  regionStats.value = statsMap[region] || statsMap.national
}

onMounted(() => {
  // Initialize dashboard data
  updateRegionStats('national')
})
</script>

<style scoped>
.government-dashboard {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-header {
  margin-bottom: 24px;
}

.header-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.welcome-section h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.welcome-section p {
  margin: 0 0 24px 0;
  color: #666;
  font-size: 16px;
}

.header-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.stat-icon {
  font-size: 24px;
  opacity: 0.8;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 4px;
}

.dashboard-content {
  margin-top: 24px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.card-content {
  padding: 24px;
}

.oversight-metrics {
  margin-bottom: 24px;
}

.metric-item {
  margin-bottom: 16px;
}

.metric-label {
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.recent-inspections h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.inspection-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.inspection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.inspection-name {
  font-weight: 500;
  color: #333;
}

.inspection-date {
  font-size: 12px;
  color: #666;
}

.inspection-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.inspection-status.pass {
  background: #f0f9ff;
  color: #67c23a;
}

.inspection-status.warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.inspection-status.fail {
  background: #fef0f0;
  color: #f56c6c;
}

.policy-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.summary-icon {
  font-size: 20px;
  color: #667eea;
}

.summary-title {
  font-size: 14px;
  color: #666;
}

.summary-value {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.policy-updates h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.update-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.update-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.update-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.update-date {
  font-size: 12px;
  color: #666;
}

.emergency-status {
  margin-bottom: 24px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: 8px;
}

.status-indicator.normal {
  background: #f0f9ff;
  color: #67c23a;
}

.status-indicator.warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.status-indicator.critical {
  background: #fef0f0;
  color: #f56c6c;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.emergency-resources h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.resource-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.resource-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.resource-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.resource-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.region-selector {
  margin-bottom: 20px;
}

.region-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .header-stats {
    grid-template-columns: 1fr;
  }
  
  .policy-summary,
  .resource-grid,
  .stat-row {
    grid-template-columns: 1fr;
  }
}
</style>
