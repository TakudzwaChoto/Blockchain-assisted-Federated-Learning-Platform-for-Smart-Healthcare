<template>
  <div class="export-center">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>导出中心</span>
              <div class="header-actions">
                <el-button type="primary" @click="createExport">
                  <el-icon><Download /></el-icon>
                  新建导出
                </el-button>
                <el-button @click="refreshExports">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>

          <!-- Export Configuration -->
          <div class="export-config">
            <el-row :gutter="16">
              <el-col :span="6">
                <el-form-item label="数据类型">
                  <el-select v-model="exportConfig.dataType" placeholder="选择数据类型">
                    <el-option label="捐赠者数据" value="donors" />
                    <el-option label="捐赠记录" value="donations" />
                    <el-option label="库存" value="inventory" />
                    <el-option label="报告" value="reports" />
                    <el-option label="分析数据" value="analytics" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="格式">
                  <el-select v-model="exportConfig.format" placeholder="选择格式">
                    <el-option label="Excel (.xlsx)" value="excel" />
                    <el-option label="CSV (.csv)" value="csv" />
                    <el-option label="PDF (.pdf)" value="pdf" />
                    <el-option label="JSON (.json)" value="json" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="日期范围">
                  <el-date-picker
                    v-model="exportConfig.dateRange"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="筛选条件">
                  <el-button @click="openFilters">配置筛选</el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <!-- Export Stats -->
          <el-divider>导出统计</el-divider>
          <el-row :gutter="16" class="export-stats">
            <el-col :span="6" v-for="stat in exportStats" :key="stat.id">
              <div class="stat-card">
                <div class="stat-icon" :style="{ backgroundColor: stat.color }">
                  <el-icon>
                    <component :is="stat.icon" />
                  </el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Recent Exports -->
          <el-divider>最近导出</el-divider>
          <el-table :data="recentExports" style="width: 100%">
            <el-table-column prop="id" label="导出ID" width="120" />
            <el-table-column prop="dataType" label="数据类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getDataTypeColor(row.dataType)">
                  {{ row.dataType }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="format" label="格式" width="100" />
            <el-table-column prop="records" label="记录数" width="100" />
            <el-table-column prop="size" label="大小" width="100" />
            <el-table-column prop="requestedBy" label="请求者" />
            <el-table-column prop="requestedAt" label="请求时间" width="150" />
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button size="small" @click="previewExport(row)" :disabled="row.status !== 'Completed'">
                  预览
                </el-button>
                <el-button size="small" type="primary" @click="downloadExport(row)" :disabled="row.status !== 'Completed'">
                  下载
                </el-button>
                <el-button size="small" @click="shareExport(row)" :disabled="row.status !== 'Completed'">
                  分享
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Scheduled Exports -->
          <el-divider>Scheduled Exports</el-divider>
          <el-table :data="scheduledExports" style="width: 100%">
            <el-table-column prop="id" label="Schedule ID" width="120" />
            <el-table-column prop="name" label="Schedule Name" />
            <el-table-column prop="dataType" label="Data Type" width="120" />
            <el-table-column prop="frequency" label="Frequency" width="100" />
            <el-table-column prop="nextRun" label="Next Run" width="150" />
            <el-table-column prop="recipients" label="Recipients" />
            <el-table-column prop="status" label="Status" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="editSchedule(row)">Edit</el-button>
                <el-button size="small" type="danger" @click="deleteSchedule(row)">Delete</el-button>
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
import { Download, Refresh, Document, TrendCharts, User, Setting } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const exportConfig = ref({
  dataType: 'donors',
  format: 'excel',
  dateRange: [],
  filters: {}
})

const exportStats = ref([
  {
    id: 'total',
    label: 'Total Exports',
    value: '1,234',
    icon: 'Document',
    color: '#409eff'
  },
  {
    id: 'today',
    label: 'Today',
    value: '23',
    icon: 'TrendCharts',
    color: '#67c23a'
  },
  {
    id: 'downloads',
    label: 'Downloads',
    value: '5,678',
    icon: 'Download',
    color: '#e6a23c'
  },
  {
    id: 'scheduled',
    label: 'Scheduled',
    value: '8',
    icon: 'Setting',
    color: '#f56c6c'
  }
])

const recentExports = ref([
  {
    id: 'EXP-001',
    dataType: 'Donor Data',
    format: 'Excel',
    records: 1500,
    size: '2.3 MB',
    requestedBy: 'Admin User',
    requestedAt: '2024-01-15 10:30',
    status: 'Completed'
  },
  {
    id: 'EXP-002',
    dataType: 'Donation Records',
    format: 'PDF',
    records: 500,
    size: '1.2 MB',
    requestedBy: 'Jane Smith',
    requestedAt: '2024-01-15 09:15',
    status: 'Processing'
  },
  {
    id: 'EXP-003',
    dataType: 'Inventory',
    format: 'CSV',
    records: 200,
    size: '0.8 MB',
    requestedBy: 'John Doe',
    requestedAt: '2024-01-14 16:45',
    status: 'Failed'
  }
])

const scheduledExports = ref([
  {
    id: 'SCH-001',
    name: 'Weekly Donor Report',
    dataType: 'Donor Data',
    frequency: 'Weekly',
    nextRun: '2024-01-22 09:00',
    recipients: 'admin@bloodbank.com',
    status: 'Active'
  },
  {
    id: 'SCH-002',
    name: 'Monthly Analytics',
    dataType: 'Analytics',
    frequency: 'Monthly',
    nextRun: '2024-02-01 00:00',
    recipients: 'reports@bloodbank.com',
    status: 'Active'
  }
])

const getDataTypeColor = (type) => {
  switch (type) {
    case 'Donor Data': return 'success'
    case 'Donation Records': return 'primary'
    case 'Inventory': return 'warning'
    case 'Reports': return 'info'
    case 'Analytics': return 'danger'
    default: return 'info'
  }
}

const getStatusType = (status) => {
  switch (status) {
    case 'Completed': return 'success'
    case 'Processing': return 'warning'
    case 'Failed': return 'danger'
    case 'Active': return 'primary'
    default: return 'info'
  }
}

const createExport = () => {
  notificationStore.info('Creating new export')
}

const refreshExports = () => {
  notificationStore.success('Exports refreshed')
}

const openFilters = () => {
  notificationStore.info('Opening export filters')
}

const previewExport = (exp) => {
  notificationStore.info(`Previewing export: ${exp.id}`)
}

const downloadExport = (exp) => {
  // Generate real data based on data type and format
  const data = generateExportData(exp.dataType, exp.format)
  const filename = `${exp.dataType}_${new Date().toISOString().split('T')[0]}.${getFileExtension(exp.format)}`
  
  // Create and download file
  downloadFile(data, filename, exp.format)
  notificationStore.success(`文件下载成功: ${filename}`)
}

const shareExport = (exp) => {
  notificationStore.info(`Sharing export: ${exp.id}`)
}

const editSchedule = (schedule) => {
  notificationStore.info(`Editing schedule: ${schedule.id}`)
}

const deleteSchedule = (schedule) => {
  notificationStore.info(`Deleting schedule: ${schedule.id}`)
}

// Generate mock data for export
const generateExportData = (dataType, format) => {
  const mockData = {
    donors: [
      { id: 1, name: '张三', bloodType: 'A+', age: 28, phone: '13800138000', donations: 5, lastDonation: '2024-01-15' },
      { id: 2, name: '李四', bloodType: 'B+', age: 32, phone: '13800138001', donations: 3, lastDonation: '2024-01-10' },
      { id: 3, name: '王五', bloodType: 'O+', age: 25, phone: '13800138002', donations: 8, lastDonation: '2024-01-20' }
    ],
    donations: [
      { id: 1, donorId: 1, donorName: '张三', bloodType: 'A+', amount: 400, date: '2024-01-15', hospital: '北京医院' },
      { id: 2, donorId: 2, donorName: '李四', bloodType: 'B+', amount: 350, date: '2024-01-10', hospital: '协和医院' },
      { id: 3, donorId: 3, donorName: '王五', bloodType: 'O+', amount: 450, date: '2024-01-20', hospital: '同仁医院' }
    ],
    inventory: [
      { bloodType: 'A+', amount: 2500, unit: 'ml', expiryDate: '2024-02-15', status: '可用' },
      { bloodType: 'B+', amount: 1800, unit: 'ml', expiryDate: '2024-02-20', status: '可用' },
      { bloodType: 'O+', amount: 3200, unit: 'ml', expiryDate: '2024-02-10', status: '可用' }
    ],
    reports: [
      { id: 1, title: '月度血液库存报告', date: '2024-01-31', totalDonations: 1250, totalUsage: 980, status: '正常' },
      { id: 2, title: '血液安全分析报告', date: '2024-01-30', safetyScore: '98.5%', issues: 2, status: '良好' }
    ],
    analytics: [
      { metric: '捐赠趋势', value: '+15%', period: '本月', category: '增长' },
      { metric: '库存周转率', value: '3.2', period: '周', category: '效率' },
      { metric: '安全指数', value: '99.2%', period: '本月', category: '质量' }
    ]
  }

  const data = mockData[dataType] || []
  
  switch (format) {
    case 'csv':
      return convertToCSV(data)
    case 'excel':
      return convertToExcel(data)
    case 'pdf':
      return convertToPDF(data, dataType)
    case 'json':
      return JSON.stringify(data, null, 2)
    default:
      return JSON.stringify(data, null, 2)
  }
}

// Convert data to CSV format
const convertToCSV = (data) => {
  if (!data || data.length === 0) return ''
  
  const headers = Object.keys(data[0])
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(header => row[header]).join(','))
  ].join('\n')
  
  return csvContent
}

// Convert data to Excel format (simplified)
const convertToExcel = (data) => {
  if (!data || data.length === 0) return ''
  
  const headers = Object.keys(data[0])
  const excelContent = [
    headers.join('\t'),
    ...data.map(row => headers.map(header => row[header]).join('\t'))
  ].join('\n')
  
  return excelContent
}

// Convert data to PDF format (simplified text)
const convertToPDF = (data, dataType) => {
  const title = getDataTypeName(dataType)
  const date = new Date().toLocaleDateString('zh-CN')
  
  let content = `${title}\n生成日期: ${date}\n\n`
  content += '=' .repeat(50) + '\n\n'
  
  if (data && data.length > 0) {
    const headers = Object.keys(data[0])
    content += headers.join('\t') + '\n'
    content += '-'.repeat(50) + '\n'
    
    data.forEach(row => {
      content += headers.map(header => row[header]).join('\t') + '\n'
    })
  } else {
    content += '暂无数据'
  }
  
  return content
}

// Get file extension for format
const getFileExtension = (format) => {
  const extensions = {
    csv: 'csv',
    excel: 'xlsx',
    pdf: 'txt', // Simplified to text file
    json: 'json'
  }
  return extensions[format] || 'txt'
}

// Get data type name in Chinese
const getDataTypeName = (dataType) => {
  const names = {
    donors: '捐赠者数据',
    donations: '捐赠记录',
    inventory: '库存数据',
    reports: '报告数据',
    analytics: '分析数据'
  }
  return names[dataType] || '数据'
}

// Download file to user's computer
const downloadFile = (content, filename, format) => {
  const blob = new Blob([content], { 
    type: getContentType(format) 
  })
  
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// Get content type for file format
const getContentType = (format) => {
  const types = {
    csv: 'text/csv',
    excel: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    pdf: 'text/plain', // Simplified to text
    json: 'application/json'
  }
  return types[format] || 'text/plain'
}
</script>

<style scoped>
.export-center {
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

.export-config {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 24px;
}

.export-stats {
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}
</style>
