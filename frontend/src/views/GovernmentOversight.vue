<template>
  <div class="government-oversight">
    <div class="oversight-header">
      <h1>监管监督</h1>
      <p>血液管理机构监督与合规检查</p>
    </div>

    <div class="oversight-content">
      <!-- Compliance Monitoring -->
      <div class="section-card">
        <div class="section-header">
          <h3>合规监控</h3>
          <div class="header-actions">
            <el-button type="primary" @click="generateReport">
              <el-icon><Document /></el-icon>
              生成报告
            </el-button>
          </div>
        </div>
        <div class="compliance-grid">
          <div class="compliance-item">
            <div class="compliance-header">
              <h4>血液安全标准</h4>
              <div class="compliance-score excellent">98%</div>
            </div>
            <div class="compliance-details">
              <div class="detail-item">
                <span class="detail-label">检测合格率</span>
                <span class="detail-value">98.5%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">存储合规</span>
                <span class="detail-value">97.2%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">运输安全</span>
                <span class="detail-value">99.1%</span>
              </div>
            </div>
          </div>
          
          <div class="compliance-item">
            <div class="compliance-header">
              <h4>质量控制</h4>
              <div class="compliance-score good">85%</div>
            </div>
            <div class="compliance-details">
              <div class="detail-item">
                <span class="detail-label">流程规范</span>
                <span class="detail-value">87.3%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">人员培训</span>
                <span class="detail-value">82.1%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">设备维护</span>
                <span class="detail-value">86.5%</span>
              </div>
            </div>
          </div>
          
          <div class="compliance-item">
            <div class="compliance-header">
              <h4>应急响应</h4>
              <div class="compliance-score good">92%</div>
            </div>
            <div class="compliance-details">
              <div class="detail-item">
                <span class="detail-label">响应时间</span>
                <span class="detail-value">94.2%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">资源调配</span>
                <span class="detail-value">89.7%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">协调效率</span>
                <span class="detail-value">92.1%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Institution Inspections -->
      <div class="section-card">
        <div class="section-header">
          <h3>机构检查</h3>
          <div class="header-actions">
            <el-button @click="scheduleInspection">
              <el-icon><Plus /></el-icon>
              安排检查
            </el-button>
            <el-button @click="exportInspections">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
          </div>
        </div>
        <div class="inspections-table">
          <el-table :data="inspections" stripe>
            <el-table-column prop="institution" label="机构名称" width="200" />
            <el-table-column prop="type" label="检查类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getInspectionTypeColor(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="检查日期" width="120" />
            <el-table-column prop="inspector" label="检查员" width="120" />
            <el-table-column prop="score" label="评分" width="100">
              <template #default="{ row }">
                <div class="score-display" :class="getScoreClass(row.score)">
                  {{ row.score }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusColor(row.status)">
                  {{ row.statusText }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="viewInspection(row)">
                  查看详情
                </el-button>
                <el-button size="small" type="primary" @click="downloadReport(row)">
                  下载报告
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Violations & Penalties -->
      <div class="section-card">
        <div class="section-header">
          <h3>违规处理</h3>
          <div class="header-actions">
            <el-button type="warning" @click="issueViolation">
              <el-icon><Warning /></el-icon>
              发出违规通知
            </el-button>
          </div>
        </div>
        <div class="violations-grid">
          <div class="violation-summary">
            <div class="summary-item critical">
              <div class="summary-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="summary-content">
                <div class="summary-title">严重违规</div>
                <div class="summary-value">{{ violations.critical }}</div>
              </div>
            </div>
            <div class="summary-item warning">
              <div class="summary-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="summary-content">
                <div class="summary-title">一般违规</div>
                <div class="summary-value">{{ violations.warning }}</div>
              </div>
            </div>
            <div class="summary-item info">
              <div class="summary-icon">
                <el-icon><InfoFilled /></el-icon>
              </div>
              <div class="summary-content">
                <div class="summary-title">轻微违规</div>
                <div class="summary-value">{{ violations.info }}</div>
              </div>
            </div>
          </div>
          
          <div class="recent-violations">
            <h4>近期违规记录</h4>
            <div class="violation-list">
              <div v-for="violation in recentViolations" :key="violation.id" class="violation-item">
                <div class="violation-header">
                  <div class="violation-institution">{{ violation.institution }}</div>
                  <div class="violation-type" :class="violation.severity">
                    {{ violation.type }}
                  </div>
                </div>
                <div class="violation-details">
                  <div class="violation-description">{{ violation.description }}</div>
                  <div class="violation-meta">
                    <span class="violation-date">{{ violation.date }}</span>
                    <span class="violation-penalty">罚金: ¥{{ violation.penalty }}</span>
                  </div>
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
import { ref } from 'vue'
import { 
  Document, 
  Plus, 
  Download, 
  Warning, 
  InfoFilled 
} from '@element-plus/icons-vue'

// Mock data
const inspections = ref([
  {
    id: 1,
    institution: '北京协和医院',
    type: '常规检查',
    date: '2024-06-20',
    inspector: '张检查员',
    score: 95,
    status: 'pass',
    statusText: '通过'
  },
  {
    id: 2,
    institution: '上海瑞金医院',
    type: '专项检查',
    date: '2024-06-18',
    inspector: '李检查员',
    score: 78,
    status: 'warning',
    statusText: '警告'
  },
  {
    id: 3,
    institution: '广州中山医院',
    type: '突击检查',
    date: '2024-06-15',
    inspector: '王检查员',
    score: 62,
    status: 'fail',
    statusText: '不通过'
  }
])

const violations = ref({
  critical: 2,
  warning: 8,
  info: 15
})

const recentViolations = ref([
  {
    id: 1,
    institution: '深圳人民医院',
    type: '存储违规',
    severity: 'critical',
    description: '血液存储温度不符合标准，存在安全隐患',
    date: '2024-06-19',
    penalty: 50000
  },
  {
    id: 2,
    institution: '天津第一医院',
    type: '记录不全',
    severity: 'warning',
    description: '血液使用记录不完整，追溯困难',
    date: '2024-06-17',
    penalty: 20000
  },
  {
    id: 3,
    institution: '杭州中心医院',
    type: '培训缺失',
    severity: 'info',
    description: '部分人员未完成年度培训',
    date: '2024-06-15',
    penalty: 10000
  }
])

// Methods
const generateReport = () => {
  console.log('Generating compliance report...')
}

const scheduleInspection = () => {
  console.log('Scheduling inspection...')
}

const exportInspections = () => {
  console.log('Exporting inspection data...')
}

const viewInspection = (inspection) => {
  console.log('Viewing inspection:', inspection)
}

const downloadReport = (inspection) => {
  console.log('Downloading report for:', inspection.institution)
}

const issueViolation = () => {
  console.log('Issuing violation notice...')
}

const getInspectionTypeColor = (type) => {
  const colorMap = {
    '常规检查': '',
    '专项检查': 'warning',
    '突击检查': 'danger'
  }
  return colorMap[type] || ''
}

const getScoreClass = (score) => {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 70) return 'average'
  return 'poor'
}

const getStatusColor = (status) => {
  const colorMap = {
    'pass': 'success',
    'warning': 'warning',
    'fail': 'danger'
  }
  return colorMap[status] || ''
}
</script>

<style scoped>
.government-oversight {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.oversight-header {
  margin-bottom: 24px;
}

.oversight-header h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.oversight-header p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.oversight-content {
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

.compliance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  padding: 24px;
}

.compliance-item {
  padding: 20px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.compliance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.compliance-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.compliance-score {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 14px;
}

.compliance-score.excellent {
  background: #f0f9ff;
  color: #67c23a;
}

.compliance-score.good {
  background: #f0f9ff;
  color: #409eff;
}

.compliance-score.average {
  background: #fdf6ec;
  color: #e6a23c;
}

.compliance-score.poor {
  background: #fef0f0;
  color: #f56c6c;
}

.compliance-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  color: #666;
  font-size: 14px;
}

.detail-value {
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.inspections-table {
  padding: 24px;
}

.score-display {
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.score-display.excellent {
  background: #f0f9ff;
  color: #67c23a;
}

.score-display.good {
  background: #f0f9ff;
  color: #409eff;
}

.score-display.average {
  background: #fdf6ec;
  color: #e6a23c;
}

.score-display.poor {
  background: #fef0f0;
  color: #f56c6c;
}

.violations-grid {
  padding: 24px;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
}

.violation-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid;
}

.summary-item.critical {
  background: #fef0f0;
  border-left-color: #f56c6c;
}

.summary-item.warning {
  background: #fdf6ec;
  border-left-color: #e6a23c;
}

.summary-item.info {
  background: #f0f9ff;
  border-left-color: #409eff;
}

.summary-icon {
  font-size: 20px;
}

.summary-item.critical .summary-icon {
  color: #f56c6c;
}

.summary-item.warning .summary-icon {
  color: #e6a23c;
}

.summary-item.info .summary-icon {
  color: #409eff;
}

.summary-title {
  font-size: 14px;
  color: #666;
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.recent-violations h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.violation-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.violation-item {
  padding: 16px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.violation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.violation-institution {
  font-weight: 600;
  color: #333;
}

.violation-type {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.violation-type.critical {
  background: #fef0f0;
  color: #f56c6c;
}

.violation-type.warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.violation-type.info {
  background: #f0f9ff;
  color: #409eff;
}

.violation-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.violation-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

@media (max-width: 768px) {
  .compliance-grid {
    grid-template-columns: 1fr;
  }
  
  .violations-grid {
    grid-template-columns: 1fr;
  }
  
  .header-actions {
    flex-direction: column;
  }
}
</style>
