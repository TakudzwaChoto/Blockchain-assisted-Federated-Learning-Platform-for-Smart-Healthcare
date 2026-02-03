<template>
  <div class="campaigns">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>血液捐赠活动</span>
              <div class="header-actions">
                <el-button type="primary" @click="createCampaign">
                  <el-icon><Plus /></el-icon>
                  新建活动
                </el-button>
                <el-button @click="refreshCampaigns">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>

          <!-- Campaign Stats -->
          <el-row :gutter="16" class="campaign-stats">
            <el-col :span="6" v-for="stat in campaignStats" :key="stat.id">
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

          <!-- Campaigns Table -->
          <el-divider>Active Campaigns</el-divider>
          <el-table :data="campaigns" style="width: 100%">
            <el-table-column prop="name" label="Campaign Name" />
            <el-table-column prop="type" label="Type" width="120">
              <template #default="{ row }">
                <el-tag :type="getCampaignTypeColor(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startDate" label="Start Date" width="120" />
            <el-table-column prop="endDate" label="End Date" width="120" />
            <el-table-column prop="target" label="Target" width="100" />
            <el-table-column prop="collected" label="Collected" width="100" />
            <el-table-column prop="progress" label="Progress" width="150">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" :color="getProgressColor(row.progress)" />
              </template>
            </el-table-column>
            <el-table-column prop="status" label="Status" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="200" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="viewCampaign(row)">View</el-button>
                <el-button size="small" type="primary" @click="editCampaign(row)">Edit</el-button>
                <el-button size="small" type="danger" @click="deleteCampaign(row)">Delete</el-button>
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
import { Plus, Refresh, Star, TrendCharts, User, Calendar } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const campaignStats = ref([
  {
    id: 'active',
    label: 'Active Campaigns',
    value: '12',
    icon: 'Star',
    color: '#409eff'
  },
  {
    id: 'total',
    label: 'Total Campaigns',
    value: '156',
    icon: 'TrendCharts',
    color: '#67c23a'
  },
  {
    id: 'participants',
    label: 'Total Participants',
    value: '3,456',
    icon: 'User',
    color: '#e6a23c'
  },
  {
    id: 'success',
    label: 'Success Rate',
    value: '87%',
    icon: 'Calendar',
    color: '#f56c6c'
  }
])

const campaigns = ref([
  {
    name: 'Summer Blood Drive 2024',
    type: 'Community',
    startDate: '2024-06-01',
    endDate: '2024-06-30',
    target: 500,
    collected: 423,
    progress: 85,
    status: 'Active'
  },
  {
    name: 'Emergency Blood Collection',
    type: 'Emergency',
    startDate: '2024-01-15',
    endDate: '2024-01-20',
    target: 200,
    collected: 198,
    progress: 99,
    status: 'Active'
  },
  {
    name: 'Hospital Partnership Drive',
    type: 'Corporate',
    startDate: '2024-02-01',
    endDate: '2024-02-28',
    target: 300,
    collected: 267,
    progress: 89,
    status: 'Active'
  }
])

const getCampaignTypeColor = (type) => {
  switch (type) {
    case 'Community': return 'success'
    case 'Emergency': return 'danger'
    case 'Corporate': return 'warning'
    default: return 'info'
  }
}

const getStatusType = (status) => {
  switch (status) {
    case 'Active': return 'success'
    case 'Completed': return 'info'
    case 'Cancelled': return 'danger'
    default: return 'warning'
  }
}

const getProgressColor = (progress) => {
  if (progress >= 90) return '#67c23a'
  if (progress >= 70) return '#409eff'
  if (progress >= 50) return '#e6a23c'
  return '#f56c6c'
}

const createCampaign = () => {
  notificationStore.info('Create new campaign')
}

const refreshCampaigns = () => {
  notificationStore.success('Campaigns refreshed')
}

const viewCampaign = (campaign) => {
  notificationStore.info(`Viewing: ${campaign.name}`)
}

const editCampaign = (campaign) => {
  notificationStore.info(`Editing: ${campaign.name}`)
}

const deleteCampaign = (campaign) => {
  notificationStore.warning(`Deleting: ${campaign.name}`)
}
</script>

<style scoped>
.campaigns {
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

.campaign-stats {
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
