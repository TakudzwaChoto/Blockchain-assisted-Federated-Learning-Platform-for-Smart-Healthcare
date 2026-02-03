<template>
  <el-container style="min-height:100vh">
    <el-aside width="260px" style="border-right:1px solid #eee; background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);">
      <div style="padding:20px 16px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div style="color:white; font-size:18px; font-weight:700; display:flex; align-items:center; gap:8px;">
          <el-icon style="font-size:24px;"><DataAnalysis /></el-icon>
          Blood Domain Engine
        </div>
        <div style="color:rgba(255,255,255,0.8); font-size:12px; margin-top:4px;">
          Analytics Platform
        </div>
      </div>
      
      <div style="padding:16px 0;">
        <div style="color:rgba(255,255,255,0.7); font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; padding:0 16px; margin-bottom:12px;">
          主要导航
        </div>
        <el-menu router :default-active="$route.path" style="border-right:none; background:transparent;" text-color="#fff" active-text-color="#fff">
          <el-menu-item index="/home">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Grid /></el-icon>
                <span>首页</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/upload">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Upload /></el-icon>
                <span>上传数据</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/workspace">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Grid /></el-icon>
                <span>工作区</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/builder">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Setting /></el-icon>
                <span>仪表板构建器</span>
              </div>
            </template>
          </el-menu-item>
        </el-menu>
        
        <div style="color:rgba(255,255,255,0.7); font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; padding:0 16px; margin:24px 0 12px 0;">
          数据分析
        </div>
        <el-menu router :default-active="$route.path" style="border-right:none; background:transparent;" text-color="#fff" active-text-color="#fff">
          <el-menu-item index="/analytics/donations">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><TrendCharts /></el-icon>
                <span>捐赠分析</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/analytics/donors">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><User /></el-icon>
                <span>捐赠者管理</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/analytics/quality">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><DataAnalysis /></el-icon>
                <span>数据质量</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/analytics/forecasting">
            <el-icon><TrendCharts /></el-icon>
            <span>预测分析</span>
          </el-menu-item>
          <el-menu-item index="/analytics/blood-inventory">
            <el-icon><Box /></el-icon>
            <span>血液库存</span>
          </el-menu-item>
          <el-menu-item index="/analytics/campaigns">
            <el-icon><Star /></el-icon>
            <span>活动管理</span>
          </el-menu-item>
        </el-menu>
        
        <div class="menu-section-title">运营管理</div>
        <el-menu router :default-active="$route.path" style="border-right:none; background:transparent;" text-color="#fff" active-text-color="#fff">
          <el-menu-item index="/operations/scheduling">
            <el-icon><Calendar /></el-icon>
            <span>预约安排</span>
          </el-menu-item>
          <el-menu-item index="/operations/batch-processing">
            <el-icon><DataAnalysis /></el-icon>
            <span>批量处理</span>
          </el-menu-item>
          <el-menu-item index="/operations/transport">
            <el-icon><Van /></el-icon>
            <span>运输物流</span>
          </el-menu-item>
          <el-menu-item index="/operations/compliance">
            <el-icon><Lock /></el-icon>
            <span>合规追踪</span>
          </el-menu-item>
        </el-menu>
        
        <div class="menu-section-title">报告</div>
        <el-menu router :default-active="$route.path" style="border-right:none; background:transparent;" text-color="#fff" active-text-color="#fff">
          <el-menu-item index="/reports/donations">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Document /></el-icon>
                <span>捐赠报告</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/reports/performance">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><DataBoard /></el-icon>
                <span>绩效指标</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/reports/export">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Download /></el-icon>
                <span>导出中心</span>
              </div>
            </template>
          </el-menu-item>
        </el-menu>
        
        <div style="color:rgba(255,255,255,0.7); font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; padding:0 16px; margin:24px 0 12px 0;">
          用户管理
        </div>
        <el-menu router :default-active="$route.path" style="border-right:none; background:transparent;" text-color="#fff" active-text-color="#fff">
          <el-menu-item index="/login">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><UserFilled /></el-icon>
                <span>登录</span>
              </div>
            </template>
          </el-menu-item>
          <el-menu-item index="/register">
            <template #title>
              <div style="display:flex; align-items:center; gap:12px;">
                <el-icon><Plus /></el-icon>
                <span>创建账户</span>
              </div>
            </template>
          </el-menu-item>
        </el-menu>
      </div>
    </el-aside>

    <el-container>
      <el-header style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #eee; background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);">
        <div style="font-weight:600; color:#303133; display:flex; align-items:center; gap:8px;">
          <el-icon style="font-size:20px; color:#409eff;"><DataAnalysis /></el-icon>
          {{ pageTitle }}
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
          <el-badge :value="3" class="notification-badge">
            <el-icon style="color:#606266;"><Bell /></el-icon>
          </el-badge>
          <el-dropdown>
            <el-avatar size="small" style="background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);">
              <el-icon><UserFilled /></el-icon>
            </el-avatar>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人资料</el-dropdown-item>
                <el-dropdown-item>设置</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Upload,
  Grid,
  Setting,
  TrendCharts,
  User,
  DataAnalysis,
  Warning,
  Document,
  DataBoard,
  Download,
  UserFilled,
  Tools,
  Bell,
  Box,
  Star,
  Calendar,
  Van,
  Lock,
  Plus
} from '@element-plus/icons-vue'

const route = useRoute()

const pageTitle = computed(() => {
  if (route.path.startsWith('/dashboard/')) return '仪表板'
  if (route.path === '/upload') return '上传数据'
  if (route.path === '/workspace') return '工作区'
  if (route.path.startsWith('/analytics/')) return '数据分析'
  if (route.path.startsWith('/operations/')) return '运营管理'
  if (route.path.startsWith('/reports/')) return '报告'
  if (route.path === '/login') return '登录'
  if (route.path === '/register') return '创建账户'
  if (route.path === '/builder') return '仪表板构建器'
  if (route.path === '/home') return '首页'
  return 'Blood Domain Engine'
})
</script>

<style scoped>
.el-aside {
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.el-menu {
  border: none;
}

.el-menu-item {
  margin: 4px 0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
  transform: translateX(4px);
}

.el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.2) !important;
  border-left: 3px solid #409eff;
}

.notification-badge {
  cursor: pointer;
}

.el-header {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.el-avatar {
  cursor: pointer;
}

.el-main {
  background: #f5f7fa;
}
</style>
