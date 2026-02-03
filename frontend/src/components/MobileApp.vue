<template>
  <div class="mobile-app">
    <div class="mobile-header">
      <div class="app-icon-container">
        <el-icon size="32" color="white"><Iphone /></el-icon>
      </div>
      <div class="app-info">
        <h3>Mobile App</h3>
        <p class="app-subtitle">Manage blood inventory anytime, anywhere</p>
      </div>
      <div class="app-status">
        <el-tag type="success" size="small" effect="dark">
          <el-icon size="12"><CircleCheck /></el-icon>
          Available
        </el-tag>
      </div>
    </div>
    
    <div class="mobile-features">
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon size="24"><Monitor /></el-icon>
          </div>
          <div class="feature-title">Blood Tracking</div>
          <div class="feature-desc">Real-time blood inventory tracking</div>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon size="24"><Monitor /></el-icon>
          </div>
          <div class="feature-title">Real-time Monitoring</div>
          <div class="feature-desc">View real-time data and trends</div>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon size="24"><Bell /></el-icon>
          </div>
          <div class="feature-title">Smart Notifications</div>
          <div class="feature-desc">Instant alerts for important events</div>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon size="24"><Iphone /></el-icon>
          </div>
          <div class="feature-title">Offline Mode</div>
          <div class="feature-desc">Works even without internet connection</div>
        </div>
      </div>
    </div>
    
    <div class="mobile-actions">
      <div class="qr-section">
        <div class="qr-code">
          <div class="qr-placeholder">
            <el-icon class="qr-icon"><Loading /></el-icon>
            <span>Scan to Download</span>
          </div>
        </div>
        <p class="qr-text">Use phone to scan QR code and download app</p>
      </div>
      
      <div class="download-buttons">
        <el-button type="primary" size="large" class="download-btn">
          <template #icon>
            <svg viewBox="0 0 24 24" class="store-icon">
              <path fill="#000" d="M3.609 1.814L13.792 12 3.61 22.186a1 1 0 0 1-1.414-1.414L10.378 12 2.195 3.814A1 1 0 0 1 3.61 2.4l10.182 10.186z"/>
              <path fill="#000" d="M20.391 1.814L10.208 12l10.183 10.186a1 1 0 0 0 1.414-1.414L13.622 12l8.183-8.186a1 1 0 0 0-1.414-1.414z"/>
            </svg>
          </template>
          Download Android
        </el-button>
        
        <el-button type="primary" size="large" class="download-btn ios">
          <template #icon>
            <svg viewBox="0 0 24 24" class="store-icon">
              <path fill="#000" d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
            </svg>
          </template>
          Download iOS
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Loading, Monitor, Bell, Iphone, CircleCheck } from '@element-plus/icons-vue'
</script>

<style scoped>
.mobile-app {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.mobile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
  position: relative;
  overflow: hidden;
}

.mobile-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  border-radius: 16px;
}

.app-icon-container {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.app-info {
  flex: 1;
  position: relative;
  z-index: 1;
}

.app-info h3 {
  margin: 0 0 6px 0;
  font-size: 24px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.app-subtitle {
  margin: 0;
  color: rgba(255, 255, 255, 0.85);
  font-size: 15px;
  font-weight: 500;
}

.app-status {
  position: relative;
  z-index: 1;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  margin: 0 auto 16px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
  position: relative;
  overflow: hidden;
}

.feature-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 100%);
  border-radius: 14px;
}

.feature-title {
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
  font-size: 16px;
}

.feature-desc {
  color: #64748b;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
}

.mobile-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: center;
}

.qr-section {
  text-align: center;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.qr-code {
  width: 140px;
  height: 140px;
  margin: 0 auto 16px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}

.qr-code::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 10px;
}

.qr-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #64748b;
  font-size: 13px;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.qr-icon {
  font-size: 24px;
  animation: spin 1s linear infinite;
  color: #667eea;
}

.qr-text {
  color: #475569;
  font-size: 14px;
  margin: 0;
  font-weight: 600;
}

.download-buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.download-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.download-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.download-btn:hover::before {
  left: 100%;
}

.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.download-btn.ios {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border: none;
  color: white;
}

.download-btn.ios:hover {
  box-shadow: 0 8px 20px rgba(30, 41, 59, 0.3);
}

.store-icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .mobile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .mobile-actions {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .qr-section {
    order: 2;
  }
  
  .download-buttons {
    order: 1;
  }
}
</style>
