<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="back-to-home">
          <el-link @click="goToHome" type="primary">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-link>
        </div>
        <div class="logo">
          <el-icon size="40" color="#667eea">
            <TrendCharts />
          </el-icon>
        </div>
        <h1>血液域分析平台</h1>
        <p>AI驱动的血液管理系统</p>
      </div>

      <!-- Account Type Selection -->
      <div class="account-type-selection" v-if="showAccountTypeSelection">
        <h3>选择账户类型</h3>
        <div class="account-type-buttons">
          <el-button 
            type="primary" 
            size="large" 
            class="account-type-btn"
            @click="selectAccountType('user')"
          >
            <el-icon><User /></el-icon>
            <div class="btn-content">
              <div class="btn-title">普通用户</div>
              <div class="btn-desc">个人用户，查看个人数据和申请用血</div>
            </div>
          </el-button>
          
          <el-button 
            type="warning" 
            size="large" 
            class="account-type-btn"
            @click="selectAccountType('doctor')"
          >
            <el-icon><User /></el-icon>
            <div class="btn-content">
              <div class="btn-title">医生用户</div>
              <div class="btn-desc">医生用户，管理患者和输血申请</div>
            </div>
          </el-button>

          <el-button 
            type="danger" 
            size="large" 
            class="account-type-btn"
            @click="selectAccountType('admin')"
          >
            <el-icon><User /></el-icon>
            <div class="btn-content">
              <div class="btn-title">管理员</div>
              <div class="btn-desc">系统管理员，管理所有用户和系统设置</div>
            </div>
          </el-button>

          <el-button 
            type="success" 
            size="large" 
            class="account-type-btn"
            @click="selectAccountType('government')"
          >
            <el-icon><OfficeBuilding /></el-icon>
            <div class="btn-content">
              <div class="btn-title">政府监管</div>
              <div class="btn-desc">政府监管机构，监督血液安全和合规</div>
            </div>
          </el-button>
        </div>
        
        <div class="existing-account">
          <el-link @click="showAccountTypeSelection = false">
            已有账户？点击登录
          </el-link>
          <el-divider direction="vertical" />
          <el-link @click="goToHome" type="primary">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-link>
        </div>
      </div>

      <!-- Registration Form -->
      <el-form 
        v-if="showRegistrationForm" 
        ref="registerForm" 
        :model="registerData" 
        :rules="registerRules" 
        class="login-form"
      >
        <h3 class="form-title">创建账户{{ getAccountTypeText() }}</h3>
        
        <el-form-item prop="name">
          <el-input
            v-model="registerData.name"
            placeholder="姓名"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="email">
          <el-input
            v-model="registerData.email"
            placeholder="邮箱地址"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="username">
          <el-input
            v-model="registerData.username"
            placeholder="用户名"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="registerData.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerData.confirmPassword"
            type="password"
            placeholder="确认密码"
            size="large"
            show-password
          />
        </el-form-item>

        <el-form-item prop="department">
          <el-input
            v-model="registerData.department"
            placeholder="部门"
            size="large"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleRegister"
          >
            创建账户
          </el-button>
        </el-form-item>

        <div class="form-footer">
          <el-link @click="showAccountTypeSelection = true">
            返回选择
          </el-link>
          <el-divider direction="vertical" />
          <el-link @click="showLoginForm = true; showRegistrationForm = false">
            已有账户？登录
          </el-link>
          <el-divider direction="vertical" />
          <el-link @click="goToHome" type="primary">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-link>
        </div>
      </el-form>

      <!-- Login Form -->
      <el-form 
        v-if="showLoginForm" 
        ref="loginForm" 
        :model="loginData" 
        :rules="rules" 
        class="login-form"
      >
        <h3 class="form-title">登录</h3>
        
        <el-form-item prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="用户名"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item prop="role">
          <el-select
            v-model="loginData.role"
            placeholder="选择账户类型"
            size="large"
            style="width: 100%"
          >
            <el-option
              v-for="role in roleOptions"
              :key="role.value"
              :label="role.label"
              :value="role.value"
            >
              <div class="role-option">
                <el-icon><component :is="role.icon" /></el-icon>
                <span>{{ role.label }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            {{ t('auth.login') }}
          </el-button>
        </el-form-item>

        <div class="form-footer">
          <el-link @click="showAccountTypeSelection = true; showLoginForm = false">
            创建新账户
          </el-link>
          <el-divider direction="vertical" />
          <el-link @click="goToHome" type="primary">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-link>
        </div>
      </el-form>

      <!-- Demo Accounts (only show when no forms are active) -->
      <div class="demo-accounts" v-if="!showAccountTypeSelection && !showRegistrationForm && !showLoginForm">
        <div class="demo-title">演示账户</div>
        <div class="demo-account">
          <strong>管理员账户</strong> admin / admin123
        </div>
        <div class="demo-account">
          <strong>用户账户</strong> user / user123
        </div>
        <div class="demo-account">
          <strong>医生账户</strong> doctor / doctor123
        </div>
        <div class="demo-actions">
          <el-button @click="showLoginForm = true">使用演示账户</el-button>
          <el-button type="primary" @click="showAccountTypeSelection = true">创建新账户</el-button>
          <el-divider direction="vertical" />
          <el-link @click="goToHome" type="primary">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  TrendCharts, User, Lock, Plus, ArrowDown, ArrowLeft, OfficeBuilding 
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

// Dummy translation function to prevent errors
const t = (key) => {
  // Return key as fallback for now
  return key
}

// Form refs
const loginForm = ref()
const registerForm = ref()

// UI state
const loading = ref(false)
const showAccountTypeSelection = ref(true)
const showRegistrationForm = ref(false)
const showLoginForm = ref(false)
const selectedAccountType = ref('')

// Login data
const loginData = reactive({
  username: '',
  password: '',
  role: ''
})

// Role options for login
const roleOptions = computed(() => [
  {
    value: 'user',
    label: '普通用户',
    icon: 'User'
  },
  {
    value: 'doctor',
    label: '医生用户',
    icon: 'User'
  },
  {
    value: 'admin',
    label: '管理员',
    icon: 'User'
  },
  {
    value: 'government',
    label: '政府监管',
    icon: 'OfficeBuilding'
  }
])

// Registration data
const registerData = reactive({
  name: '',
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  department: ''
})

// Login form rules
const rules = computed(() => ({
  username: [
    { required: true, message: t('validation.usernameRequired'), trigger: 'blur' }
  ],
  password: [
    { required: true, message: t('validation.passwordRequired'), trigger: 'blur' },
    { min: 6, message: t('validation.passwordMinLength'), trigger: 'blur' }
  ],
  role: [
    { required: true, message: t('validation.roleRequired'), trigger: 'change' }
  ]
}))

// Registration form rules
const registerRules = computed(() => ({
  name: [
    { required: true, message: t('validation.nameRequired'), trigger: 'blur' }
  ],
  email: [
    { required: true, message: t('validation.emailRequired'), trigger: 'blur' }
  ],
  username: [
    { required: true, message: t('validation.usernameRequired'), trigger: 'blur' },
    { min: 3, message: t('validation.usernameMinLength'), trigger: 'blur' }
  ],
  password: [
    { required: true, message: t('validation.passwordRequired'), trigger: 'blur' },
    { min: 6, message: t('validation.passwordMinLength'), trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: t('validation.confirmPasswordRequired'), trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value !== registerData.password) {
          callback(new Error(t('validation.passwordMismatch')))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  department: [
    { required: true, message: t('validation.departmentRequired'), trigger: 'change' }
  ]
}))

// Methods
const goToHome = () => {
  router.push('/')
}

const selectAccountType = (type) => {
  selectedAccountType.value = type
  showAccountTypeSelection.value = false
  showRegistrationForm.value = true
}

const getAccountTypeText = () => {
  const texts = {
    'user': ' - 普通用户',
    'doctor': ' - 医生用户',
    'admin': ' - 管理员',
    'government': ' - 政府监管'
  }
  return texts[selectedAccountType.value] || ''
}

const handleLogin = async () => {
  try {
    await loginForm.value.validate()
    loading.value = true

    const result = authStore.login({
      username: loginData.username,
      password: loginData.password,
      role: loginData.role
    })
    
    if (result.success) {
      // Verify that user's role matches selected role
      if (result.user.role !== loginData.role) {
        ElMessage.error('角色不匹配')
        return
      }

      ElMessage.success(`欢迎回来，${result.user.name}！`)
      
      // Redirect based on role
      if (result.user.role === 'admin') {
        router.push('/admin/dashboard')
      } else if (result.user.role === 'doctor') {
        router.push('/doctor/dashboard')
      } else {
        router.push('/user/dashboard')
      }
    } else {
      ElMessage.error(result.error)
    }
  } catch (error) {
    console.error('Login validation failed:', error)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  try {
    await registerForm.value.validate()
    loading.value = true

    // Create new user based on selected account type
    const newUser = {
      name: registerData.name,
      email: registerData.email,
      username: registerData.username,
      password: registerData.password, // Keep password for login validation
      role: selectedAccountType.value, // 'user', 'doctor', or 'admin'
      department: registerData.department,
      status: 'active',
      permissions: selectedAccountType.value === 'admin' 
        ? ['view_all', 'manage_users', 'manage_system', 'view_reports']
        : selectedAccountType.value === 'doctor' 
        ? ['view_own', 'view_reports', 'manage_donors', 'manage_requests']
        : ['view_own', 'view_reports']
    }

    // Add to auth store using mock database
    const result = authStore.addUser(newUser)
    
    if (!result.success) {
      ElMessage.error(result.error)
      return
    }
    
    ElMessage.success(`${getAccountTypeText()} 账户创建成功`)
    
    // Auto-login the new user
    const loginResult = authStore.login({
      username: registerData.username,
      password: registerData.password
    })
    
    if (loginResult.success) {
      ElMessage.success(`欢迎，${loginResult.user.name}！`)
      
      // Redirect based on role
      if (loginResult.user.role === 'admin') {
        router.push('/admin/dashboard')
      } else {
        router.push('/user/dashboard')
      }
    }
    
  } catch (error) {
    console.error('Registration validation failed:', error)
  } finally {
    loading.value = false
  }
}

// Load existing auth state on mount
authStore.load()
if (authStore.isAuthenticated) {
  // Already logged in, redirect to appropriate dashboard
  if (authStore.isAdmin) {
    router.push('/admin/dashboard')
  } else if (authStore.isDoctor) {
    router.push('/doctor/dashboard')
  } else {
    router.push('/user/dashboard')
  }
}

// Listen for account creation trigger from landing page
window.addEventListener('showAccountCreation', () => {
  showAccountTypeSelection.value = true
  showLoginForm.value = false
})
</script>

<style scoped>
/* 返回首页 Button */
.back-to-home {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1000;
}

.back-to-home .el-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #667eea;
  text-decoration: none;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #667eea;
}

.back-to-home .el-link:hover {
  color: #4a5fc1;
  transform: translateX(-2px);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 24px;
  font-weight: 700;
}

.login-header p {
  color: #666;
  margin: 0;
}

.login-form {
  margin-bottom: 30px;
}

.login-form .el-form-item {
  margin-bottom: 20px;
}

.login-form .el-input {
  width: 100%;
}

.demo-accounts {
  border-top: 1px solid #eee;
  padding-top: 20px;
  font-size: 14px;
  color: #666;
}

.demo-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.demo-account {
  margin-bottom: 4px;
}

.demo-account strong {
  color: #333;
}

/* Account Type Selection Styles */
.account-type-selection {
  text-align: center;
  padding: 20px 0;
}

.account-type-selection h3 {
  margin: 0 0 30px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.account-type-buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 30px;
}

.account-type-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  height: auto;
  text-align: left;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.account-type-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.btn-content {
  flex: 1;
}

.btn-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #333;
}

.btn-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.existing-account {
  margin-top: 20px;
}

.form-title {
  text-align: center;
  margin: 0 0 30px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.form-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  gap: 16px;
  flex-wrap: wrap;
}

.demo-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 20px;
  align-items: center;
  flex-wrap: wrap;
}

/* Role Selection Styles */
.role-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.role-option .el-icon {
  color: #667eea;
}

@media (max-width: 480px) {
  .account-type-buttons {
    gap: 12px;
  }
  
  .account-type-btn {
    padding: 16px;
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .form-footer {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .demo-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
}
</style>
