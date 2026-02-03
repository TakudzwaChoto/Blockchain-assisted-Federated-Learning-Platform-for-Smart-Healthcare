<template>
  <div class="landing-page">
    <!-- Navigation Header -->
    <header class="landing-header">
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <el-icon size="32" color="#667eea">
              <TrendCharts />
            </el-icon>
            <span class="logo-text">血液域分析平台</span>
          </div>
          <div class="header-actions">
                        <el-link @click="goToLogin" type="primary">
              登录
            </el-link>
            <el-button type="primary" @click="goToRegister">
              创建账户
            </el-button>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-pattern"></div>
      </div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">血液域分析平台</h1>
          <p class="hero-subtitle">
            AI驱动的血液管理和输血安全分析系统
          </p>
          <p class="hero-description">
              全面的血液库存管理、输血安全分析、捐献者管理和智能决策支持，为医疗机构提高输血安全和效率
            </p>
          <div class="hero-actions">
            <el-button type="primary" size="large" class="cta-button" @click="scrollToSection('pricing')">
              查看价格方案
              View Pricing Plans
            </el-button>
            <el-button size="large" class="secondary-button" @click="scrollToSection('features')">
              了解功能
            </el-button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="dashboard-preview">
            <div class="preview-header">
              <div class="preview-nav">
                <div class="nav-dots">
                  <span class="dot active"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </div>
                <div class="preview-time">实时数据</div>
              </div>
            </div>
            <div class="preview-content">
              <div class="preview-stats">
                <div class="stat-item">
                  <div class="stat-number">2,847</div>
                  <div class="stat-label">活跃捐献者</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">156</div>
                  <div class="stat-label">今日输血</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">98.5%</div>
                  <div class="stat-label">安全率</div>
                </div>
              </div>
              <div class="preview-chart">
                <div class="chart-bars">
                  <div class="chart-bar" style="height: 60%"></div>
                  <div class="chart-bar" style="height: 80%"></div>
                  <div class="chart-bar" style="height: 45%"></div>
                  <div class="chart-bar" style="height: 90%"></div>
                  <div class="chart-bar" style="height: 70%"></div>
                  <div class="chart-bar" style="height: 85%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">核心功能</h2>
          <p class="section-subtitle">
            全面的血液管理解决方案，涵盖从捐献者管理到输血安全的完整流程
          </p>
        </div>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">
              <el-icon :size="48">
                <component :is="feature.icon" />
              </el-icon>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
            <ul class="feature-list">
              <li v-for="item in feature.features" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section">
      <div class="container">
        <div class="benefits-content">
          <div class="benefits-text">
            <h2 class="benefits-title">为什么选择我们的平台？</h2>
            <div class="benefits-grid">
              <div class="benefit-item" v-for="benefit in benefits" :key="benefit.id">
                <div class="benefit-icon">
                  <el-icon :size="24">
                    <component :is="benefit.icon" />
                  </el-icon>
                </div>
                <div class="benefit-content">
                  <h4 class="benefit-name">{{ benefit.name }}</h4>
                  <p class="benefit-description">{{ benefit.description }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="benefits-visual">
            <div class="stats-showcase">
              <div class="showcase-item">
                <div class="showcase-number">500+</div>
                <div class="showcase-label">医疗机构</div>
              </div>
              <div class="showcase-item">
                <div class="showcase-number">50万+</div>
                <div class="showcase-label">捐献者数据</div>
              </div>
              <div class="showcase-item">
                <div class="showcase-number">99.9%</div>
                <div class="showcase-label">系统稳定性</div>
              </div>
              <div class="showcase-item">
                <div class="showcase-number">24/7</div>
                <div class="showcase-label">技术支持</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="pricing-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">选择适合您的方案</h2>
          <p class="section-subtitle">
            灵活的定价方案，满足不同规模医疗机构的需求
          </p>
        </div>
        <div class="pricing-grid">
          <div class="pricing-card" v-for="plan in pricingPlans" :key="plan.id">
            <div class="pricing-header">
              <h3 class="plan-name">{{ plan.name }}</h3>
              <div class="plan-price">
                <span class="price-currency">¥</span>
                <span class="price-amount">{{ plan.price }}</span>
                <span class="price-period">/月</span>
              </div>
              <p class="plan-description">{{ plan.description }}</p>
            </div>
            <div class="pricing-features">
              <ul class="features-list">
                <li v-for="feature in plan.features" :key="feature" class="feature-item">
                  <el-icon class="feature-check"><Check /></el-icon>
                  <span>{{ feature }}</span>
                </li>
              </ul>
            </div>
            <div class="pricing-action">
              <el-button 
                :type="plan.recommended ? 'primary' : 'default'"
                size="large"
                class="pricing-button"
                @click="handlePlanSelect(plan)"
              >
                {{ plan.recommended ? '立即开始' : '选择方案' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">准备提升您的血液管理水平？</h2>
          <p class="cta-description">
            立即注册账户，体验智能血液管理系统的强大功能
          </p>
          <div class="cta-actions">
            <el-button type="primary" size="large" @click="goToRegister">
              免费注册
            </el-button>
            <el-button size="large" @click="goToLogin">
              已有账户？登录
            </el-button>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <div class="footer-logo">
              <el-icon size="32" color="#667eea">
                <TrendCharts />
              </el-icon>
              <span class="logo-text">血液域分析平台</span>
            </div>
            <p class="footer-description">
              专业的血液管理和输血安全分析解决方案
            </p>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">产品功能</h4>
            <ul class="footer-links">
              <li><a href="#features">核心功能</a></li>
              <li><a href="#pricing">价格方案</a></li>
              <li><a href="#" @click="goToLogin">系统登录</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">支持服务</h4>
            <ul class="footer-links">
              <li><a href="#">技术支持</a></li>
              <li><a href="#">培训服务</a></li>
              <li><a href="#">API文档</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">联系我们</h4>
            <ul class="footer-links">
              <li>电话: 400-123-4567</li>
              <li>邮箱: support@blooddomain.com</li>
              <li>Address: Chaoyang District, Beijing</li>
            </ul>
          </div>
          <div class="footer-section">
            <FooterSocial />
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 血液域分析平台. 版权所有.</p>
        </div>
      </div>
    </footer>

    <!-- Payment Modal -->
    <el-dialog 
      v-model="showPaymentModal" 
      title="Select Payment Method" 
      width="600px"
      :before-close="() => { showPaymentModal = false; selectedPaymentMethod = '' }"
    >
      <div v-if="selectedPlan" class="payment-plan-info">
        <div class="selected-plan">
          <h3>{{ selectedPlan.name }}</h3>
          <div class="plan-price-display">
            <span class="price-currency">¥</span>
            <span class="price-amount">{{ selectedPlan.price }}</span>
            <span class="price-period">/月</span>
          </div>
          <p class="plan-description">{{ selectedPlan.description }}</p>
          
          <!-- Service Details -->
          <div class="service-details">
            <h4>You will get the following services:</h4>
            <div class="service-grid">
              <div v-for="feature in selectedPlan.features" :key="feature" class="service-item">
                <el-icon class="service-icon"><Check /></el-icon>
                <span>{{ feature }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="payment-methods">
        <h4>Select Payment Method</h4>
        <div class="methods-grid">
          <div 
            v-for="method in paymentMethods" 
            :key="method.id"
            class="payment-method-card"
            :class="{ 
              'selected': selectedPaymentMethod === method.id,
              'popular': method.popular 
            }"
            @click="handlePaymentMethodSelect(method)"
          >
            <div class="method-header">
              <div class="method-icon" :style="{ backgroundColor: method.color }">
                <el-icon size="24" color="white">
                  <component :is="getPaymentIcon(method.icon)" />
                </el-icon>
              </div>
              <div class="method-info">
                <h5>{{ method.name }}</h5>
                <p>{{ method.description }}</p>
              </div>
              <div class="method-badge" v-if="method.popular">
                <span>推荐</span>
              </div>
            </div>
            <div class="method-selected" v-if="selectedPaymentMethod === method.id">
              <el-icon color="#07C160" size="20"><Check /></el-icon>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="payment-actions">
          <el-button @click="showPaymentModal = false">Cancel</el-button>
          <el-button 
            type="primary" 
            :loading="paymentLoading"
            :disabled="!selectedPaymentMethod"
            @click="handlePayment"
          >
            Confirm Payment ¥{{ selectedPlan?.price || '0' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Payment Success Component -->
    <PaymentSuccess 
      v-if="purchaseCompleted"
      :purchased-plan="purchaseDetails.plan"
      :payment-method="purchaseDetails.paymentMethod"
      :order-id="purchaseDetails.orderId"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  TrendCharts, User, Document, Box, Warning, Monitor, 
  Setting, Check, Lock, Clock, DataAnalysis, CreditCard,
  Wallet, Money, Postcard
} from '@element-plus/icons-vue'
import FooterSocial from '../components/FooterSocial.vue'
import PaymentSuccess from '../components/PaymentSuccess.vue'

const router = useRouter()

// Features data
const features = ref([
  {
    id: 1,
    icon: 'User',
    title: '捐献者管理',
    description: '全面的捐献者信息管理，包括健康记录、捐献历史、资格审核等',
    features: [
      '捐献者档案管理',
      '健康状况跟踪',
      '捐献历史记录',
      '资格审核流程'
    ]
  },
  {
    id: 2,
    icon: 'Document',
    title: '输血请求管理',
    description: '标准化的输血请求流程，确保输血安全和合规性',
    features: [
      '在线申请提交',
      '血型匹配验证',
      '紧急请求处理'
    ]
  },
  {
    id: 3,
    icon: 'Box',
    title: '库存管理',
    description: '实时血液库存监控，配备智能警报和分配建议',
    features: [
      '实时库存监控',
      '过期提醒',
      '智能分配建议'
    ]
  },
  {
    id: 4,
    icon: 'DataAnalysis',
    title: '数据分析',
    description: '基于AI的数据分析，提供决策支持和趋势预测',
    features: [
      '使用趋势分析',
      '需求预测模型',
      '安全风险评估'
    ]
  }
])

// Benefits data
const benefits = ref([
  {
    id: 1,
    icon: 'Lock',
    name: '数据安全',
    description: '企业级加密保护，确保数据安全和隐私',
  },
  {
    id: 2,
    icon: 'Clock',
    name: '提高工作效率',
    description: '自动化流程减少手动操作，提高工作效率'
  },
  {
    id: 3,
    icon: 'Setting',
    name: '合规保证',
    description: '符合医疗行业标准，确保监管合规'
  },
  {
    id: 4,
    icon: 'Monitor',
    name: '效率提升',
    description: '自动化流程减少手动操作，提高工作效率'
  }
])

// Pricing plans
const pricingPlans = ref([
  {
    id: 1,
    name: '基础方案',
    price: '999',
    description: '适合小型医疗机构',
    features: [
      '最多50个用户',
      '基础捐献者管理',
      '库存监控',
      '标准报表',
      '邮件支持'
    ],
    recommended: false
  },
  {
    id: 2,
    name: '专业方案',
    price: '2,999',
    description: '适合中型医疗机构',
    features: [
      '最多200个用户',
      '完整捐献者管理',
      '智能库存管理',
      '高级数据分析',
      'API接口',
      '优先技术支持'
    ],
    recommended: true
  },
  {
    id: 3,
    name: '企业方案',
    price: '9,999',
    description: '适合大型医疗集团',
    features: [
      '无限用户',
      '所有功能模块',
      '定制开发',
      '专属服务器',
      '现场培训',
      '24/7专属支持'
    ],
    recommended: false
  }
])

// Payment Modal State
const showPaymentModal = ref(false)
const selectedPlan = ref(null)
const selectedPaymentMethod = ref('')
const paymentLoading = ref(false)
const purchaseCompleted = ref(false)
const purchaseDetails = ref({
  plan: null,
  paymentMethod: '',
  orderId: ''
})

// Payment Methods
const paymentMethods = ref([
  {
    id: 'wechat',
    name: 'WeChat Pay',
    icon: 'Wallet',
    description: 'Pay with WeChat QR code',
    color: '#07C160',
    popular: true
  },
  {
    id: 'alipay',
    name: 'Alipay',
    icon: 'CreditCard',
    description: 'Pay with Alipay QR code',
    color: '#1677FF',
    popular: true
  },
  {
    id: 'bank',
    name: 'Bank Transfer',
    icon: 'Postcard',
    description: 'Pay with bank card or online banking',
    color: '#FF6B35',
    popular: false
  },
  {
    id: 'paypal',
    name: 'PayPal',
    icon: 'Money',
    description: 'Pay with PayPal international payment',
    color: '#003087',
    popular: false
  }
])

// Methods
const scrollToSection = (sectionId) => {
  const element = window.document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const handlePlanSelect = (plan) => {
  selectedPlan.value = plan
  showPaymentModal.value = true
}

const handlePaymentMethodSelect = (method) => {
  selectedPaymentMethod.value = method.id
}

const handlePayment = async () => {
  if (!selectedPaymentMethod.value) {
    ElMessage.warning('Please select payment method')
    return
  }
  
  paymentLoading.value = true
  
  try {
    // Simulate payment processing
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const method = paymentMethods.find(m => m.id === selectedPaymentMethod.value)
    const orderId = 'BD' + Date.now() + Math.random().toString(36).substr(2, 9).toUpperCase()
    
    // Store purchase details
    purchaseDetails.value = {
      plan: selectedPlan.value,
      paymentMethod: selectedPaymentMethod.value,
      orderId: orderId
    }
    
    // Show success
    showPaymentModal.value = false
    purchaseCompleted.value = true
    
    ElMessage.success('支付成功！')
  } catch (error) {
    ElMessage.error('支付失败，请重试')
  } finally {
    paymentLoading.value = false
  }
}

const getPaymentIcon = (iconName) => {
  const iconMap = {
    'Wallet': Wallet,
    'CreditCard': CreditCard,
    'Postcard': Postcard,
    'Money': Money
  }
  return iconMap[iconName] || CreditCard
}

const goToRegister = () => {
  router.push('/login')
  // Trigger account creation flow after navigation
  setTimeout(() => {
    window.dispatchEvent(new CustomEvent('showAccountCreation'))
  }, 100)
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: #ffffff;
}

/* Landing Header */
.landing-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  z-index: 1000;
  padding: 16px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* Hero Section */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding-top: 80px; /* Account for fixed header */
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;
}

.hero-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-text {
  color: white;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
}

.hero-subtitle {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 16px;
  opacity: 0.9;
}

.hero-description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 40px;
  opacity: 0.8;
}

.hero-actions {
  display: flex;
  gap: 20px;
}

.cta-button {
  background: white;
  color: #667eea;
  border: none;
  font-weight: 600;
  padding: 16px 32px;
}

.cta-button:hover {
  background: #f8f9fa;
  color: #667eea;
}

.secondary-button {
  background: transparent;
  color: white;
  border: 2px solid white;
  font-weight: 600;
  padding: 14px 32px;
}

.secondary-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* Dashboard Preview */
.hero-visual {
  display: flex;
  justify-content: center;
}

.dashboard-preview {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 400px;
  overflow: hidden;
}

.preview-header {
  background: #f8f9fa;
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
}

.preview-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-dots {
  display: flex;
  gap: 6px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #dee2e6;
}

.dot.active {
  background: #667eea;
}

.preview-time {
  font-size: 12px;
  color: #666;
}

.preview-content {
  padding: 24px;
}

.preview-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.preview-chart {
  height: 120px;
  display: flex;
  align-items: flex-end;
  padding: 20px 0;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 100%;
  width: 100%;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
}

/* Common Section Styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 18px;
  color: #666;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* Features Section */
.features-section {
  padding: 100px 0;
  background: #f8f9fa;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.feature-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  color: #667eea;
  margin-bottom: 24px;
}

.feature-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.feature-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 24px;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.feature-list li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #667eea;
  font-weight: bold;
}

/* Benefits Section */
.benefits-section {
  padding: 100px 0;
  background: white;
}

.benefits-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.benefits-title {
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin-bottom: 40px;
}

.benefits-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.benefit-item {
  display: flex;
  gap: 16px;
}

.benefit-icon {
  color: #667eea;
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.benefit-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.benefit-description {
  color: #666;
  line-height: 1.5;
}

.benefits-visual {
  display: flex;
  justify-content: center;
}

.stats-showcase {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.showcase-item {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 32px;
  border-radius: 16px;
  text-align: center;
}

.showcase-number {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.showcase-label {
  font-size: 14px;
  opacity: 0.9;
}

/* Pricing Section */
.pricing-section {
  padding: 100px 0;
  background: #f8f9fa;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.pricing-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

.pricing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.pricing-card:nth-child(2) {
  border: 2px solid #667eea;
  transform: scale(1.05);
}

.pricing-header {
  text-align: center;
  margin-bottom: 32px;
}

.plan-name {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.plan-price {
  margin-bottom: 16px;
}

.price-currency {
  font-size: 20px;
  color: #666;
  vertical-align: top;
}

.price-amount {
  font-size: 48px;
  font-weight: 700;
  color: #333;
}

.price-period {
  color: #666;
  font-size: 16px;
}

.plan-description {
  color: #666;
  line-height: 1.5;
}

.pricing-features {
  margin-bottom: 32px;
}

.features-list {
  list-style: none;
  padding: 0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-check {
  color: #67c23a;
  flex-shrink: 0;
}

.pricing-action {
  text-align: center;
}

.pricing-button {
  width: 100%;
  padding: 16px;
  font-weight: 600;
}

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
}

.cta-description {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.cta-actions .el-button {
  padding: 16px 32px;
  font-weight: 600;
}

.cta-actions .el-button--primary {
  background: white;
  color: #667eea;
  border: none;
}

.cta-actions .el-button--default {
  background: transparent;
  color: white;
  border: 2px solid white;
}

/* Footer */
.footer {
  background: #2c3e50;
  color: white;
  padding: 60px 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
}

.footer-description {
  color: #95a5a6;
  line-height: 1.6;
}

.footer-links {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  color: #95a5a6;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #34495e;
  color: #95a5a6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .landing-header {
    padding: 12px 0;
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .header-actions {
    gap: 8px;
  }
  
  .hero-section {
    padding-top: 100px; /* Account for larger header on mobile */
  }
  
  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .benefits-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .stats-showcase {
    grid-template-columns: 1fr;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }

  .pricing-card:nth-child(2) {
    transform: none;
  }
}

/* Payment Modal Styles */
.payment-plan-info {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.selected-plan h3 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.plan-price-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 8px;
}

.price-currency {
  font-size: 18px;
  color: #667eea;
  font-weight: 600;
}

.price-amount {
  font-size: 28px;
  color: #667eea;
  font-weight: 700;
}

.price-period {
  font-size: 14px;
  color: #666;
}

.plan-description {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.service-details {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.service-details h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.service-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.service-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #555;
}

.service-icon {
  color: #67c23a;
  font-size: 14px;
  flex-shrink: 0;
}

.payment-methods h4 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.methods-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.payment-method-card {
  position: relative;
  padding: 20px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.payment-method-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.payment-method-card.selected {
  border-color: #667eea;
  background: #f0f4ff;
}

.payment-method-card.popular {
  border-color: #ff6b35;
}

.method-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.method-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.method-info h5 {
  margin: 0 0 4px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.method-info p {
  margin: 0;
  color: #666;
  font-size: 12px;
  line-height: 1.4;
}

.method-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff6b35;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
}

.method-selected {
  position: absolute;
  top: 8px;
  right: 8px;
  background: white;
  border-radius: 50%;
  padding: 4px;
}

.payment-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 768px) {
  .methods-grid {
    grid-template-columns: 1fr;
  }
  
  .payment-actions {
    flex-direction: column;
  }
  
  .payment-actions .el-button {
    width: 100%;
  }
}
</style>
