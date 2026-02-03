<template>
  <div class="user-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="welcome-section">
          <h1>个人工作台</h1>
          <p>{{ userStore.user?.department }} - {{ userStore.user?.name }}</p>
        </div>
        <div class="user-info">
          <el-dropdown @command="handleUserAction">
            <div class="user-avatar">
              <el-avatar :size="40">{{ userStore.user?.name?.charAt(0) }}</el-avatar>
              <div class="user-details">
                <div class="user-name">{{ userStore.user?.name }}</div>
                <div class="user-role">{{ userStore.user?.department }}</div>
              </div>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="settings">个人设置</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- Personal Stats -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon donors">
            <el-icon size="32"><TrendCharts /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ personalStats.myDonors }}</div>
            <div class="stat-label">我的捐赠者</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon requests">
            <el-icon size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ personalStats.myRequests }}</div>
            <div class="stat-label">待处理申请</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon inventory">
            <el-icon size="32"><Box /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ personalStats.myInventory }}</div>
            <div class="stat-label">库存监控</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon alerts">
            <el-icon size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ personalStats.myAlerts }}</div>
            <div class="stat-label">我的提醒</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- My Donors -->
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <h3>我的捐赠者管理</h3>
            <el-button type="primary" @click="showAddDonorDialog = true">
              <el-icon><Plus /></el-icon>
              添加捐赠者
            </el-button>
          </div>
        </template>
        <div class="donors-list">
          <el-table :data="myDonors" style="width: 100%">
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="bloodType" label="血型" width="80">
              <template #default="{ row }">
                <el-tag :type="getBloodTypeColor(row.bloodType)">
                  {{ row.bloodType }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="phone" label="电话" width="120" />
            <el-table-column prop="lastDonation" label="最近捐赠" width="100" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'info'">
                  {{ row.status === 'active' ? '活跃' : '暂停' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="viewDonor(row)">查看</el-button>
                <el-button size="small" type="primary" @click="editDonor(row)">编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      <!-- My Requests -->
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <h3>输血申请</h3>
            <el-button type="primary" @click="showAddRequestDialog = true">
              <el-icon><Plus /></el-icon>
              新建申请
            </el-button>
          </div>
        </template>
        <div class="requests-list">
          <el-table :data="myRequests" style="width: 100%">
            <el-table-column prop="patientName" label="患者姓名" width="100" />
            <el-table-column prop="bloodType" label="血型" width="80">
              <template #default="{ row }">
                <el-tag :type="getBloodTypeColor(row.bloodType)">
                  {{ row.bloodType }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="需求量" width="80">
              <template #default="{ row }">
                {{ row.amount }}ml
              </template>
            </el-table-column>
            <el-table-column prop="urgency" label="紧急程度" width="100">
              <template #default="{ row }">
                <el-tag :type="getUrgencyColor(row.urgency)">
                  {{ getUrgencyText(row.urgency) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusColor(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button size="small" @click="viewRequest(row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      <!-- Personal Analytics -->
      <el-card class="content-card full-width">
        <template #header>
          <h3>个人数据分析</h3>
        </template>
        <div class="personal-analytics">
          <div class="analytics-section">
            <h4>本月捐赠统计</h4>
            <div class="monthly-stats">
              <div class="stat-item">
                <div class="stat-label">新增捐赠者</div>
                <div class="stat-value">{{ monthlyStats.newDonors }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">成功捐赠</div>
                <div class="stat-value">{{ monthlyStats.successfulDonations }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">处理申请</div>
                <div class="stat-value">{{ monthlyStats.processedRequests }}</div>
              </div>
            </div>
          </div>

          <div class="analytics-section">
            <h4>血型分布</h4>
            <div class="blood-type-chart">
              <div class="chart-item" v-for="type in myBloodTypeDistribution" :key="type.type">
                <div class="chart-info">
                  <span class="type-name">{{ type.type }}</span>
                  <span class="type-count">{{ type.count }}人</span>
                </div>
                <div class="chart-bar">
                  <div class="bar-fill" :style="{ width: (type.count / maxDonors * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- Recent Activities -->
      <el-card class="content-card">
        <template #header>
          <h3>最近活动</h3>
        </template>
        <div class="recent-activities">
          <div class="activity-item" v-for="activity in myRecentActivities" :key="activity.id">
            <div class="activity-icon">
              <el-icon :color="getActivityColor(activity.type)">
                <component :is="getActivityIcon(activity.type)" />
              </el-icon>
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-desc">{{ activity.description }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Add Donor Dialog -->
    <el-dialog v-model="showAddDonorDialog" title="添加捐赠者" width="500px">
      <el-form :model="newDonor" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="newDonor.name" />
        </el-form-item>
        <el-form-item label="血型">
          <el-select v-model="newDonor.bloodType" style="width: 100%">
            <el-option label="A+" value="A+" />
            <el-option label="B+" value="B+" />
            <el-option label="O+" value="O+" />
            <el-option label="AB+" value="AB+" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="newDonor.phone" />
        </el-form-item>
        <el-form-item label="身份证">
          <el-input v-model="newDonor.idCard" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDonorDialog = false">取消</el-button>
        <el-button type="primary" @click="addDonor">确定</el-button>
      </template>
    </el-dialog>

    <!-- Add Request Dialog -->
    <el-dialog v-model="showAddRequestDialog" title="新建输血申请" width="500px">
      <el-form :model="newRequest" label-width="80px">
        <el-form-item label="患者姓名">
          <el-input v-model="newRequest.patientName" />
        </el-form-item>
        <el-form-item label="血型">
          <el-select v-model="newRequest.bloodType" style="width: 100%">
            <el-option label="A+" value="A+" />
            <el-option label="B+" value="B+" />
            <el-option label="O+" value="O+" />
            <el-option label="AB+" value="AB+" />
          </el-select>
        </el-form-item>
        <el-form-item label="需求量">
          <el-input v-model="newRequest.amount" placeholder="毫升">
            <template #append>ml</template>
          </el-input>
        </el-form-item>
        <el-form-item label="紧急程度">
          <el-select v-model="newRequest.urgency" style="width: 100%">
            <el-option label="常规" value="normal" />
            <el-option label="紧急" value="urgent" />
            <el-option label="非常紧急" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="newRequest.notes" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddRequestDialog = false">取消</el-button>
        <el-button type="primary" @click="addRequest">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  TrendCharts, Document, Box, Warning, ArrowDown, Plus, 
  User, Clock, Check
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const userStore = useAuthStore()

const showAddDonorDialog = ref(false)
const showAddRequestDialog = ref(false)

// Personal stats based on user
const personalStats = reactive({
  myDonors: 23,
  myRequests: 5,
  myInventory: 8,
  myAlerts: 2
})

// Mock data for current user
const myDonors = ref([
  {
    id: 'donor-001',
    name: '王小明',
    bloodType: 'A+',
    phone: '13800138001',
    lastDonation: '2024-06-15',
    status: 'active'
  },
  {
    id: 'donor-002',
    name: '李小红',
    bloodType: 'O+',
    phone: '13800138002',
    lastDonation: '2024-05-20',
    status: 'active'
  },
  {
    id: 'donor-003',
    name: '张小华',
    bloodType: 'B+',
    phone: '13800138003',
    lastDonation: '2024-04-10',
    status: 'inactive'
  }
])

const myRequests = ref([
  {
    id: 'req-001',
    patientName: '患者A',
    bloodType: 'A+',
    amount: 400,
    urgency: 'urgent',
    status: 'pending'
  },
  {
    id: 'req-002',
    patientName: '患者B',
    bloodType: 'O+',
    amount: 300,
    urgency: 'normal',
    status: 'approved'
  }
])

const monthlyStats = reactive({
  newDonors: 5,
  successfulDonations: 12,
  processedRequests: 8
})

const myBloodTypeDistribution = ref([
  { type: 'A+', count: 8 },
  { type: 'B+', count: 6 },
  { type: 'O+', count: 7 },
  { type: 'AB+', count: 2 }
])

const myRecentActivities = ref([
  {
    id: 1,
    type: 'donor',
    title: '新增捐赠者',
    description: '添加了新的捐赠者：王小明',
    time: '2小时前'
  },
  {
    id: 2,
    type: 'request',
    title: '处理申请',
    description: '完成了输血申请审批',
    time: '4小时前'
  },
  {
    id: 3,
    type: 'donation',
    title: '记录捐赠',
    description: '记录了李小红的血液捐赠',
    time: '1天前'
  }
])

const newDonor = reactive({
  name: '',
  bloodType: '',
  phone: '',
  idCard: ''
})

const newRequest = reactive({
  patientName: '',
  bloodType: '',
  amount: '',
  urgency: 'normal',
  notes: ''
})

const maxDonors = computed(() => 
  Math.max(...myBloodTypeDistribution.value.map(type => type.count))
)

// Helper functions
const getBloodTypeColor = (type) => {
  const colors = {
    'A+': 'primary',
    'B+': 'success',
    'O+': 'warning',
    'AB+': 'danger'
  }
  return colors[type] || 'info'
}

const getUrgencyColor = (urgency) => {
  const colors = {
    'normal': 'success',
    'urgent': 'warning',
    'critical': 'danger'
  }
  return colors[urgency] || 'info'
}

const getUrgencyText = (urgency) => {
  const texts = {
    'normal': '常规',
    'urgent': '紧急',
    'critical': '非常紧急'
  }
  return texts[urgency] || urgency
}

const getStatusColor = (status) => {
  const colors = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'completed': 'info'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'pending': '待处理',
    'approved': '已批准',
    'rejected': '已拒绝',
    'completed': '已完成'
  }
  return texts[status] || status
}

const getActivityColor = (type) => {
  const colors = {
    'donor': '#67c23a',
    'request': '#e6a23c',
    'donation': '#409eff'
  }
  return colors[type] || '#909399'
}

const getActivityIcon = (type) => {
  const icons = {
    'donor': User,
    'request': Document,
    'donation': Check
  }
  return icons[type] || Clock
}

// Action handlers
const handleUserAction = (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中')
      break
    case 'settings':
      ElMessage.info('个人设置功能开发中')
      break
    case 'logout':
      userStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
      break
  }
}

const viewDonor = (donor) => {
  ElMessage.info(`查看捐赠者: ${donor.name}`)
}

const editDonor = (donor) => {
  ElMessage.info(`编辑捐赠者: ${donor.name}`)
}

const viewRequest = (request) => {
  ElMessage.info(`查看申请: ${request.patientName}`)
}

const addDonor = () => {
  if (!newDonor.name || !newDonor.bloodType || !newDonor.phone) {
    ElMessage.warning('请填写必要信息')
    return
  }

  const donorData = {
    id: `donor-${Date.now()}`,
    ...newDonor,
    lastDonation: '暂无',
    status: 'active'
  }

  myDonors.value.push(donorData)
  showAddDonorDialog.value = false
  
  // Reset form
  Object.keys(newDonor).forEach(key => {
    newDonor[key] = ''
  })

  ElMessage.success('捐赠者添加成功')
  personalStats.myDonors++
}

const addRequest = () => {
  if (!newRequest.patientName || !newRequest.bloodType || !newRequest.amount) {
    ElMessage.warning('请填写必要信息')
    return
  }

  const requestData = {
    id: `req-${Date.now()}`,
    ...newRequest,
    status: 'pending'
  }

  myRequests.value.push(requestData)
  showAddRequestDialog.value = false
  
  // Reset form
  Object.keys(newRequest).forEach(key => {
    if (key === 'urgency') {
      newRequest[key] = 'normal'
    } else {
      newRequest[key] = ''
    }
  })

  ElMessage.success('申请创建成功')
  personalStats.myRequests++
}

onMounted(() => {
  // Check if user is not admin
  if (userStore.isAdmin) {
    router.push('/admin/dashboard')
  }
})
</script>

<style scoped>
.user-dashboard {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-section h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.welcome-section p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.user-avatar:hover {
  background-color: #f5f7fa;
}

.user-details {
  text-align: right;
}

.user-name {
  font-weight: 600;
  color: #333;
}

.user-role {
  font-size: 12px;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon.donors { background: linear-gradient(135deg, #f093fb, #f5576c); }
.stat-icon.requests { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.inventory { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.alerts { background: linear-gradient(135deg, #fa709a, #fee140); }

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.stat-label {
  color: #666;
  font-size: 14px;
  margin-top: 4px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.content-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.content-card.full-width {
  grid-column: 1 / -1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  color: #333;
}

.donors-list,
.requests-list {
  max-height: 400px;
  overflow-y: auto;
}

.personal-analytics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.analytics-section h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.monthly-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.blood-type-chart {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chart-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chart-info {
  width: 80px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.type-count {
  color: #666;
}

.chart-bar {
  flex: 1;
  height: 20px;
  background: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.recent-activities {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.activity-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #999;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .personal-analytics {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .monthly-stats {
    flex-direction: column;
  }
}
</style>
