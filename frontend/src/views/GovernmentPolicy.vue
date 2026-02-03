<template>
  <div class="government-policy">
    <div class="policy-header">
      <h1>政策管理</h1>
      <p>血液管理政策制定与实施监督</p>
    </div>

    <div class="policy-content">
      <!-- Policy Overview -->
      <div class="section-card">
        <div class="section-header">
          <h3>政策概览</h3>
          <div class="header-actions">
            <el-button type="primary" @click="createPolicy">
              <el-icon><Plus /></el-icon>
              制定新政策
            </el-button>
          </div>
        </div>
        <div class="policy-stats">
          <div class="stat-item">
            <div class="stat-number">{{ policyStats.active }}</div>
            <div class="stat-label">现行政策</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ policyStats.pending }}</div>
            <div class="stat-label">待审核</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ policyStats.draft }}</div>
            <div class="stat-label">草案</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ policyStats.archived }}</div>
            <div class="stat-label">已归档</div>
          </div>
        </div>
      </div>

      <!-- Active Policies -->
      <div class="section-card">
        <div class="section-header">
          <h3>现行政策</h3>
          <div class="header-actions">
            <el-select v-model="policyFilter" placeholder="筛选政策类型">
              <el-option label="全部" value="" />
              <el-option label="安全管理" value="safety" />
              <el-option label="质量控制" value="quality" />
              <el-option label="应急响应" value="emergency" />
              <el-option label="监督管理" value="oversight" />
            </el-select>
          </div>
        </div>
        <div class="policies-list">
          <div v-for="policy in filteredPolicies" :key="policy.id" class="policy-item">
            <div class="policy-header">
              <div class="policy-info">
                <h4>{{ policy.title }}</h4>
                <div class="policy-meta">
                  <span class="policy-type" :class="policy.type">{{ policy.typeText }}</span>
                  <span class="policy-date">发布日期: {{ policy.publishDate }}</span>
                  <span class="policy-effective">生效日期: {{ policy.effectiveDate }}</span>
                </div>
              </div>
              <div class="policy-status">
                <el-tag :type="getStatusType(policy.status)">
                  {{ policy.statusText }}
                </el-tag>
              </div>
            </div>
            <div class="policy-content">
              <p>{{ policy.summary }}</p>
              <div class="policy-actions">
                <el-button size="small" @click="viewPolicy(policy)">
                  查看详情
                </el-button>
                <el-button size="small" type="primary" @click="editPolicy(policy)">
                  编辑
                </el-button>
                <el-button size="small" @click="trackCompliance(policy)">
                  合规跟踪
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Policy Development -->
      <div class="section-card">
        <div class="section-header">
          <h3>政策制定</h3>
          <div class="header-actions">
            <el-button @click="reviewDrafts">
              <el-icon><Document /></el-icon>
              审核草案
            </el-button>
          </div>
        </div>
        <div class="development-timeline">
          <div class="timeline-item">
            <div class="timeline-marker research">
              <el-icon><Search /></el-icon>
            </div>
            <div class="timeline-content">
              <h4>政策研究</h4>
              <p>基于数据分析和社会需求进行政策研究</p>
              <div class="timeline-status">
                <span class="status-text">进行中</span>
                <span class="status-progress">3个项目</span>
              </div>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker drafting">
              <el-icon><Edit /></el-icon>
            </div>
            <div class="timeline-content">
              <h4>草案制定</h4>
              <p>起草政策文件和相关实施细则</p>
              <div class="timeline-status">
                <span class="status-text">审核中</span>
                <span class="status-progress">2个草案</span>
              </div>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker review">
              <el-icon><User /></el-icon>
            </div>
            <div class="timeline-content">
              <h4>专家评审</h4>
              <p>组织专家委员会进行政策评审</p>
              <div class="timeline-status">
                <span class="status-text">待安排</span>
                <span class="status-progress">1个政策</span>
              </div>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker implementation">
              <el-icon><Check /></el-icon>
            </div>
            <div class="timeline-content">
              <h4>实施发布</h4>
              <p>政策正式发布并开始实施</p>
              <div class="timeline-status">
                <span class="status-text">已完成</span>
                <span class="status-progress">5个政策</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Compliance Tracking -->
      <div class="section-card">
        <div class="section-header">
          <h3>合规跟踪</h3>
          <div class="header-actions">
            <el-button type="success" @click="generateComplianceReport">
              <el-icon><DataAnalysis /></el-icon>
              生成合规报告
            </el-button>
          </div>
        </div>
        <div class="compliance-overview">
          <div class="compliance-chart">
            <h4>政策合规率趋势</h4>
            <div class="chart-placeholder">
              <!-- 这里可以集成实际的图表组件 -->
              <div class="mock-chart">
                <div class="chart-bar" style="height: 85%">
                  <span class="chart-label">Q1</span>
                  <span class="chart-value">85%</span>
                </div>
                <div class="chart-bar" style="height: 88%">
                  <span class="chart-label">Q2</span>
                  <span class="chart-value">88%</span>
                </div>
                <div class="chart-bar" style="height: 92%">
                  <span class="chart-label">Q3</span>
                  <span class="chart-value">92%</span>
                </div>
                <div class="chart-bar" style="height: 94%">
                  <span class="chart-label">Q4</span>
                  <span class="chart-value">94%</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="compliance-details">
            <h4>合规详情</h4>
            <div class="compliance-list">
              <div v-for="compliance in complianceData" :key="compliance.policy" class="compliance-item">
                <div class="compliance-policy">{{ compliance.policy }}</div>
                <div class="compliance-rate">
                  <div class="rate-bar">
                    <div class="rate-fill" :style="{ width: compliance.rate + '%' }"></div>
                  </div>
                  <span class="rate-text">{{ compliance.rate }}%</span>
                </div>
                <div class="compliance-trend" :class="compliance.trend">
                  <el-icon>
                    <component :is="compliance.trend === 'up' ? 'TrendCharts' : 'TrendCharts'" />
                  </el-icon>
                  {{ compliance.change }}%
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
import { ref, computed } from 'vue'
import { 
  Plus, 
  Document, 
  Search, 
  Edit, 
  User, 
  Check,
  DataAnalysis,
  TrendCharts
} from '@element-plus/icons-vue'

// Reactive data
const policyFilter = ref('')

const policyStats = ref({
  active: 28,
  pending: 5,
  draft: 3,
  archived: 12
})

const policies = ref([
  {
    id: 1,
    title: '血液安全管理条例',
    type: 'safety',
    typeText: '安全管理',
    publishDate: '2024-01-15',
    effectiveDate: '2024-02-01',
    status: 'active',
    statusText: '生效中',
    summary: '规范血液采集、检测、储存、运输和使用全过程的安全管理要求，确保血液安全。'
  },
  {
    id: 2,
    title: '血液质量控制标准',
    type: 'quality',
    typeText: '质量控制',
    publishDate: '2024-03-10',
    effectiveDate: '2024-04-01',
    status: 'active',
    statusText: '生效中',
    summary: '建立血液质量控制的标准化流程和检测要求，提高血液质量水平。'
  },
  {
    id: 3,
    title: '应急血液调配预案',
    type: 'emergency',
    typeText: '应急响应',
    publishDate: '2024-05-20',
    effectiveDate: '2024-06-01',
    status: 'pending',
    statusText: '待生效',
    summary: '制定应急情况下的血液调配机制和流程，保障紧急用血需求。'
  },
  {
    id: 4,
    title: '血液机构监督管理办法',
    type: 'oversight',
    typeText: '监督管理',
    publishDate: '2024-02-28',
    effectiveDate: '2024-03-15',
    status: 'active',
    statusText: '生效中',
    summary: '明确血液管理机构的监督职责和检查标准，加强行业监管。'
  }
])

const complianceData = ref([
  {
    policy: '血液安全管理条例',
    rate: 95,
    trend: 'up',
    change: 3.2
  },
  {
    policy: '血液质量控制标准',
    rate: 88,
    trend: 'up',
    change: 2.1
  },
  {
    policy: '应急血液调配预案',
    rate: 92,
    trend: 'down',
    change: -1.5
  },
  {
    policy: '血液机构监督管理办法',
    rate: 94,
    trend: 'up',
    change: 4.7
  }
])

// Computed
const filteredPolicies = computed(() => {
  if (!policyFilter.value) return policies.value
  return policies.value.filter(policy => policy.type === policyFilter.value)
})

// Methods
const createPolicy = () => {
  console.log('Creating new policy...')
}

const viewPolicy = (policy) => {
  console.log('Viewing policy:', policy.title)
}

const editPolicy = (policy) => {
  console.log('Editing policy:', policy.title)
}

const trackCompliance = (policy) => {
  console.log('Tracking compliance for:', policy.title)
}

const reviewDrafts = () => {
  console.log('Reviewing policy drafts...')
}

const generateComplianceReport = () => {
  console.log('Generating compliance report...')
}

const getStatusType = (status) => {
  const typeMap = {
    'active': 'success',
    'pending': 'warning',
    'draft': 'info',
    'archived': ''
  }
  return typeMap[status] || ''
}
</script>

<style scoped>
.government-policy {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.policy-header {
  margin-bottom: 24px;
}

.policy-header h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.policy-header p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.policy-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.section-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.policy-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  padding: 24px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 8px;
}

.policies-list {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.policy-item {
  padding: 20px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.policy-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.policy-info h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.policy-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.policy-type {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.policy-type.safety {
  background: #f0f9ff;
  color: #409eff;
}

.policy-type.quality {
  background: #f0f9ff;
  color: #67c23a;
}

.policy-type.emergency {
  background: #fef0f0;
  color: #f56c6c;
}

.policy-type.oversight {
  background: #fdf6ec;
  color: #e6a23c;
}

.policy-date,
.policy-effective {
  font-size: 12px;
  color: #666;
}

.policy-content p {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.policy-actions {
  display: flex;
  gap: 8px;
}

.development-timeline {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.timeline-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.timeline-marker {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.timeline-marker.research {
  background: #409eff;
}

.timeline-marker.drafting {
  background: #e6a23c;
}

.timeline-marker.review {
  background: #67c23a;
}

.timeline-marker.implementation {
  background: #f56c6c;
}

.timeline-content {
  flex: 1;
}

.timeline-content h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.timeline-content p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.timeline-status {
  display: flex;
  gap: 12px;
  align-items: center;
}

.status-text {
  font-size: 12px;
  color: #666;
}

.status-progress {
  font-size: 12px;
  color: #409eff;
  font-weight: 500;
}

.compliance-overview {
  padding: 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.compliance-chart h4,
.compliance-details h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.mock-chart {
  display: flex;
  align-items: end;
  gap: 20px;
  height: 200px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: end;
  padding-bottom: 8px;
  color: white;
  font-weight: 500;
  font-size: 12px;
}

.compliance-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.compliance-item {
  display: grid;
  grid-template-columns: 2fr 1fr 80px;
  gap: 12px;
  align-items: center;
}

.compliance-policy {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.compliance-rate {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rate-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.rate-fill {
  height: 100%;
  background: #67c23a;
  transition: width 0.3s ease;
}

.rate-text {
  font-size: 12px;
  color: #666;
  font-weight: 500;
  min-width: 35px;
}

.compliance-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.compliance-trend.up {
  color: #67c23a;
}

.compliance-trend.down {
  color: #f56c6c;
}

@media (max-width: 768px) {
  .policy-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .compliance-overview {
    grid-template-columns: 1fr;
  }
  
  .policy-meta {
    flex-direction: column;
    gap: 4px;
  }
  
  .timeline-item {
    flex-direction: column;
    text-align: center;
  }
  
  .compliance-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>
