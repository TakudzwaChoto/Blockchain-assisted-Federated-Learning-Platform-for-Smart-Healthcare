<template>
  <div class="transfusion-requests">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">输血申请管理</h1>
          <p class="page-subtitle">管理和处理输血申请请求</p>
        </div>
        <div class="header-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索申请..."
            prefix-icon="Search"
            style="width: 300px; margin-right: 16px"
            @input="handleSearch"
          />
          <el-select v-model="statusFilter" placeholder="筛选状态" style="width: 120px; margin-right: 16px">
            <el-option label="全部" value="" />
            <el-option label="待审核" value="pending" />
            <el-option label="已批准" value="approved" />
            <el-option label="已完成" value="completed" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
          <el-select v-model="urgencyFilter" placeholder="紧急程度" style="width: 120px; margin-right: 16px">
            <el-option label="全部" value="" />
            <el-option label="常规" value="常规" />
            <el-option label="紧急" value="紧急" />
            <el-option label="非常紧急" value="非常紧急" />
          </el-select>
          <el-button type="primary" @click="showNewRequest = true">
            <el-icon><Plus /></el-icon>
            新建申请
          </el-button>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon total">
            <el-icon size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.total }}</div>
            <div class="stat-label">总申请数</div>
          </div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon pending">
            <el-icon size="32"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.pending }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon approved">
            <el-icon size="32"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.approved }}</div>
            <div class="stat-label">已批准</div>
          </div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon completed">
            <el-icon size="32"><Box /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.completed }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Requests Table -->
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <h3>申请列表</h3>
          <div class="table-actions">
            <el-button @click="exportRequests">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
            <el-button @click="refreshData" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="filteredRequests" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="申请编号" width="100" />
        <el-table-column prop="patientName" label="患者姓名" width="120" />
        <el-table-column prop="patientId" label="患者ID" width="120" />
        <el-table-column prop="bloodType" label="血型" width="80">
          <template #default="{ row }">
            <el-tag :type="getBloodTypeColor(row.bloodType)" size="small">
              {{ row.bloodType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="申请量(ml)" width="120" sortable />
        <el-table-column prop="urgency" label="紧急程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getUrgencyColor(row.urgency)" size="small">
              {{ row.urgency }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="requestDate" label="申请日期" width="120" sortable>
          <template #default="{ row }">
            {{ formatDate(row.requestDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="requestedBy" label="申请医生" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="expectedDate" label="期望日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.expectedDate) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewRequest(row)">查看</el-button>
            <el-button 
              v-if="row.status === 'pending'" 
              size="small" 
              type="success" 
              @click="approveRequest(row)"
            >
              批准
            </el-button>
            <el-button 
              v-if="row.status === 'pending'" 
              size="small" 
              type="danger" 
              @click="rejectRequest(row)"
            >
              拒绝
            </el-button>
            <el-dropdown trigger="click">
              <el-button size="small" type="info">
                更多<el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editRequest(row)">编辑申请</el-dropdown-item>
                  <el-dropdown-item @click="printRequest(row)">打印申请</el-dropdown-item>
                  <el-dropdown-item @click="viewHistory(row)">查看历史</el-dropdown-item>
                  <el-dropdown-item 
                    v-if="row.status === 'approved'" 
                    @click="confirmTransfusion(row)"
                  >
                    确认输血
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="deleteRequest(row)" class="text-danger">
                    删除申请
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- New Request Dialog -->
    <el-dialog v-model="showNewRequest" title="新建输血申请" width="700px">
      <el-form :model="newRequest" :rules="requestRules" ref="requestForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="患者姓名" prop="patientName">
              <el-input v-model="newRequest.patientName" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="患者ID" prop="patientId">
              <el-input v-model="newRequest.patientId" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="血型" prop="bloodType">
              <el-select v-model="newRequest.bloodType" style="width: 100%">
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
          </el-col>
          <el-col :span="12">
            <el-form-item label="申请量(ml)" prop="amount">
              <el-input-number v-model="newRequest.amount" :min="100" :max="2000" :step="100" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="紧急程度" prop="urgency">
              <el-select v-model="newRequest.urgency" style="width: 100%">
                <el-option label="常规" value="常规" />
                <el-option label="紧急" value="紧急" />
                <el-option label="非常紧急" value="非常紧急" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="期望日期" prop="expectedDate">
              <el-date-picker
                v-model="newRequest.expectedDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="输血原因" prop="reason">
          <el-input v-model="newRequest.reason" type="textarea" rows="4" />
        </el-form-item>
        <el-form-item label="备注信息">
          <el-input v-model="newRequest.notes" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showNewRequest = false">取消</el-button>
        <el-button type="primary" @click="submitRequest">提交申请</el-button>
      </template>
    </el-dialog>

    <!-- Request Details Dialog -->
    <el-dialog v-model="showRequestDetails" title="申请详情" width="800px">
      <div class="request-details" v-if="selectedRequest">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="申请编号">{{ selectedRequest.id }}</el-descriptions-item>
          <el-descriptions-item label="患者姓名">{{ selectedRequest.patientName }}</el-descriptions-item>
          <el-descriptions-item label="患者ID">{{ selectedRequest.patientId }}</el-descriptions-item>
          <el-descriptions-item label="血型">
            <el-tag :type="getBloodTypeColor(selectedRequest.bloodType)">
              {{ selectedRequest.bloodType }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="申请量">{{ selectedRequest.amount }}ml</el-descriptions-item>
          <el-descriptions-item label="紧急程度">
            <el-tag :type="getUrgencyColor(selectedRequest.urgency)">
              {{ selectedRequest.urgency }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="申请日期">{{ formatDate(selectedRequest.requestDate) }}</el-descriptions-item>
          <el-descriptions-item label="期望日期">{{ formatDate(selectedRequest.expectedDate) }}</el-descriptions-item>
          <el-descriptions-item label="申请医生">{{ selectedRequest.requestedBy }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusColor(selectedRequest.status)">
              {{ getStatusText(selectedRequest.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="输血原因" :span="2">{{ selectedRequest.reason }}</el-descriptions-item>
          <el-descriptions-item label="备注信息" :span="2">{{ selectedRequest.notes || '-' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- Approval History -->
        <div class="approval-history" v-if="selectedRequest.approvalHistory">
          <h4>审批历史</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in selectedRequest.approvalHistory"
              :key="index"
              :timestamp="formatDateTime(item.timestamp)"
              :type="getTimelineType(item.action)"
            >
              <div class="timeline-content">
                <strong>{{ item.action }}</strong>
                <p>{{ item.comment }}</p>
                <span>操作人: {{ item.operator }}</span>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
      <template #footer>
        <el-button @click="showRequestDetails = false">关闭</el-button>
        <el-button 
          v-if="selectedRequest?.status === 'pending'" 
          type="success" 
          @click="approveRequest(selectedRequest)"
        >
          批准
        </el-button>
        <el-button 
          v-if="selectedRequest?.status === 'pending'" 
          type="danger" 
          @click="rejectRequest(selectedRequest)"
        >
          拒绝
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Document, Plus, Search, Download, Refresh, Check, Clock, 
  Box, ArrowDown 
} from '@element-plus/icons-vue'
import dataService from '../services/dataService'

// Reactive data
const loading = ref(false)
const showNewRequest = ref(false)
const showRequestDetails = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const urgencyFilter = ref('')
const selectedRequest = ref(null)

// Statistics
const requestStats = reactive({
  total: 0,
  pending: 0,
  approved: 0,
  completed: 0
})

// Pagination
const pagination = reactive({
  current: 1,
  size: 20,
  total: 0
})

// Requests data
const requests = ref([])

// New request form
const newRequest = reactive({
  patientName: '',
  patientId: '',
  bloodType: '',
  amount: 400,
  urgency: '常规',
  expectedDate: '',
  reason: '',
  notes: ''
})

// Form rules
const requestRules = {
  patientName: [
    { required: true, message: '请输入患者姓名', trigger: 'blur' }
  ],
  patientId: [
    { required: true, message: '请输入患者ID', trigger: 'blur' }
  ],
  bloodType: [
    { required: true, message: '请选择血型', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入申请量', trigger: 'blur' }
  ],
  urgency: [
    { required: true, message: '请选择紧急程度', trigger: 'change' }
  ],
  expectedDate: [
    { required: true, message: '请选择期望日期', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入输血原因', trigger: 'blur' }
  ]
}

// Computed properties
const filteredRequests = computed(() => {
  let filtered = requests.value
  
  if (searchQuery.value) {
    filtered = filtered.filter(request => 
      request.patientName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      request.patientId.includes(searchQuery.value) ||
      request.id.includes(searchQuery.value)
    )
  }
  
  if (statusFilter.value) {
    filtered = filtered.filter(request => request.status === statusFilter.value)
  }
  
  if (urgencyFilter.value) {
    filtered = filtered.filter(request => request.urgency === urgencyFilter.value)
  }
  
  return filtered
})

// Methods
const loadRequests = async () => {
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock data
    requests.value = [
      {
        id: 'REQ001',
        patientName: '张三',
        patientId: 'P001',
        bloodType: 'A+',
        amount: 400,
        urgency: '紧急',
        requestDate: new Date('2024-01-20'),
        expectedDate: new Date('2024-01-22'),
        requestedBy: '李医生',
        status: 'pending',
        reason: '患者手术需要输血',
        notes: '患者血红蛋白偏低，需要紧急输血',
        approvalHistory: [
          {
            action: '申请提交',
            timestamp: new Date('2024-01-20 09:00'),
            operator: '李医生',
            comment: '患者手术需要输血'
          }
        ]
      },
      {
        id: 'REQ002',
        patientName: '李四',
        patientId: 'P002',
        bloodType: 'O+',
        amount: 300,
        urgency: '常规',
        requestDate: new Date('2024-01-19'),
        expectedDate: new Date('2024-01-25'),
        requestedBy: '王医生',
        status: 'approved',
        reason: '贫血治疗',
        notes: '慢性贫血，定期输血治疗',
        approvalHistory: [
          {
            action: '申请提交',
            timestamp: new Date('2024-01-19 14:00'),
            operator: '王医生',
            comment: '贫血治疗'
          },
          {
            action: '申请批准',
            timestamp: new Date('2024-01-20 10:00'),
            operator: '血库管理员',
            comment: '库存充足，批准申请'
          }
        ]
      },
      {
        id: 'REQ003',
        patientName: '王五',
        patientId: 'P003',
        bloodType: 'B+',
        amount: 500,
        urgency: '非常紧急',
        requestDate: new Date('2024-01-21'),
        expectedDate: new Date('2024-01-21'),
        requestedBy: '张医生',
        status: 'completed',
        reason: '急诊手术',
        notes: '外伤导致大出血，急需输血',
        approvalHistory: [
          {
            action: '申请提交',
            timestamp: new Date('2024-01-21 08:00'),
            operator: '张医生',
            comment: '急诊手术'
          },
          {
            action: '申请批准',
            timestamp: new Date('2024-01-21 08:30'),
            operator: '血库管理员',
            comment: '紧急情况，立即批准'
          },
          {
            action: '输血完成',
            timestamp: new Date('2024-01-21 12:00'),
            operator: '护士长',
            comment: '输血完成，患者情况稳定'
          }
        ]
      }
    ]
    
    // Update stats
    requestStats.total = requests.value.length
    requestStats.pending = requests.value.filter(r => r.status === 'pending').length
    requestStats.approved = requests.value.filter(r => r.status === 'approved').length
    requestStats.completed = requests.value.filter(r => r.status === 'completed').length
    
    // Update pagination
    pagination.total = requests.value.length
    
  } catch (error) {
    ElMessage.error('加载申请数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // Search logic handled by computed property
}

const handleSizeChange = (size) => {
  pagination.size = size
  loadRequests()
}

const handlePageChange = (page) => {
  pagination.current = page
  loadRequests()
}

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

const getUrgencyColor = (urgency) => {
  const colors = {
    '常规': 'info',
    '紧急': 'warning',
    '非常紧急': 'danger'
  }
  return colors[urgency] || 'info'
}

const getStatusColor = (status) => {
  const colors = {
    'pending': 'warning',
    'approved': 'success',
    'completed': 'info',
    'rejected': 'danger'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'pending': '待审核',
    'approved': '已批准',
    'completed': '已完成',
    'rejected': '已拒绝'
  }
  return texts[status] || status
}

const getTimelineType = (action) => {
  const types = {
    '申请提交': 'primary',
    '申请批准': 'success',
    '申请拒绝': 'danger',
    '输血完成': 'success'
  }
  return types[action] || 'info'
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const viewRequest = (request) => {
  selectedRequest.value = request
  showRequestDetails.value = true
}

const approveRequest = async (request) => {
  try {
    await ElMessageBox.confirm(
      `确定要批准申请 ${request.id} 吗？`,
      '确认批准',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    request.status = 'approved'
    if (!request.approvalHistory) {
      request.approvalHistory = []
    }
    request.approvalHistory.push({
      action: '申请批准',
      timestamp: new Date(),
      operator: '当前用户',
      comment: '申请已批准'
    })
    
    ElMessage.success('申请批准成功')
    loadRequests()
  } catch (error) {
    // User cancelled
  }
}

const rejectRequest = async (request) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      '请输入拒绝理由',
      '拒绝申请',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /.+/,
        inputErrorMessage: '请输入拒绝理由'
      }
    )
    
    request.status = 'rejected'
    if (!request.approvalHistory) {
      request.approvalHistory = []
    }
    request.approvalHistory.push({
      action: '申请拒绝',
      timestamp: new Date(),
      operator: '当前用户',
      comment: reason
    })
    
    ElMessage.success('申请已拒绝')
    loadRequests()
  } catch (error) {
    // User cancelled
  }
}

const confirmTransfusion = (request) => {
  request.status = 'completed'
  if (!request.approvalHistory) {
    request.approvalHistory = []
  }
  request.approvalHistory.push({
    action: '输血完成',
    timestamp: new Date(),
    operator: '当前用户',
    comment: '输血已完成'
  })
  
  ElMessage.success('输血确认成功')
  loadRequests()
}

const editRequest = (request) => {
  ElMessage.info(`编辑申请: ${request.id}`)
}

const printRequest = (request) => {
  ElMessage.info(`打印申请: ${request.id}`)
}

const viewHistory = (request) => {
  ElMessage.info(`查看历史: ${request.id}`)
}

const deleteRequest = async (request) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除申请 ${request.id} 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    ElMessage.success('申请删除成功')
    loadRequests()
  } catch (error) {
    // User cancelled
  }
}

const submitRequest = async () => {
  try {
    // Submit request logic here
    ElMessage.success('申请提交成功')
    showNewRequest.value = false
    // Reset form
    Object.assign(newRequest, {
      patientName: '',
      patientId: '',
      bloodType: '',
      amount: 400,
      urgency: '常规',
      expectedDate: '',
      reason: '',
      notes: ''
    })
    loadRequests()
  } catch (error) {
    ElMessage.error('提交申请失败')
  }
}

const exportRequests = () => {
  ElMessage.success('导出申请数据')
}

const refreshData = () => {
  loadRequests()
}

// Load data on mount
onMounted(() => {
  loadRequests()
})
</script>

<style scoped>
.transfusion-requests {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* Header Styles */
.page-header {
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

.title-section h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.title-section p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.header-actions {
  display: flex;
  align-items: center;
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

.stat-icon.total { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.pending { background: linear-gradient(135deg, #e6a23c, #ebb563); }
.stat-icon.approved { background: linear-gradient(135deg, #67c23a, #85ce61); }
.stat-icon.completed { background: linear-gradient(135deg, #409eff, #66b1ff); }

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

/* Main Card */
.main-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
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

.table-actions {
  display: flex;
  gap: 12px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* Dialog Styles */
.request-details {
  max-height: 600px;
  overflow-y: auto;
}

.approval-history {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.approval-history h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.timeline-content strong {
  display: block;
  margin-bottom: 4px;
}

.timeline-content p {
  margin: 4px 0;
  color: #666;
}

.timeline-content span {
  font-size: 12px;
  color: #999;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
