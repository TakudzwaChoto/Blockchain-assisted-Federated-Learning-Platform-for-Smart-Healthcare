<template>
  <div class="transport-logistics">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>运输物流</span>
              <div class="header-actions">
                <el-button type="primary" @click="createShipment">
                  <el-icon><Plus /></el-icon>
                  新建运输
                </el-button>
                <el-button @click="refreshShipments">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>

          <!-- Logistics Stats -->
          <el-row :gutter="16" class="logistics-stats">
            <el-col :span="6" v-for="stat in logisticsStats" :key="stat.id">
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

          <!-- Active Shipments -->
          <el-divider>活跃运输</el-divider>
          <el-table :data="activeShipments" style="width: 100%">
            <el-table-column prop="id" label="运输ID" width="120" />
            <el-table-column prop="origin" label="起点" />
            <el-table-column prop="destination" label="终点" />
            <el-table-column prop="bloodType" label="血型" width="100" />
            <el-table-column prop="units" label="单位数" width="80" />
            <el-table-column prop="temperature" label="温度" width="100">
              <template #default="{ row }">
                <el-tag :type="getTempStatus(row.temperature)">
                  {{ row.temperature }}°C
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getShipmentStatus(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="eta" label="预计到达" width="120" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="trackShipment(row)">追踪</el-button>
                <el-button size="small" type="primary" @click="updateStatus(row)">更新</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Delivery Map -->
          <el-divider>实时追踪</el-divider>
          <el-row :gutter="16">
            <el-col :span="16">
              <el-card>
                <template #header>
                  <span>配送地图</span>
                </template>
                <div class="map-placeholder">
                  <el-empty description="交互式地图将在此处显示">
                    <template #image>
                      <div class="map-icon">
                        <el-icon style="font-size: 48px; color: #409eff;"><Location /></el-icon>
                      </div>
                    </template>
                  </el-empty>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <template #header>
                  <span>路线信息</span>
                </template>
                <div class="route-info">
                  <div class="route-item">
                    <div class="route-label">总距离</div>
                    <div class="route-value">245 公里</div>
                  </div>
                  <div class="route-item">
                    <div class="route-label">预计时间</div>
                    <div class="route-value">3小时45分钟</div>
                  </div>
                  <div class="route-item">
                    <div class="route-label">司机</div>
                    <div class="route-value">约翰·史密斯</div>
                  </div>
                  <div class="route-item">
                    <div class="route-label">车辆</div>
                    <div class="route-value">货车-001</div>
                  </div>
                  <div class="route-item">
                    <div class="route-label">最后更新</div>
                    <div class="route-value">5分钟前</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus, Refresh, Van, TrendCharts, Warning, Location } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const logisticsStats = ref([
  {
    id: 'active',
    label: '活跃运输',
    value: '12',
    icon: 'Van',
    color: '#409eff'
  },
  {
    id: 'delivered',
    label: '今日送达',
    value: '28',
    icon: 'TrendCharts',
    color: '#67c23a'
  },
  {
    id: 'transit',
    label: '运输中',
    value: '45',
    icon: 'Location',
    color: '#e6a23c'
  },
  {
    id: 'alerts',
    label: '温度警报',
    value: '2',
    icon: 'Warning',
    color: '#f56c6c'
  }
])

const activeShipments = ref([
  {
    id: 'SHP-001',
    origin: '主血库',
    destination: '市医院',
    bloodType: 'O+',
    units: 50,
    temperature: 4.2,
    status: 'In Transit',
    eta: '2024-01-15 14:30'
  },
  {
    id: 'SHP-002',
    origin: '区域中心',
    destination: '社区诊所',
    bloodType: 'A+',
    units: 25,
    temperature: 3.8,
    status: 'Delivered',
    eta: '2024-01-15 12:00'
  },
  {
    id: 'SHP-003',
    origin: '主血库',
    destination: '急诊室',
    bloodType: 'AB-',
    units: 10,
    temperature: 5.1,
    status: 'Delayed',
    eta: '2024-01-15 16:00'
  }
])

const getShipmentStatus = (status) => {
  switch (status) {
    case 'In Transit': return '运输中'
    case 'Delivered': return '已送达'
    case 'Delayed': return '延迟'
    case 'Pending': return '待处理'
    default: return status
  }
}

const getTempStatus = (temp) => {
  if (temp >= 2 && temp <= 6) return 'success'
  if (temp >= 1 && temp <= 8) return 'warning'
  return 'danger'
}

const getStatusType = (status) => {
  switch (status) {
    case 'In Transit': return 'warning'
    case 'Delivered': return 'success'
    case 'Delayed': return 'danger'
    case 'Pending': return 'info'
    default: return 'info'
  }
}

const createShipment = () => {
  notificationStore.info('创建新运输')
}

const refreshShipments = () => {
  notificationStore.success('运输信息已刷新')
}

const trackShipment = (shipment) => {
  notificationStore.info(`追踪运输: ${shipment.id}`)
}

const updateStatus = (shipment) => {
  notificationStore.info(`更新状态: ${shipment.id}`)
}
</script>

<style scoped>
.transport-logistics {
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

.logistics-stats {
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

.map-placeholder {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-icon {
  padding: 20px;
  border-radius: 50%;
  background: #ecf5ff;
}

.route-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.route-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.route-item:last-child {
  border-bottom: none;
}

.route-label {
  font-weight: 500;
  color: #606266;
}

.route-value {
  font-weight: 600;
  color: #303133;
}
</style>
