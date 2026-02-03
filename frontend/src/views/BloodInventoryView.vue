<template>
  <div class="blood-inventory">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>血液库存管理</span>
              <div class="header-actions">
                <el-button type="primary" @click="refreshInventory">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
                <el-button @click="exportInventory">
                  <el-icon><Download /></el-icon>
                  导出
                </el-button>
              </div>
            </div>
          </template>

          <!-- Inventory Overview -->
          <el-row :gutter="16" class="inventory-overview">
            <el-col :span="6" v-for="bloodType in bloodInventory" :key="bloodType.type">
              <div class="blood-type-card" :class="getStockLevelClass(bloodType.percentage)">
                <div class="blood-type-header">
                  <div class="blood-type">{{ bloodType.type }}</div>
                  <div class="blood-type-icon" :style="{ backgroundColor: bloodType.color }">
                    <el-icon><Box /></el-icon>
                  </div>
                </div>
                <div class="blood-type-stats">
                  <div class="units">{{ bloodType.units }} 单位</div>
                  <div class="percentage">{{ bloodType.percentage }}%</div>
                  <div class="status">{{ getBloodStatus(bloodType.status) }}</div>
                </div>
                <div class="stock-level">
                  <el-progress 
                    :percentage="bloodType.percentage" 
                    :color="getProgressColor(bloodType.percentage)"
                    :show-text="false"
                  />
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- Inventory Table -->
          <el-divider>详细库存</el-divider>
          <el-table :data="inventoryDetails" style="width: 100%">
            <el-table-column prop="bloodType" label="血型" width="100" />
            <el-table-column prop="rhFactor" label="RH因子" width="100" />
            <el-table-column prop="totalUnits" label="总单位数" width="120" />
            <el-table-column prop="availableUnits" label="可用" width="120" />
            <el-table-column prop="reservedUnits" label="预留" width="120" />
            <el-table-column prop="expiryDate" label="下次过期" width="120" />
            <el-table-column prop="storageLocation" label="存储位置" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="adjustInventory(row)">调整</el-button>
                <el-button size="small" type="primary" @click="transferInventory(row)">转移</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Alerts Section -->
          <el-divider>库存警报</el-divider>
          <div class="alerts-section">
            <el-row :gutter="16">
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <span>低库存警报</span>
                  </template>
                  <div class="alert-list">
                    <div v-for="alert in lowStockAlerts" :key="alert.id" class="alert-item critical">
                      <el-icon><Warning /></el-icon>
                      <span>{{ alert.message }}</span>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <span>过期警报</span>
                  </template>
                  <div class="alert-list">
                    <div v-for="alert in expiryAlerts" :key="alert.id" class="alert-item warning">
                      <el-icon><Clock /></el-icon>
                      <span>{{ alert.message }}</span>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Refresh, Download, Box, Warning, Bell, TrendCharts, Clock } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

// State
const loading = ref(false)
const selectedBloodType = ref('')
const dateRange = ref([])

// Blood Inventory Data
const bloodInventory = ref([
  {
    type: 'O+',
    units: 156,
    percentage: 78,
    status: 'Adequate',
    color: '#e74c3c',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 10:30',
    expiryDays: 35
  },
  {
    type: 'A+',
    units: 142,
    percentage: 71,
    status: 'Adequate', 
    color: '#3498db',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 09:15',
    expiryDays: 28
  },
  {
    type: 'B+',
    units: 38,
    percentage: 19,
    status: 'Low',
    color: '#2ecc71',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 11:45',
    expiryDays: 42
  },
  {
    type: 'AB+',
    units: 12,
    percentage: 6,
    status: 'Critical',
    color: '#9b59b6',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 08:00',
    expiryDays: 21
  },
  {
    type: 'O-',
    units: 25,
    percentage: 12,
    status: 'Critical',
    color: '#c0392b',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 12:00',
    expiryDays: 18
  },
  {
    type: 'A-',
    units: 45,
    percentage: 22,
    status: 'Low',
    color: '#2980b9',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 07:30',
    expiryDays: 31
  },
  {
    type: 'B-',
    units: 18,
    percentage: 9,
    status: 'Critical',
    color: '#27ae60',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 10:00',
    expiryDays: 25
  },
  {
    type: 'AB-',
    units: 8,
    percentage: 4,
    status: 'Critical',
    color: '#8e44ad',
    minRequired: 50,
    maxCapacity: 200,
    lastUpdated: '2024-01-20 09:45',
    expiryDays: 15
  }
])

// Detailed Inventory Data
const inventoryDetails = ref([
  {
    id: 'B001',
    bloodType: 'O+',
    units: 24,
    collectionDate: '2024-01-15',
    expiryDate: '2024-02-19',
    status: 'Available',
    location: 'Main Bank',
    donorId: 'D001',
    temperature: '4°C',
    notes: 'Regular donation'
  },
  {
    id: 'B002',
    bloodType: 'A+',
    units: 18,
    collectionDate: '2024-01-18',
    expiryDate: '2024-02-22',
    status: 'Available',
    location: 'Main Bank',
    donorId: 'D002',
    temperature: '4°C',
    notes: 'First-time donor'
  },
  {
    id: 'B003',
    bloodType: 'B+',
    units: 12,
    collectionDate: '2024-01-10',
    expiryDate: '2024-02-14',
    status: 'Reserved',
    location: 'Hospital A',
    donorId: 'D003',
    temperature: '4°C',
    notes: 'Reserved for surgery'
  }
])

// Inventory Alerts
const inventoryAlerts = ref([
  {
    id: 1,
    type: 'critical',
    bloodType: 'AB-',
    message: 'Only 8 units remaining (4% capacity)',
    time: '2 hours ago',
    action: 'Urgent collection needed'
  },
  {
    id: 2,
    type: 'warning',
    bloodType: 'B+',
    message: '38 units remaining (19% capacity)',
    time: '4 hours ago',
    action: 'Schedule collection drive'
  },
  {
    id: 3,
    type: 'expiry',
    bloodType: 'O-',
    message: '5 units expiring in 3 days',
    time: '6 hours ago',
    action: 'Contact hospitals for usage'
  }
])

// Computed Properties
const totalUnits = computed(() => {
  return bloodInventory.value.reduce((total, type) => total + type.units, 0)
})

const criticalTypes = computed(() => {
  return bloodInventory.value.filter(type => type.status === 'Critical')
})

const lowTypes = computed(() => {
  return bloodInventory.value.filter(type => type.status === 'Low')
})

const expiringSoon = computed(() => {
  return inventoryDetails.value.filter(item => {
    const daysToExpiry = Math.ceil((new Date(item.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))
    return daysToExpiry <= 7
  })
})

// Alert Properties
const lowStockAlerts = computed(() => {
  return inventoryAlerts.value.filter(alert => alert.type === 'critical' || alert.type === 'warning')
})

const expiryAlerts = computed(() => {
  return inventoryAlerts.value.filter(alert => alert.type === 'expiry')
})

// Methods
const refreshInventory = async () => {
  loading.value = true
  
  // Simulate data refresh
  setTimeout(() => {
    // Update some values to show changes
    bloodInventory.value.forEach(type => {
      const change = Math.floor(Math.random() * 10) - 5
      type.units = Math.max(0, Math.min(type.maxCapacity, type.units + change))
      type.percentage = Math.round((type.units / type.maxCapacity) * 100)
      type.lastUpdated = new Date().toLocaleString()
      
      // Update status based on new percentage
      if (type.percentage >= 60) {
        type.status = 'Adequate'
      } else if (type.percentage >= 20) {
        type.status = 'Low'
      } else {
        type.status = 'Critical'
      }
    })
    
    loading.value = false
    notificationStore.success('Inventory data refreshed successfully')
  }, 1500)
}

const exportInventory = () => {
  const exportContent = {
    bloodInventory: bloodInventory.value,
    inventoryDetails: inventoryDetails.value,
    alerts: inventoryAlerts.value,
    summary: {
      totalUnits: totalUnits.value,
      criticalTypes: criticalTypes.value.length,
      lowTypes: lowTypes.value.length,
      expiringSoon: expiringSoon.value.length
    },
    exportTime: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(exportContent, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = window.document.createElement('a')
  link.href = url
  link.download = `blood-inventory-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  notificationStore.success(`Exported inventory data: ${totalUnits.value} total units`)
}

const getBloodStatus = (status) => {
  switch (status) {
    case 'Adequate': return '充足'
    case 'Low': return '偏低'
    case 'Critical': return '紧急'
    default: return status
  }
}

const getStockLevelClass = (percentage) => {
  if (percentage >= 60) return 'adequate'
  if (percentage >= 20) return 'low'
  return 'critical'
}

const getProgressColor = (percentage) => {
  if (percentage >= 60) return '#67c23a'
  if (percentage >= 20) return '#e6a23c'
  return '#f56c6c'
}

const handleAlertAction = (alert) => {
  notificationStore.info(`Taking action: ${alert.action}`)
}

const adjustInventory = (item) => {
  notificationStore.info(`Adjusting inventory for ${item.bloodType}`)
}

const transferInventory = (item) => {
  notificationStore.info(`Transferring ${item.bloodType} units`)
}
</script>

<style scoped>
.blood-inventory {
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

.inventory-overview {
  margin-bottom: 32px;
}

.blood-type-card {
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e4e7ed;
  transition: all 0.3s ease;
}

.blood-type-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.blood-type-card.critical {
  border-color: #f56c6c;
  background: linear-gradient(135deg, #fef0f0 0%, #fde2e2 100%);
}

.blood-type-card.low {
  border-color: #e6a23c;
  background: linear-gradient(135deg, #fdf6ec 0%, #faecd8 100%);
}

.blood-type-card.adequate {
  border-color: #409eff;
  background: linear-gradient(135deg, #ecf5ff 0%, #d9ecff 100%);
}

.blood-type-card.good {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e1f3d8 100%);
}

.blood-type-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.blood-type {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.blood-type-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.blood-type-stats {
  text-align: center;
  margin-bottom: 16px;
}

.units {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.percentage {
  font-size: 18px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 4px;
}

.status {
  font-size: 14px;
  font-weight: 500;
  text-transform: uppercase;
}

.alerts-section {
  margin-top: 24px;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
}

.alert-item.critical {
  background: #fef0f0;
  color: #f56c6c;
  border: 1px solid #fbc4c4;
}

.alert-item.warning {
  background: #fdf6ec;
  color: #e6a23c;
  border: 1px solid #f5dabf;
}
</style>
