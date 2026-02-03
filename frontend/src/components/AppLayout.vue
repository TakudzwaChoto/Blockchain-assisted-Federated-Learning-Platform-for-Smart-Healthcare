<template>
  <div class="app-layout">
    <!-- Navigation -->
    <nav class="navbar" v-if="authStore.isAuthenticated">
      <div class="nav-brand">
        <el-icon size="24" color="#667eea">
          <TrendCharts />
        </el-icon>
        <div class="brand-text">
          <div class="brand-title">血液域分析平台</div>
          <div class="brand-subtitle">{{ authStore.user?.department }}</div>
        </div>
      </div>

      <div class="nav-menu">
        <!-- Admin Navigation -->
        <template v-if="authStore.isAdmin">
          <router-link to="/admin/dashboard" class="nav-item" :class="{ active: $route.path === '/admin/dashboard' }">
            <el-icon><Monitor /></el-icon>
            <span>管理控制台</span>
          </router-link>
          <router-link to="/admin/data-import-export" class="nav-item" :class="{ active: $route.path === '/admin/data-import-export' }">
            <el-icon><Upload /></el-icon>
            <span>数据导入/导出</span>
          </router-link>
          <router-link to="/admin/advanced-analytics" class="nav-item" :class="{ active: $route.path === '/admin/advanced-analytics' }">
            <el-icon><DataAnalysis /></el-icon>
            <span>高级分析与预测</span>
          </router-link>
          <router-link to="/admin/dashboard-builder" class="nav-item" :class="{ active: $route.path === '/admin/dashboard-builder' }">
            <el-icon><Grid /></el-icon>
            <span>仪表板构建器</span>
          </router-link>
          <router-link to="/admin/users" class="nav-item" :class="{ active: $route.path === '/admin/users' }">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </router-link>
          <router-link to="/admin/analytics" class="nav-item" :class="{ active: $route.path === '/admin/analytics' }">
            <el-icon><TrendCharts /></el-icon>
            <span>数据分析</span>
          </router-link>
          <router-link to="/admin/system" class="nav-item" :class="{ active: $route.path === '/admin/system' }">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </router-link>
        </template>

        <!-- User Navigation -->
        <template v-else-if="authStore.isUser">
          <router-link to="/user/dashboard" class="nav-item" :class="{ active: $route.path === '/user/dashboard' }">
            <el-icon><Monitor /></el-icon>
            <span>个人工作空间</span>
          </router-link>
          <router-link to="/user/donors" class="nav-item" :class="{ active: $route.path === '/user/donors' }">
            <el-icon><User /></el-icon>
            <span>供血者管理</span>
          </router-link>
          <router-link to="/user/requests" class="nav-item" :class="{ active: $route.path === '/user/requests' }">
            <el-icon><Document /></el-icon>
            <span>输血请求</span>
          </router-link>
          <router-link to="/user/analytics" class="nav-item" :class="{ active: $route.path === '/user/analytics' }">
            <el-icon><TrendCharts /></el-icon>
            <span>个人分析</span>
          </router-link>
        </template>

        <!-- Doctor Navigation -->
        <template v-else-if="authStore.isDoctor">
          <router-link to="/doctor/dashboard" class="nav-item" :class="{ active: $route.path === '/doctor/dashboard' }">
            <el-icon><Monitor /></el-icon>
            <span>个人工作空间</span>
          </router-link>
          <router-link to="/doctor/donors" class="nav-item" :class="{ active: $route.path === '/doctor/donors' }">
            <el-icon><User /></el-icon>
            <span>供血者管理</span>
          </router-link>
          <router-link to="/doctor/requests" class="nav-item" :class="{ active: $route.path === '/doctor/requests' }">
            <el-icon><Document /></el-icon>
            <span>输血请求</span>
          </router-link>
          <router-link to="/doctor/analytics" class="nav-item" :class="{ active: $route.path === '/doctor/analytics' }">
            <el-icon><TrendCharts /></el-icon>
            <span>个人分析</span>
          </router-link>
        </template>

        <!-- Government Navigation -->
        <template v-else-if="authStore.isGovernment">
          <router-link to="/government/dashboard" class="nav-item" :class="{ active: $route.path === '/government/dashboard' }">
            <el-icon><Monitor /></el-icon>
            <span>监管仪表板</span>
          </router-link>
          <router-link to="/government/oversight" class="nav-item" :class="{ active: $route.path === '/government/oversight' }">
            <el-icon><DataAnalysis /></el-icon>
            <span>监管监督</span>
          </router-link>
          <router-link to="/government/policy" class="nav-item" :class="{ active: $route.path === '/government/policy' }">
            <el-icon><Document /></el-icon>
            <span>政策管理</span>
          </router-link>
          <router-link to="/government/emergency" class="nav-item" :class="{ active: $route.path === '/government/emergency' }">
            <el-icon><Warning /></el-icon>
            <span>应急协调</span>
          </router-link>
        </template>
      </div>

      <div class="nav-actions">
        <!-- Theme Switcher -->
        <ThemeSwitcher />
        
        <el-dropdown @command="handleUserAction" placement="bottom-end">
          <div class="user-menu">
            <div class="user-avatar-container">
              <el-avatar :size="40" class="user-avatar">
                {{ authStore.user?.name?.charAt(0) }}
              </el-avatar>
              <div class="user-status-indicator online"></div>
            </div>
            <div class="user-info">
              <div class="user-name">{{ authStore.user?.name }}</div>
              <div class="user-role">{{ authStore.user?.role || 'User' }}</div>
            </div>
            <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu class="user-dropdown-menu">
              <div class="dropdown-header">
                <div class="header-user-info">
                  <el-avatar :size="48" class="header-avatar">
                    {{ authStore.user?.name?.charAt(0) }}
                  </el-avatar>
                  <div class="header-user-details">
                    <div class="header-user-name">{{ authStore.user?.name }}</div>
                    <div class="header-user-email">{{ authStore.user?.email }}</div>
                    <div class="header-user-department">{{ authStore.user?.department }}</div>
                  </div>
                </div>
              </div>
              <el-dropdown-item command="profile" class="menu-item">
                <div class="menu-item-content">
                  <el-icon class="menu-icon"><User /></el-icon>
                  <div class="menu-text">
                    <div class="menu-title">个人资料</div>
                    <div class="menu-subtitle">Manage your personal information</div>
                  </div>
                </div>
              </el-dropdown-item>
              <el-dropdown-item command="settings" class="menu-item">
                <div class="menu-item-content">
                  <el-icon class="menu-icon"><Setting /></el-icon>
                  <div class="menu-text">
                    <div class="menu-title">设置</div>
                    <div class="menu-subtitle">Configure system preferences</div>
                  </div>
                </div>
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided class="menu-item logout-item">
                <div class="menu-item-content">
                  <el-icon class="menu-icon logout-icon"><ArrowDown /></el-icon>
                  <div class="menu-text">
                    <div class="menu-title">退出登录</div>
                    <div class="menu-subtitle">Sign out of your account</div>
                  </div>
                </div>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  TrendCharts, Monitor, User, Document, Setting, ArrowDown, Upload, DataAnalysis, Grid, Warning 
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/authStore'
import ThemeSwitcher from './ThemeSwitcher.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
// Initialize app on mount
onMounted(() => {
  
  // Load auth state on app mount
  authStore.load()
  
  // Redirect to login if not authenticated and not on login page
  if (!authStore.isAuthenticated && route.path !== '/login') {
    router.push('/login')
  }
  
  // Redirect to appropriate dashboard if on root path
  if (route.path === '/' && authStore.isAuthenticated) {
    if (authStore.isAdmin) {
      router.push('/admin/dashboard')
    } else if (authStore.isDoctor) {
      router.push('/doctor/dashboard')
    } else if (authStore.isGovernment) {
      router.push('/government/dashboard')
    } else {
      router.push('/user/dashboard')
    }
  }
})

const handleUserAction = (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中')
      break
    case 'settings':
      ElMessage.info('设置功能开发中')
      break
    case 'logout':
      authStore.logout()
      router.push('/login')
      ElMessage.success('退出登录成功')
      break
  }
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  background: #f5f7fa;
}

.navbar {
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.brand-subtitle {
  font-size: 12px;
  color: #666;
}

.nav-menu {
  display: flex;
  gap: 8px;
  align-items: center;
}

.language-switcher-nav {
  margin-left: auto;
  margin-right: 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: #666;
  transition: all 0.3s ease;
  font-size: 14px;
}

.nav-item:hover {
  background: #f5f7fa;
  color: #333;
}

.nav-item.active {
  background: #667eea;
  color: white;
}

.nav-actions {
  display: flex;
  align-items: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 10px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  position: relative;
}

.user-menu:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.user-avatar-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  font-size: 16px;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.user-status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-status-indicator.online {
  background: #10b981;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dropdown-arrow {
  color: #64748b;
  transition: transform 0.3s ease;
}

.user-menu:hover .dropdown-arrow {
  transform: translateY(2px);
  color: #667eea;
}

/* Dropdown Menu Styles */
.user-dropdown-menu {
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  padding: 0;
  min-width: 280px;
}

.dropdown-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-avatar {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
  font-size: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.header-user-details {
  flex: 1;
}

.header-user-name {
  color: white;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.header-user-email {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  margin-bottom: 2px;
}

.header-user-department {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
  display: inline-block;
}

.menu-item {
  padding: 0;
  margin: 0;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.menu-item-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  width: 100%;
}

.menu-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.menu-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.menu-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.2;
}

.menu-subtitle {
  font-size: 12px;
  color: #64748b;
  font-weight: 400;
  line-height: 1.3;
}

.logout-item .menu-icon {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.logout-item:hover {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.logout-icon {
  transform: rotate(90deg);
}

.main-content {
  flex: 1;
  padding: 0;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 16px;
  }
  
  .nav-brand {
    gap: 12px;
  }
  
  .brand-title {
    font-size: 16px;
  }
  
  .brand-subtitle {
    display: none;
  }
  
  .nav-menu {
    gap: 4px;
  }
  
  .nav-item {
    padding: 8px 12px;
    font-size: 12px;
  }
  
  .nav-item span {
    display: none;
  }
  
  .user-name {
    display: none;
  }
}
</style>
