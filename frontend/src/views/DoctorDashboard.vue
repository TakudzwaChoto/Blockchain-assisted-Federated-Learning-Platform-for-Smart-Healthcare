<template>
  <div class="doctor-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="welcome-section">
          <h1 class="welcome-title">医生工作台</h1>
          <p class="welcome-subtitle">血液管理与输血安全分析系统</p>
        </div>
        <div class="user-info">
          <div class="user-details">
            <span class="user-name">{{ user?.name || '医生用户' }}</span>
            <span class="user-role">主治医师</span>
          </div>
          <el-avatar :size="40" :src="user?.avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon patients">
            <el-icon size="32"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ doctorStats.totalPatients }}</div>
            <div class="stat-label">管理患者</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon requests">
            <el-icon size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ doctorStats.pendingRequests }}</div>
            <div class="stat-label">待审核申请</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon transfusions">
            <el-icon size="32"><Box /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ doctorStats.todayTransfusions }}</div>
            <div class="stat-label">今日输血</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon alerts">
            <el-icon size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ doctorStats.criticalAlerts }}</div>
            <div class="stat-label">紧急警报</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Patient Management -->
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <h3>患者管理</h3>
            <div class="header-actions">
              <el-input
                v-model="patientSearch"
                placeholder="搜索患者..."
                prefix-icon="Search"
                style="width: 200px; margin-right: 12px"
                @input="filterPatients"
              />
              <el-button type="primary" @click="showAddPatient = true">
                <el-icon><Plus /></el-icon>
                添加患者
              </el-button>
            </div>
          </div>
        </template>
        <div class="patient-management">
          <el-table :data="filteredPatients" style="width: 100%" v-loading="loadingPatients">
            <el-table-column prop="name" label="患者姓名" width="120" sortable />
            <el-table-column prop="bloodType" label="血型" width="80">
              <template #default="{ row }">
                <el-tag :type="getBloodTypeColor(row.bloodType)" size="small">
                  {{ row.bloodType }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="age" label="年龄" width="60" sortable />
            <el-table-column prop="condition" label="病情" width="150">
              <template #default="{ row }">
                <el-tag :type="getConditionColor(row.condition)" size="small">
                  {{ row.condition }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="lastTransfusion" label="最近输血" width="120" sortable>
              <template #default="{ row }">
                {{ formatDate(row.lastTransfusion) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusColor(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button size="small" @click="viewPatientDetails(row)">查看详情</el-button>
                <el-button size="small" type="primary" @click="createTransfusionRequest(row)">
                  申请输血
                </el-button>
                <el-dropdown trigger="click">
                  <el-button size="small" type="info">
                    更多<el-icon><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="editPatient(row)">编辑信息</el-dropdown-item>
                      <el-dropdown-item @click="viewPatientHistory(row)">输血历史</el-dropdown-item>
                      <el-dropdown-item @click="generatePatientReport(row)">生成报告</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="patientPagination.current"
              v-model:page-size="patientPagination.size"
              :page-sizes="[5, 10, 20, 50]"
              :total="patientPagination.total"
              layout="total, sizes, prev, pager, next"
              @size-change="handlePatientSizeChange"
              @current-change="handlePatientPageChange"
            />
          </div>
        </div>
      </el-card>

      <!-- Transfusion Requests -->
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <h3>输血申请管理</h3>
            <div class="header-actions">
              <el-select v-model="requestFilter" placeholder="筛选状态" style="width: 120px; margin-right: 12px">
                <el-option label="全部" value="" />
                <el-option label="待审核" value="pending" />
                <el-option label="已批准" value="approved" />
                <el-option label="已完成" value="completed" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
              <el-button @click="viewAllRequests">查看全部</el-button>
            </div>
          </div>
        </template>
        <div class="requests-list">
          <div class="request-item" v-for="request in filteredRequests" :key="request.id">
            <div class="request-header">
              <div class="request-patient">
                <el-icon><User /></el-icon>
                {{ request.patientName }}
              </div>
              <div class="request-status">
                <el-tag :type="getRequestStatusColor(request.status)" size="small">
                  {{ getRequestStatusText(request.status) }}
                </el-tag>
              </div>
            </div>
            <div class="request-details">
              <div class="request-info">
                <span class="info-label">血型:</span>
                <el-tag :type="getBloodTypeColor(request.bloodType)" size="small">
                  {{ request.bloodType }}
                </el-tag>
              </div>
              <div class="request-info">
                <span class="info-label">用量:</span>
                <span class="info-value">{{ request.amount }}ml</span>
              </div>
              <div class="request-info">
                <span class="info-label">紧急度:</span>
                <el-tag :type="getUrgencyColor(request.urgency)" size="small">
                  {{ request.urgency }}
                </el-tag>
              </div>
              <div class="request-info">
                <span class="info-label">申请时间:</span>
                <span class="info-value">{{ formatDateTime(request.createdAt) }}</span>
              </div>
            </div>
            <div class="request-reason" v-if="request.reason">
              <strong>输血原因:</strong> {{ request.reason }}
            </div>
            <div class="request-actions">
              <el-button size="small" @click="viewRequestDetails(request)">详情</el-button>
              <el-button 
                v-if="request.status === 'pending'" 
                size="small" 
                type="warning" 
                @click="editRequest(request)"
              >
                编辑
              </el-button>
              <el-button 
                v-if="request.status === 'pending'" 
                size="small" 
                type="danger" 
                @click="cancelRequest(request)"
              >
                取消
              </el-button>
              <el-button 
                v-if="request.status === 'approved'" 
                size="small" 
                type="success" 
                @click="confirmTransfusion(request)"
              >
                确认输血
              </el-button>
            </div>
          </div>
        </div>
      </el-card>

      <!-- Blood Inventory Status -->
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <h3>血液库存状态</h3>
            <el-button @click="refreshInventory" :loading="loadingInventory">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </template>
        <div class="inventory-status">
          <div class="inventory-summary">
            <div class="summary-item">
              <span class="summary-label">总库存:</span>
              <span class="summary-value">{{ totalInventory }}ml</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">低库存血型:</span>
              <span class="summary-value low-stock">{{ lowStockTypes.length }}种</span>
            </div>
          </div>
          <div class="blood-types">
            <div class="blood-type" v-for="type in bloodInventory" :key="type.type">
              <div class="type-header">
                <div class="type-label">{{ type.type }}</div>
                <div class="type-amount">{{ type.amount }}ml</div>
              </div>
              <div class="type-bar">
                <div 
                  class="bar-fill" 
                  :style="{ width: `${Math.min(type.percentage, 100)}%` }"
                  :class="{ 'low-stock': type.percentage < 30, 'medium-stock': type.percentage >= 30 && type.percentage < 60 }"
                ></div>
              </div>
              <div class="type-status">
                <span class="status-text" :class="getStockStatusClass(type.percentage)">
                  {{ getStockStatusText(type.percentage) }}
                </span>
              </div>
            </div>
          </div>
          <div class="inventory-actions">
            <el-button type="primary" @click="requestBloodSupply">申请血液供应</el-button>
            <el-button @click="viewInventoryHistory">库存历史</el-button>
          </div>
        </div>
      </el-card>

      <!-- Personal Analytics -->
      <el-card class="content-card full-width">
        <template #header>
          <div class="card-header">
            <h3>个人工作分析</h3>
            <div class="header-actions">
              <el-date-picker
                v-model="analyticsPeriod"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                @change="updateAnalytics"
              />
              <el-button @click="exportAnalytics">
                <el-icon><Download /></el-icon>
                导出报告
              </el-button>
            </div>
          </div>
        </template>
        <div class="analytics-content">
          <!-- Analytics Summary -->
          <div class="analytics-summary">
            <div class="summary-card">
              <div class="summary-icon patients">
                <el-icon><User /></el-icon>
              </div>
              <div class="summary-info">
                <div class="summary-number">{{ personalAnalytics.totalPatients }}</div>
                <div class="summary-label">管理患者总数</div>
              </div>
            </div>
            <div class="summary-card">
              <div class="summary-icon requests">
                <el-icon><Document /></el-icon>
              </div>
              <div class="summary-info">
                <div class="summary-number">{{ personalAnalytics.totalRequests }}</div>
                <div class="summary-label">输血申请总数</div>
              </div>
            </div>
            <div class="summary-card">
              <div class="summary-icon transfusions">
                <el-icon><Box /></el-icon>
              </div>
              <div class="summary-info">
                <div class="summary-number">{{ personalAnalytics.completedTransfusions }}</div>
                <div class="summary-label">完成输血总数</div>
              </div>
            </div>
            <div class="summary-card">
              <div class="summary-icon efficiency">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="summary-info">
                <div class="summary-number">{{ personalAnalytics.efficiency }}%</div>
                <div class="summary-label">工作效率</div>
              </div>
            </div>
          </div>

          <!-- Charts Section -->
          <div class="charts-section">
            <div class="chart-container">
              <h4>月度输血趋势</h4>
              <div class="chart-placeholder">
                <div class="mock-chart">
                  <div class="chart-bar" v-for="(value, index) in monthlyTrends" :key="index" :style="{ height: `${value}%` }"></div>
                </div>
                <div class="chart-labels">
                  <span v-for="(month, index) in chartMonths" :key="index">{{ month }}</span>
                </div>
              </div>
            </div>
            <div class="chart-container">
              <h4>血型使用分布</h4>
              <div class="blood-type-chart">
                <div class="distribution-item" v-for="type in bloodTypeDistribution" :key="type.type">
                  <div class="type-info">
                    <span class="type-name">{{ type.type }}</span>
                    <span class="type-percentage">{{ type.percentage }}%</span>
                  </div>
                  <div class="type-bar">
                    <div class="bar-fill" :style="{ width: `${type.percentage}%` }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Activities -->
          <div class="recent-activities">
            <h4>最近工作活动</h4>
            <div class="activity-timeline">
              <div class="timeline-item" v-for="activity in recentActivities" :key="activity.id">
                <div class="timeline-dot" :class="getActivityTypeClass(activity.type)"></div>
                <div class="timeline-content">
                  <div class="activity-header">
                    <span class="activity-title">{{ activity.title }}</span>
                    <span class="activity-time">{{ formatDateTime(activity.timestamp) }}</span>
                  </div>
                  <div class="activity-description">{{ activity.description }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Add Patient Dialog -->
    <el-dialog v-model="showAddPatient" title="添加患者" width="600px">
      <el-form :model="newPatient" :rules="patientRules" ref="patientForm" label-width="100px">
        <el-form-item label="患者姓名" prop="name">
          <el-input v-model="newPatient.name" />
        </el-form-item>
        <el-form-item label="血型" prop="bloodType">
          <el-select v-model="newPatient.bloodType" style="width: 100%">
            <el-option label="A+" value="A+" />
            <el-option label="A-" value="A-" />
            <el-option label="B+" value="B+" />
            <el-option label="B-" value="B-" />
            <el-option label="O+" value="O+" />
            <el-option label="O-" value="O-" />
            <el-option label="AB+" value="AB+" />
            <el-option label="AB-" value="AB-" />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="newPatient.age" :min="0" :max="150" />
        </el-form-item>
        <el-form-item label="病情描述" prop="condition">
          <el-input v-model="newPatient.condition" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="过敏史" prop="allergies">
          <el-input v-model="newPatient.allergies" type="textarea" rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddPatient = false">取消</el-button>
        <el-button type="primary" @click="addPatient">确定</el-button>
      </template>
    </el-dialog>

    <!-- Transfusion Request Dialog -->
    <el-dialog v-model="showTransfusionRequest" title="输血申请" width="600px">
      <el-form :model="transfusionRequest" :rules="requestRules" ref="requestForm" label-width="100px">
        <el-form-item label="患者">
          <el-input v-model="transfusionRequest.patientName" readonly />
        </el-form-item>
        <el-form-item label="血型">
          <el-input v-model="transfusionRequest.bloodType" readonly />
        </el-form-item>
        <el-form-item label="输血量(ml)" prop="amount">
          <el-input-number v-model="transfusionRequest.amount" :min="100" :max="2000" :step="100" />
        </el-form-item>
        <el-form-item label="紧急程度" prop="urgency">
          <el-select v-model="transfusionRequest.urgency" style="width: 100%">
            <el-option label="常规" value="常规" />
            <el-option label="紧急" value="紧急" />
            <el-option label="非常紧急" value="非常紧急" />
          </el-select>
        </el-form-item>
        <el-form-item label="输血原因" prop="reason">
          <el-input v-model="transfusionRequest.reason" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTransfusionRequest = false">取消</el-button>
        <el-button type="primary" @click="submitTransfusionRequest">提交申请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { ElMessage } from 'element-plus'
import { 
  User, Document, Box, Warning, Plus, TrendCharts, Search, 
  ArrowDown, Refresh, Download 
} from '@element-plus/icons-vue'
import dataService from '../services/dataService'

const router = useRouter()
const authStore = useAuthStore()

// Get current user
const user = authStore.user

// Reactive data
const loading = ref(false)
const loadingPatients = ref(false)
const loadingInventory = ref(false)
const showAddPatient = ref(false)
const showTransfusionRequest = ref(false)

// Search and filter
const patientSearch = ref('')
const requestFilter = ref('')

// Pagination
const patientPagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// Analytics period
const analyticsPeriod = ref([])

// Doctor statistics
const doctorStats = reactive({
  totalPatients: 0,
  pendingRequests: 0,
  todayTransfusions: 0,
  criticalAlerts: 0
})

// Personal analytics
const personalAnalytics = reactive({
  totalPatients: 0,
  totalRequests: 0,
  completedTransfusions: 0,
  efficiency: 0
})

// Chart data
const monthlyTrends = ref([65, 80, 45, 90, 75, 85])
const chartMonths = ref(['1月', '2月', '3月', '4月', '5月', '6月'])
const bloodTypeDistribution = ref([
  { type: 'A+', percentage: 35 },
  { type: 'B+', percentage: 25 },
  { type: 'O+', percentage: 30 },
  { type: 'AB+', percentage: 10 }
])

// Recent data
const recentPatients = ref([])
const recentRequests = ref([])
const recentActivities = ref([])
const bloodInventory = ref([])

// Computed properties
const filteredPatients = computed(() => {
  let filtered = recentPatients.value
  if (patientSearch.value) {
    filtered = filtered.filter(patient => 
      patient.name.toLowerCase().includes(patientSearch.value.toLowerCase()) ||
      patient.bloodType.toLowerCase().includes(patientSearch.value.toLowerCase())
    )
  }
  return filtered
})

const filteredRequests = computed(() => {
  let filtered = recentRequests.value
  if (requestFilter.value) {
    filtered = filtered.filter(request => request.status === requestFilter.value)
  }
  return filtered
})

const totalInventory = computed(() => {
  return bloodInventory.value.reduce((total, type) => total + type.amount, 0)
})

const lowStockTypes = computed(() => {
  return bloodInventory.value.filter(type => type.percentage < 30)
})

// New patient form
const newPatient = reactive({
  name: '',
  bloodType: '',
  age: 0,
  condition: '',
  allergies: ''
})

// Patient form rules
const patientRules = {
  name: [
    { required: true, message: '请输入患者姓名', trigger: 'blur' }
  ],
  bloodType: [
    { required: true, message: '请选择血型', trigger: 'change' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' }
  ],
  condition: [
    { required: true, message: '请输入病情描述', trigger: 'blur' }
  ]
}

// Transfusion request form
const transfusionRequest = reactive({
  patientName: '',
  bloodType: '',
  amount: 400,
  urgency: '常规',
  reason: ''
})

// Request form rules
const requestRules = {
  amount: [
    { required: true, message: '请输入输血量', trigger: 'blur' }
  ],
  urgency: [
    { required: true, message: '请选择紧急程度', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入输血原因', trigger: 'blur' }
  ]
}

// Load dashboard data
const loadDashboardData = async () => {
  loading.value = true
  try {
    // Get doctor-specific data
    const data = dataService.getDoctorDashboardData()
    
    // Update stats
    doctorStats.totalPatients = data.stats.totalPatients
    doctorStats.pendingRequests = data.stats.pendingRequests
    doctorStats.todayTransfusions = data.stats.todayTransfusions
    doctorStats.criticalAlerts = data.stats.criticalAlerts
    
    // Update personal analytics
    personalAnalytics.totalPatients = data.stats.totalPatients
    personalAnalytics.totalRequests = data.stats.totalPatients + Math.floor(Math.random() * 10)
    personalAnalytics.completedTransfusions = data.stats.todayTransfusions * 30
    personalAnalytics.efficiency = Math.floor(Math.random() * 20) + 80
    
    // Update recent data
    recentPatients.value = data.recentPatients.map(patient => ({
      ...patient,
      age: Math.floor(Math.random() * 60) + 20,
      condition: ['稳定', '恢复中', '需要观察', '危重'][Math.floor(Math.random() * 4)]
    }))
    recentRequests.value = data.recentRequests.map(request => ({
      ...request,
      reason: request.reason || '患者需要输血治疗'
    }))
    
    // Update inventory
    const inventoryStatus = dataService.getInventoryStatus()
    bloodInventory.value = inventoryStatus.map(inv => ({
      type: inv.bloodType,
      amount: inv.amount,
      percentage: (inv.amount / inv.capacity) * 100
    }))
    
    // Update pagination
    patientPagination.total = recentPatients.value.length
    
    // Generate recent activities
    recentActivities.value = [
      {
        id: 1,
        type: 'patient',
        title: '新增患者',
        description: '添加患者张三到管理系统',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      },
      {
        id: 2,
        type: 'request',
        title: '提交输血申请',
        description: '为患者李四申请400ml O型血',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000)
      },
      {
        id: 3,
        type: 'transfusion',
        title: '完成输血',
        description: '患者王五输血治疗完成',
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000)
      },
      {
        id: 4,
        type: 'system',
        title: '系统更新',
        description: '输血协议已更新',
        timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000)
      }
    ]
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// Add missing methods
const createTransfusionRequest = (patient) => {
  transfusionRequest.patientName = patient.name
  transfusionRequest.bloodType = patient.bloodType
  showTransfusionRequest.value = true
}

// Helper functions
const getBloodTypeColor = (bloodType) => {
  const colors = {
    'A+': 'success',
    'A-': 'info',
    'B+': 'warning',
    'B-': 'info',
    'O+': 'danger',
    'O-': 'info',
    'AB+': 'primary',
    'AB-': 'info'
  }
  return colors[bloodType] || 'info'
}

const getConditionColor = (condition) => {
  const colors = {
    '稳定': 'success',
    '恢复中': 'warning',
    '需要观察': 'info',
    '危重': 'danger'
  }
  return colors[condition] || 'info'
}

const getStatusColor = (status) => {
  const colors = {
    'stable': 'success',
    'critical': 'danger',
    'recovering': 'warning',
    'observation': 'info',
    'discharged': 'info'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'stable': '稳定',
    'critical': '危重',
    'recovering': '恢复中',
    'observation': '需要观察',
    'discharged': '已出院'
  }
  return texts[status] || status
}

const getRequestStatusColor = (status) => {
  const colors = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'completed': 'info'
  }
  return colors[status] || 'info'
}

const getRequestStatusText = (status) => {
  const texts = {
    'pending': '待审核',
    'approved': '已批准',
    'rejected': '已拒绝',
    'completed': '已完成'
  }
  return texts[status] || status
}

const getUrgencyColor = (urgency) => {
  const colors = {
    '常规': 'info',
    '紧急': 'warning',
    '非常紧急': 'danger'
  }
  return colors[urgency] || 'info'
}

const getStockStatusClass = (percentage) => {
  if (percentage < 30) return 'low-stock'
  if (percentage < 60) return 'medium-stock'
  return 'good-stock'
}

const getStockStatusText = (percentage) => {
  if (percentage < 30) return '库存不足'
  if (percentage < 60) return '库存偏低'
  return '库存充足'
}

const getActivityTypeClass = (type) => {
  const classes = {
    'patient': 'activity-patient',
    'request': 'activity-request',
    'transfusion': 'activity-transfusion',
    'system': 'activity-system'
  }
  return classes[type] || 'activity-default'
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

// Action handlers
const filterPatients = () => {
  // Filter logic handled by computed property
}

const handlePatientSizeChange = (size) => {
  patientPagination.size = size
  loadDashboardData()
}

const handlePatientPageChange = (page) => {
  patientPagination.current = page
  loadDashboardData()
}

const viewPatientDetails = (patient) => {
  ElMessage.info(`查看患者详情: ${patient.name}`)
}

const editPatient = (patient) => {
  ElMessage.info(`编辑患者信息: ${patient.name}`)
}

const viewPatientHistory = (patient) => {
  ElMessage.info(`查看输血历史: ${patient.name}`)
}

const generatePatientReport = (patient) => {
  ElMessage.info(`生成患者报告: ${patient.name}`)
}

const viewRequestDetails = (request) => {
  ElMessage.info(`查看申请详情: ${request.id}`)
}

const editRequest = (request) => {
  ElMessage.info(`编辑申请: ${request.id}`)
}

const confirmTransfusion = (request) => {
  ElMessage.success(`确认输血: ${request.id}`)
  request.status = 'completed'
}

const refreshInventory = async () => {
  loadingInventory.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('库存数据已刷新')
    loadDashboardData()
  } finally {
    loadingInventory.value = false
  }
}

const requestBloodSupply = () => {
  ElMessage.info('申请血液供应')
}

const viewInventoryHistory = () => {
  ElMessage.info('查看库存历史')
}

const updateAnalytics = () => {
  ElMessage.info('更新分析数据')
  loadDashboardData()
}

const exportAnalytics = () => {
  ElMessage.success('导出分析报告')
}

const viewAllRequests = () => {
  ElMessage.info('查看全部申请')
}

const addPatient = async () => {
  try {
    // Add patient logic here
    ElMessage.success('患者添加成功')
    showAddPatient.value = false
    // Reset form
    Object.assign(newPatient, {
      name: '',
      bloodType: '',
      age: 0,
      condition: '',
      allergies: ''
    })
    // Reload data
    loadDashboardData()
  } catch (error) {
    ElMessage.error('添加患者失败')
  }
}

const submitTransfusionRequest = async () => {
  try {
    // Submit request logic here
    ElMessage.success('输血申请提交成功')
    showTransfusionRequest.value = false
    // Reload data
    loadDashboardData()
  } catch (error) {
    ElMessage.error('提交申请失败')
  }
}

// Load data on mount
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.doctor-dashboard {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* Header Styles */
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
  font-weight: 600;
}

.welcome-subtitle {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-details {
  text-align: right;
}

.user-name {
  display: block;
  font-weight: 600;
  color: #333;
}

.user-role {
  display: block;
  font-size: 14px;
  color: #666;
}

/* Stats Grid */
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
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon.patients { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.requests { background: linear-gradient(135deg, #f093fb, #f5576c); }
.stat-icon.transfusions { background: linear-gradient(135deg, #4facfe, #00f2fe); }
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

/* Content Grid */
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

/* Patient Management */
.patient-management {
  max-height: 400px;
  overflow-y: auto;
}

/* Requests List */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.request-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e9ecef;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.request-patient {
  font-weight: 600;
  color: #333;
}

.request-details {
  display: flex;
  gap: 20px;
  margin-bottom: 12px;
}

.request-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #666;
}

.info-value {
  font-size: 14px;
  color: #333;
}

.request-actions {
  display: flex;
  gap: 8px;
}

/* Inventory Status */
.inventory-status {
  padding: 20px 0;
}

.blood-types {
  display: flex;
  flex-direction: column;
  gap: 12px;
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

.type-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.bar-fill.low-stock {
  background: linear-gradient(90deg, #f5576c, #f093fb);
}

/* Guidelines List */
.guidelines-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.guideline-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.guideline-icon {
  color: #667eea;
  flex-shrink: 0;
}

.guideline-content {
  flex: 1;
}

.guideline-title {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.guideline-summary {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.guideline-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.guideline-date {
  font-size: 12px;
  color: #999;
}

/* Enhanced Header Styles */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Enhanced Patient Management */
.patient-management {
  max-height: 500px;
  overflow-y: auto;
}

.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

/* Enhanced Request Management */
.requests-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 500px;
  overflow-y: auto;
}

.request-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.request-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.request-patient {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #333;
  font-size: 16px;
}

.request-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}

.request-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: #333;
  font-weight: 600;
}

.request-reason {
  background: white;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #555;
  border-left: 4px solid #667eea;
}

.request-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* Enhanced Inventory Status */
.inventory-status {
  padding: 24px 0;
}

.inventory-summary {
  display: flex;
  gap: 32px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-label {
  font-size: 14px;
  color: #666;
}

.summary-value {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.summary-value.low-stock {
  color: #f56c6c;
}

.blood-types {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.blood-type {
  background: white;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.type-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.type-label {
  font-weight: 600;
  color: #333;
  font-size: 16px;
}

.type-amount {
  font-weight: 600;
  color: #667eea;
}

.type-bar {
  height: 12px;
  background: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 6px;
  transition: width 0.3s ease;
}

.bar-fill.low-stock {
  background: linear-gradient(90deg, #f56c6c, #f78989);
}

.bar-fill.medium-stock {
  background: linear-gradient(90deg, #e6a23c, #ebb563);
}

.type-status {
  text-align: right;
}

.status-text {
  font-size: 12px;
  font-weight: 500;
}

.status-text.low-stock {
  color: #f56c6c;
}

.status-text.medium-stock {
  color: #e6a23c;
}

.status-text.good-stock {
  color: #67c23a;
}

.inventory-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

/* Enhanced Personal Analytics */
.analytics-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.analytics-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.summary-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
}

.summary-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.summary-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.summary-icon.patients { background: linear-gradient(135deg, #667eea, #764ba2); }
.summary-icon.requests { background: linear-gradient(135deg, #f093fb, #f5576c); }
.summary-icon.transfusions { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.summary-icon.efficiency { background: linear-gradient(135deg, #fa709a, #fee140); }

.summary-number {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.summary-label {
  color: #666;
  font-size: 14px;
  margin-top: 4px;
}

.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.chart-container {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.chart-container h4 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px 0;
}

.mock-chart {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 160px;
  width: 100%;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  transition: height 0.3s ease;
}

.chart-labels {
  display: flex;
  justify-content: space-around;
  margin-top: 12px;
  font-size: 12px;
  color: #666;
}

.blood-type-chart {
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
  font-size: 14px;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.type-percentage {
  color: #666;
}

.recent-activities {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.recent-activities h4 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.timeline-item {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.timeline-item:last-child {
  border-bottom: none;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 6px;
}

.timeline-dot.activity-patient { background: #667eea; }
.timeline-dot.activity-request { background: #f093fb; }
.timeline-dot.activity-transfusion { background: #4facfe; }
.timeline-dot.activity-system { background: #fa709a; }
.timeline-dot.activity-default { background: #909399; }

.timeline-content {
  flex: 1;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.activity-title {
  font-weight: 600;
  color: #333;
}

.activity-time {
  font-size: 12px;
  color: #666;
}

.activity-description {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .user-info {
    flex-direction: column;
    text-align: center;
  }
  
  .user-details {
    text-align: center;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .analytics-summary {
    grid-template-columns: 1fr;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .request-details {
    grid-template-columns: 1fr;
  }
  
  .inventory-summary {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
