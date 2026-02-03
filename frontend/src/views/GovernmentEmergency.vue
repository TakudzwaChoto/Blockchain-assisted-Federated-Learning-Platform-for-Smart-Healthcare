<template>
  <div class="government-emergency">
    <div class="emergency-header">
      <h1>应急协调中心</h1>
      <p>血液应急响应与资源调配管理</p>
    </div>

    <div class="emergency-content">
      <!-- Emergency Status -->
      <div class="section-card">
        <div class="section-header">
          <h3>应急状态</h3>
          <div class="header-actions">
            <el-button type="danger" @click="declareEmergency">
              <el-icon><Warning /></el-icon>
              宣布紧急状态
            </el-button>
          </div>
        </div>
        <div class="emergency-status-display">
          <div class="status-indicator" :class="emergencyStatus.level">
            <div class="status-icon">
              <el-icon>
                <component :is="getStatusIcon(emergencyStatus.level)" />
              </el-icon>
            </div>
            <div class="status-content">
              <div class="status-title">{{ emergencyStatus.title }}</div>
              <div class="status-description">{{ emergencyStatus.description }}</div>
              <div class="status-time">更新时间: {{ emergencyStatus.updateTime }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Emergencies -->
      <div class="section-card">
        <div class="section-header">
          <h3>活跃紧急事件</h3>
          <div class="header-actions">
            <el-button @click="refreshEmergencies">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
        <div class="emergencies-list">
          <div v-for="emergency in activeEmergencies" :key="emergency.id" class="emergency-item">
            <div class="emergency-header">
              <div class="emergency-info">
                <h4>{{ emergency.title }}</h4>
                <div class="emergency-meta">
                  <span class="emergency-location">{{ emergency.location }}</span>
                  <span class="emergency-time">{{ emergency.reportTime }}</span>
                  <span class="emergency-urgency" :class="emergency.urgency">
                    {{ emergency.urgencyText }}
                  </span>
                </div>
              </div>
              <div class="emergency-actions">
                <el-button size="small" type="primary" @click="coordinateResponse(emergency)">
                  协调响应
                </el-button>
              </div>
            </div>
            <div class="emergency-details">
              <p>{{ emergency.description }}</p>
              <div class="emergency-requirements">
                <div class="requirement-item">
                  <span class="requirement-label">血液需求:</span>
                  <span class="requirement-value">{{ emergency.bloodRequirement }}</span>
                </div>
                <div class="requirement-item">
                  <span class="requirement-label">响应时间:</span>
                  <span class="requirement-value">{{ emergency.responseTime }}</span>
                </div>
                <div class="requirement-item">
                  <span class="requirement-label">协调机构:</span>
                  <span class="requirement-value">{{ emergency.coordinatedInstitutions }} 家</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Resource Management -->
      <div class="section-card">
        <div class="section-header">
          <h3>资源管理</h3>
          <div class="header-actions">
            <el-button type="success" @click="allocateResources">
              <el-icon><Position /></el-icon>
              资源调配
            </el-button>
          </div>
        </div>
        <div class="resources-grid">
          <div class="resource-category">
            <div class="category-header">
              <h4>血液储备</h4>
              <div class="category-total">{{ resources.blood.total }} 单位</div>
            </div>
            <div class="resource-breakdown">
              <div v-for="type in resources.blood.types" :key="type.type" class="resource-item">
                <div class="resource-type">{{ type.type }}</div>
                <div class="resource-amount">{{ type.amount }}</div>
                <div class="resource-status" :class="type.status">
                  {{ type.statusText }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="resource-category">
            <div class="category-header">
              <h4>运输能力</h4>
              <div class="category-total">{{ resources.transport.total }} 辆</div>
            </div>
            <div class="resource-breakdown">
              <div v-for="vehicle in resources.transport.vehicles" :key="vehicle.type" class="resource-item">
                <div class="resource-type">{{ vehicle.type }}</div>
                <div class="resource-amount">{{ vehicle.available }}/{{ vehicle.total }}</div>
                <div class="resource-status" :class="vehicle.status">
                  {{ vehicle.statusText }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="resource-category">
            <div class="category-header">
              <h4>人员配置</h4>
              <div class="category-total">{{ resources.personnel.total }} 人</div>
            </div>
            <div class="resource-breakdown">
              <div v-for="staff in resources.personnel.staff" :key="staff.role" class="resource-item">
                <div class="resource-type">{{ staff.role }}</div>
                <div class="resource-amount">{{ staff.available }}/{{ staff.total }}</div>
                <div class="resource-status" :class="staff.status">
                  {{ staff.statusText }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Coordination Network -->
      <div class="section-card">
        <div class="section-header">
          <h3>协调网络</h3>
          <div class="header-actions">
            <el-button @click="testCommunication">
              <el-icon><Message /></el-icon>
              测试通信
            </el-button>
          </div>
        </div>
        <div class="coordination-map">
          <div class="map-placeholder">
            <div class="network-visualization">
              <div class="central-node">
                <div class="node-label">应急中心</div>
              </div>
              <div v-for="institution in networkInstitutions" :key="institution.id" 
                   class="institution-node" 
                   :class="institution.status"
                   :style="{ 
                     left: institution.position.x + '%', 
                     top: institution.position.y + '%' 
                   }">
                <div class="node-dot"></div>
                <div class="node-label">{{ institution.name }}</div>
              </div>
            </div>
          </div>
          <div class="network-status">
            <h4>网络状态</h4>
            <div class="status-grid">
              <div class="status-item">
                <span class="status-label">在线机构</span>
                <span class="status-value">{{ networkStatus.online }}</span>
              </div>
              <div class="status-item">
                <span class="status-label">离线机构</span>
                <span class="status-value">{{ networkStatus.offline }}</span>
              </div>
              <div class="status-item">
                <span class="status-label">通信延迟</span>
                <span class="status-value">{{ networkStatus.latency }}ms</span>
              </div>
              <div class="status-item">
                <span class="status-label">网络质量</span>
                <span class="status-value" :class="networkStatus.quality">{{ networkStatus.qualityText }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Response History -->
      <div class="section-card">
        <div class="section-header">
          <h3>响应历史</h3>
          <div class="header-actions">
            <el-button @click="exportHistory">
              <el-icon><Download /></el-icon>
              导出记录
            </el-button>
          </div>
        </div>
        <div class="history-timeline">
          <div v-for="event in responseHistory" :key="event.id" class="timeline-item">
            <div class="timeline-marker" :class="event.type">
              <el-icon>
                <component :is="getEventIcon(event.type)" />
              </el-icon>
            </div>
            <div class="timeline-content">
              <div class="event-header">
                <h4>{{ event.title }}</h4>
                <span class="event-time">{{ event.timestamp }}</span>
              </div>
              <p>{{ event.description }}</p>
              <div class="event-outcome">
                <span class="outcome-label">处理结果:</span>
                <span class="outcome-value" :class="event.outcome">{{ event.outcomeText }}</span>
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
  Warning, 
  Refresh, 
  Position, 
  Message, 
  Download,
  Check,
  Clock,
  TrendCharts
} from '@element-plus/icons-vue'

// Reactive data
const emergencyStatus = ref({
  level: 'normal',
  title: '正常状态',
  description: '当前无紧急事件，系统运行正常',
  updateTime: new Date().toLocaleString('zh-CN')
})

const activeEmergencies = ref([
  {
    id: 1,
    title: '重大交通事故应急用血',
    location: '北京市朝阳区',
    reportTime: '2024-06-20 14:30',
    urgency: 'critical',
    urgencyText: '紧急',
    description: '朝阳区发生重大交通事故，多名伤员急需输血救治',
    bloodRequirement: 'A+型血 800ml, O+型血 1200ml',
    responseTime: '30分钟内',
    coordinatedInstitutions: 5
  },
  {
    id: 2,
    title: '医院手术备血请求',
    location: '上海市浦东新区',
    reportTime: '2024-06-20 16:15',
    urgency: 'urgent',
    urgencyText: '急迫',
    description: '浦东医院急诊手术需要大量备用血液',
    bloodRequirement: '各血型共计 2000ml',
    responseTime: '1小时内',
    coordinatedInstitutions: 3
  }
])

const resources = ref({
  blood: {
    total: 12500,
    types: [
      { type: 'A+', amount: 3200, status: 'sufficient', statusText: '充足' },
      { type: 'B+', amount: 2800, status: 'sufficient', statusText: '充足' },
      { type: 'O+', amount: 4100, status: 'warning', statusText: '紧张' },
      { type: 'AB+', amount: 2400, status: 'sufficient', statusText: '充足' }
    ]
  },
  transport: {
    total: 45,
    vehicles: [
      { type: '冷藏车', available: 12, total: 15, status: 'available', statusText: '可用' },
      { type: '急救车', available: 8, total: 10, status: 'available', statusText: '可用' },
      { type: '普通运输', available: 18, total: 20, status: 'available', statusText: '可用' }
    ]
  },
  personnel: {
    total: 128,
    staff: [
      { role: '协调员', available: 15, total: 20, status: 'available', statusText: '在岗' },
      { role: '医护人员', available: 45, total: 60, status: 'available', statusText: '在岗' },
      { role: '司机', available: 28, total: 35, status: 'busy', statusText: '任务中' },
      { role: '技术员', available: 40, total: 48, status: 'available', statusText: '在岗' }
    ]
  }
})

const networkInstitutions = ref([
  { id: 1, name: '北京血站', status: 'online', position: { x: 20, y: 30 } },
  { id: 2, name: '上海血站', status: 'online', position: { x: 70, y: 25 } },
  { id: 3, name: '广州血站', status: 'online', position: { x: 65, y: 70 } },
  { id: 4, name: '深圳血站', status: 'offline', position: { x: 75, y: 80 } },
  { id: 5, name: '天津血站', status: 'online', position: { x: 35, y: 20 } }
])

const networkStatus = ref({
  online: 4,
  offline: 1,
  latency: 45,
  quality: 'good',
  qualityText: '良好'
})

const responseHistory = ref([
  {
    id: 1,
    title: '地震应急响应',
    type: 'emergency',
    timestamp: '2024-06-15 08:30',
    description: '四川地震地区紧急血液调配，成功运送血液制品3000ml',
    outcome: 'success',
    outcomeText: '成功'
  },
  {
    id: 2,
    title: '大型活动保障',
    type: 'event',
    timestamp: '2024-06-10 14:00',
    description: '国际会议期间血液保障工作，确保医疗机构血液供应',
    outcome: 'success',
    outcomeText: '成功'
  },
  {
    id: 3,
    title: '系统故障处理',
    type: 'system',
    timestamp: '2024-06-05 16:45',
    description: '血液管理系统故障，启动应急预案，手动协调血液供应',
    outcome: 'partial',
    outcomeText: '部分成功'
  }
])

// Methods
const declareEmergency = () => {
  console.log('Declaring emergency state...')
}

const refreshEmergencies = () => {
  console.log('Refreshing emergency data...')
}

const coordinateResponse = (emergency) => {
  console.log('Coordinating response for:', emergency.title)
}

const allocateResources = () => {
  console.log('Allocating emergency resources...')
}

const testCommunication = () => {
  console.log('Testing emergency communication network...')
}

const exportHistory = () => {
  console.log('Exporting response history...')
}

const getStatusIcon = (level) => {
  const iconMap = {
    'normal': Check,
    'warning': Warning,
    'critical': Warning
  }
  return iconMap[level] || Check
}

const getEventIcon = (type) => {
  const iconMap = {
    'emergency': Warning,
    'event': TrendCharts,
    'system': Clock
  }
  return iconMap[type] || Clock
}
</script>

<style scoped>
.government-emergency {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.emergency-header {
  margin-bottom: 24px;
}

.emergency-header h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.emergency-header p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.emergency-content {
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

.emergency-status-display {
  padding: 24px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  border-radius: 12px;
  border-left: 4px solid;
}

.status-indicator.normal {
  background: #f0f9ff;
  border-left-color: #67c23a;
}

.status-indicator.warning {
  background: #fdf6ec;
  border-left-color: #e6a23c;
}

.status-indicator.critical {
  background: #fef0f0;
  border-left-color: #f56c6c;
}

.status-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.status-indicator.normal .status-icon {
  background: #67c23a;
}

.status-indicator.warning .status-icon {
  background: #e6a23c;
}

.status-indicator.critical .status-icon {
  background: #f56c6c;
}

.status-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.status-description {
  color: #666;
  margin-bottom: 8px;
}

.status-time {
  font-size: 12px;
  color: #999;
}

.emergencies-list {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.emergency-item {
  padding: 20px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.emergency-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.emergency-info h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.emergency-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.emergency-location,
.emergency-time {
  font-size: 12px;
  color: #666;
}

.emergency-urgency {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.emergency-urgency.critical {
  background: #fef0f0;
  color: #f56c6c;
}

.emergency-urgency.urgent {
  background: #fdf6ec;
  color: #e6a23c;
}

.emergency-urgency.normal {
  background: #f0f9ff;
  color: #409eff;
}

.emergency-details p {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 14px;
}

.emergency-requirements {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
}

.requirement-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.requirement-label {
  color: #666;
}

.requirement-value {
  color: #333;
  font-weight: 500;
}

.resources-grid {
  padding: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.resource-category {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.category-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.category-total {
  font-size: 18px;
  font-weight: 700;
  color: #667eea;
}

.resource-breakdown {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.resource-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  font-size: 14px;
}

.resource-type {
  color: #333;
  font-weight: 500;
}

.resource-amount {
  text-align: center;
  color: #666;
}

.resource-status {
  text-align: right;
  font-size: 12px;
  font-weight: 500;
}

.resource-status.sufficient {
  color: #67c23a;
}

.resource-status.warning {
  color: #e6a23c;
}

.resource-status.critical {
  color: #f56c6c;
}

.resource-status.available {
  color: #67c23a;
}

.resource-status.busy {
  color: #e6a23c;
}

.coordination-map {
  padding: 24px;
}

.map-placeholder {
  height: 300px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.network-visualization {
  position: relative;
  width: 100%;
  height: 100%;
}

.central-node {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #667eea;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 12px;
  z-index: 10;
}

.institution-node {
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 5;
}

.node-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin: 0 auto 4px;
}

.institution-node.online .node-dot {
  background: #67c23a;
}

.institution-node.offline .node-dot {
  background: #f56c6c;
}

.node-label {
  font-size: 10px;
  color: #666;
  text-align: center;
  white-space: nowrap;
}

.network-status h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.status-label {
  color: #666;
  font-size: 14px;
}

.status-value {
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.status-value.good {
  color: #67c23a;
}

.status-value.warning {
  color: #e6a23c;
}

.status-value.poor {
  color: #f56c6c;
}

.history-timeline {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.timeline-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.timeline-marker {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  font-size: 14px;
}

.timeline-marker.emergency {
  background: #f56c6c;
}

.timeline-marker.event {
  background: #409eff;
}

.timeline-marker.system {
  background: #e6a23c;
}

.timeline-content {
  flex: 1;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.event-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.event-time {
  font-size: 12px;
  color: #999;
}

.timeline-content p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.event-outcome {
  display: flex;
  gap: 8px;
  align-items: center;
}

.outcome-label {
  font-size: 12px;
  color: #666;
}

.outcome-value {
  font-size: 12px;
  font-weight: 500;
}

.outcome-value.success {
  color: #67c23a;
}

.outcome-value.partial {
  color: #e6a23c;
}

.outcome-value.failed {
  color: #f56c6c;
}

@media (max-width: 768px) {
  .resources-grid {
    grid-template-columns: 1fr;
  }
  
  .emergency-requirements {
    grid-template-columns: 1fr;
  }
  
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .resource-item {
    grid-template-columns: 1fr;
    gap: 4px;
  }
}
</style>
