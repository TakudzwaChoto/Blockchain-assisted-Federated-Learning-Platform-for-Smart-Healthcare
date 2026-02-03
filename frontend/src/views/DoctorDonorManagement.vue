<template>
  <div class="donor-management">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">捐赠者管理</h1>
          <p class="page-subtitle">管理和跟踪血液捐赠者信息</p>
        </div>
        <div class="header-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索捐赠者..."
            prefix-icon="Search"
            style="width: 300px; margin-right: 16px"
            @input="handleSearch"
          />
          <el-select v-model="statusFilter" placeholder="筛选状态" style="width: 120px; margin-right: 16px">
            <el-option label="全部" value="" />
            <el-option label="活跃" value="active" />
            <el-option label="非活跃" value="inactive" />
            <el-option label="暂停" value="suspended" />
          </el-select>
          <el-button type="primary" @click="showAddDonor = true">
            <el-icon><Plus /></el-icon>
            添加捐赠者
          </el-button>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon total">
            <el-icon size="32"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ donorStats.total }}</div>
            <div class="stat-label">总捐赠者</div>
          </div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon active">
            <el-icon size="32"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ donorStats.active }}</div>
            <div class="stat-label">活跃捐赠者</div>
          </div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon recent">
            <el-icon size="32"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ donorStats.recentDonations }}</div>
            <div class="stat-label">本月捐赠</div>
          </div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon pending">
            <el-icon size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ donorStats.pending }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Donors Table -->
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <h3>捐赠者列表</h3>
          <div class="table-actions">
            <el-button @click="exportDonors">
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
      
      <el-table :data="filteredDonors" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="姓名" width="120" sortable>
          <template #default="{ row }">
            <div class="donor-name">
              <el-avatar :size="32" :src="row.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="idNumber" label="身份证号" width="180" />
        <el-table-column prop="bloodType" label="血型" width="80">
          <template #default="{ row }">
            <el-tag :type="getBloodTypeColor(row.bloodType)" size="small">
              {{ row.bloodType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="lastDonation" label="最近捐赠" width="120" sortable>
          <template #default="{ row }">
            {{ formatDate(row.lastDonation) }}
          </template>
        </el-table-column>
        <el-table-column prop="totalDonations" label="总捐赠次数" width="120" sortable />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="nextEligible" label="下次可捐赠" width="120">
          <template #default="{ row }">
            <span :class="{ 'text-danger': isNextDonationOverdue(row.nextEligible) }">
              {{ formatDate(row.nextEligible) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDonor(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editDonor(row)">编辑</el-button>
            <el-dropdown trigger="click">
              <el-button size="small" type="info">
                更多<el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="viewDonationHistory(row)">捐赠历史</el-dropdown-item>
                  <el-dropdown-item @click="scheduleDonation(row)">预约捐赠</el-dropdown-item>
                  <el-dropdown-item @click="sendReminder(row)">发送提醒</el-dropdown-item>
                  <el-dropdown-item @click="updateStatus(row)">更新状态</el-dropdown-item>
                  <el-dropdown-item divided @click="deleteDonor(row)" class="text-danger">
                    删除捐赠者
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

    <!-- Add Donor Dialog -->
    <el-dialog v-model="showAddDonor" title="添加捐赠者" width="600px">
      <el-form :model="newDonor" :rules="donorRules" ref="donorForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="newDonor.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="血型" prop="bloodType">
              <el-select v-model="newDonor.bloodType" style="width: 100%">
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
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身份证号" prop="idNumber">
              <el-input v-model="newDonor.idNumber" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="newDonor.phone" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birthDate">
              <el-date-picker
                v-model="newDonor.birthDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="newDonor.gender" style="width: 100%">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="地址" prop="address">
          <el-input v-model="newDonor.address" />
        </el-form-item>
        <el-form-item label="健康状况" prop="healthStatus">
          <el-input v-model="newDonor.healthStatus" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDonor = false">取消</el-button>
        <el-button type="primary" @click="addDonor">确定</el-button>
      </template>
    </el-dialog>

    <!-- Donor Details Dialog -->
    <el-dialog v-model="showDonorDetails" title="捐赠者详情" width="800px">
      <div class="donor-details" v-if="selectedDonor">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ selectedDonor.name }}</el-descriptions-item>
          <el-descriptions-item label="血型">
            <el-tag :type="getBloodTypeColor(selectedDonor.bloodType)">
              {{ selectedDonor.bloodType }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ selectedDonor.idNumber }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedDonor.phone }}</el-descriptions-item>
          <el-descriptions-item label="出生日期">{{ formatDate(selectedDonor.birthDate) }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ selectedDonor.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">{{ selectedDonor.address }}</el-descriptions-item>
          <el-descriptions-item label="最近捐赠">{{ formatDate(selectedDonor.lastDonation) }}</el-descriptions-item>
          <el-descriptions-item label="总捐赠次数">{{ selectedDonor.totalDonations }}</el-descriptions-item>
          <el-descriptions-item label="下次可捐赠">{{ formatDate(selectedDonor.nextEligible) }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusColor(selectedDonor.status)">
              {{ getStatusText(selectedDonor.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="健康状况" :span="2">{{ selectedDonor.healthStatus }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="showDonorDetails = false">关闭</el-button>
        <el-button type="primary" @click="editDonor(selectedDonor)">编辑</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  User, Plus, Search, Download, Refresh, Check, Clock, 
  Warning, ArrowDown 
} from '@element-plus/icons-vue'
import dataService from '../services/dataService'

// Reactive data
const loading = ref(false)
const showAddDonor = ref(false)
const showDonorDetails = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const selectedDonor = ref(null)

// Statistics
const donorStats = reactive({
  total: 0,
  active: 0,
  recentDonations: 0,
  pending: 0
})

// Pagination
const pagination = reactive({
  current: 1,
  size: 20,
  total: 0
})

// Donors data
const donors = ref([])

// New donor form
const newDonor = reactive({
  name: '',
  bloodType: '',
  idNumber: '',
  phone: '',
  birthDate: '',
  gender: '',
  address: '',
  healthStatus: ''
})

// Form rules
const donorRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  bloodType: [
    { required: true, message: '请选择血型', trigger: 'change' }
  ],
  idNumber: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  birthDate: [
    { required: true, message: '请选择出生日期', trigger: 'change' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ]
}

// Computed properties
const filteredDonors = computed(() => {
  let filtered = donors.value
  
  if (searchQuery.value) {
    filtered = filtered.filter(donor => 
      donor.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      donor.idNumber.includes(searchQuery.value) ||
      donor.phone.includes(searchQuery.value)
    )
  }
  
  if (statusFilter.value) {
    filtered = filtered.filter(donor => donor.status === statusFilter.value)
  }
  
  return filtered
})

// Methods
const loadDonors = async () => {
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock data
    donors.value = [
      {
        id: 1,
        name: '张三',
        idNumber: '110101199001011234',
        bloodType: 'A+',
        phone: '13800138001',
        birthDate: '1990-01-01',
        gender: 'male',
        address: '北京市朝阳区',
        healthStatus: '良好，无重大疾病史',
        lastDonation: new Date('2024-01-15'),
        totalDonations: 12,
        status: 'active',
        nextEligible: new Date('2024-02-12')
      },
      {
        id: 2,
        name: '李四',
        idNumber: '110101199202022345',
        bloodType: 'O+',
        phone: '13800138002',
        birthDate: '1992-02-02',
        gender: 'female',
        address: '北京市海淀区',
        healthStatus: '良好，定期体检',
        lastDonation: new Date('2024-01-10'),
        totalDonations: 8,
        status: 'active',
        nextEligible: new Date('2024-02-07')
      },
      {
        id: 3,
        name: '王五',
        idNumber: '110101198803033456',
        bloodType: 'B+',
        phone: '13800138003',
        birthDate: '1988-03-03',
        gender: 'male',
        address: '北京市西城区',
        healthStatus: '轻度高血压，控制良好',
        lastDonation: new Date('2023-12-20'),
        totalDonations: 15,
        status: 'suspended',
        nextEligible: new Date('2024-01-16')
      }
    ]
    
    // Update stats
    donorStats.total = donors.value.length
    donorStats.active = donors.value.filter(d => d.status === 'active').length
    donorStats.recentDonations = donors.value.filter(d => {
      const lastMonth = new Date()
      lastMonth.setMonth(lastMonth.getMonth() - 1)
      return d.lastDonation > lastMonth
    }).length
    donorStats.pending = donors.value.filter(d => d.status === 'pending').length
    
    // Update pagination
    pagination.total = donors.value.length
    
  } catch (error) {
    ElMessage.error('加载捐赠者数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // Search logic handled by computed property
}

const handleSizeChange = (size) => {
  pagination.size = size
  loadDonors()
}

const handlePageChange = (page) => {
  pagination.current = page
  loadDonors()
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

const getStatusColor = (status) => {
  const colors = {
    'active': 'success',
    'inactive': 'info',
    'suspended': 'warning',
    'pending': 'danger'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'active': '活跃',
    'inactive': '非活跃',
    'suspended': '暂停',
    'pending': '待审核'
  }
  return texts[status] || status
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const isNextDonationOverdue = (nextEligible) => {
  if (!nextEligible) return false
  return new Date(nextEligible) < new Date()
}

const viewDonor = (donor) => {
  selectedDonor.value = donor
  showDonorDetails.value = true
}

const editDonor = (donor) => {
  ElMessage.info(`编辑捐赠者: ${donor.name}`)
}

const addDonor = async () => {
  try {
    // Add donor logic here
    ElMessage.success('捐赠者添加成功')
    showAddDonor.value = false
    // Reset form
    Object.assign(newDonor, {
      name: '',
      bloodType: '',
      idNumber: '',
      phone: '',
      birthDate: '',
      gender: '',
      address: '',
      healthStatus: ''
    })
    loadDonors()
  } catch (error) {
    ElMessage.error('添加捐赠者失败')
  }
}

const deleteDonor = async (donor) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除捐赠者 ${donor.name} 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    ElMessage.success('捐赠者删除成功')
    loadDonors()
  } catch (error) {
    // User cancelled
  }
}

const viewDonationHistory = (donor) => {
  ElMessage.info(`查看 ${donor.name} 的捐赠历史`)
}

const scheduleDonation = (donor) => {
  ElMessage.info(`为 ${donor.name} 预约捐赠`)
}

const sendReminder = (donor) => {
  ElMessage.info(`向 ${donor.name} 发送提醒`)
}

const updateStatus = (donor) => {
  ElMessage.info(`更新 ${donor.name} 的状态`)
}

const exportDonors = () => {
  ElMessage.success('导出捐赠者数据')
}

const refreshData = () => {
  loadDonors()
}

// Load data on mount
onMounted(() => {
  loadDonors()
})
</script>

<style scoped>
.donor-management {
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
.stat-icon.active { background: linear-gradient(135deg, #67c23a, #85ce61); }
.stat-icon.recent { background: linear-gradient(135deg, #e6a23c, #ebb563); }
.stat-icon.pending { background: linear-gradient(135deg, #f56c6c, #f78989); }

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

/* Table Styles */
.donor-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.text-danger {
  color: #f56c6c;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* Dialog Styles */
.donor-details {
  max-height: 500px;
  overflow-y: auto;
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
