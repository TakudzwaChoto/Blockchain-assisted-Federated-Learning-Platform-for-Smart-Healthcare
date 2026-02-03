<template>
  <div class="batch-processing">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>批量处理</span>
              <div class="header-actions">
                <el-button type="primary" @click="startBatch">
                  <el-icon><VideoPlay /></el-icon>
                  开始新批次
                </el-button>
                <el-button @click="refreshBatches">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>

          <!-- Processing Stats -->
          <el-row :gutter="16" class="processing-stats">
            <el-col :span="6" v-for="stat in processingStats" :key="stat.id">
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

          <!-- Active Batches -->
          <el-divider>活跃批次</el-divider>
          <el-table :data="activeBatches" style="width: 100%">
            <el-table-column prop="id" label="批次ID" width="120" />
            <el-table-column prop="name" label="批次名称" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getBatchTypeColor(row.type)">
                  {{ getBatchType(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="records" label="Records" width="100" />
            <el-table-column prop="progress" label="进度" width="200">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" :color="getProgressColor(row.progress)" />
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startTime" label="开始时间" width="150" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="viewBatch(row)">查看</el-button>
                <el-button size="small" type="danger" @click="stopBatch(row)" :disabled="row.status === 'Completed'">
                  停止
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Batch History -->
          <el-divider>批次历史</el-divider>
          <el-table :data="batchHistory" style="width: 100%">
            <el-table-column prop="id" label="批次ID" width="120" />
            <el-table-column prop="name" label="批次名称" />
            <el-table-column prop="type" label="Type" width="120">
              <template #default="{ row }">
                <el-tag :type="getBatchTypeColor(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="records" label="记录数" width="100" />
            <el-table-column prop="success" label="成功" width="100" />
            <el-table-column prop="errors" label="错误" width="100" />
            <el-table-column prop="duration" label="持续时间" width="120" />
            <el-table-column prop="completedAt" label="完成时间" width="150" />
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button size="small" @click="viewDetails(row)">详情</el-button>
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
import { VideoPlay, Refresh, Setting, Document, TrendCharts, Warning } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const processingStats = ref([
  {
    id: 'active',
    label: '活跃批次',
    value: '3',
    icon: 'Setting',
    color: '#409eff'
  },
  {
    id: 'today',
    label: '今日处理',
    value: '1,234',
    icon: 'Document',
    color: '#67c23a'
  },
  {
    id: 'success',
    label: '成功率',
    value: '98.5%',
    icon: 'TrendCharts',
    color: '#e6a23c'
  },
  {
    id: 'errors',
    label: '错误率',
    value: '1.5%',
    icon: 'Warning',
    color: '#f56c6c'
  }
])

const activeBatches = ref([
  {
    id: 'BATCH-001',
    name: 'Donor Data Import',
    type: 'Import',
    records: 5000,
    progress: 75,
    status: 'Processing',
    startTime: '2024-01-15 09:30:00'
  },
  {
    id: 'BATCH-002',
    name: 'Quality Validation',
    type: 'Validation',
    records: 3500,
    progress: 45,
    status: 'Processing',
    startTime: '2024-01-15 10:15:00'
  },
  {
    id: 'BATCH-003',
    name: 'Report Generation',
    type: 'Export',
    records: 1200,
    progress: 90,
    status: 'Processing',
    startTime: '2024-01-15 11:00:00'
  }
])

const batchHistory = ref([
  {
    id: 'BATCH-998',
    name: 'Monthly Report',
    type: 'Export',
    records: 2500,
    success: 2498,
    errors: 2,
    duration: '3m 45s',
    completedAt: '2024-01-14 16:30:00'
  },
  {
    id: 'BATCH-997',
    name: 'Data Cleanup',
    type: 'Processing',
    records: 8000,
    success: 7992,
    errors: 8,
    duration: '12m 20s',
    completedAt: '2024-01-14 14:15:00'
  }
])

const getBatchType = (type) => {
  switch (type) {
    case 'Import': return '导入'
    case 'Export': return '导出'
    case 'Processing': return '处理'
    case 'Validation': return '验证'
    default: return type
  }
}

const getBatchTypeColor = (type) => {
  switch (type) {
    case 'Import': return 'primary'
    case 'Export': return 'success'
    case 'Processing': return 'warning'
    case 'Validation': return 'info'
    default: return 'info'
  }
}

const getStatusType = (status) => {
  switch (status) {
    case 'Processing': return 'warning'
    case 'Completed': return 'success'
    case 'Failed': return 'danger'
    case 'Stopped': return 'info'
    default: return 'info'
  }
}

const getProgressColor = (progress) => {
  if (progress >= 90) return '#67c23a'
  if (progress >= 70) return '#409eff'
  if (progress >= 50) return '#e6a23c'
  return '#f56c6c'
}

const startBatch = () => {
  notificationStore.info('开始新批次处理')
}

const refreshBatches = () => {
  notificationStore.success('批次列表已刷新')
}

const viewBatch = (batch) => {
  notificationStore.info(`查看批次: ${batch.id}`)
}

const stopBatch = (batch) => {
  notificationStore.warning(`停止批次: ${batch.id}`)
}

const viewDetails = (batch) => {
  notificationStore.info(`查看详情: ${batch.id}`)
}
</script>

<style scoped>
.batch-processing {
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

.processing-stats {
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
