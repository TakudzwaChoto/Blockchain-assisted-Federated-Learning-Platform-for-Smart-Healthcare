<template>
  <div class="compliance-tracking">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>Compliance Tracking</span>
              <div class="header-actions">
                <el-button type="primary" @click="runAudit">
                  <el-icon><Document /></el-icon>
                  Run Audit
                </el-button>
                <el-button @click="refreshCompliance">
                  <el-icon><Refresh /></el-icon>
                  Refresh
                </el-button>
              </div>
            </div>
          </template>

          <!-- Compliance Score -->
          <el-row :gutter="16" class="compliance-overview">
            <el-col :span="8">
              <div class="compliance-score-card">
                <div class="score-circle" :class="getScoreClass(overallScore)">
                  <div class="score-value">{{ overallScore }}</div>
                  <div class="score-label">Compliance Score</div>
                </div>
              </div>
            </el-col>
            <el-col :span="16">
              <div class="compliance-metrics">
                <div v-for="metric in complianceMetrics" :key="metric.name" class="metric-item">
                  <div class="metric-label">{{ metric.label }}</div>
                  <div class="metric-progress">
                    <el-progress :percentage="metric.value" :color="getProgressColor(metric.value)" />
                    <div class="metric-value">{{ metric.value }}%</div>
                  </div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Compliance Areas -->
          <el-divider>Compliance Areas</el-divider>
          <el-row :gutter="16">
            <el-col :span="8" v-for="area in complianceAreas" :key="area.id">
              <div class="compliance-area-card" :class="area.status.toLowerCase()">
                <div class="area-header">
                  <div class="area-icon" :style="{ backgroundColor: area.color }">
                    <el-icon>
                      <component :is="area.icon" />
                    </el-icon>
                  </div>
                  <div class="area-title">{{ area.title }}</div>
                </div>
                <div class="area-score">{{ area.score }}%</div>
                <div class="area-status">{{ area.status }}</div>
                <el-progress :percentage="area.score" :color="getProgressColor(area.score)" />
              </div>
            </el-col>
          </el-row>

          <!-- Recent Audits -->
          <el-divider>Recent Audits</el-divider>
          <el-table :data="recentAudits" style="width: 100%">
            <el-table-column prop="id" label="Audit ID" width="120" />
            <el-table-column prop="type" label="Type" width="150">
              <template #default="{ row }">
                <el-tag :type="getAuditTypeColor(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="Date" width="120" />
            <el-table-column prop="auditor" label="Auditor" />
            <el-table-column prop="score" label="Score" width="100">
              <template #default="{ row }">
                <el-tag :type="getScoreTagType(row.score)">
                  {{ row.score }}%
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="findings" label="Findings" width="100" />
            <el-table-column prop="status" label="Status" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="viewAudit(row)">View</el-button>
                <el-button size="small" type="primary" @click="downloadReport(row)">Report</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Violations -->
          <el-divider>Active Violations</el-divider>
          <el-table :data="violations" style="width: 100%">
            <el-table-column prop="id" label="Violation ID" width="120" />
            <el-table-column prop="category" label="Category" width="150" />
            <el-table-column prop="description" label="Description" />
            <el-table-column prop="severity" label="Severity" width="100">
              <template #default="{ row }">
                <el-tag :type="getSeverityType(row.severity)">
                  {{ row.severity }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="Date" width="120" />
            <el-table-column prop="status" label="Status" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="investigate(row)">Investigate</el-button>
                <el-button size="small" type="primary" @click="resolve(row)">Resolve</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Document, Refresh, Lock, Warning, TrendCharts } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const overallScore = ref(92)
const complianceMetrics = ref([
  { name: 'documentation', label: 'Documentation', value: 95 },
  { name: 'storage', label: 'Storage Conditions', value: 88 },
  { name: 'transport', label: 'Transport Protocol', value: 92 },
  { name: 'testing', label: 'Testing Standards', value: 96 }
])

const complianceAreas = ref([
  {
    id: 'storage',
    title: 'Storage Compliance',
    icon: 'Lock',
    score: 88,
    status: 'Compliant',
    color: '#409eff'
  },
  {
    id: 'transport',
    title: 'Transport Safety',
    icon: 'Lock',
    score: 92,
    status: 'Compliant',
    color: '#67c23a'
  },
  {
    id: 'documentation',
    title: 'Documentation',
    icon: 'Document',
    score: 95,
    status: 'Compliant',
    color: '#e6a23c'
  }
])

const recentAudits = ref([
  {
    id: 'AUD-001',
    type: 'Storage Audit',
    date: '2024-01-15',
    auditor: 'Dr. Smith',
    score: 94,
    findings: 2,
    status: 'Completed'
  },
  {
    id: 'AUD-002',
    type: 'Transport Review',
    date: '2024-01-10',
    auditor: 'Jane Wilson',
    score: 88,
    findings: 5,
    status: 'In Progress'
  }
])

const violations = ref([
  {
    id: 'VIO-001',
    category: 'Temperature',
    description: 'Storage temperature exceeded 6°C for 2 hours',
    severity: 'Medium',
    date: '2024-01-14',
    status: 'Under Investigation'
  },
  {
    id: 'VIO-002',
    category: 'Documentation',
    description: 'Missing donor consent forms',
    severity: 'High',
    date: '2024-01-13',
    status: 'Resolved'
  }
])

const getScoreClass = (score) => {
  if (score >= 95) return 'excellent'
  if (score >= 85) return 'good'
  if (score >= 75) return 'fair'
  return 'poor'
}

const getProgressColor = (value) => {
  if (value >= 90) return '#67c23a'
  if (value >= 80) return '#409eff'
  if (value >= 70) return '#e6a23c'
  return '#f56c6c'
}

const getAuditTypeColor = (type) => {
  switch (type) {
    case 'Storage Audit': return 'success'
    case 'Transport Review': return 'warning'
    case 'Documentation Check': return 'info'
    default: return 'info'
  }
}

const getScoreTagType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'warning'
  return 'danger'
}

const getSeverityType = (severity) => {
  switch (severity) {
    case 'Low': return 'info'
    case 'Medium': return 'warning'
    case 'High': return 'danger'
    default: return 'info'
  }
}

const getStatusType = (status) => {
  switch (status) {
    case 'Completed': return 'success'
    case 'In Progress': return 'warning'
    case 'Under Investigation': return 'warning'
    case 'Resolved': return 'success'
    default: return 'info'
  }
}

const runAudit = () => {
  notificationStore.info('Starting compliance audit')
}

const refreshCompliance = () => {
  notificationStore.success('Compliance data refreshed')
}

const viewAudit = (audit) => {
  notificationStore.info(`Viewing audit: ${audit.id}`)
}

const downloadReport = (audit) => {
  notificationStore.success(`Downloading report for: ${audit.id}`)
}

const investigate = (violation) => {
  notificationStore.warning(`Investigating: ${violation.id}`)
}

const resolve = (violation) => {
  notificationStore.success(`Resolving violation: ${violation.id}`)
}
</script>

<style scoped>
.compliance-tracking {
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

.compliance-overview {
  margin-bottom: 32px;
}

.compliance-score-card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s ease;
}

.score-circle.excellent {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.score-circle.good {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
}

.score-circle.fair {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
  color: white;
}

.score-circle.poor {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: white;
}

.score-value {
  font-size: 36px;
  line-height: 1;
}

.score-label {
  font-size: 14px;
  margin-top: 8px;
}

.compliance-metrics {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  height: 200px;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.metric-label {
  width: 120px;
  font-weight: 500;
}

.metric-progress {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.metric-value {
  width: 50px;
  text-align: right;
  font-weight: 600;
}

.compliance-area-card {
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e4e7ed;
  transition: all 0.3s ease;
  margin-bottom: 16px;
}

.compliance-area-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.compliance-area-card.compliant {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e1f3d8 100%);
}

.area-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.area-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.area-title {
  font-weight: 600;
  color: #303133;
}

.area-score {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.area-status {
  font-size: 14px;
  color: #606266;
  margin-bottom: 12px;
}
</style>
