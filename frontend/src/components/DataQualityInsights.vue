<template>
  <el-card class="data-quality-insights">
    <template #header>
      <div class="insights-header">
        <span>
          <el-icon><DataAnalysis /></el-icon>
          Data Quality Insights
        </span>
        <el-button size="small" @click="refreshInsights">
          <el-icon><Refresh /></el-icon>
          Refresh
        </el-button>
      </div>
    </template>

    <!-- Overall Quality Score -->
    <div class="quality-overview">
      <div class="quality-score">
        <div class="score-circle" :class="getScoreClass(overallScore)">
          <div class="score-value">{{ overallScore }}</div>
          <div class="score-label">Overall Score</div>
        </div>
      </div>
      <div class="quality-details">
        <div class="detail-item" v-for="metric in qualityMetrics" :key="metric.name">
          <div class="detail-label">{{ metric.label }}</div>
          <div class="detail-value">
            <el-progress
              :percentage="metric.value"
              :color="getProgressColor(metric.value)"
              :show-text="false"
              style="width: 100px"
            />
            <span class="value-text">{{ metric.value }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quality Issues -->
    <el-divider>Quality Issues</el-divider>
    <div class="quality-issues">
      <div
        v-for="issue in qualityIssues"
        :key="issue.id"
        class="issue-item"
        :class="`issue-${issue.severity}`"
      >
        <div class="issue-icon">
          <el-icon v-if="issue.severity === 'critical'"><CircleCloseFilled /></el-icon>
          <el-icon v-else-if="issue.severity === 'error'"><WarningFilled /></el-icon>
          <el-icon v-else-if="issue.severity === 'warning'"><Warning /></el-icon>
          <el-icon v-else><InfoFilled /></el-icon>
        </div>
        <div class="issue-content">
          <div class="issue-title">{{ issue.title }}</div>
          <div class="issue-description">{{ issue.description }}</div>
          <div class="issue-details">
            <span class="issue-count">{{ issue.count }} records affected</span>
            <span class="issue-percentage">({{ issue.percentage }}%)</span>
          </div>
        </div>
        <div class="issue-actions">
          <el-button size="small" @click="viewIssueDetails(issue)">View Details</el-button>
          <el-button size="small" type="primary" @click="fixIssue(issue)">Fix Issue</el-button>
        </div>
      </div>
    </div>

    <!-- Validation Rules Status -->
    <el-divider>Validation Rules</el-divider>
    <div class="validation-rules">
      <div class="rules-summary">
        <div class="summary-item">
          <div class="summary-value">{{ validationRules.total }}</div>
          <div class="summary-label">Total Rules</div>
        </div>
        <div class="summary-item">
          <div class="summary-value success">{{ validationRules.passed }}</div>
          <div class="summary-label">Passed</div>
        </div>
        <div class="summary-item">
          <div class="summary-value warning">{{ validationRules.failed }}</div>
          <div class="summary-label">Failed</div>
        </div>
        <div class="summary-item">
          <div class="summary-value info">{{ validationRules.skipped }}</div>
          <div class="summary-label">Skipped</div>
        </div>
      </div>
      
      <div class="rules-list">
        <div
          v-for="rule in validationRules.rules"
          :key="rule.id"
          class="rule-item"
          :class="`rule-${rule.status}`"
        >
          <div class="rule-info">
            <div class="rule-name">{{ rule.name }}</div>
            <div class="rule-description">{{ rule.description }}</div>
          </div>
          <div class="rule-status">
            <el-tag :type="getRuleTagType(rule.status)" size="small">
              {{ rule.status }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- Recommendations -->
    <el-divider>Recommendations</el-divider>
    <div class="recommendations">
      <div
        v-for="recommendation in recommendations"
        :key="recommendation.id"
        class="recommendation-item"
      >
        <div class="recommendation-icon">
          <el-icon><InfoFilled /></el-icon>
        </div>
        <div class="recommendation-content">
          <div class="recommendation-title">{{ recommendation.title }}</div>
          <div class="recommendation-description">{{ recommendation.description }}</div>
          <div class="recommendation-impact">
            <el-tag :type="getImpactTagType(recommendation.impact)" size="small">
              {{ recommendation.impact }} impact
            </el-tag>
            <span class="recommendation-effort">Effort: {{ recommendation.effort }}</span>
          </div>
        </div>
        <div class="recommendation-actions">
          <el-button size="small" @click="applyRecommendation(recommendation)">
            Apply
          </el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  DataAnalysis,
  Refresh,
  TrendCharts,
  CircleCloseFilled,
  WarningFilled,
  Warning,
  InfoFilled,
  SuccessFilled,
  Bell
} from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const emit = defineEmits(['issue-selected', 'fix-issue', 'apply-recommendation'])

const notificationStore = useNotificationStore()

const overallScore = ref(85)
const qualityMetrics = ref([
  { name: 'completeness', label: 'Completeness', value: 92 },
  { name: 'accuracy', label: 'Accuracy', value: 88 },
  { name: 'consistency', label: 'Consistency', value: 78 },
  { name: 'validity', label: 'Validity', value: 85 },
  { name: 'timeliness', label: 'Timeliness', value: 82 }
])

const qualityIssues = ref([
  {
    id: 1,
    severity: 'error',
    title: 'Missing Blood Type Information',
    description: 'Some donor records are missing blood type information',
    count: 45,
    percentage: 3.2
  },
  {
    id: 2,
    severity: 'warning',
    title: 'Inconsistent Date Formats',
    description: 'Donation dates have inconsistent formatting across records',
    count: 128,
    percentage: 9.1
  },
  {
    id: 3,
    severity: 'info',
    title: 'Optional Contact Information Missing',
    description: 'Some records are missing optional email addresses',
    count: 234,
    percentage: 16.7
  }
])

const validationRules = ref({
  total: 15,
  passed: 12,
  failed: 2,
  skipped: 1,
  rules: [
    {
      id: 1,
      name: 'Blood Type Validation',
      description: 'Validates blood type format and values',
      status: 'passed'
    },
    {
      id: 2,
      name: 'Donor Age Range',
      description: 'Validates donor age is within acceptable range',
      status: 'failed'
    },
    {
      id: 3,
      name: 'Email Format',
      description: 'Validates email format if provided',
      status: 'passed'
    }
  ]
})

const recommendations = ref([
  {
    id: 1,
    title: 'Standardize Date Formats',
    description: 'Implement consistent date formatting across all donation records',
    impact: 'high',
    effort: 'medium'
  },
  {
    id: 2,
    title: 'Add Blood Type Validation',
    description: 'Enforce blood type validation at data entry point',
    impact: 'medium',
    effort: 'low'
  },
  {
    id: 3,
    title: 'Implement Data Profiling',
    description: 'Set up automated data profiling to catch issues early',
    impact: 'high',
    effort: 'high'
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

const getRuleTagType = (status) => {
  switch (status) {
    case 'passed': return 'success'
    case 'failed': return 'danger'
    case 'skipped': return 'info'
    default: return 'info'
  }
}

const getImpactTagType = (impact) => {
  switch (impact) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'info'
    default: return 'info'
  }
}

const refreshInsights = () => {
  // Simulate refreshing data
  notificationStore.info('Refreshing data quality insights...')
  setTimeout(() => {
    notificationStore.success('Data quality insights updated')
  }, 1000)
}

const viewIssueDetails = (issue) => {
  emit('issue-selected', issue)
}

const fixIssue = (issue) => {
  emit('fix-issue', issue)
  notificationStore.success(`Initiated fix for: ${issue.title}`)
}

const applyRecommendation = (recommendation) => {
  emit('apply-recommendation', recommendation)
  notificationStore.success(`Applied recommendation: ${recommendation.title}`)
}

onMounted(() => {
  // Load initial data
})
</script>

<style scoped>
.data-quality-insights {
  margin-bottom: 20px;
}

.insights-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quality-overview {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 24px;
}

.quality-score {
  flex-shrink: 0;
}

.score-circle {
  width: 120px;
  height: 120px;
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
  font-size: 32px;
  line-height: 1;
}

.score-label {
  font-size: 12px;
  opacity: 0.9;
  margin-top: 4px;
}

.quality-details {
  flex: 1;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.detail-label {
  font-weight: 500;
  color: #606266;
}

.detail-value {
  display: flex;
  align-items: center;
  gap: 8px;
}

.value-text {
  font-weight: 600;
  color: #303133;
  min-width: 40px;
}

.quality-issues {
  margin-bottom: 24px;
}

.issue-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 12px;
  border-left: 4px solid #e4e7ed;
  background-color: #fafafa;
}

.issue-critical {
  border-left-color: #f56c6c;
  background-color: #fef0f0;
}

.issue-error {
  border-left-color: #e6a23c;
  background-color: #fdf6ec;
}

.issue-warning {
  border-left-color: #e6a23c;
  background-color: #fdf6ec;
}

.issue-info {
  border-left-color: #409eff;
  background-color: #ecf5ff;
}

.issue-icon {
  font-size: 20px;
  margin-top: 2px;
}

.issue-critical .issue-icon {
  color: #f56c6c;
}

.issue-error .issue-icon {
  color: #e6a23c;
}

.issue-warning .issue-icon {
  color: #e6a23c;
}

.issue-info .issue-icon {
  color: #409eff;
}

.issue-content {
  flex: 1;
}

.issue-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: #303133;
}

.issue-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 8px;
}

.issue-details {
  font-size: 12px;
  color: #909399;
}

.issue-count {
  margin-right: 8px;
}

.issue-actions {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.validation-rules {
  margin-bottom: 24px;
}

.rules-summary {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
}

.summary-item {
  text-align: center;
}

.summary-value {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 4px;
}

.summary-value.success {
  color: #67c23a;
}

.summary-value.warning {
  color: #e6a23c;
}

.summary-value.info {
  color: #409eff;
}

.summary-label {
  font-size: 12px;
  color: #909399;
  text-transform: uppercase;
}

.rules-list {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.rule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
}

.rule-item:last-child {
  border-bottom: none;
}

.rule-passed {
  background-color: #f0f9ff;
}

.rule-failed {
  background-color: #fef0f0;
}

.rule-skipped {
  background-color: #fafafa;
}

.rule-info {
  flex: 1;
}

.rule-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.rule-description {
  font-size: 12px;
  color: #909399;
}

.recommendations {
  margin-bottom: 24px;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 12px;
  background-color: #f8f9fa;
  border: 1px solid #e4e7ed;
}

.recommendation-icon {
  font-size: 20px;
  color: #409eff;
  margin-top: 2px;
}

.recommendation-content {
  flex: 1;
}

.recommendation-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: #303133;
}

.recommendation-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 8px;
}

.recommendation-impact {
  display: flex;
  align-items: center;
  gap: 12px;
}

.recommendation-effort {
  font-size: 12px;
  color: #909399;
}

.recommendation-actions {
  align-items: flex-start;
}

@media (max-width: 768px) {
  .quality-overview {
    flex-direction: column;
    text-align: center;
  }
  
  .rules-summary {
    flex-wrap: wrap;
    justify-content: space-around;
  }
  
  .issue-item,
  .recommendation-item {
    flex-direction: column;
    text-align: center;
  }
  
  .issue-actions,
  .recommendation-actions {
    justify-content: center;
    width: 100%;
  }
}
</style>
