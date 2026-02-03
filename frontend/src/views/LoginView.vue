<template>
  <div class="login-container">
    <!-- Background Elements -->
    <div class="background-pattern"></div>
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <!-- Main Login Card -->
    <div class="login-wrapper">
      <el-card class="login-card" shadow="hover">
        <!-- Header Section -->
        <template #header>
          <div class="login-header">
            <div class="logo-container">
              <div class="logo-icon">
                <el-icon size="32" color="white"><DataAnalysis /></el-icon>
              </div>
              <div class="logo-text">
                <h1>血液域分析平台</h1>
                <p>AI驱动的血液管理系统</p>
              </div>
            </div>
          </div>
        </template>

        <!-- Login Form -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="rules"
          label-width="0"
          size="large"
          @submit.prevent="handleLogin"
          class="login-form"
        >
          <!-- Email Field -->
          <el-form-item prop="email">
            <div class="input-group">
              <div class="input-label">
                <el-icon><Message /></el-icon>
                <span>邮箱地址</span>
              </div>
              <el-input
                v-model="loginForm.email"
                placeholder="请输入邮箱地址"
                prefix-icon="Message"
                size="large"
                class="custom-input"
              />
            </div>
          </el-form-item>

          <!-- Password Field -->
          <el-form-item prop="password">
            <div class="input-group">
              <div class="input-label">
                <el-icon><Lock /></el-icon>
                <span>密码</span>
              </div>
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                prefix-icon="Lock"
                size="large"
                show-password
                @keyup.enter="handleLogin"
                class="custom-input"
              />
            </div>
          </el-form-item>

          <!-- Role Selection -->
          <el-form-item>
            <div class="input-group">
              <div class="input-label">
                <el-icon><UserFilled /></el-icon>
                <span>登录身份</span>
              </div>
              <el-select
                v-model="loginForm.role"
                placeholder="选择登录身份"
                size="large"
                class="custom-select"
              >
                <el-option label="系统管理员" value="admin" />
                <el-option label="医生" value="doctor" />
                <el-option label="普通用户" value="user" />
                <el-option label="政府监管" value="government" />
              </el-select>
            </div>
          </el-form-item>

          <!-- Form Options -->
          <el-form-item>
            <div class="form-options">
              <el-checkbox v-model="loginForm.remember" class="remember-checkbox">
                记住我
              </el-checkbox>
              <el-link type="primary" @click="forgotPassword" class="forgot-link">
                忘记密码？
              </el-link>
            </div>
          </el-form-item>

          <!-- Submit Button -->
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
            >
              <template #loading>
                <el-icon class="loading-icon"><Loading /></el-icon>
              </template>
              登录
            </el-button>
          </el-form-item>

          <!-- Divider -->
          <el-divider class="divider">
            <span class="divider-text">或</span>
          </el-divider>

          <!-- Register Section -->
          <el-form-item>
            <div class="register-section">
              <p class="register-text">没有账户？</p>
              <el-button type="success" size="large" class="register-button" @click="goToRegister">
                <el-icon class="button-icon"><Plus /></el-icon>
                创建账户
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- Footer -->
      <div class="login-footer">
        <div class="footer-links">
          <el-link @click="showTerms">服务条款</el-link>
          <el-link @click="showPrivacy">隐私政策</el-link>
          <el-link @click="showSupport">支持</el-link>
        </div>
        <div class="copyright">
          <p>&copy; 2024 血液域分析平台. 版权所有.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, Lock, DataAnalysis, Loading, Plus, UserFilled } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  email: '',
  password: '',
  role: 'admin',
  remember: false
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    // Use authStore login method
    const result = await authStore.login({
      username: loginForm.email,
      password: loginForm.password,
      role: loginForm.role
    })
    
    if (result.success) {
      ElMessage.success('登录成功')
      
      // Redirect based on role
      if (loginForm.role === 'admin') {
        router.push('/admin/dashboard')
      } else if (loginForm.role === 'doctor') {
        router.push('/doctor/dashboard')
      } else if (loginForm.role === 'government') {
        router.push('/government/dashboard')
      } else {
        router.push('/user/dashboard')
      }
    } else {
      ElMessage.error(result.error || '登录失败')
    }
  } catch (error) {
    loading.value = false
    ElMessage.error('登录失败，请重试')
  }
}

const forgotPassword = () => {
  ElMessage.info('密码重置链接已发送至您的邮箱')
}

const goToRegister = () => {
  router.push('/register')
}

const showTerms = () => {
  ElMessage.info('服务条款 - 即将推出')
}

const showPrivacy = () => {
  ElMessage.info('隐私政策 - 即将推出')
}

const showSupport = () => {
  ElMessage.info('支持 - 联系 admin@blooddomain.com')
}

onMounted(() => {
  // Initialize component
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.background-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.floating-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 60px;
  height: 60px;
  top: 70%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  right: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 480px;
}

.login-card {
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 10px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 20px 0;
  position: relative;
}

.login-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  right: 20%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.logo-text h1 {
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.logo-text p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

.language-selector {
  flex-shrink: 0;
}

.login-form {
  padding: 0 8px;
}

.input-group {
  width: 100%;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.custom-input,
.custom-select {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
  width: 100%;
}

.custom-input:focus,
.custom-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.custom-select .el-input__wrapper {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

.custom-select .el-input__wrapper:hover {
  border-color: #667eea;
}

.custom-select .el-input__wrapper.is-focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0;
}

.remember-checkbox {
  font-weight: 500;
}

.forgot-link {
  font-weight: 600;
  color: #667eea;
}

.login-button {
  width: 100%;
  height: 52px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.divider {
  margin: 24px 0;
  border-color: #e5e7eb;
}

.divider-text {
  color: #64748b;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.95);
  padding: 0 12px;
}

.register-section {
  text-align: center;
}

.register-text {
  margin-bottom: 16px;
  color: #64748b;
  font-size: 14px;
}

.register-button {
  width: 100%;
  height: 52px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  position: relative;
  overflow: hidden;
}

.register-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.register-button:hover::before {
  left: 100%;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
}

.button-icon {
  margin-right: 8px;
}

.login-footer {
  margin-top: 32px;
  text-align: center;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
}

.footer-links .el-link {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.footer-links .el-link:hover {
  color: white;
}

.copyright {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  margin: 0;
}

@media (max-width: 768px) {
  .login-container {
    padding: 16px;
  }
  
  .login-wrapper {
    max-width: 100%;
  }
  
  .logo-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .footer-links {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
