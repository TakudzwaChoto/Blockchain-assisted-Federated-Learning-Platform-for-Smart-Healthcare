<template>
  <div class="admin-user-management">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1>用户管理</h1>
          <p>管理系统用户账户和权限</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="showAddUserDialog = true">
            <el-icon><Plus /></el-icon>
            添加用户
          </el-button>
          <el-button @click="exportUsers">
            <el-icon><Download /></el-icon>
            导出用户
          </el-button>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <el-card class="filter-card">
      <div class="filter-section">
        <div class="filter-row">
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户名、姓名或邮箱"
            prefix-icon="Search"
            style="width: 300px"
            @input="handleSearch"
          />
          
          <el-select v-model="roleFilter" placeholder="筛选角色" style="width: 150px" @change="handleFilter">
            <el-option label="全部角色" value="" />
            <el-option label="管理员" value="admin" />
            <el-option label="用户" value="user" />
          </el-select>

          <el-select v-model="statusFilter" placeholder="筛选状态" style="width: 150px" @change="handleFilter">
            <el-option label="全部状态" value="" />
            <el-option label="活跃" value="active" />
            <el-option label="离线" value="offline" />
            <el-option label="暂停" value="suspended" />
          </el-select>

          <el-button @click="resetFilters">重置筛选</el-button>
        </div>
      </div>
    </el-card>

    <!-- User Statistics -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon total">
            <el-icon size="24"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ userStats.total }}</div>
            <div class="stat-label">总用户数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon admin">
            <el-icon size="24"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ userStats.admins }}</div>
            <div class="stat-label">管理员</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon active">
            <el-icon size="24"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ userStats.active }}</div>
            <div class="stat-label">活跃用户</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon new">
            <el-icon size="24"><Plus /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ userStats.newThisMonth }}</div>
            <div class="stat-label">本月新增</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Users Table -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <h3>用户列表</h3>
          <div class="table-info">
            <span>共 {{ filteredUsers.length }} 个用户</span>
          </div>
        </div>
      </template>

      <el-table 
        :data="paginatedUsers" 
        style="width: 100%" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="用户信息" min-width="200">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="40">{{ row.name?.charAt(0) }}</el-avatar>
              <div class="user-details">
                <div class="user-name">{{ row.name }}</div>
                <div class="user-email">{{ row.email }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="username" label="用户名" width="120" />

        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'" size="small">
              {{ row.role === 'admin' ? '管理员' : '用户' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="department" label="部门" width="150" />

        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="lastLogin" label="最后登录" width="150">
          <template #default="{ row }">
            {{ formatLastLogin(row.lastLogin) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewUser(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editUser(row)">编辑</el-button>
            <el-dropdown @command="(command) => handleUserAction(command, row)">
              <el-button size="small">
                更多<el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="reset-password">重置密码</el-dropdown-item>
                  <el-dropdown-item command="toggle-status">
                    {{ row.status === 'active' ? '暂停账户' : '激活账户' }}
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除用户</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredUsers.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Add/Edit User Dialog -->
    <el-dialog 
      v-model="showAddUserDialog" 
      :title="editingUser ? '编辑用户' : '添加用户'" 
      width="600px"
    >
      <el-form :model="userForm" :rules="userFormRules" ref="userFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" :disabled="editingUser" />
        </el-form-item>

        <el-form-item label="密码" prop="password" v-if="!editingUser">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>

        <el-form-item label="部门" prop="department">
          <el-input v-model="userForm.department" placeholder="请输入部门" />
        </el-form-item>

        <el-form-item label="状态" prop="status" v-if="editingUser">
          <el-select v-model="userForm.status" style="width: 100%">
            <el-option label="活跃" value="active" />
            <el-option label="离线" value="offline" />
            <el-option label="暂停" value="suspended" />
          </el-select>
        </el-form-item>

        <el-form-item label="权限" prop="permissions">
          <el-checkbox-group v-model="userForm.permissions">
            <el-checkbox label="view_own">查看个人数据</el-checkbox>
            <el-checkbox label="view_reports">查看报告</el-checkbox>
            <el-checkbox label="view_all" v-if="userForm.role === 'admin'">查看所有数据</el-checkbox>
            <el-checkbox label="manage_users" v-if="userForm.role === 'admin'">管理用户</el-checkbox>
            <el-checkbox label="manage_system" v-if="userForm.role === 'admin'">管理系统</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAddUserDialog = false">取消</el-button>
        <el-button type="primary" @click="saveUser" :loading="saving">
          {{ editingUser ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- User Details Dialog -->
    <el-dialog v-model="showUserDetailsDialog" title="用户详情" width="600px">
      <div class="user-details-content" v-if="selectedUser">
        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <label>姓名:</label>
              <span>{{ selectedUser.name }}</span>
            </div>
            <div class="detail-item">
              <label>邮箱:</label>
              <span>{{ selectedUser.email }}</span>
            </div>
            <div class="detail-item">
              <label>用户名:</label>
              <span>{{ selectedUser.username }}</span>
            </div>
            <div class="detail-item">
              <label>角色:</label>
              <el-tag :type="selectedUser.role === 'admin' ? 'danger' : 'primary'">
                {{ selectedUser.role === 'admin' ? '管理员' : '用户' }}
              </el-tag>
            </div>
            <div class="detail-item">
              <label>部门:</label>
              <span>{{ selectedUser.department }}</span>
            </div>
            <div class="detail-item">
              <label>状态:</label>
              <el-tag :type="getStatusColor(selectedUser.status)">
                {{ getStatusText(selectedUser.status) }}
              </el-tag>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>活动信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <label>创建时间:</label>
              <span>{{ formatDate(selectedUser.createdAt) }}</span>
            </div>
            <div class="detail-item">
              <label>最后登录:</label>
              <span>{{ formatLastLogin(selectedUser.lastLogin) }}</span>
            </div>
            <div class="detail-item">
              <label>登录次数:</label>
              <span>{{ selectedUser.loginCount || 0 }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>权限列表</h4>
          <div class="permissions-list">
            <el-tag 
              v-for="permission in selectedUser.permissions" 
              :key="permission"
              style="margin-right: 8px; margin-bottom: 8px"
            >
              {{ getPermissionText(permission) }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Download, Search, User, Check, ArrowDown
} from '@element-plus/icons-vue'

// Reactive data
const loading = ref(false)
const saving = ref(false)
const showAddUserDialog = ref(false)
const showUserDetailsDialog = ref(false)
const editingUser = ref(null)
const selectedUser = ref(null)
const userFormRef = ref()

// Filters
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')

// Pagination
const currentPage = ref(1)
const pageSize = ref(20)
const selectedUsers = ref([])

// User statistics
const userStats = reactive({
  total: 0,
  admins: 0,
  active: 0,
  newThisMonth: 0
})

// Mock users data
const users = ref([
  {
    id: 'admin-001',
    name: '系统管理员',
    email: 'admin@blooddomain.com',
    username: 'admin',
    role: 'admin',
    department: '系统管理部',
    status: 'active',
    permissions: ['view_all', 'manage_users', 'manage_system', 'view_reports'],
    lastLogin: new Date(),
    createdAt: new Date('2024-01-01'),
    loginCount: 156
  },
  {
    id: 'user-001',
    name: '张医生',
    email: 'zhang@hospital.com',
    username: 'user',
    role: 'user',
    department: '血液科',
    status: 'active',
    permissions: ['view_own', 'view_reports'],
    lastLogin: new Date(Date.now() - 2 * 60 * 60 * 1000),
    createdAt: new Date('2024-02-15'),
    loginCount: 89
  },
  {
    id: 'user-002',
    name: '李医生',
    email: 'li@hospital.com',
    username: 'doctor',
    role: 'user',
    department: '输血科',
    status: 'active',
    permissions: ['view_own', 'view_reports'],
    lastLogin: new Date(Date.now() - 24 * 60 * 60 * 1000),
    createdAt: new Date('2024-03-10'),
    loginCount: 67
  },
  {
    id: 'user-003',
    name: '王护士',
    email: 'wang@hospital.com',
    username: 'nurse',
    role: 'user',
    department: '护理部',
    status: 'offline',
    permissions: ['view_own', 'view_reports'],
    lastLogin: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    createdAt: new Date('2024-04-05'),
    loginCount: 45
  }
])

// User form
const userForm = reactive({
  name: '',
  email: '',
  username: '',
  password: '',
  role: 'user',
  department: '',
  status: 'active',
  permissions: ['view_own', 'view_reports']
})

const userFormRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度至少3位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  department: [
    { required: true, message: '请输入部门', trigger: 'blur' }
  ]
}

// Computed properties
const filteredUsers = computed(() => {
  let filtered = users.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user => 
      user.name.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      user.username.toLowerCase().includes(query)
    )
  }

  // Role filter
  if (roleFilter.value) {
    filtered = filtered.filter(user => user.role === roleFilter.value)
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(user => user.status === statusFilter.value)
  }

  return filtered
})

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredUsers.value.slice(start, end)
})

// Methods
const updateStats = () => {
  userStats.total = users.value.length
  userStats.admins = users.value.filter(u => u.role === 'admin').length
  userStats.active = users.value.filter(u => u.status === 'active').length
  
  const thisMonth = new Date().getMonth()
  userStats.newThisMonth = users.value.filter(u => 
    u.createdAt.getMonth() === thisMonth
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
  roleFilter.value = ''
  statusFilter.value = ''
  currentPage.value = 1
}

const handleSelectionChange = (selection) => {
  selectedUsers.value = selection
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}

const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    offline: 'info',
    suspended: 'danger'
  }
  return colors[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    active: '活跃',
    offline: '离线',
    suspended: '暂停'
  }
  return texts[status] || status
}

const getPermissionText = (permission) => {
  const texts = {
    view_own: '查看个人数据',
    view_reports: '查看报告',
    view_all: '查看所有数据',
    manage_users: '管理用户',
    manage_system: '管理系统'
  }
  return texts[permission] || permission
}

const formatLastLogin = (date) => {
  if (!date) return '从未登录'
  
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)
  
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

const formatDate = (date) => {
  return date.toLocaleDateString('zh-CN')
}

const viewUser = (user) => {
  selectedUser.value = user
  showUserDetailsDialog.value = true
}

const editUser = (user) => {
  editingUser.value = user
  Object.keys(userForm).forEach(key => {
    userForm[key] = user[key] || ''
  })
  showAddUserDialog.value = true
}

const saveUser = async () => {
  try {
    await userFormRef.value.validate()
    saving.value = true

    if (editingUser.value) {
      // Update existing user
      const index = users.value.findIndex(u => u.id === editingUser.value.id)
      if (index > -1) {
        users.value[index] = { ...users.value[index], ...userForm }
        ElMessage.success('用户更新成功')
      }
    } else {
      // Add new user
      const newUser = {
        id: `user-${Date.now()}`,
        ...userForm,
        createdAt: new Date(),
        lastLogin: null,
        loginCount: 0
      }
      users.value.push(newUser)
      ElMessage.success('用户添加成功')
    }

    showAddUserDialog.value = false
    resetUserForm()
    updateStats()
  } catch (error) {
    console.error('Form validation failed:', error)
  } finally {
    saving.value = false
  }
}

const resetUserForm = () => {
  editingUser.value = null
  Object.keys(userForm).forEach(key => {
    if (key === 'role') {
      userForm[key] = 'user'
    } else if (key === 'status') {
      userForm[key] = 'active'
    } else if (key === 'permissions') {
      userForm[key] = ['view_own', 'view_reports']
    } else {
      userForm[key] = ''
    }
  })
}

const handleUserAction = async (command, user) => {
  switch (command) {
    case 'reset-password':
      try {
        await ElMessageBox.confirm(
          `确定要重置用户 ${user.name} 的密码吗？`,
          '重置密码',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        ElMessage.success('密码重置成功，新密码已发送到用户邮箱')
      } catch (error) {
        // User cancelled
      }
      break

    case 'toggle-status':
      const newStatus = user.status === 'active' ? 'suspended' : 'active'
      const statusText = newStatus === 'active' ? '激活' : '暂停'
      
      try {
        await ElMessageBox.confirm(
          `确定要${statusText}用户 ${user.name} 吗？`,
          `${statusText}用户`,
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        user.status = newStatus
        ElMessage.success(`用户${statusText}成功`)
        updateStats()
      } catch (error) {
        // User cancelled
      }
      break

    case 'delete':
      try {
        await ElMessageBox.confirm(
          `确定要删除用户 ${user.name} 吗？此操作不可恢复！`,
          '删除用户',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'error'
          }
        )
        
        const index = users.value.findIndex(u => u.id === user.id)
        if (index > -1) {
          users.value.splice(index, 1)
          ElMessage.success('用户删除成功')
          updateStats()
        }
      } catch (error) {
        // User cancelled
      }
      break
  }
}

const exportUsers = () => {
  ElMessage.info('导出功能开发中')
}

onMounted(() => {
  updateStats()
})
</script>

<style scoped>
.admin-user-management {
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
.stat-icon.admin { background: linear-gradient(135deg, #f093fb, #f5576c); }
.stat-icon.active { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.new { background: linear-gradient(135deg, #43e97b, #38f9d7); }

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

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  flex: 1;
}

.user-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.user-email {
  font-size: 12px;
  color: #666;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.user-details-content {
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

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
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
