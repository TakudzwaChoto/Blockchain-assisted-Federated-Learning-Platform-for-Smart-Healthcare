<template>
  <div class="data-quality">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>数据质量管理</span>
              <el-button type="primary" @click="runQualityCheck">
                <el-icon><Refresh /></el-icon>
                运行质量检查
              </el-button>
            </div>
          </template>

          <!-- Quality Score Overview -->
          <el-row :gutter="16" class="quality-overview">
            <el-col :span="8">
              <div class="quality-score-card">
                <div class="score-circle" :class="getScoreClass(overallScore)">
                  <div class="score-value">{{ overallScore }}</div>
                  <div class="score-label">总体评分</div>
                </div>
              </div>
            </el-col>
            <el-col :span="16">
              <div class="quality-metrics">
                <div v-for="metric in qualityMetrics" :key="metric.name" class="metric-item">
                  <div class="metric-label">{{ metric.label }}</div>
                  <el-progress :percentage="metric.value" :color="getProgressColor(metric.value)" />
                  <div class="metric-value">{{ metric.value }}%</div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Quality Issues -->
          <el-divider>质量问题</el-divider>
          <el-table :data="qualityIssues" style="width: 100%">
            <el-table-column prop="severity" label="严重程度" width="100">
              <template #default="{ row }">
                <el-tag :type="getSeverityType(row.severity)">
                  {{ row.severity }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="issue" label="问题" />
            <el-table-column prop="count" label="数量" width="100" />
            <el-table-column prop="percentage" label="百分比" width="120" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="fixIssue(row)">修复</el-button>
                <el-button size="small" type="primary" @click="viewDetails(row)">详情</el-button>
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
import { Refresh } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const overallScore = ref(85)
const qualityMetrics = ref([
  { name: 'completeness', label: '完整性', value: 92 },
  { name: 'accuracy', label: '准确性', value: 88 },
  { name: 'consistency', label: '一致性', value: 78 },
  { name: 'validity', label: '有效性', value: 85 }
])

const qualityIssues = ref([
  {
    severity: 'error',
    issue: '缺少血型信息',
    count: 45,
    percentage: '3.2%'
  },
  {
    severity: 'warning',
    issue: '日期格式不一致',
    count: 128,
    percentage: '9.1%'
  },
  {
    severity: 'info',
    issue: '缺少可选联系信息',
    count: 234,
    percentage: '16.7%'
  }
])

const getScoreClass = (score) => {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 70) return 'fair'
  return 'poor'
}

const getProgressColor = (value) => {
  if (value >= 90) return '#67c23a'
  if (value >= 80) return '#409eff'
  if (value >= 70) return '#e6a23c'
  return '#f56c6c'
}

const getSeverityType = (severity) => {
  switch (severity) {
    case 'error': return 'danger'
    case 'warning': return 'warning'
    case 'info': return 'info'
    default: return 'info'
  }
}

const runQualityCheck = () => {
  notificationStore.success('质量检查已完成')
}

const fixIssue = (issue) => {
  notificationStore.success(`正在修复: ${issue.issue}`)
}

const viewDetails = (issue) => {
  notificationStore.info(`查看详情: ${issue.issue}`)
}
</script>

<style scoped>
.data-quality {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quality-overview {
  margin-bottom: 32px;
}

.quality-score-card {
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

.quality-metrics {
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

.metric-value {
  width: 50px;
  text-align: right;
  font-weight: 600;
}
</style>
