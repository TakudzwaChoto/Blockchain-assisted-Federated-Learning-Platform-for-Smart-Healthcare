<template>
  <div class="donor-management">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>捐赠者管理</span>
              <div class="header-actions">
                <el-button type="primary" @click="addDonor">
                  <el-icon><Plus /></el-icon>
                  添加捐赠者
                </el-button>
                <el-button @click="exportData">
                  <el-icon><Download /></el-icon>
                  导出
                </el-button>
                <el-button @click="refreshData" :loading="loading">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>

          <!-- Search and Filters -->
          <div class="search-section">
            <el-row :gutter="16">
              <el-col :span="8">
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索捐赠者姓名、ID或邮箱..."
                  prefix-icon="Search"
                  clearable
                  @input="handleSearch"
                />
              </el-col>
              <el-col :span="4">
                <el-select v-model="bloodTypeFilter" placeholder="血型" clearable @change="applyFilters">
                  <el-option label="所有类型" value="" />
                  <el-option label="A+" value="A+" />
                  <el-option label="A-" value="A-" />
                  <el-option label="B+" value="B+" />
                  <el-option label="B-" value="B-" />
                  <el-option label="AB+" value="AB+" />
                  <el-option label="AB-" value="AB-" />
                  <el-option label="O+" value="O+" />
                  <el-option label="O-" value="O-" />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-select v-model="statusFilter" placeholder="状态" clearable @change="applyFilters">
                  <el-option label="所有状态" value="" />
                  <el-option label="活跃" value="active" />
                  <el-option label="非活跃" value="inactive" />
                  <el-option label="暂停" value="suspended" />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetFilters">重置</el-button>
              </el-col>
              <el-col :span="4">
                <el-button type="primary" @click="applyFilters">应用</el-button>
              </el-col>
            </el-row>
          </div>

          <!-- Donors Table -->
          <el-table
            :data="paginatedDonors"
            style="width: 100%"
            v-loading="loading"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="姓名" width="150" />
            <el-table-column prop="email" label="邮箱" width="200" />
            <el-table-column prop="phone" label="电话" width="130" />
            <el-table-column prop="bloodType" label="血型" width="100" />
            <el-table-column prop="lastDonation" label="最后捐赠" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editDonor(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteDonor(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Pagination -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="totalCount"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Plus, Download, Refresh, Search, Edit, Delete, View } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

// State
const loading = ref(false)
const searchQuery = ref('')
const bloodTypeFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const selectedDonors = ref([])

// Mock donor data
const donors = ref([
  {
    id: 'D001',
    name: 'John Smith',
    email: 'john.smith@email.com',
    phone: '+1-234-567-8900',
    bloodType: 'O+',
    donations: 12,
    lastDonation: '2024-01-15',
    status: 'active',
    registeredDate: '2023-03-15'
  },
  {
    id: 'D002',
    name: 'Sarah Johnson',
    email: 'sarah.j@email.com',
    phone: '+1-234-567-8901',
    bloodType: 'A+',
    donations: 8,
    lastDonation: '2024-01-10',
    status: 'active',
    registeredDate: '2023-05-20'
  },
  {
    id: 'D003',
    name: 'Michael Brown',
    email: 'michael.b@email.com',
    phone: '+1-234-567-8902',
    bloodType: 'B-',
    donations: 15,
    lastDonation: '2023-12-28',
    status: 'active',
    registeredDate: '2023-01-10'
  },
  {
    id: 'D004',
    name: 'Emily Davis',
    email: 'emily.d@email.com',
    phone: '+1-234-567-8903',
    bloodType: 'AB+',
    donations: 6,
    lastDonation: '2023-11-15',
    status: 'inactive',
    registeredDate: '2023-06-01'
  },
  {
    id: 'D005',
    name: 'Robert Wilson',
    email: 'robert.w@email.com',
    phone: '+1-234-567-8904',
    bloodType: 'O-',
    donations: 20,
    lastDonation: '2024-01-18',
    status: 'active',
    registeredDate: '2022-12-01'
  }
])

// Computed filtered donors
const filteredDonors = computed(() => {
  let filtered = donors.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(donor => 
      donor.name.toLowerCase().includes(query) ||
      donor.id.toLowerCase().includes(query) ||
      donor.email.toLowerCase().includes(query)
    )
  }

  // Apply blood type filter
  if (bloodTypeFilter.value) {
    filtered = filtered.filter(donor => donor.bloodType === bloodTypeFilter.value)
  }

  // Apply status filter
  if (statusFilter.value) {
    filtered = filtered.filter(donor => donor.status === statusFilter.value)
  }

  return filtered
})

// Computed paginated donors
const paginatedDonors = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredDonors.value.slice(start, end)
})

// Computed total count
const totalCount = computed(() => filteredDonors.value.length)

// Methods
const refreshData = async () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    notificationStore.success('捐献者数据刷新成功')
  }, 1000)
}

const handleSearch = () => {
  currentPage.value = 1
}

const resetFilters = () => {
  searchQuery.value = ''
  bloodTypeFilter.value = ''
  statusFilter.value = ''
  currentPage.value = 1
  notificationStore.info('Filters reset')
}

const applyFilters = () => {
  currentPage.value = 1
  notificationStore.success(`Filters applied: ${totalCount.value} donors found`)
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

const addDonor = () => {
  notificationStore.info('Opening donor registration form...')
}

const editDonor = (donor) => {
  notificationStore.info(`Editing donor: ${donor.name} (${donor.id})`)
}

const deleteDonor = (donor) => {
  notificationStore.warning(`Deleting donor: ${donor.name} (${donor.id})`)
}

const viewDonor = (donor) => {
  notificationStore.info(`Viewing donor details: ${donor.name} (${donor.id})`)
}

const exportData = () => {
  const exportContent = {
    donors: filteredDonors.value,
    exportTime: new Date().toISOString(),
    filters: {
      search: searchQuery.value,
      bloodType: bloodTypeFilter.value,
      status: statusFilter.value
    }
  }
  
  const blob = new Blob([JSON.stringify(exportContent, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = window.document.createElement('a')
  link.href = url
  link.download = `donor-data-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  notificationStore.success(`Exported ${totalCount.value} donor records`)
}

const getStatusType = (status) => {
  switch (status) {
    case 'active': return 'success'
    case 'inactive': return 'info'
    case 'suspended': return 'danger'
    default: return 'info'
  }
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.donor-management {
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

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
