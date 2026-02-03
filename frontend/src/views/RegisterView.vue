<template>
  <div class="register-container">
    <!-- Background Elements -->
    <div class="background-pattern"></div>
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <!-- Main Register Card -->
    <div class="register-wrapper">
      <el-card class="register-card" shadow="hover">
        <!-- Header Section -->
        <template #header>
          <div class="register-header">
            <div class="logo-container">
              <div class="logo-icon">
                <el-icon size="32" color="white"><DataAnalysis /></el-icon>
              </div>
              <div class="logo-text">
                <h1>{{ t('register.title') }}</h1>
                <p>{{ t('register.subtitle') }}</p>
              </div>
            </div>
            <div class="language-selector">
              <LanguageSwitcher />
            </div>
          </div>
        </template>
        <!-- Progress Steps -->
        <div class="progress-steps">
          <div class="step" :class="{ active: currentStep >= 1 }">
            <div class="step-number">1</div>
            <div class="step-label">{{ t('register.accountInfo') }}</div>
          </div>
          <div class="step" :class="{ active: currentStep >= 2 }">
            <div class="step-number">2</div>
            <div class="step-label">{{ t('register.personalInfo') }}</div>
          </div>
          <div class="step" :class="{ active: currentStep >= 3 }">
            <div class="step-number">3</div>
            <div class="step-label">{{ t('register.confirmation') }}</div>
          </div>
        </div>

        <!-- Account Type Selection -->
        <div class="account-type-selector">
          <div class="selector-header">
            <h3 class="selector-title">{{ t('register.selectAccountType') }}</h3>
            <p class="selector-subtitle">{{ t('register.accountTypeDescription') }}</p>
          </div>
          <div class="account-types">
            <div 
              class="account-type-option" 
              :class="{ active: registerForm.role === 'admin' }"
              @click="selectAccountType('admin')"
            >
              <div class="option-icon">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="option-content">
                <h4>{{ t('register.administrator') }}</h4>
                <p>{{ t('register.adminDescription') }}</p>
              </div>
              <div class="option-check">
                <el-icon v-if="registerForm.role === 'admin'"><CircleCheck /></el-icon>
              </div>
            </div>
            <div 
              class="account-type-option" 
              :class="{ active: registerForm.role === 'doctor' }"
              @click="selectAccountType('doctor')"
            >
              <div class="option-icon">
                <el-icon><Stethoscope /></el-icon>
              </div>
              <div class="option-content">
                <h4>{{ t('register.doctor') }}</h4>
                <p>{{ t('register.doctorDescription') }}</p>
              </div>
              <div class="option-check">
                <el-icon v-if="registerForm.role === 'doctor'"><CircleCheck /></el-icon>
              </div>
            </div>
            <div 
              class="account-type-option" 
              :class="{ active: registerForm.role === 'user' }"
              @click="selectAccountType('user')"
            >
              <div class="option-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="option-content">
                <h4>{{ t('register.regularUser') }}</h4>
                <p>{{ t('register.userDescription') }}</p>
              </div>
              <div class="option-check">
                <el-icon v-if="registerForm.role === 'user'"><CircleCheck /></el-icon>
              </div>
            </div>
            <div 
              class="account-type-option" 
              :class="{ active: registerForm.role === 'government' }"
              @click="selectAccountType('government')"
            >
              <div class="option-icon">
                <el-icon><OfficeBuilding /></el-icon>
              </div>
              <div class="option-content">
                <h4>政府监管</h4>
                <p>卫生健康委员会监管人员，负责血液管理政策制定和监督执行</p>
              </div>
              <div class="option-check">
                <el-icon v-if="registerForm.role === 'government'"><CircleCheck /></el-icon>
              </div>
            </div>
          </div>
        </div>

        <!-- Password Strength Indicator -->
        <div class="password-strength-section" v-if="registerForm.password">
          <div class="strength-header">
            <h4>{{ t('register.passwordStrength') }}</h4>
            <div class="strength-meter">
              <div class="strength-bar" :class="passwordStrengthClass">
                <div class="strength-fill" :style="{ width: passwordStrengthWidth }"></div>
              </div>
              <span class="strength-text" :class="passwordStrengthClass">
                {{ t(`register.strength.${passwordStrength}`) }}
              </span>
            </div>
          </div>
          <div class="requirements-list">
            <div class="requirement" :class="{ met: meetsLengthRequirement }">
              <el-icon class="req-icon"><CircleCheck v-if="meetsLengthRequirement" /><CircleClose v-else /></el-icon>
              <span>{{ t('register.requirements.length') }}</span>
            </div>
            <div class="requirement" :class="{ met: meetsUppercaseRequirement }">
              <el-icon class="req-icon"><CircleCheck v-if="meetsUppercaseRequirement" /><CircleClose v-else /></el-icon>
              <span>{{ t('register.requirements.uppercase') }}</span>
            </div>
            <div class="requirement" :class="{ met: meetsLowercaseRequirement }">
              <el-icon class="req-icon"><CircleCheck v-if="meetsLowercaseRequirement" /><CircleClose v-else /></el-icon>
              <span>{{ t('register.requirements.lowercase') }}</span>
            </div>
            <div class="requirement" :class="{ met: meetsNumberRequirement }">
              <el-icon class="req-icon"><CircleCheck v-if="meetsNumberRequirement" /><CircleClose v-else /></el-icon>
              <span>{{ t('register.requirements.number') }}</span>
            </div>
            <div class="requirement" :class="{ met: meetsSpecialRequirement }">
              <el-icon class="req-icon"><CircleCheck v-if="meetsSpecialRequirement" /><CircleClose v-else /></el-icon>
              <span>{{ t('register.requirements.special') }}</span>
            </div>
          </div>
        </div>

        <!-- Security Features -->
        <div class="security-features">
          <div class="features-header">
            <h3>{{ t('register.securityFeatures') }}</h3>
            <p>{{ t('register.securityDescription') }}</p>
          </div>
          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><Lock /></el-icon>
              </div>
              <div class="feature-text">
                <h4>{{ t('register.encryption') }}</h4>
                <p>{{ t('register.encryptionDesc') }}</p>
              </div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><Shield /></el-icon>
              </div>
              <div class="feature-text">
                <h4>{{ t('register.twoFactor') }}</h4>
                <p>{{ t('register.twoFactorDesc') }}</p>
              </div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="feature-text">
                <h4>{{ t('register.monitoring') }}</h4>
                <p>{{ t('register.monitoringDesc') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Advanced AI Assistant -->
        <div class="ai-assistant">
          <div class="ai-header">
            <div class="ai-icon">
              <el-icon><MagicStick /></el-icon>
            </div>
            <div class="ai-title">
              <h3>{{ t('register.aiAssistant') }}</h3>
              <p>{{ t('register.aiDescription') }}</p>
            </div>
            <div class="ai-status">
              <div class="status-dot"></div>
              <span>{{ t('register.aiOnline') }}</span>
            </div>
          </div>
          <div class="ai-chat">
            <div class="chat-messages" ref="chatMessages">
              <div class="message ai-message">
                <div class="message-avatar">
                  <el-icon><MagicStick /></el-icon>
                </div>
                <div class="message-content">
                  <p>{{ t('register.aiWelcome') }}</p>
                </div>
              </div>
              <div v-for="(message, index) in chatHistory" :key="index" 
                   :class="['message', message.type + '-message']">
                <div class="message-avatar">
                  <el-icon v-if="message.type === 'ai'"><MagicStick /></el-icon>
                  <el-icon v-else><User /></el-icon>
                </div>
                <div class="message-content">
                  <p>{{ message.text }}</p>
                </div>
              </div>
            </div>
            <div class="chat-input">
              <el-input
                v-model="chatInput"
                :placeholder="t('register.aiPlaceholder')"
                @keyup.enter="sendAiMessage"
                class="ai-input"
              >
                <template #append>
                  <el-button @click="sendAiMessage" type="primary" class="send-button">
                    <el-icon><Promotion /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </div>
          </div>
        </div>

        <!-- Biometric Authentication -->
        <div class="biometric-section">
          <div class="biometric-header">
            <h3>{{ t('register.biometricAuth') }}</h3>
            <p>{{ t('register.biometricDescription') }}</p>
          </div>
          <div class="biometric-options">
            <div class="biometric-card" @click="enableBiometric('fingerprint')">
              <div class="biometric-icon">
                <el-icon><Fingerprint /></el-icon>
              </div>
              <div class="biometric-info">
                <h4>{{ t('register.fingerprint') }}</h4>
                <p>{{ t('register.fingerprintDesc') }}</p>
              </div>
              <div class="biometric-toggle">
                <el-switch v-model="biometricEnabled.fingerprint" />
              </div>
            </div>
            <div class="biometric-card" @click="enableBiometric('face')">
              <div class="biometric-icon">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="biometric-info">
                <h4>{{ t('register.faceRecognition') }}</h4>
                <p>{{ t('register.faceDesc') }}</p>
              </div>
              <div class="biometric-toggle">
                <el-switch v-model="biometricEnabled.face" />
              </div>
            </div>
            <div class="biometric-card" @click="enableBiometric('voice')">
              <div class="biometric-icon">
                <el-icon><Microphone /></el-icon>
              </div>
              <div class="biometric-info">
                <h4>{{ t('register.voiceRecognition') }}</h4>
                <p>{{ t('register.voiceDesc') }}</p>
              </div>
              <div class="biometric-toggle">
                <el-switch v-model="biometricEnabled.voice" />
              </div>
            </div>
          </div>
        </div>

        <!-- Advanced Analytics Preview -->
        <div class="analytics-preview">
          <div class="analytics-header">
            <h3>{{ t('register.analyticsPreview') }}</h3>
            <p>{{ t('register.analyticsDescription') }}</p>
          </div>
          <div class="analytics-grid">
            <div class="analytics-card">
              <div class="analytics-icon">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="analytics-content">
                <h4>{{ t('register.realTimeAnalytics') }}</h4>
                <div class="analytics-metrics">
                  <div class="metric">
                    <span class="metric-value">2,847</span>
                    <span class="metric-label">{{ t('register.activeUsers') }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-value">98.2%</span>
                    <span class="metric-label">{{ t('register.uptime') }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="analytics-card">
              <div class="analytics-icon">
                <el-icon><DataAnalysis /></el-icon>
              </div>
              <div class="analytics-content">
                <h4>{{ t('register.bloodInventory') }}</h4>
                <div class="inventory-bars">
                  <div class="inventory-bar">
                    <div class="bar-label">A+</div>
                    <div class="bar-progress">
                      <div class="bar-fill" style="width: 75%"></div>
                    </div>
                    <span class="bar-value">75%</span>
                  </div>
                  <div class="inventory-bar">
                    <div class="bar-label">B+</div>
                    <div class="bar-progress">
                      <div class="bar-fill" style="width: 60%"></div>
                    </div>
                    <span class="bar-value">60%</span>
                  </div>
                  <div class="inventory-bar">
                    <div class="bar-label">O+</div>
                    <div class="bar-progress">
                      <div class="bar-fill" style="width: 90%"></div>
                    </div>
                    <span class="bar-value">90%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Smart Recommendations -->
        <div class="recommendations-section">
          <div class="recommendations-header">
            <h3>{{ t('register.smartRecommendations') }}</h3>
            <p>{{ t('register.recommendationsDescription') }}</p>
          </div>
          <div class="recommendations-list">
            <div class="recommendation-item">
              <div class="rec-icon">
                <el-icon><Star /></el-icon>
              </div>
              <div class="rec-content">
                <h4>{{ t('register.recommendation1') }}</h4>
                <p>{{ t('register.recommendation1Desc') }}</p>
              </div>
              <div class="rec-action">
                <el-button size="small" type="primary">{{ t('register.apply') }}</el-button>
              </div>
            </div>
            <div class="recommendation-item">
              <div class="rec-icon">
                <el-icon><Lightning /></el-icon>
              </div>
              <div class="rec-content">
                <h4>{{ t('register.recommendation2') }}</h4>
                <p>{{ t('register.recommendation2Desc') }}</p>
              </div>
              <div class="rec-action">
                <el-button size="small" type="primary">{{ t('register.apply') }}</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- Register Form -->
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="rules"
          label-width="0"
          size="large"
          @submit.prevent="handleRegister"
          class="register-form"
        >
          <!-- Account Information -->
          <div class="form-section">
            <h3 class="section-title">{{ t('register.accountInfo') }}</h3>
            
            <el-form-item prop="name">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><User /></el-icon>
                  <span>{{ t('register.fullName') }}</span>
                </div>
                <el-input
                  v-model="registerForm.name"
                  :placeholder="t('register.fullNamePlaceholder')"
                  prefix-icon="User"
                  size="large"
                  class="custom-input"
                />
              </div>
            </el-form-item>

            <el-form-item prop="email">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><Message /></el-icon>
                  <span>{{ t('register.email') }}</span>
                </div>
                <el-input
                  v-model="registerForm.email"
                  :placeholder="t('register.emailPlaceholder')"
                  prefix-icon="Message"
                  size="large"
                  class="custom-input"
                />
              </div>
            </el-form-item>

            <el-form-item prop="username">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><User /></el-icon>
                  <span>{{ t('register.username') }}</span>
                </div>
                <el-input
                  v-model="registerForm.username"
                  :placeholder="t('register.usernamePlaceholder')"
                  prefix-icon="User"
                  size="large"
                  class="custom-input"
                />
              </div>
            </el-form-item>
          </div>

          <!-- Personal Information -->
          <div class="form-section">
            <h3 class="section-title">{{ t('register.personalInfo') }}</h3>
            
            <el-form-item prop="phone">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><Phone /></el-icon>
                  <span>{{ t('register.phone') }}</span>
                </div>
                <el-input
                  v-model="registerForm.phone"
                  :placeholder="t('register.phonePlaceholder')"
                  prefix-icon="Phone"
                  size="large"
                  class="custom-input"
                />
              </div>
            </el-form-item>

            <el-form-item prop="department">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><OfficeBuilding /></el-icon>
                  <span>{{ t('register.department') }}</span>
                </div>
                <el-select
                  v-model="registerForm.department"
                  :placeholder="t('register.departmentPlaceholder')"
                  size="large"
                  class="custom-select"
                >
                  <el-option label="Blood Management Center" value="Blood Management Center" />
                  <el-option label="Emergency Services" value="Emergency Services" />
                  <el-option label="Hospital Administration" value="Hospital Administration" />
                  <el-option label="Research Laboratory" value="Research Laboratory" />
                </el-select>
              </div>
            </el-form-item>

            <el-form-item prop="role">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><UserFilled /></el-icon>
                  <span>{{ t('register.role') }}</span>
                </div>
                <el-select
                  v-model="registerForm.role"
                  :placeholder="t('register.rolePlaceholder')"
                  size="large"
                  class="custom-select"
                >
                  <el-option label="Administrator" value="admin" />
                  <el-option label="Doctor" value="doctor" />
                  <el-option label="User" value="user" />
                </el-select>
              </div>
            </el-form-item>
          </div>

          <!-- Security Information -->
          <div class="form-section">
            <h3 class="section-title">{{ t('register.securityInfo') }}</h3>
            
            <el-form-item prop="password">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><Lock /></el-icon>
                  <span>{{ t('register.password') }}</span>
                </div>
                <el-input
                  v-model="registerForm.password"
                  type="password"
                  :placeholder="t('register.passwordPlaceholder')"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                  class="custom-input"
                />
              </div>
            </el-form-item>

            <el-form-item prop="confirmPassword">
              <div class="input-group">
                <div class="input-label">
                  <el-icon><Lock /></el-icon>
                  <span>{{ t('register.confirmPassword') }}</span>
                </div>
                <el-input
                  v-model="registerForm.confirmPassword"
                  type="password"
                  :placeholder="t('register.confirmPasswordPlaceholder')"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                  class="custom-input"
                />
              </div>
            </el-form-item>
          </div>

          <!-- Terms and Conditions -->
          <el-form-item>
            <div class="terms-section">
              <el-checkbox v-model="registerForm.agreeTerms" class="terms-checkbox">
                {{ t('register.agreeTerms') }}
              </el-checkbox>
              <el-link type="primary" @click="showTerms" class="terms-link">
                {{ t('register.termsOfService') }}
              </el-link>
            </div>
          </el-form-item>

          <!-- Submit Button -->
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              :disabled="!registerForm.agreeTerms"
              class="register-button"
              @click="handleRegister"
            >
              <template #loading>
                <el-icon class="loading-icon"><Loading /></el-icon>
              </template>
              <el-icon class="button-icon"><Plus /></el-icon>
              {{ t('register.createAccount') }}
            </el-button>
          </el-form-item>

          <!-- Login Link -->
          <el-form-item>
            <div class="login-section">
              <p class="login-text">{{ t('register.hasAccount') }}</p>
              <el-link type="success" @click="goToLogin" class="login-link">
                {{ t('register.signIn') }}
              </el-link>
            </div>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- Footer -->
      <div class="register-footer">
        <div class="footer-links">
          <el-link @click="showTerms">{{ t('register.terms') }}</el-link>
          <el-link @click="showPrivacy">{{ t('register.privacy') }}</el-link>
          <el-link @click="showSupport">{{ t('register.support') }}</el-link>
        </div>
        <div class="copyright">
          <p>&copy; 2024 {{ t('app.name') }}. {{ t('register.allRights') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  User, Message, Lock, Phone, OfficeBuilding, UserFilled, Loading, Plus, DataAnalysis,
  CircleCheck, CircleClose, Stethoscope, Shield, Monitor, MagicStick, Promotion,
  Fingerprint, Microphone, TrendCharts, Star, Lightning
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const registerFormRef = ref()
const loading = ref(false)
const currentStep = ref(1)
const chatMessages = ref(null)

const registerForm = reactive({
  name: '',
  email: '',
  username: '',
  phone: '',
  department: '',
  role: 'user',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

// AI Assistant
const chatInput = ref('')
const chatHistory = ref([])

const sendAiMessage = () => {
  if (!chatInput.value.trim()) return
  
  // Add user message
  chatHistory.value.push({
    type: 'user',
    text: chatInput.value
  })
  
  const userMessage = chatInput.value
  chatInput.value = ''
  
  // Simulate AI response
  setTimeout(() => {
    let aiResponse = ''
    
    if (userMessage.toLowerCase().includes('password')) {
      aiResponse = t('register.aiPasswordHelp')
    } else if (userMessage.toLowerCase().includes('security')) {
      aiResponse = t('register.aiSecurityHelp')
    } else if (userMessage.toLowerCase().includes('account')) {
      aiResponse = t('register.aiAccountHelp')
    } else {
      aiResponse = t('register.aiDefaultResponse')
    }
    
    chatHistory.value.push({
      type: 'ai',
      text: aiResponse
    })
    
    // Scroll to bottom
    nextTick(() => {
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight
      }
    })
  }, 1000)
}

// Biometric Authentication
const biometricEnabled = reactive({
  fingerprint: false,
  face: false,
  voice: false
})

const enableBiometric = (type) => {
  biometricEnabled[type] = !biometricEnabled[type]
  
  if (biometricEnabled[type]) {
    ElMessage.success(t(`register.biometricEnabled.${type}`))
  }
}

// Password strength computation
const passwordStrength = computed(() => {
  const password = registerForm.password
  if (!password) return 'empty'
  
  let strength = 0
  if (password.length >= 8) strength++
  if (password.length >= 12) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  
  if (strength <= 2) return 'weak'
  if (strength <= 4) return 'medium'
  return 'strong'
})

const passwordStrengthClass = computed(() => {
  return `strength-${passwordStrength.value}`
})

const passwordStrengthWidth = computed(() => {
  const strength = passwordStrength.value
  if (strength === 'empty') return '0%'
  if (strength === 'weak') return '33%'
  if (strength === 'medium') return '66%'
  return '100%'
})

// Password requirements
const meetsLengthRequirement = computed(() => registerForm.password.length >= 8)
const meetsUppercaseRequirement = computed(() => /[A-Z]/.test(registerForm.password))
const meetsLowercaseRequirement = computed(() => /[a-z]/.test(registerForm.password))
const meetsNumberRequirement = computed(() => /[0-9]/.test(registerForm.password))
const meetsSpecialRequirement = computed(() => /[^A-Za-z0-9]/.test(registerForm.password))

// Account type selection
const selectAccountType = (type) => {
  registerForm.role = type
  updateStepProgress()
}

const updateStepProgress = () => {
  const hasAccountInfo = registerForm.name && registerForm.email && registerForm.username
  const hasPersonalInfo = registerForm.phone && registerForm.department && registerForm.role
  const hasSecurityInfo = registerForm.password && registerForm.confirmPassword
  
  if (hasSecurityInfo) {
    currentStep.value = 3
  } else if (hasPersonalInfo) {
    currentStep.value = 2
  } else if (hasAccountInfo) {
    currentStep.value = 1
  } else {
    currentStep.value = 1
  }
}

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error(t('register.passwordRequired')))
  } else if (value.length < 8) {
    callback(new Error(t('register.passwordMinLength')))
  } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&].{8,}$/.test(value)) {
    callback(new Error(t('register.passwordRequirements')))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error(t('register.confirmPasswordRequired')))
  } else if (value !== registerForm.password) {
    callback(new Error(t('register.passwordMismatch')))
  } else {
    callback()
  }
}

const rules = {
  name: [
    { required: true, message: t('register.nameRequired'), trigger: 'blur' },
    { min: 2, message: t('register.nameMinLength'), trigger: 'blur' }
  ],
  email: [
    { required: true, message: t('register.emailRequired'), trigger: 'blur' },
    { type: 'email', message: t('register.emailInvalid'), trigger: ['blur', 'change'] }
  ],
  username: [
    { required: true, message: t('register.usernameRequired'), trigger: 'blur' },
    { min: 3, message: t('register.usernameMinLength'), trigger: 'blur' }
  ],
  phone: [
    { required: true, message: t('register.phoneRequired'), trigger: 'blur' },
    { pattern: /^[\d\s\-\(\)]+$/, message: t('register.phoneInvalid'), trigger: 'blur' }
  ],
  department: [
    { required: true, message: t('register.departmentRequired'), trigger: 'change' }
  ],
  role: [
    { required: true, message: t('register.roleRequired'), trigger: 'change' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  agreeTerms: [
    { required: true, message: t('register.termsRequired'), trigger: 'change' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    // Simulate registration API call
    setTimeout(() => {
      loading.value = false
      
      // Set user data and role
      authStore.setUser({
        id: 1,
        name: registerForm.name,
        email: registerForm.email,
        role: registerForm.role,
        department: registerForm.department
      })
      
      ElMessage.success(t('register.success'))
      router.push('/admin/dashboard')
    }, 2000)
  } catch (error) {
    loading.value = false
    ElMessage.error(t('register.failed'))
  }
}

const goToLogin = () => {
  router.push('/login')
}

const showTerms = () => {
  ElMessage.info(t('register.termsInfo'))
}

const showPrivacy = () => {
  ElMessage.info(t('register.privacyInfo'))
}

const showSupport = () => {
  ElMessage.info(t('register.supportInfo'))
}

onMounted(() => {
  // Initialize component
})
</script>

<style scoped>
.register-container {

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

  .register-wrapper {
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 600px;
  }

  .register-card {
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 
      0 20px 40px rgba(0, 0, 0, 0.15),
      0 10px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .register-header {
    text-align: center;
    margin-bottom: 32px;
    padding: 20px 0;
    position: relative;
  }

  .register-header::after {
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

  .progress-steps {
    display: flex;
    justify-content: space-between;
    margin-bottom: 32px;
    padding: 0 20px;
  }

  .step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    position: relative;
  }

  .step::before {
    content: '';
    position: absolute;
    top: 20px;
    left: 50%;
    right: 0;
    height: 2px;
    background: #e5e7eb;
    z-index: 1;
  }

  .step.active::before {
    background: #667eea;
  }

  .step-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #e5e7eb;
    color: #9ca3af;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 8px;
    position: relative;
    z-index: 2;
  }

  .step.active .step-number {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .step-label {
    font-size: 12px;
    color: #64748b;
    font-weight: 500;
    text-align: center;
  }

  .step.active .step-label {
    color: #1e293b;
    font-weight: 600;
  }

  .register-form {
    padding: 0 8px;
  }

  .account-types {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 32px;
  }

  .account-type-option {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    border: 2px solid #e5e7eb;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
  }

  .account-type-option:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    transform: translateY(-2px);
  }

  .account-type-option.active {
    border-color: #667eea;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
  }

  .option-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    flex-shrink: 0;
  }

  .option-content {
    flex: 1;
  }

  .option-content h4 {
    margin: 0 0 4px 0;
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
  }

  .option-content p {
    margin: 0;
    font-size: 14px;
    color: #64748b;
    line-height: 1.5;
  }

  .option-check {
    color: #667eea;
    font-size: 20px;
    flex-shrink: 0;
  }

  .form-section {
    margin-bottom: 32px;
  }

  .section-title {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #e5e7eb;
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
  }

  .custom-input:focus,
  .custom-select:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  .terms-section {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 16px 0;
  }

  .terms-checkbox {
    font-weight: 500;
  }

  .terms-link {
    font-weight: 600;
    color: #667eea;
  }

  .register-button {
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

  .register-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  }

  .register-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .loading-icon {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .button-icon {
    margin-right: 8px;
  }

  .login-section {
    text-align: center;
  }

  .login-text {
    margin-bottom: 12px;
    color: #64748b;
    font-size: 14px;
  }

  .login-link {
    font-weight: 600;
    color: #10b981;
  }

  .register-footer {
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
    .register-container {
      padding: 16px;
    }
    
    .register-wrapper {
      max-width: 100%;
    }
    
    .progress-steps {
      flex-direction: column;
      gap: 16px;
    }
    
    .step::before {
      display: none;
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
}
</style>
