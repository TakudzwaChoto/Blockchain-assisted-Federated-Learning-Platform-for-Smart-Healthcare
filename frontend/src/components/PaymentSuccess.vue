<template>
  <div class="payment-success-container">
    <div class="success-header">
      <div class="success-icon">
        <el-icon size="64" color="#67c23a"><CircleCheckFilled /></el-icon>
      </div>
      <h2>支付成功！</h2>
      <p>恭喜您成功购买血液管理服务</p>
    </div>

    <div class="purchase-details">
      <h3>购买详情</h3>
      <div class="plan-card">
        <div class="plan-info">
          <h4>{{ purchasedPlan?.name }}</h4>
          <div class="plan-price">
            <span class="currency">¥</span>
            <span class="amount">{{ purchasedPlan?.price }}</span>
            <span class="period">/月</span>
          </div>
          <p class="plan-description">{{ purchasedPlan?.description }}</p>
        </div>
        <div class="payment-info">
          <div class="payment-method">
            <span class="label">支付方式：</span>
            <span class="value">{{ paymentMethodName }}</span>
          </div>
          <div class="payment-time">
            <span class="label">支付时间：</span>
            <span class="value">{{ paymentTime }}</span>
          </div>
          <div class="order-id">
            <span class="label">订单号：</span>
            <span class="value">{{ orderId }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="services-section">
      <h3>您的服务权益</h3>
      <div class="services-grid">
        <div v-for="feature in purchasedPlan?.features" :key="feature" class="service-card">
          <el-icon class="service-icon"><Check /></el-icon>
          <span>{{ feature }}</span>
        </div>
      </div>
    </div>

    <div class="next-steps">
      <h3>下一步操作</h3>
      <div class="steps-list">
        <div class="step-item">
          <div class="step-number">1</div>
          <div class="step-content">
            <h4>创建账户</h4>
            <p>注册您的管理员账户以开始使用服务</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-number">2</div>
          <div class="step-content">
            <h4>完善信息</h4>
            <p>填写医疗机构信息和配置系统参数</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-number">3</div>
          <div class="step-content">
            <h4>开始使用</h4>
            <p>登录系统并开始管理您的血液业务</p>
          </div>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <el-button type="primary" size="large" @click="goToRegister">
        立即注册账户
      </el-button>
      <el-button size="large" @click="viewInvoice">
        查看发票
      </el-button>
    </div>

    <div class="support-info">
      <p>如有疑问，请联系客服：400-123-4567 或 support@blooddomain.com</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { CircleCheckFilled, Check } from '@element-plus/icons-vue'

const router = useRouter()

// Props
const props = defineProps({
  purchasedPlan: {
    type: Object,
    required: true
  },
  paymentMethod: {
    type: String,
    required: true
  },
  orderId: {
    type: String,
    required: true
  }
})

// Computed
const paymentMethodName = computed(() => {
  const methodMap = {
    'wechat': '微信支付',
    'alipay': '支付宝',
    'bank': '银行转账',
    'paypal': 'PayPal'
  }
  return methodMap[props.paymentMethod] || props.paymentMethod
})

const paymentTime = computed(() => {
  return new Date().toLocaleString('zh-CN')
})

// Methods
const goToRegister = () => {
  router.push('/login')
  // Trigger account creation flow after navigation
  setTimeout(() => {
    window.dispatchEvent(new CustomEvent('showAccountCreation'))
  }, 100)
}

const viewInvoice = () => {
  // Generate and show invoice
  console.log('View invoice for order:', props.orderId)
}
</script>

<style scoped>
.payment-success-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.success-header {
  margin-bottom: 40px;
}

.success-icon {
  margin-bottom: 20px;
}

.success-header h2 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 32px;
  font-weight: 700;
}

.success-header p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.purchase-details {
  margin-bottom: 40px;
  text-align: left;
}

.purchase-details h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.plan-card {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.plan-info {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.plan-info h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 8px;
}

.currency {
  font-size: 18px;
  color: #667eea;
  font-weight: 600;
}

.amount {
  font-size: 28px;
  color: #667eea;
  font-weight: 700;
}

.period {
  font-size: 14px;
  color: #666;
}

.plan-description {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.payment-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.payment-method,
.payment-time,
.order-id {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label {
  font-size: 12px;
  color: #999;
  font-weight: 500;
}

.value {
  font-size: 14px;
  color: #333;
  font-weight: 600;
}

.services-section {
  margin-bottom: 40px;
  text-align: left;
}

.services-section h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.service-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #67c23a;
}

.service-icon {
  color: #67c23a;
  font-size: 16px;
  flex-shrink: 0;
}

.service-card span {
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.next-steps {
  margin-bottom: 40px;
  text-align: left;
}

.next-steps h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.steps-list {
  display: grid;
  gap: 16px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.step-number {
  width: 32px;
  height: 32px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h4 {
  margin: 0 0 4px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.step-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 40px;
}

.support-info {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.support-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .payment-info {
    grid-template-columns: 1fr;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button {
    width: 100%;
  }
}
</style>
