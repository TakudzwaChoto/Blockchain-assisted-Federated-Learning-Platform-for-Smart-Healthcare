<template>
  <div class="auth-selection-container">
    <!-- Background Elements -->
    <div class="background-pattern"></div>
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
      <div class="shape shape-4"></div>
    </div>

    <!-- Main Content -->
    <div class="auth-wrapper">
      <!-- Platform Header -->
      <div class="platform-header">
        <div class="platform-logo">
          <div class="logo-icon">
            <el-icon size="48" color="white"><DataAnalysis /></el-icon>
          </div>
          <div class="logo-text">
            <h1>{{ t('platform.name') }}</h1>
            <p>{{ t('platform.subtitle') }}</p>
          </div>
        </div>
        <div class="language-selector">
          <LanguageSwitcher />
        </div>
      </div>

      <!-- Welcome Message -->
      <div class="welcome-section">
        <h2 class="welcome-title">欢迎</h2>
        <p class="welcome-subtitle">选择您的账户类型开始使用系统</p>
      </div>

      <!-- User Type Selection -->
      <div class="user-type-selection">
        <h3 class="selection-title">选择用户类型</h3>
        
        <div class="user-cards">
          <!-- Admin Card -->
          <div class="user-card admin-card" @click="goToAdminLogin">
            <div class="card-header">
              <div class="card-icon">
                <el-icon size="36"><UserFilled /></el-icon>
              </div>
              <div class="card-badge">
                <el-tag type="danger" size="small" effect="dark">管理员</el-tag>
              </div>
            </div>
            <div class="card-content">
              <h4 class="card-title">管理员</h4>
              <p class="card-description">系统管理员，管理所有用户和系统设置</p>
              <div class="feature-list">
                <div class="feature-item">
                  <el-icon class="feature-icon"><Setting /></el-icon>
                  <span>系统管理</span>
                </div>
                <div class="feature-item">
                  <el-icon class="feature-icon"><DataAnalysis /></el-icon>
                  <span>完整分析</span>
                </div>
                <div class="feature-item">
                  <el-icon class="feature-icon"><User /></el-icon>
                  <span>用户控制</span>
                </div>
              </div>
              <div class="card-action">
                <el-button type="danger" size="large" class="action-button admin-button">
                  <el-icon class="button-icon"><ArrowRight /></el-icon>
                  管理员登录
                </el-button>
              </div>
            </div>
          </div>

          <!-- Doctor Card -->
          <div class="user-card doctor-card" @click="goToDoctorLogin">
            <div class="card-header">
              <div class="card-icon">
                <el-icon size="36"><Stethoscope /></el-icon>
              </div>
              <div class="card-badge">
                <el-tag type="primary" size="small" effect="dark">医生</el-tag>
              </div>
            </div>
            <div class="card-content">
              <h4 class="card-title">医生用户</h4>
              <p class="card-description">医生用户，管理患者和输血申请</p>
              <div class="feature-list">
                <div class="feature-item">
                  <el-icon class="feature-icon"><Monitor /></el-icon>
                  <span>患者管理</span>
                </div>
                <div class="feature-item">
                  <el-icon class="feature-icon"><Document /></el-icon>
                  <span>医疗记录</span>
                </div>
                <div class="feature-item">
                  <el-icon class="feature-icon"><TrendCharts /></el-icon>
                  <span>血液分析</span>
                </div>
              </div>
              <div class="card-action">
                <el-button type="primary" size="large" class="action-button doctor-button">
                  <el-icon class="button-icon"><ArrowRight /></el-icon>
                  医生登录
                </el-button>
              </div>
            </div>
          </div>

          <!-- Regular User Card -->
          <div class="user-card user-card" @click="goToUserLogin">
            <div class="card-header">
              <div class="card-icon">
                <el-icon size="36"><User /></el-icon>
              </div>
              <div class="card-badge">
                <el-tag type="success" size="small" effect="dark">用户</el-tag>
              </div>
            </div>
            <div class="card-content">
              <h4 class="card-title">普通用户</h4>
              <p class="card-description">个人用户，查看个人数据和申请用血</p>
              <div class="feature-list">
                <div class="feature-item">
                  <el-icon class="feature-icon"><View /></el-icon>
                  <span>查看报告</span>
                </div>
                <div class="feature-item">
                  <el-icon class="feature-icon"><Bell /></el-icon>
                  <span>通知</span>
                </div>
                <div class="feature-item">
                  <el-icon class="feature-icon"><Iphone /></el-icon>
                  <span>移动端访问</span>
                </div>
              </div>
              <div class="card-action">
                <el-button type="success" size="large" class="action-button user-button">
                  <el-icon class="button-icon"><ArrowRight /></el-icon>
                  用户登录
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Alternative Actions -->
      <div class="alternative-actions">
        <div class="action-links">
          <el-link @click="goToHome" class="home-link">
            <el-icon class="link-icon"><House /></el-icon>
            返回首页
          </el-link>
          <el-link @click="showHelp" class="help-link">
            <el-icon class="link-icon"><QuestionFilled /></el-icon>
            需要帮助？
          </el-link>
        </div>
      </div>

      <!-- Footer -->
      <div class="auth-footer">
        <div class="footer-content">
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
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  DataAnalysis, User, Plus, CircleCheck, Star, ArrowRight, House, QuestionFilled,
  UserFilled, Stethoscope, Setting, Monitor, Document, TrendCharts, View, Bell, Iphone
} from '@element-plus/icons-vue'

const router = useRouter()

const goToAdminLogin = () => {
  router.push('/login')
}

const goToDoctorLogin = () => {
  router.push('/login')
}

const goToUserLogin = () => {
  router.push('/login')
}

const goToHome = () => {
  router.push('/')
}

const showHelp = () => {
  ElMessage.info('帮助信息 - 即将推出')
}

const showTerms = () => {
  ElMessage.info('服务条款 - 即将推出')
}

const showPrivacy = () => {
  ElMessage.info('隐私政策 - 即将推出')
}

const showSupport = () => {
  ElMessage.info('支持信息 - 即将推出')
}

onMounted(() => {
  // Initialize component
})
</script>

<style scoped>
.auth-selection-container {
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
    radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 60% 70%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
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
  animation: float 8s ease-in-out infinite;
}

.shape-1 {
  width: 120px;
  height: 120px;
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}

.shape-2 {
  width: 80px;
  height: 80px;
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 15%;
  left: 15%;
  animation-delay: 4s;
}

.shape-4 {
  width: 60px;
  height: 60px;
  top: 30%;
  right: 25%;
  animation-delay: 6s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(180deg); }
}

.auth-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 900px;
}

.platform-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 48px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.platform-logo {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
}

.logo-text h1 {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 800;
  color: white;
  letter-spacing: -1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo-text p {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: 600;
}

.language-selector {
  flex-shrink: 0;
}

.welcome-section {
  text-align: center;
  margin-bottom: 48px;
}

.welcome-title {
  font-size: 36px;
  font-weight: 800;
  color: white;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.welcome-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  font-weight: 500;
}

.user-type-selection {
  margin-bottom: 48px;
}

.selection-title {
  font-size: 28px;
  font-weight: 800;
  color: white;
  text-align: center;
  margin: 0 0 40px 0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.5px;
}

.user-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.user-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 36px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 30px 60px rgba(0, 0, 0, 0.2),
    0 15px 30px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.user-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.admin-card::before {
  background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%);
}

.doctor-card::before {
  background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
}

.user-card::before {
  background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%);
}

.user-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 
    0 40px 80px rgba(0, 0, 0, 0.25),
    0 20px 40px rgba(0, 0, 0, 0.2);
}

.user-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  transition: all 0.6s ease;
  opacity: 0;
}

.user-card:hover::after {
  opacity: 1;
  animation: shimmer 0.6s ease;
}

@keyframes shimmer {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.admin-card .card-icon {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  color: white;
}

.doctor-card .card-icon {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  color: white;
}

.user-card .card-icon {
  background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
  color: white;
}

.card-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
  border-radius: 20px;
}

.card-badge {
  flex-shrink: 0;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card-title {
  font-size: 24px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.5px;
}

.card-description {
  color: #64748b;
  font-size: 16px;
  line-height: 1.6;
  margin: 0;
  font-weight: 500;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 15px;
  color: #374151;
  font-weight: 600;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  transform: translateX(4px);
}

.feature-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.admin-card .feature-icon {
  color: #dc2626;
}

.doctor-card .feature-icon {
  color: #2563eb;
}

.user-card .feature-icon {
  color: #16a34a;
}

.card-action {
  margin-top: 8px;
}

.action-button {
  width: 100%;
  height: 56px;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 700;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
  transition: all 0.3s ease;
}

.action-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.6s ease;
}

.action-button:hover::before {
  left: 100%;
}

.admin-button {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  box-shadow: 0 8px 24px rgba(220, 38, 38, 0.3);
}

.doctor-button {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
}

.user-button {
  background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.3);
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.admin-button:hover {
  box-shadow: 0 12px 32px rgba(220, 38, 38, 0.4);
}

.doctor-button:hover {
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.4);
}

.user-button:hover {
  box-shadow: 0 12px 32px rgba(22, 163, 74, 0.4);
}

.button-icon {
  margin-right: 12px;
  font-size: 20px;
}

.alternative-actions {
  text-align: center;
  margin-bottom: 48px;
}

.action-links {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.home-link,
.help-link {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.home-link:hover,
.help-link:hover {
  color: white;
  transform: translateY(-2px);
}

.link-icon {
  font-size: 18px;
}

.auth-footer {
  text-align: center;
}

.footer-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.footer-links .el-link {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
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
  .auth-selection-container {
    padding: 16px;
  }
  
  .auth-wrapper {
    max-width: 100%;
  }
  
  .platform-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .logo-text h1 {
    font-size: 24px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .account-cards {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .action-links {
    flex-direction: column;
    gap: 16px;
  }
  
  .footer-links {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
