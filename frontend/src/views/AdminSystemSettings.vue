<template>
  <div class="admin-system-settings">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1>系统设置</h1>
          <p>管理系统配置和全局设置</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="saveSettings" :loading="saving">
            <el-icon><Check /></el-icon>
            保存设置
          </el-button>
          <el-button @click="resetSettings">
            <el-icon><RefreshLeft /></el-icon>
            重置
          </el-button>
        </div>
      </div>
    </div>

    <!-- Settings Categories -->
    <div class="settings-grid">
      <!-- Basic Settings -->
      <el-card class="settings-card">
        <template #header>
          <h3>基本设置</h3>
        </template>
        <div class="settings-content">
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" placeholder="血液领域分析平台" />
            </el-form-item>
            
            <el-form-item label="系统版本">
              <el-input v-model="basicSettings.systemVersion" readonly />
            </el-form-item>
            
            <el-form-item label="管理员邮箱">
              <el-input v-model="basicSettings.adminEmail" placeholder="admin@blooddomain.com" />
            </el-form-item>
            
            <el-form-item label="时区设置">
              <el-select v-model="basicSettings.timezone" style="width: 100%">
                <el-option label="北京时间 (UTC+8)" value="Asia/Shanghai" />
                <el-option label="东京时间 (UTC+9)" value="Asia/Tokyo" />
                <el-option label="纽约时间 (UTC-5)" value="America/New_York" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="语言设置">
              <el-select v-model="basicSettings.language" style="width: 100%">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- Security Settings -->
      <el-card class="settings-card">
        <template #header>
          <h3>安全设置</h3>
        </template>
        <div class="settings-content">
          <el-form :model="securitySettings" label-width="120px">
            <el-form-item label="密码策略">
              <el-checkbox-group v-model="securitySettings.passwordPolicy">
                <el-checkbox label="minLength">最少8位字符</el-checkbox>
                <el-checkbox label="requireUppercase">包含大写字母</el-checkbox>
                <el-checkbox label="requireNumbers">包含数字</el-checkbox>
                <el-checkbox label="requireSpecial">包含特殊字符</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item label="会话超时">
              <el-input-number 
                v-model="securitySettings.sessionTimeout" 
                :min="30" 
                :max="480" 
                controls-position="right"
              />
              <span style="margin-left: 8px; color: #666;">分钟</span>
            </el-form-item>
            
            <el-form-item label="登录失败限制">
              <el-input-number 
                v-model="securitySettings.maxLoginAttempts" 
                :min="3" 
                :max="10" 
                controls-position="right"
              />
              <span style="margin-left: 8px; color: #666;">次</span>
            </el-form-item>
            
            <el-form-item label="双因素认证">
              <el-switch 
                v-model="securitySettings.twoFactorAuth" 
                active-text="启用" 
                inactive-text="禁用"
              />
            </el-form-item>
            
            <el-form-item label="IP白名单">
              <el-input 
                v-model="securitySettings.ipWhitelist" 
                type="textarea" 
                :rows="3"
                placeholder="每行一个IP地址或IP段"
              />
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- Notification Settings -->
      <el-card class="settings-card">
        <template #header>
          <h3>通知设置</h3>
        </template>
        <div class="settings-content">
          <el-form :model="notificationSettings" label-width="120px">
            <el-form-item label="邮件通知">
              <el-switch 
                v-model="notificationSettings.emailEnabled" 
                active-text="启用" 
                inactive-text="禁用"
              />
            </el-form-item>
            
            <el-form-item label="SMTP服务器">
              <el-input v-model="notificationSettings.smtpHost" placeholder="smtp.example.com" />
            </el-form-item>
            
            <el-form-item label="SMTP端口">
              <el-input-number v-model="notificationSettings.smtpPort" :min="1" :max="65535" />
            </el-form-item>
            
            <el-form-item label="发件人邮箱">
              <el-input v-model="notificationSettings.fromEmail" placeholder="noreply@blooddomain.com" />
            </el-form-item>
            
            <el-form-item label="通知类型">
              <el-checkbox-group v-model="notificationSettings.notificationTypes">
                <el-checkbox label="userLogin">用户登录</el-checkbox>
                <el-checkbox label="systemAlert">系统警报</el-checkbox>
                <el-checkbox label="dataBackup">数据备份</el-checkbox>
                <el-checkbox label="securityEvent">安全事件</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- Data Settings -->
      <el-card class="settings-card">
        <template #header>
          <h3>数据设置</h3>
        </template>
        <div class="settings-content">
          <el-form :model="dataSettings" label-width="120px">
            <el-form-item label="数据备份">
              <el-switch 
                v-model="dataSettings.autoBackup" 
                active-text="自动备份" 
                inactive-text="手动备份"
              />
            </el-form-item>
            
            <el-form-item label="备份频率">
              <el-select v-model="dataSettings.backupFrequency" style="width: 100%">
                <el-option label="每日" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="数据保留期">
              <el-input-number 
                v-model="dataSettings.dataRetentionDays" 
                :min="30" 
                :max="3650" 
                controls-position="right"
              />
              <span style="margin-left: 8px; color: #666;">天</span>
            </el-form-item>
            
            <el-form-item label="日志级别">
              <el-select v-model="dataSettings.logLevel" style="width: 100%">
                <el-option label="错误" value="error" />
                <el-option label="警告" value="warning" />
                <el-option label="信息" value="info" />
                <el-option label="调试" value="debug" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="数据压缩">
              <el-switch 
                v-model="dataSettings.dataCompression" 
                active-text="启用" 
                inactive-text="禁用"
              />
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- System Status -->
      <el-card class="settings-card full-width">
        <template #header>
          <h3>系统状态</h3>
        </template>
        <div class="system-status">
          <div class="status-grid">
            <div class="status-item">
              <div class="status-label">系统运行时间</div>
              <div class="status-value">{{ systemStatus.uptime }}</div>
            </div>
            <div class="status-item">
              <div class="status-label">CPU使用率</div>
              <div class="status-value">
                <el-progress 
                  :percentage="systemStatus.cpuUsage" 
                  :color="getUsageColor(systemStatus.cpuUsage)"
                  :show-text="false"
                  style="width: 100px"
                />
                <span style="margin-left: 8px">{{ systemStatus.cpuUsage }}%</span>
              </div>
            </div>
            <div class="status-item">
              <div class="status-label">内存使用率</div>
              <div class="status-value">
                <el-progress 
                  :percentage="systemStatus.memoryUsage" 
                  :color="getUsageColor(systemStatus.memoryUsage)"
                  :show-text="false"
                  style="width: 100px"
                />
                <span style="margin-left: 8px">{{ systemStatus.memoryUsage }}%</span>
              </div>
            </div>
            <div class="status-item">
              <div class="status-label">磁盘使用率</div>
              <div class="status-value">
                <el-progress 
                  :percentage="systemStatus.diskUsage" 
                  :color="getUsageColor(systemStatus.diskUsage)"
                  :show-text="false"
                  style="width: 100px"
                />
                <span style="margin-left: 8px">{{ systemStatus.diskUsage }}%</span>
              </div>
            </div>
            <div class="status-item">
              <div class="status-label">数据库状态</div>
              <div class="status-value">
                <el-tag :type="systemStatus.databaseStatus === 'connected' ? 'success' : 'danger'">
                  {{ systemStatus.databaseStatus === 'connected' ? '已连接' : '连接失败' }}
                </el-tag>
              </div>
            </div>
            <div class="status-item">
              <div class="status-label">最后备份</div>
              <div class="status-value">{{ formatDate(systemStatus.lastBackup) }}</div>
            </div>
          </div>
          
          <div class="status-actions">
            <el-button @click="checkSystemHealth">
              <el-icon><Refresh /></el-icon>
              检查系统健康
            </el-button>
            <el-button @click="runBackup">
              <el-icon><Download /></el-icon>
              立即备份
            </el-button>
            <el-button @click="clearCache">
              <el-icon><Delete /></el-icon>
              清理缓存
            </el-button>
            <el-button type="danger" @click="restartSystem">
              <el-icon><RefreshRight /></el-icon>
              重启系统
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Check, RefreshLeft, Refresh, Download, Delete, RefreshRight 
} from '@element-plus/icons-vue'

const saving = ref(false)

// Settings data
const basicSettings = reactive({
  systemName: '血液领域分析平台',
  systemVersion: 'v1.0.0',
  adminEmail: 'admin@blooddomain.com',
  timezone: 'Asia/Shanghai',
  language: 'zh-CN'
})

const securitySettings = reactive({
  passwordPolicy: ['minLength', 'requireNumbers'],
  sessionTimeout: 120,
  maxLoginAttempts: 5,
  twoFactorAuth: false,
  ipWhitelist: ''
})

const notificationSettings = reactive({
  emailEnabled: true,
  smtpHost: 'smtp.gmail.com',
  smtpPort: 587,
  fromEmail: 'noreply@blooddomain.com',
  notificationTypes: ['systemAlert', 'dataBackup']
})

const dataSettings = reactive({
  autoBackup: true,
  backupFrequency: 'daily',
  dataRetentionDays: 365,
  logLevel: 'info',
  dataCompression: true
})

const systemStatus = reactive({
  uptime: '15天 8小时 32分钟',
  cpuUsage: 45,
  memoryUsage: 68,
  diskUsage: 32,
  databaseStatus: 'connected',
  lastBackup: new Date(Date.now() - 2 * 60 * 60 * 1000)
})

// Methods
const getUsageColor = (percentage) => {
  if (percentage < 50) return '#67c23a'
  if (percentage < 80) return '#e6a23c'
  return '#f56c6c'
}

const formatDate = (date) => {
  return date.toLocaleString('zh-CN')
}

const saveSettings = async () => {
  saving.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('设置保存失败')
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  ElMessageBox.confirm(
    '确定要重置所有设置吗？此操作不可恢复！',
    '重置设置',
    {
      confirmButtonText: '确定重置',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // Reset to defaults
    Object.assign(basicSettings, {
      systemName: '血液领域分析平台',
      systemVersion: 'v1.0.0',
      adminEmail: 'admin@blooddomain.com',
      timezone: 'Asia/Shanghai',
      language: 'zh-CN'
    })
    
    ElMessage.success('设置已重置为默认值')
  }).catch(() => {
    // User cancelled
  })
}

const checkSystemHealth = () => {
  ElMessage.info('系统健康检查中...')
  setTimeout(() => {
    ElMessage.success('系统运行正常')
  }, 2000)
}

const runBackup = () => {
  ElMessage.info('正在备份数据...')
  setTimeout(() => {
    systemStatus.lastBackup = new Date()
    ElMessage.success('数据备份完成')
  }, 3000)
}

const clearCache = () => {
  ElMessageBox.confirm(
    '确定要清理系统缓存吗？',
    '清理缓存',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.info('正在清理缓存...')
    setTimeout(() => {
      ElMessage.success('缓存清理完成')
    }, 1500)
  })
}

const restartSystem = () => {
  ElMessageBox.confirm(
    '确定要重启系统吗？这将中断所有用户连接！',
    '重启系统',
    {
      confirmButtonText: '确定重启',
      cancelButtonText: '取消',
      type: 'error'
    }
  ).then(() => {
    ElMessage.warning('系统正在重启，请稍候...')
  })
}

onMounted(() => {
  // Initialize settings
})
</script>

<style scoped>
.admin-system-settings {
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

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.settings-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.settings-card.full-width {
  grid-column: 1 / -1;
}

.settings-card h3 {
  margin: 0;
  color: #333;
}

.settings-content {
  padding: 16px 0;
}

.system-status {
  padding: 20px 0;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.status-item {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.status-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.status-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
  
  .status-grid {
    grid-template-columns: 1fr;
  }
  
  .status-actions {
    flex-direction: column;
  }
}
</style>
