<template>
  <div class="user-donor-management">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1>捐赠者管理</h1>
          <p>管理您的捐赠者信息</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="showAddDonorDialog = true">
            <el-icon><Plus /></el-icon>
            添加捐赠者
          </el-button>
          <el-button @click="exportDonors">
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
            <el-icon size="24"><User /></el-icon>
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
            <el-icon size="24"><Check /></el-icon>
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
            <el-icon size="24"><Clock /></el-icon>
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
            <el-icon size="24"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ donorStats.pending }}</div>
            <div class="stat-label">待审核</div>
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
            placeholder="搜索捐赠者姓名、电话或身份证"
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

          <el-select v-model="statusFilter" placeholder="筛选状态" style="width: 120px" @change="handleFilter">
            <el-option label="全部状态" value="" />
            <el-option label="活跃" value="active" />
            <el-option label="暂停" value="inactive" />
            <el-option label="待审核" value="pending" />
          </el-select>

          <el-button @click="resetFilters">重置筛选</el-button>
        </div>
      </div>
    </el-card>

    <!-- Donors Table -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <h3>捐赠者列表</h3>
          <div class="table-info">
            <span>共 {{ filteredDonors.length }} 个捐赠者</span>
          </div>
        </div>
      </template>

      <el-table 
        :data="paginatedDonors" 
        style="width: 100%" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="基本信息" min-width="200">
          <template #default="{ row }">
            <div class="donor-info">
              <el-avatar :size="40">{{ row.name?.charAt(0) }}</el-avatar>
              <div class="donor-details">
                <div class="donor-name">{{ row.name }}</div>
                <div class="donor-contact">{{ row.phone }}</div>
              </div>
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

        <el-table-column prop="idCard" label="身份证号" width="180" />

        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="lastDonation" label="最近捐赠" width="120">
          <template #default="{ row }">
            {{ formatDate(row.lastDonation) }}
          </template>
        </el-table-column>

        <el-table-column prop="totalDonations" label="总捐赠次数" width="120">
          <template #default="{ row }">
            <span class="donation-count">{{ row.totalDonations || 0 }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDonor(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editDonor(row)">编辑</el-button>
            <el-button size="small" type="success" @click="recordDonation(row)">记录捐赠</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="filteredDonors.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Add/Edit Donor Dialog -->
    <el-dialog 
      v-model="showAddDonorDialog" 
      :title="editingDonor ? '编辑捐赠者' : '添加捐赠者'" 
      width="600px"
    >
      <el-form :model="donorForm" :rules="donorFormRules" ref="donorFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="donorForm.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="血型" prop="bloodType">
          <el-select v-model="donorForm.bloodType" style="width: 100%">
            <el-option label="A+" value="A+" />
            <el-option label="B+" value="B+" />
            <el-option label="O+" value="O+" />
            <el-option label="AB+" value="AB+" />
          </el-select>
        </el-form-item>

        <el-form-item label="电话" prop="phone">
          <el-input v-model="donorForm.phone" placeholder="请输入电话号码" />
        </el-form-item>

        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="donorForm.idCard" placeholder="请输入身份证号" />
        </el-form-item>

        <el-form-item label="地址" prop="address">
          <el-input v-model="donorForm.address" placeholder="请输入地址" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-select v-model="donorForm.status" style="width: 100%">
            <el-option label="活跃" value="active" />
            <el-option label="暂停" value="inactive" />
            <el-option label="待审核" value="pending" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注" prop="notes">
          <el-input v-model="donorForm.notes" type="textarea" :rows="3" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAddDonorDialog = false">取消</el-button>
        <el-button type="primary" @click="saveDonor" :loading="saving">
          {{ editingDonor ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Record Donation Dialog -->
    <el-dialog v-model="showDonationDialog" title="记录捐赠" width="500px">
      <el-form :model="donationForm" :rules="donationFormRules" ref="donationFormRef" label-width="100px">
        <el-form-item label="捐赠者">
          <el-input :value="selectedDonor?.name" readonly />
        </el-form-item>

        <el-form-item label="捐赠日期" prop="donationDate">
          <el-date-picker
            v-model="donationForm.donationDate"
            type="date"
            placeholder="选择捐赠日期"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="捐赠量" prop="amount">
          <el-input-number 
            v-model="donationForm.amount" 
            :min="200" 
            :max="400" 
            :step="50"
            controls-position="right"
          />
          <span style="margin-left: 8px">ml</span>
        </el-form-item>

        <el-form-item label="捐赠类型" prop="donationType">
          <el-select v-model="donationForm.donationType" style="width: 100%">
            <el-option label="全血" value="whole" />
            <el-option label="血小板" value="platelets" />
            <el-option label="血浆" value="plasma" />
          </el-select>
        </el-form-item>

        <el-form-item label="健康状况" prop="healthStatus">
          <el-select v-model="donationForm.healthStatus" style="width: 100%">
            <el-option label="良好" value="good" />
            <el-option label="一般" value="fair" />
            <el-option label="需观察" value="observe" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注" prop="notes">
          <el-input v-model="donationForm.notes" type="textarea" :rows="2" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showDonationDialog = false">取消</el-button>
        <el-button type="primary" @click="saveDonation" :loading="saving">记录捐赠</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Plus, Download, Search, User, Check, Clock, Warning
} from '@element-plus/icons-vue'

const loading = ref(false)
const saving = ref(false)
const showAddDonorDialog = ref(false)
const showDonationDialog = ref(false)
const editingDonor = ref(null)
const selectedDonor = ref(null)
const donorFormRef = ref()
const donationFormRef = ref()

// Filters
const searchQuery = ref('')
const bloodTypeFilter = ref('')
const statusFilter = ref('')

// Pagination
const currentPage = ref(1)
const pageSize = ref(20)
const selectedDonors = ref([])

// Statistics
const donorStats = reactive({
  total: 0,
  active: 0,
  recentDonations: 0,
  pending: 0
})

// Mock donors data
const donors = ref([
  {
    id: 'donor-001',
    name: '王小明',
    bloodType: 'A+',
    phone: '13800138001',
    idCard: '110101199001011234',
    address: '北京市朝阳区',
    status: 'active',
    lastDonation: new Date('2024-06-15'),
    totalDonations: 12,
    notes: '定期捐赠者，健康状况良好'
  },
  {
    id: 'donor-002',
    name: '李小红',
    bloodType: 'O+',
    phone: '13800138002',
    idCard: '110101199002022345',
    address: '北京市海淀区',
    status: 'active',
    lastDonation: new Date('2024-05-20'),
    totalDonations: 8,
    notes: '首次捐赠者'
  },
  {
    id: 'donor-003',
    name: '张小华',
    bloodType: 'B+',
    phone: '13800138003',
    idCard: '110101199003033456',
    address: '北京市西城区',
    status: 'inactive',
    lastDonation: new Date('2024-04-10'),
    totalDonations: 5,
    notes: '因健康原因暂停捐赠'
  }
])

// Donor form
const donorForm = reactive({
  name: '',
  bloodType: '',
  phone: '',
  idCard: '',
  address: '',
  status: 'active',
  notes: ''
})

const donorFormRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  bloodType: [
    { required: true, message: '请选择血型', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入电话号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  idCard: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/, message: '请输入正确的身份证号', trigger: 'blur' }
  ]
}

// Donation form
const donationForm = reactive({
  donationDate: new Date(),
  amount: 200,
  donationType: 'whole',
  healthStatus: 'good',
  notes: ''
})

const donationFormRules = {
  donationDate: [
    { required: true, message: '请选择捐赠日期', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入捐赠量', trigger: 'blur' }
  ],
  donationType: [
    { required: true, message: '请选择捐赠类型', trigger: 'change' }
  ],
  healthStatus: [
    { required: true, message: '请选择健康状况', trigger: 'change' }
  ]
}

// Computed properties
const filteredDonors = computed(() => {
  let filtered = donors.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(donor => 
      donor.name.toLowerCase().includes(query) ||
      donor.phone.includes(query) ||
      donor.idCard.includes(query)
    )
  }

  // Blood type filter
  if (bloodTypeFilter.value) {
    filtered = filtered.filter(donor => donor.bloodType === bloodTypeFilter.value)
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(donor => donor.status === statusFilter.value)
  }

  return filtered
})

const paginatedDonors = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredDonors.value.slice(start, end)
})

// Methods
const updateStats = () => {
  donorStats.total = donors.value.length
  donorStats.active = donors.value.filter(d => d.status === 'active').length
  donorStats.pending = donors.value.filter(d => d.status === 'pending').length
  
  const thisMonth = new Date().getMonth()
  donorStats.recentDonations = donors.value.filter(d => 
    d.lastDonation && d.lastDonation.getMonth() === thisMonth
  ).length
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
  statusFilter.value = ''
  currentPage.value = 1
}

const handleSelectionChange = (selection) => {
  selectedDonors.value = selection
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

const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    inactive: 'info',
    pending: 'warning'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    active: '活跃',
    inactive: '暂停',
    pending: '待审核'
  }
  return texts[status] || status
}

const formatDate = (date) => {
  if (!date) return '暂无'
  return date.toLocaleDateString('zh-CN')
}

const viewDonor = (donor) => {
  ElMessage.info(`查看捐赠者: ${donor.name}`)
}

const editDonor = (donor) => {
  editingDonor.value = donor
  Object.keys(donorForm).forEach(key => {
    donorForm[key] = donor[key] || ''
  })
  showAddDonorDialog.value = true
}

const recordDonation = (donor) => {
  selectedDonor.value = donor
  showDonationDialog.value = true
}

const saveDonor = async () => {
  try {
    await donorFormRef.value.validate()
    saving.value = true

    if (editingDonor.value) {
      // Update existing donor
      const index = donors.value.findIndex(d => d.id === editingDonor.value.id)
      if (index > -1) {
        donors.value[index] = { ...donors.value[index], ...donorForm }
        ElMessage.success('捐赠者信息更新成功')
      }
    } else {
      // Add new donor
      const newDonor = {
        id: `donor-${Date.now()}`,
        ...donorForm,
        lastDonation: null,
        totalDonations: 0
      }
      donors.value.push(newDonor)
      ElMessage.success('捐赠者添加成功')
    }

    showAddDonorDialog.value = false
    resetDonorForm()
    updateStats()
  } catch (error) {
    console.error('Form validation failed:', error)
  } finally {
    saving.value = false
  }
}

const saveDonation = async () => {
  try {
    await donationFormRef.value.validate()
    saving.value = true

    // Update donor's last donation and total count
    if (selectedDonor.value) {
      selectedDonor.value.lastDonation = donationForm.donationDate
      selectedDonor.value.totalDonations = (selectedDonor.value.totalDonations || 0) + 1
    }

    ElMessage.success('捐赠记录保存成功')
    showDonationDialog.value = false
    resetDonationForm()
    updateStats()
  } catch (error) {
    console.error('Form validation failed:', error)
  } finally {
    saving.value = false
  }
}

const resetDonorForm = () => {
  editingDonor.value = null
  Object.keys(donorForm).forEach(key => {
    if (key === 'status') {
      donorForm[key] = 'active'
    } else {
      donorForm[key] = ''
    }
  })
}

const resetDonationForm = () => {
  selectedDonor.value = null
  Object.keys(donationForm).forEach(key => {
    if (key === 'donationDate') {
      donationForm[key] = new Date()
    } else if (key === 'amount') {
      donationForm[key] = 200
    } else if (key === 'donationType') {
      donationForm[key] = 'whole'
    } else if (key === 'healthStatus') {
      donationForm[key] = 'good'
    } else {
      donationForm[key] = ''
    }
  })
}

const exportDonors = () => {
  ElMessage.info('导出功能开发中')
}

onMounted(() => {
  updateStats()
})
</script>

<style scoped>
.user-donor-management {
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
.stat-icon.active { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.recent { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.stat-icon.pending { background: linear-gradient(135deg, #fa709a, #fee140); }

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

.donor-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.donor-details {
  flex: 1;
}

.donor-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.donor-contact {
  font-size: 12px;
  color: #666;
}

.donation-count {
  font-weight: 600;
  color: #667eea;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
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
}
</style>
