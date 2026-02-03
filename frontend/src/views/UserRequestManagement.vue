<template>
  <div class="user-request-management">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1>输血申请管理</h1>
          <p>管理您的输血申请</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="showAddRequestDialog = true">
            <el-icon><Plus /></el-icon>
            新建申请
          </el-button>
          <el-button @click="exportRequests">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon total">
            <el-icon size="24"><Document /></el-icon>
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
            <el-icon size="24"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.pending }}</div>
            <div class="stat-label">待处理</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon approved">
            <el-icon size="24"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.approved }}</div>
            <div class="stat-label">已批准</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon urgent">
            <el-icon size="24"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ requestStats.urgent }}</div>
            <div class="stat-label">紧急申请</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Search and Filters -->
    <el-card class="filter-card">
      <div class="filter-section">
        <div class="filter-row">
          <el-input
            v-model="searchQuery"
            placeholder="搜索患者姓名或申请编号"
            prefix-icon="Search"
            style="width: 300px"
            @input="handleSearch"
          />
          
          <el-select v-model="bloodTypeFilter" placeholder="筛选血型" style="width: 120px" @change="handleFilter">
            <el-option label="全部血型" value="" />
            <el-option label="A+" value="A+" />
            <el-option label="B+" value="B+" />
            <el-option label="O+" value="O+" />
            <el-option label="AB+" value="AB+" />
          </el-select>

          <el-select v-model="urgencyFilter" placeholder="筛选紧急程度" style="width: 120px" @change="handleFilter">
            <el-option label="全部程度" value="" />
            <el-option label="常规" value="normal" />
            <el-option label="紧急" value="urgent" />
            <el-option label="非常紧急" value="critical" />
          </el-select>

          <el-select v-model="statusFilter" placeholder="筛选状态" style="width: 120px" @change="handleFilter">
            <el-option label="全部状态" value="" />
            <el-option label="待处理" value="pending" />
            <el-option label="已批准" value="approved" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="已完成" value="completed" />
          </el-select>

          <el-button @click="resetFilters">重置筛选</el-button>
        </div>
      </div>
    </el-card>

    <!-- Requests Table -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <h3>申请列表</h3>
          <div class="table-info">
            <span>共 {{ filteredRequests.length }} 个申请</span>
          </div>
        </div>
      </template>

      <el-table 
        :data="paginatedRequests" 
        style="width: 100%" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="申请信息" min-width="200">
          <template #default="{ row }">
            <div class="request-info">
              <div class="request-id">{{ row.id }}</div>
              <div class="request-date">{{ formatDate(row.createdAt) }}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="患者信息" min-width="150">
          <template #default="{ row }">
            <div class="patient-info">
              <div class="patient-name">{{ row.patientName }}</div>
              <div class="patient-age">{{ row.patientAge }}岁</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="血型" width="80">
          <template #default="{ row }">
            <el-tag :type="getBloodTypeColor(row.bloodType)" size="small">
              {{ row.bloodType }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="需求量" width="100">
          <template #default="{ row }">
            <span class="amount">{{ row.amount }}ml</span>
          </template>
        </el-table-column>

        <el-table-column label="紧急程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getUrgencyColor(row.urgency)" size="small">
              {{ getUrgencyText(row.urgency) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="申请医生" width="100">
          <template #default="{ row }">
            {{ row.doctorName }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewRequest(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editRequest(row)" v-if="row.status === 'pending'">编辑</el-button>
            <el-button size="small" type="success" @click="processRequest(row)" v-if="row.status === 'approved'">处理</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="filteredRequests.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Add/Edit Request Dialog -->
    <el-dialog 
      v-model="showAddRequestDialog" 
      :title="editingRequest ? '编辑申请' : '新建输血申请'" 
      width="600px"
    >
      <el-form :model="requestForm" :rules="requestFormRules" ref="requestFormRef" label-width="100px">
        <el-form-item label="患者姓名" prop="patientName">
          <el-input v-model="requestForm.patientName" placeholder="请输入患者姓名" />
        </el-form-item>

        <el-form-item label="患者年龄" prop="patientAge">
          <el-input-number 
            v-model="requestForm.patientAge" 
            :min="0" 
            :max="150" 
            controls-position="right"
          />
        </el-form-item>

        <el-form-item label="血型" prop="bloodType">
          <el-select v-model="requestForm.bloodType" style="width: 100%">
            <el-option label="A+" value="A+" />
            <el-option label="B+" value="B+" />
            <el-option label="O+" value="O+" />
            <el-option label="AB+" value="AB+" />
          </el-select>
        </el-form-item>

        <el-form-item label="需求量" prop="amount">
          <el-input-number 
            v-model="requestForm.amount" 
            :min="100" 
            :max="2000" 
            :step="50"
            controls-position="right"
          />
          <span style="margin-left: 8px">ml</span>
        </el-form-item>

        <el-form-item label="紧急程度" prop="urgency">
          <el-select v-model="requestForm.urgency" style="width: 100%">
            <el-option label="常规" value="normal" />
            <el-option label="紧急" value="urgent" />
            <el-option label="非常紧急" value="critical" />
          </el-select>
        </el-form-item>

        <el-form-item label="诊断" prop="diagnosis">
          <el-input v-model="requestForm.diagnosis" placeholder="请输入诊断信息" />
        </el-form-item>

        <el-form-item label="手术类型" prop="surgeryType">
          <el-input v-model="requestForm.surgeryType" placeholder="请输入手术类型" />
        </el-form-item>

        <el-form-item label="备注" prop="notes">
          <el-input v-model="requestForm.notes" type="textarea" :rows="3" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAddRequestDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRequest" :loading="saving">
          {{ editingRequest ? '更新' : '提交申请' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Request Details Dialog -->
    <el-dialog v-model="showRequestDetailsDialog" title="申请详情" width="700px">
      <div class="request-details-content" v-if="selectedRequest">
        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <label>申请编号:</label>
              <span>{{ selectedRequest.id }}</span>
            </div>
            <div class="detail-item">
              <label>申请时间:</label>
              <span>{{ formatDateTime(selectedRequest.createdAt) }}</span>
            </div>
            <div class="detail-item">
              <label>患者姓名:</label>
              <span>{{ selectedRequest.patientName }}</span>
            </div>
            <div class="detail-item">
              <label>患者年龄:</label>
              <span>{{ selectedRequest.patientAge }}岁</span>
            </div>
            <div class="detail-item">
              <label>血型:</label>
              <el-tag :type="getBloodTypeColor(selectedRequest.bloodType)">
                {{ selectedRequest.bloodType }}
              </el-tag>
            </div>
            <div class="detail-item">
              <label>需求量:</label>
              <span>{{ selectedRequest.amount }}ml</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>医疗信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <label>诊断:</label>
              <span>{{ selectedRequest.diagnosis }}</span>
            </div>
            <div class="detail-item">
              <label>手术类型:</label>
              <span>{{ selectedRequest.surgeryType }}</span>
            </div>
            <div class="detail-item">
              <label>紧急程度:</label>
              <el-tag :type="getUrgencyColor(selectedRequest.urgency)">
                {{ getUrgencyText(selectedRequest.urgency) }}
              </el-tag>
            </div>
            <div class="detail-item">
              <label>申请医生:</label>
              <span>{{ selectedRequest.doctorName }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>处理状态</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <label>当前状态:</label>
              <el-tag :type="getStatusColor(selectedRequest.status)">
                {{ getStatusText(selectedRequest.status) }}
              </el-tag>
            </div>
            <div class="detail-item" v-if="selectedRequest.processedAt">
              <label>处理时间:</label>
              <span>{{ formatDateTime(selectedRequest.processedAt) }}</span>
            </div>
            <div class="detail-item" v-if="selectedRequest.processedBy">
              <label>处理人员:</label>
              <span>{{ selectedRequest.processedBy }}</span>
            </div>
            <div class="detail-item">
              <label>备注:</label>
              <span>{{ selectedRequest.notes || '无' }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Plus, Download, Search, Document, Clock, Check, Warning
} from '@element-plus/icons-vue'

const loading = ref(false)
const saving = ref(false)
const showAddRequestDialog = ref(false)
const showRequestDetailsDialog = ref(false)
const editingRequest = ref(null)
const selectedRequest = ref(null)
const requestFormRef = ref()

// Filters
const searchQuery = ref('')
const bloodTypeFilter = ref('')
const urgencyFilter = ref('')
const statusFilter = ref('')

// Pagination
const currentPage = ref(1)
const pageSize = ref(20)
const selectedRequests = ref([])

// Statistics
const requestStats = reactive({
  total: 0,
  pending: 0,
  approved: 0,
  urgent: 0
})

// Mock requests data
const requests = ref([
  {
    id: 'REQ-2024-001',
    patientName: '张三',
    patientAge: 45,
    bloodType: 'A+',
    amount: 400,
    urgency: 'urgent',
    status: 'pending',
    diagnosis: '胃出血',
    surgeryType: '急诊手术',
    doctorName: '李医生',
    notes: '患者情况紧急，需要尽快输血',
    createdAt: new Date('2024-06-20T10:30:00'),
    processedAt: null,
    processedBy: null
  },
  {
    id: 'REQ-2024-002',
    patientName: '李四',
    patientAge: 32,
    bloodType: 'O+',
    amount: 300,
    urgency: 'normal',
    status: 'approved',
    diagnosis: '贫血',
    surgeryType: '择期手术',
    doctorName: '王医生',
    notes: '择期手术，可提前准备',
    createdAt: new Date('2024-06-19T14:20:00'),
    processedAt: new Date('2024-06-19T16:45:00'),
    processedBy: '血库管理员'
  },
  {
    id: 'REQ-2024-003',
    patientName: '王五',
    patientAge: 28,
    bloodType: 'B+',
    amount: 200,
    urgency: 'critical',
    status: 'completed',
    diagnosis: '外伤大出血',
    surgeryType: '急诊手术',
    doctorName: '张医生',
    notes: '交通事故，大出血',
    createdAt: new Date('2024-06-18T22:15:00'),
    processedAt: new Date('2024-06-18T23:30:00'),
    processedBy: '血库管理员'
  }
])

// Request form
const requestForm = reactive({
  patientName: '',
  patientAge: 0,
  bloodType: '',
  amount: 200,
  urgency: 'normal',
  diagnosis: '',
  surgeryType: '',
  notes: ''
})

const requestFormRules = {
  patientName: [
    { required: true, message: '请输入患者姓名', trigger: 'blur' }
  ],
  patientAge: [
    { required: true, message: '请输入患者年龄', trigger: 'blur' }
  ],
  bloodType: [
    { required: true, message: '请选择血型', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入需求量', trigger: 'blur' }
  ],
  urgency: [
    { required: true, message: '请选择紧急程度', trigger: 'change' }
  ],
  diagnosis: [
    { required: true, message: '请输入诊断信息', trigger: 'blur' }
  ]
}

// Computed properties
const filteredRequests = computed(() => {
  let filtered = requests.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(request => 
      request.patientName.toLowerCase().includes(query) ||
      request.id.toLowerCase().includes(query)
    )
  }

  // Blood type filter
  if (bloodTypeFilter.value) {
    filtered = filtered.filter(request => request.bloodType === bloodTypeFilter.value)
  }

  // Urgency filter
  if (urgencyFilter.value) {
    filtered = filtered.filter(request => request.urgency === urgencyFilter.value)
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(request => request.status === statusFilter.value)
  }

  return filtered
})

const paginatedRequests = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredRequests.value.slice(start, end)
})

// Methods
const updateStats = () => {
  requestStats.total = requests.value.length
  requestStats.pending = requests.value.filter(r => r.status === 'pending').length
  requestStats.approved = requests.value.filter(r => r.status === 'approved').length
  requestStats.urgent = requests.value.filter(r => r.urgency === 'critical' || r.urgency === 'urgent').length
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleFilter = () => {
  currentPage.value = 1
}

const resetFilters = () => {
  searchQuery.value = ''
  bloodTypeFilter.value = ''
  urgencyFilter.value = ''
  statusFilter.value = ''
  currentPage.value = 1
}

const handleSelectionChange = (selection) => {
  selectedRequests.value = selection
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}

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
    'approved': 'primary',
    'rejected': 'danger',
    'completed': 'success'
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

const formatDate = (date) => {
  return date.toLocaleDateString('zh-CN')
}

const formatDateTime = (date) => {
  return date.toLocaleString('zh-CN')
}

const viewRequest = (request) => {
  selectedRequest.value = request
  showRequestDetailsDialog.value = true
}

const editRequest = (request) => {
  editingRequest.value = request
  Object.keys(requestForm).forEach(key => {
    requestForm[key] = request[key] || ''
  })
  showAddRequestDialog.value = true
}

const processRequest = (request) => {
  ElMessage.info(`处理申请: ${request.id}`)
}

const saveRequest = async () => {
  try {
    await requestFormRef.value.validate()
    saving.value = true

    if (editingRequest.value) {
      // Update existing request
      const index = requests.value.findIndex(r => r.id === editingRequest.value.id)
      if (index > -1) {
        requests.value[index] = { ...requests.value[index], ...requestForm }
        ElMessage.success('申请更新成功')
      }
    } else {
      // Add new request
      const newRequest = {
        id: `REQ-${new Date().getFullYear()}-${String(requests.value.length + 1).padStart(3, '0')}`,
        ...requestForm,
        doctorName: '当前用户', // Should come from auth store
        createdAt: new Date(),
        processedAt: null,
        processedBy: null
      }
      requests.value.push(newRequest)
      ElMessage.success('申请提交成功')
    }

    showAddRequestDialog.value = false
    resetRequestForm()
    updateStats()
  } catch (error) {
    console.error('Form validation failed:', error)
  } finally {
    saving.value = false
  }
}

const resetRequestForm = () => {
  editingRequest.value = null
  Object.keys(requestForm).forEach(key => {
    if (key === 'patientAge') {
      requestForm[key] = 0
    } else if (key === 'amount') {
      requestForm[key] = 200
    } else if (key === 'urgency') {
      requestForm[key] = 'normal'
    } else {
      requestForm[key] = ''
    }
  })
}

const exportRequests = () => {
  ElMessage.info('导出功能开发中')
}

onMounted(() => {
  updateStats()
})
</script>

<style scoped>
.user-request-management {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

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
  font-weight: 700;
}

.title-section p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon.total { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.pending { background: linear-gradient(135deg, #fa709a, #fee140); }
.stat-icon.approved { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.urgent { background: linear-gradient(135deg, #f093fb, #f5576c); }

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.stat-label {
  color: #666;
  font-size: 14px;
  margin-top: 4px;
}

.filter-card {
  margin-bottom: 24px;
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.filter-section {
  padding: 16px;
}

.filter-row {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.table-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header h3 {
  margin: 0;
  color: #333;
}

.table-info {
  color: #666;
  font-size: 14px;
}

.request-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.request-id {
  font-weight: 600;
  color: #333;
}

.request-date {
  font-size: 12px;
  color: #666;
}

.patient-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.patient-name {
  font-weight: 600;
  color: #333;
}

.patient-age {
  font-size: 12px;
  color: #666;
}

.amount {
  font-weight: 600;
  color: #667eea;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.request-details-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-section h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-item label {
  font-weight: 500;
  color: #666;
  min-width: 80px;
}

.detail-item span {
  color: #333;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
