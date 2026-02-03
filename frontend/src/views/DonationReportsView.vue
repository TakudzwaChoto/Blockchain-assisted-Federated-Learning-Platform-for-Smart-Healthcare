<template>
  <div class="donation-reports">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>捐赠报告</span>
              <div class="header-actions">
                <el-button type="primary" @click="generateReport">
                  <el-icon><Document /></el-icon>
                  生成报告
                </el-button>
                <el-button @click="refreshReports">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>

          <!-- Report Configuration -->
          <div class="report-config">
            <el-row :gutter="16">
              <el-col :span="6">
                <el-form-item label="报告类型">
                  <el-select v-model="reportConfig.type" placeholder="选择报告类型">
                    <el-option label="月度总结" value="monthly" />
                    <el-option label="季度分析" value="quarterly" />
                    <el-option label="年度报告" value="annual" />
                    <el-option label="自定义周期" value="custom" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="日期范围">
                  <el-date-picker
                    v-model="reportConfig.dateRange"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="格式">
                  <el-select v-model="reportConfig.format" placeholder="选择格式">
                    <el-option label="PDF" value="pdf" />
                    <el-option label="Excel" value="excel" />
                    <el-option label="CSV" value="csv" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="包含图表">
                  <el-switch v-model="reportConfig.includeCharts" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <!-- Report Summary -->
          <el-divider>报告摘要</el-divider>
          <el-row :gutter="16" class="report-summary">
            <el-col :span="6" v-for="summary in reportSummary" :key="summary.id">
              <div class="summary-card">
                <div class="summary-icon" :style="{ backgroundColor: summary.color }">
                  <el-icon>
                    <component :is="summary.icon" />
                  </el-icon>
                </div>
                <div class="summary-content">
                  <div class="summary-value">{{ summary.value }}</div>
                  <div class="summary-label">{{ summary.label }}</div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Generated Reports -->
          <el-divider>已生成报告</el-divider>
          <el-table :data="generatedReports" style="width: 100%">
            <el-table-column prop="id" label="报告ID" width="120" />
            <el-table-column prop="type" label="类型" width="150">
              <template #default="{ row }">
                <el-tag :type="getReportTypeColor(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="period" label="周期" />
            <el-table-column prop="generatedBy" label="生成者" />
            <el-table-column prop="generatedAt" label="生成时间" width="150" />
            <el-table-column prop="format" label="格式" width="100" />
            <el-table-column prop="size" label="大小" width="100" />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button size="small" @click="previewReport(row)">预览</el-button>
                <el-button size="small" type="primary" @click="downloadReport(row)">下载</el-button>
                <el-button size="small" @click="shareReport(row)">分享</el-button>
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
import { Document, Refresh, TrendCharts, DataAnalysis, Download } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const reportConfig = ref({
  type: 'monthly',
  dateRange: [],
  format: 'pdf',
  includeCharts: true
})

const reportSummary = ref([
  {
    id: 'total',
    label: 'Total Reports',
    value: '156',
    icon: 'Document',
    color: '#409eff'
  },
  {
    id: 'this-month',
    label: 'This Month',
    value: '12',
    icon: 'TrendCharts',
    color: '#67c23a'
  },
  {
    id: 'downloads',
    label: 'Downloads',
    value: '1,234',
    icon: 'Download',
    color: '#e6a23c'
  },
  {
    id: 'scheduled',
    label: 'Scheduled',
    value: '8',
    icon: 'DataAnalysis',
    color: '#f56c6c'
  }
])

const generatedReports = ref([
  {
    id: 'RPT-001',
    type: 'Monthly Summary',
    period: 'January 2024',
    generatedBy: 'Admin User',
    generatedAt: '2024-01-15 10:30',
    format: 'PDF',
    size: '2.3 MB'
  },
  {
    id: 'RPT-002',
    type: 'Quarterly Analysis',
    period: 'Q4 2023',
    generatedBy: 'Jane Smith',
    generatedAt: '2024-01-10 14:15',
    format: 'Excel',
    size: '5.7 MB'
  },
  {
    id: 'RPT-003',
    type: 'Annual Report',
    period: '2023',
    generatedBy: 'System Admin',
    generatedAt: '2024-01-05 09:00',
    format: 'PDF',
    size: '12.4 MB'
  }
])

const getReportTypeColor = (type) => {
  switch (type) {
    case 'Monthly Summary': return 'success'
    case 'Quarterly Analysis': return 'warning'
    case 'Annual Report': return 'danger'
    case 'Custom Period': return 'info'
    default: return 'info'
  }
}

const generateReport = () => {
  notificationStore.success('Report generation started')
}

const refreshReports = () => {
  notificationStore.success('Reports refreshed')
}

const previewReport = (report) => {
  notificationStore.info(`Previewing report: ${report.id}`)
}

const downloadReport = (report) => {
  notificationStore.success(`Downloading: ${report.id}`)
}

const shareReport = (report) => {
  notificationStore.info(`Sharing report: ${report.id}`)
}
</script>

<style scoped>
.donation-reports {
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

.report-config {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 24px;
}

.report-summary {
  margin-bottom: 32px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.summary-content {
  flex: 1;
}

.summary-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.summary-label {
  font-size: 14px;
  color: #606266;
}
</style>
