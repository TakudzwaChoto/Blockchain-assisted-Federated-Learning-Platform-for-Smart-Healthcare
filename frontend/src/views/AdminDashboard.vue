<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="welcome-section">
          <h1>Admin Console</h1>
          <p>System Management Dashboard</p>
          <div class="system-status">
            <div class="status-indicator online">
              <span class="status-dot"></span>
              System Online
            </div>
            <div class="last-update">
              Last Update: {{ lastUpdateTime }}
            </div>
          </div>
        </div>
        <div class="user-info">
          <el-dropdown @command="handleUserAction">
            <div class="user-avatar">
              <el-avatar :size="40">{{ authStore.user?.name?.charAt(0) }}</el-avatar>
              <div class="user-details">
                <div class="user-name">{{ authStore.user?.name }}</div>
                <div class="user-role">Administrator</div>
              </div>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">Profile</el-dropdown-item>
                <el-dropdown-item command="settings">Settings</el-dropdown-item>
                <el-dropdown-item command="logout" divided>Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon users">
            <el-icon size="32"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ userStats.total }}</div>
            <div class="stat-label">Total Users</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon donors">
            <el-icon size="32"><TrendCharts /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ systemStats.totalDonors }}</div>
            <div class="stat-label">Total Donors</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon inventory">
            <el-icon size="32"><Box /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ systemStats.totalRequests }}</div>
            <div class="stat-label">Total Requests</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon alerts">
            <el-icon size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ systemStats.pendingRequests }}</div>
            <div class="stat-label">Pending Requests</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Real-time Dashboard -->
      <el-card class="content-card full-width">
        <template #header>
          <h3>Real-time Monitoring</h3>
        </template>
        <RealTimeDashboard />
      </el-card>

      <!-- AI Predictions -->
      <el-card class="content-card full-width">
        <template #header>
          <h3>AI Predictions</h3>
        </template>
        <AIPredictions />
      </el-card>

      <!-- Mobile App -->
      <el-card class="content-card full-width">
        <template #header>
          <h3>Mobile App</h3>
        </template>
        <MobileApp />
      </el-card>

      <!-- User Management -->
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <h3>User Management</h3>
            <el-button type="primary" @click="showAddUserDialog = true">
              <el-icon><Plus /></el-icon>
              Add User
            </el-button>
          </div>
        </template>
        <div class="user-management">
          <el-table :data="users" style="width: 100%">
            <el-table-column prop="name" label="Name" width="120" />
            <el-table-column prop="email" label="Email" width="200" />
            <el-table-column prop="role" label="Role" width="100">
              <template #default="{ row }">
                <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
                  {{ row.role === 'admin' ? 'Admin' : 'User' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="department" label="Department" width="150" />
            <el-table-column prop="status" label="Status" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'info'">
                  {{ row.status === 'active' ? 'Active' : 'Offline' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="200">
              <template #default="{ row }">
                <el-button size="small" @click="editUser(row)">编辑用户</el-button>
                <el-button size="small" type="danger" @click="deleteUser(row)">删除用户</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      <!-- System Overview -->
      <el-card class="content-card">
        <template #header>
          <h3>系统概览</h3>
        </template>
        <div class="system-overview">
          <div class="overview-item">
            <div class="overview-label">血液库存</div>
            <div class="inventory-status">
              <div class="blood-type" v-for="type in bloodInventory" :key="type.type">
                <span class="type-label">{{ type.type }}</span>
                <el-progress 
                  :percentage="type.percentage" 
                  :color="type.percentage > 30 ? '#67c23a' : '#f56c6c'"
                  :show-text="false"
                />
                <span class="type-amount">{{ type.amount }}ml</span>
              </div>
            </div>
          </div>

          <div class="overview-item">
            <div class="overview-label">最近活动</div>
            <div class="recent-activities">
              <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
                <div class="activity-icon">
                  <el-icon :color="getActivityColor(activity.type)">
                    <component :is="getActivityIcon(activity.type)" />
                  </el-icon>
                </div>
                <div class="activity-content">
                  <div class="activity-desc">{{ activity.description }}</div>
                  <div class="activity-time">{{ formatDate(activity.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- Data Analytics -->
      <el-card class="content-card full-width">
        <template #header>
          <h3>数据分析</h3>
        </template>
        <div class="analytics-grid">
          <div class="analytics-item">
            <h4>血液趋势</h4>
            <div class="chart-placeholder">
              <div class="mock-chart">
                <div class="chart-bar" v-for="(value, index) in donationTrends" :key="index" 
                     :style="{ height: value + '%' }">
                </div>
              </div>
            </div>
          </div>

          <div class="analytics-item">
            <h4>Blood Type Distribution</h4>
            <div class="blood-type-distribution">
              <div class="distribution-item" v-for="type in bloodTypeDistribution" :key="type.type">
                <div class="type-info">
                  <span class="type-name">{{ type.type }}</span>
                  <span class="type-percentage">{{ type.percentage }}%</span>
                </div>
                <div class="type-bar">
                  <div class="bar-fill" :style="{ width: type.percentage + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Add User Dialog -->
    <el-dialog v-model="showAddUserDialog" title="添加新用户" width="500px">
      <el-form :model="newUser" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="newUser.name" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="newUser.email" />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="newUser.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="newUser.password" type="password" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="newUser.role" style="width: 100%">
            <el-option label="用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="newUser.department" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddUserDialog = false">取消</el-button>
        <el-button type="primary" @click="addUser">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  User, TrendCharts, Box, Warning, ArrowDown, Plus 
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/authStore'
import RealTimeDashboard from '../components/RealTimeDashboard.vue'
import AIPredictions from '../components/AIPredictions.vue'
import MobileApp from '../components/MobileApp.vue'
import dataService from '../services/dataService'

const router = useRouter()
const authStore = useAuthStore()

// Reactive data
const loading = ref(false)
const userStats = reactive({
  total: 0,
  admins: 0,
  active: 0,
  newThisMonth: 0
})

const systemStats = reactive({
  totalDonors: 0,
  totalRequests: 0,
  totalDonations: 0,
  pendingRequests: 0,
  inventoryStatus: []
})

const recentUsers = ref([])
const recentActivities = ref([])
const users = ref([])
const bloodInventory = ref([])
const donationTrends = ref([65, 80, 45, 90, 75, 85])
const bloodTypeDistribution = ref([
  { type: 'A+', percentage: 45 },
  { type: 'B+', percentage: 30 },
  { type: 'O+', percentage: 20 },
  { type: 'AB+', percentage: 5 }
])

// Add user dialog
const showAddUserDialog = ref(false)
const newUser = reactive({
  name: '',
  email: '',
  username: '',
  password: '',
  role: 'user',
  department: ''
})

// System status
const lastUpdateTime = ref(new Date().toLocaleTimeString())

// Load dashboard data
const loadDashboardData = async () => {
  loading.value = true
  try {
    const data = dataService.getAdminDashboardData()
    
    // Update last update time
    lastUpdateTime.value = new Date().toLocaleTimeString()
    
    // Update user stats
    userStats.total = data.stats.totalUsers
    userStats.admins = data.stats.totalUsers - 2 // Subtract demo users
    userStats.active = data.stats.activeUsers
    userStats.newThisMonth = data.stats.newThisMonth
    
    // Update system stats
    systemStats.totalDonors = data.stats.totalDonors
    systemStats.totalRequests = data.stats.totalRequests
    systemStats.totalDonations = data.stats.totalDonations
    systemStats.pendingRequests = data.stats.pendingRequests
    systemStats.inventoryStatus = dataService.getInventoryStatus()
    
    // Update recent data
    recentUsers.value = data.recentUsers
    recentActivities.value = data.recentActivities
    users.value = dataService.getAllUsers()
    
    // Update inventory display
    bloodInventory.value = systemStats.inventoryStatus.map(inv => ({
      type: inv.bloodType,
      amount: inv.amount,
      percentage: (inv.amount / inv.capacity) * 100
    }))
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// Action handlers
const handleUserAction = (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中')
      break
    case 'settings':
      ElMessage.info('设置功能开发中')
      break
    case 'logout':
      authStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
      break
  }
}

const viewUser = (user) => {
  ElMessage.info(`查看用户: ${user.name}`)
}

const editUser = (user) => {
  ElMessage.info(`编辑用户: ${user.name}`)
}

const deleteUser = (user) => {
  ElMessageBox.confirm(
    `确定删除用户 ${user.name} 吗？`,
    '删除用户',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('用户删除成功')
    loadDashboardData()
  })
}

const formatDate = (date) => {
  if (!date) return '从未'
  return new Date(date).toLocaleDateString('zh-CN')
}

const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    inactive: 'info',
    suspended: 'danger'
  }
  return colors[status] || 'info'
}

const getActivityIcon = (type) => {
  const icons = {
    user: User,
    request: Document,
    donation: Box
  }
  return icons[type] || Warning
}

const getActivityColor = (type) => {
  const colors = {
    user: '#409eff',
    request: '#67c23a',
    donation: '#e6a23c'
  }
  return colors[type] || '#909399'
}

const addUser = () => {
  // Add user logic here
  ElMessage.success('用户添加成功')
  showAddUserDialog.value = false
  // Reset form
  Object.assign(newUser, {
    name: '',
    email: '',
    username: '',
    password: '',
    role: 'user',
    department: ''
  })
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.admin-dashboard {
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
  margin: 0 0 16px 0;
  color: #666;
  font-size: 16px;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 24px;
  font-size: 14px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-indicator.online {
  color: #67c23a;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #67c23a;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.last-update {
  color: #909399;
  font-size: 13px;
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

.stat-icon.users { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.donors { background: linear-gradient(135deg, #f093fb, #f5576c); }
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

.user-management {
  max-height: 400px;
  overflow-y: auto;
}

.system-overview {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.overview-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.inventory-status {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.blood-type {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-label {
  width: 40px;
  font-weight: 600;
  color: #333;
}

.type-amount {
  width: 80px;
  text-align: right;
  font-size: 12px;
  color: #666;
}

.recent-activities {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-desc {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #666;
}

.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.analytics-item {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
}

.analytics-item h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.chart-placeholder {
  height: 120px;
  display: flex;
  align-items: flex-end;
  padding: 10px;
  background: white;
  border-radius: 4px;
}

.mock-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 100%;
  width: 100%;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 2px 2px 0 0;
  min-height: 10px;
}

.blood-type-distribution {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-info {
  width: 80px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.type-percentage {
  color: #666;
}

.type-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 200px;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.mock-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 100%;
}

.chart-bar {
  width: 30px;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
}

.blood-type-distribution {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-info {
  width: 60px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.type-percentage {
  color: #666;
}

.type-bar {
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

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .analytics-grid {
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
}
</style>
