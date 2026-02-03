<template>
  <div class="social-share">
    <div class="share-title">Share to Social Platforms</div>
    <div class="share-buttons">
      <!-- WeChat -->
      <el-button 
        class="share-btn wechat" 
        @click="shareToWeChat"
        :icon="wechatIcon"
        circle
        size="large"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" class="share-icon">
            <path fill="#07C160" d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.504a.59.59 0 0 0 .804.7l1.923-1.067a.59.59 0 0 1 .548-.042 10.35 10.35 0 0 0 2.591.328c.056 0 .11-.002.166-.003A5.872 5.872 0 0 1 7.877 14.3c0-3.696 3.531-6.689 7.881-6.689.274 0 .544.016.81.045C15.534 4.832 12.46 2.188 8.69 2.188zM5.785 5.991c.642 0 1.162.52 1.162 1.162s-.52 1.162-1.162 1.162-1.162-.52-1.162-1.162.52-1.162 1.162-1.162zm5.812 0c.642 0 1.162.52 1.162 1.162s-.52 1.162-1.162 1.162-1.162-.52-1.162-1.162.52-1.162 1.162-1.162z"/>
            <path fill="#07C160" d="M15.758 8.611c-3.696 0-6.689 2.993-6.689 6.689s2.993 6.689 6.689 6.689c.634 0 1.245-.088 1.827-.253a.59.59 0 0 1 .548.042l1.923 1.067a.59.59 0 0 0 .804-.7l-.39-1.504a.59.59 0 0 1 .213-.665c1.832-1.347 3.002-3.338 3.002-5.55 0-4.054-3.891-7.342-8.691-7.342zm-2.338 3.324c.642 0 1.162.52 1.162 1.162s-.52 1.162-1.162 1.162-1.162-.52-1.162-1.162.52-1.162 1.162-1.162zm4.676 0c.642 0 1.162.52 1.162 1.162s-.52 1.162-1.162 1.162-1.162-.52-1.162-1.162.52-1.162 1.162-1.162z"/>
          </svg>
        </template>
      </el-button>
      
      <!-- Douyin -->
      <el-button 
        class="share-btn douyin" 
        @click="shareToDouyin"
        circle
        size="large"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" class="share-icon">
            <path fill="#FE2C55" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-2-2 4-4 2 2-4 4zm8-8l-2-2-4 4 2 2 4-4z"/>
            <circle fill="#FE2C55" cx="12" cy="12" r="3"/>
          </svg>
        </template>
      </el-button>
      
      <!-- RedNote (Xiaohongshu) -->
      <el-button 
        class="share-btn rednote" 
        @click="shareToRedNote"
        circle
        size="large"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" class="share-icon">
            <path fill="#FF2442" d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
            <path fill="white" d="M9 12l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </template>
      </el-button>
      
      <!-- Weibo -->
      <el-button 
        class="share-btn weibo" 
        @click="shareToWeibo"
        circle
        size="large"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" class="share-icon">
            <path fill="#E6162D" d="M10.09 18.37c-2.78.37-5.18-.98-5.37-3.01-.19-2.03 1.92-4.03 4.7-4.4 2.78-.37 5.18.98 5.37 3.01.19 2.03-1.92 4.03-4.7 4.4z"/>
            <circle fill="#E6162D" cx="7.5" cy="14.5" r="1.5"/>
            <path fill="#E6162D" d="M21 10c0-1.1-.9-2-2-2h-1c-.55 0-1 .45-1 1s.45 1 1 1h1c.55 0 1 .45 1 1v7c0 .55-.45 1-1 1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1c1.1 0 2-.9 2-2v-7z"/>
          </svg>
        </template>
      </el-button>
      
      <!-- QQ -->
      <el-button 
        class="share-btn qq" 
        @click="shareToQQ"
        circle
        size="large"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" class="share-icon">
            <circle fill="#12B7F5" cx="12" cy="12" r="10"/>
            <path fill="white" d="M8 10c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm4 0c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2z"/>
            <path fill="white" d="M9 14c0 .55.45 1 1 1h4c.55 0 1-.45 1-1s-.45-1-1-1h-4c-.55 0-1 .45-1 1z"/>
          </svg>
        </template>
      </el-button>
      
      <!-- Copy Link -->
      <el-button 
        class="share-btn copy" 
        @click="copyLink"
        circle
        size="large"
      >
        <template #icon>
          <el-icon><Link /></el-icon>
        </template>
      </el-button>
    </div>
    
    <!-- QR Code Modal -->
    <el-dialog 
      v-model="qrModalVisible" 
      :title="'WeChat QR Code Share'"
      width="400px"
      center
      @open="handleModalOpen"
    >
      <div class="qr-container">
        <div class="qr-code" ref="qrCodeRef">
          <img v-if="qrCodeUrl" :src="qrCodeUrl" alt="QR Code" />
          <div v-else class="qr-placeholder">
            <el-icon class="qr-icon"><Loading /></el-icon>
            <span>生成中...</span>
          </div>
        </div>
        <p class="qr-text">Scan QR code with WeChat to share with friends</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Link, Loading } from '@element-plus/icons-vue'
import { generateQRCode, generateShareUrl, copyToClipboard } from '../utils/shareUtils'

const qrModalVisible = ref(false)
const qrCodeRef = ref()
const qrCodeUrl = ref('')

// Share data
const shareData = {
  title: 'Blood Domain Analytics Platform',
  description: 'AI-powered blood management and transfusion safety analysis system',
  url: window.location.href,
  image: '/logo.png'
}

// Generate QR code for WeChat
const generateWeChatQR = async () => {
  try {
    qrCodeUrl.value = await generateQRCode(shareData.url, 200)
  } catch (error) {
    console.error('QR code generation failed:', error)
  }
}

// WeChat sharing (QR Code)
const shareToWeChat = async () => {
  await generateWeChatQR()
  qrModalVisible.value = true
  ElMessage.info('Please scan QR code with WeChat to share')
}

// Douyin sharing
const shareToDouyin = () => {
  // Copy content for manual sharing to Douyin
  const shareText = `${shareData.title}\n${shareData.description}\n${shareData.url}`
  copyToClipboard(shareText)
  ElMessage.success('Douyin share page opened')
}

// RedNote (Xiaohongshu) sharing
const shareToRedNote = () => {
  const shareText = `${shareData.title}\n${shareData.description}\n${shareData.url}`
  copyToClipboard(shareText)
  ElMessage.success('Content copied to clipboard, please paste in RedNote app')
}

// Weibo sharing
const shareToWeibo = () => {
  const shareUrl = generateShareUrl('weibo', shareData)
  window.open(shareUrl, '_blank', 'width=600,height=400')
  ElMessage.success('Weibo share page opened')
}

// QQ sharing
const shareToQQ = () => {
  const shareUrl = generateShareUrl('qq', shareData)
  window.open(shareUrl, '_blank', 'width=600,height=400')
  ElMessage.success('QQ share page opened')
}

// Copy link to clipboard
const copyLink = async () => {
  const success = await copyToClipboard(shareData.url)
  if (success) {
    ElMessage.success('Link copied to clipboard')
  }
}

// Generate QR code when modal opens
const handleModalOpen = () => {
  if (qrModalVisible.value) {
    generateWeChatQR()
  }
}

onMounted(() => {
  // Pre-generate QR code
  generateWeChatQR()
})
</script>

<style scoped>
.social-share {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 12px;
  margin: 20px 0;
}

.share-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.share-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.share-btn {
  width: 48px;
  height: 48px;
  border: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.share-btn.wechat {
  background: linear-gradient(135deg, #07C160, #00A048);
}

.share-btn.douyin {
  background: linear-gradient(135deg, #FE2C55, #FF0050);
}

.share-btn.rednote {
  background: linear-gradient(135deg, #FF2442, #E60012);
}

.share-btn.weibo {
  background: linear-gradient(135deg, #E6162D, #C4001F);
}

.share-btn.qq {
  background: linear-gradient(135deg, #12B7F5, #0091EA);
}

.share-btn.copy {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.share-icon {
  width: 24px;
  height: 24px;
  color: white;
}

.qr-container {
  text-align: center;
  padding: 20px;
}

.qr-code {
  width: 200px;
  height: 200px;
  margin: 0 auto 16px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.qr-code img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.qr-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #999;
  font-size: 14px;
}

.qr-icon {
  font-size: 24px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.qr-text {
  color: #666;
  font-size: 14px;
  margin: 0;
}

@media (max-width: 768px) {
  .share-buttons {
    gap: 8px;
  }
  
  .share-btn {
    width: 40px;
    height: 40px;
  }
  
  .share-icon {
    width: 20px;
    height: 20px;
  }
}
</style>
