<template>
  <div class="advanced-dashboard" :class="{ 'dark-mode': isDarkMode }">
    <!-- Professional Navigation Header -->
    <nav class="professional-nav">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="brand-logo">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <div class="brand-text">
            <h1>血液领域分析平台</h1>
            <!--<span>Blood Domain Analytics</span>-->
          </div>
        </div>
        
        <div class="nav-menu">
          <el-tooltip content="血液系统概览 - 实时监控血液库存、捐赠数据和系统状态" placement="bottom">
            <el-button class="nav-item" :class="{ active: currentView === 'dashboard' }" @click="navigateToDashboard" 
                     data-tooltip="血液系统概览 - 实时监控血液库存、捐赠数据和系统状态">
              <el-icon><TrendCharts /></el-icon>
              <span>仪表板</span>
            </el-button>
          </el-tooltip>
          <el-tooltip content="自定义仪表板 - 构建个性化血液数据分析界面" placement="bottom">
            <el-button class="nav-item" :class="{ active: currentView === 'dashboard-builder' }" @click="navigateToDashboardBuilder"
                     data-tooltip="自定义仪表板 - 构建个性化血液数据分析界面">
              <el-icon><Setting /></el-icon>
              <span>构建器</span>
            </el-button>
          </el-tooltip>
          <el-tooltip content="系统健康监控 - 监控血液管理系统运行状态和性能" placement="bottom">
            <el-button class="nav-item" :class="{ active: currentView === 'system-status' }" @click="navigateToSystemStatus"
                     data-tooltip="系统健康监控 - 监控血液管理系统运行状态和性能">
              <el-icon><Monitor /></el-icon>
              <span>系统状态</span>
            </el-button>
          </el-tooltip>
          <el-tooltip content="任务流程管理 - 管理血液检测、配送和相关任务" placement="bottom">
            <el-button class="nav-item" :class="{ active: currentView === 'task-management' }" @click="navigateToTaskManagement"
                     data-tooltip="任务流程管理 - 管理血液检测、配送和相关任务">
              <el-icon><List /></el-icon>
              <span>任务管理</span>
            </el-button>
          </el-tooltip>
          <el-tooltip content="深度数据分析 - 分析血液趋势、预测和统计报告" placement="bottom">
            <el-button class="nav-item" :class="{ active: currentView === 'analytics' }" @click="navigateToAnalytics"
                     data-tooltip="深度数据分析 - 分析血液趋势、预测和统计报告">
              <el-icon><DataAnalysis /></el-icon>
              <span>数据分析</span>
            </el-button>
          </el-tooltip>
          <!-- More dropdown for additional items -->
          <el-dropdown trigger="click" class="nav-dropdown">
            <el-button class="nav-item" data-tooltip="更多功能 - 捐赠者管理和应急响应">
              <el-icon><MoreFilled /></el-icon>
              <span>更多</span>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="navigateToDonors">
                  <el-icon><User /></el-icon>
                  <span>捐赠者管理</span>
                </el-dropdown-item>
                <el-dropdown-item @click="navigateToEmergency">
                  <el-icon><Warning /></el-icon>
                  <span>应急响应</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        
        <div class="nav-actions">
          <el-tooltip :content="isDarkMode ? '切换到浅色模式 - 适合日间使用' : '切换到深色模式 - 适合夜间使用'" placement="bottom">
            <el-button @click="toggleDarkMode" class="action-btn theme-btn" :class="{ active: isDarkMode }"
                     :data-tooltip="isDarkMode ? '切换到浅色模式 - 适合日间使用' : '切换到深色模式 - 适合夜间使用'">
              <el-icon><component :is="isDarkMode ? Sunny : Moon" /></el-icon>
              <span>{{ isDarkMode ? '浅色' : '深色' }}</span>
            </el-button>
          </el-tooltip>
          <el-tooltip content="个人中心 - 管理血液分析师档案和设置" placement="bottom">
            <el-button @click="toggleProfile" class="action-btn profile-btn" :class="{ active: showProfile }"
                     data-tooltip="个人中心 - 管理血液分析师档案和设置">
              <el-icon><User /></el-icon>
              <span>个人中心</span>
            </el-button>
          </el-tooltip>
        </div>
      </div>
    </nav>

    <!-- AI Assistant Panel -->
    <div class="ai-assistant" :class="{ active: showAIAssistant }">
      <div class="ai-header">
        <h4>AI 助手</h4>
        <el-button @click="toggleAIAssistant" text>
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      <div class="ai-content">
        <div class="ai-messages">
          <div v-for="message in aiMessages" :key="message.id" class="ai-message" :class="message.type">
            <div class="message-content">{{ message.text }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
        <div class="ai-input">
          <el-input
            v-model="aiInput"
            placeholder="询问任何关于数据的问题..."
            @keyup.enter="sendAIMessage"
          >
            <template #append>
              <el-button @click="sendAIMessage">
                <el-icon><Promotion /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>

    <!-- Hero Section with Enhanced Animations -->
    <div class="hero-section">
      <div class="animated-bg">
        <div class="floating-shapes">
          <div class="shape shape-1"></div>
          <div class="shape shape-2"></div>
          <div class="shape shape-3"></div>
          <div class="shape shape-4"></div>
          <div class="shape shape-5"></div>
          <div class="shape shape-6"></div>
        </div>
        <div class="particle-container">
          <div v-for="particle in particles" :key="particle.id" class="particle" 
               :style="{ left: particle.x + '%', top: particle.y + '%', animationDelay: particle.delay + 's' }">
          </div>
        </div>
      </div>
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="gradient-text">血液领域</span>
            <span class="highlight">分析平台</span>
          </h1>
          <p class="hero-subtitle">先进的血液管理和分析系统</p>
          <div class="hero-stats">
            <div class="stat-item" v-for="stat in heroStats" :key="stat.id">
              <div class="stat-number" :class="{ 'pulse-animation': stat.animated }">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-change" :class="stat.trend">
                <el-icon v-if="stat.trend === 'up'"><TrendCharts /></el-icon>
                <el-icon v-else><TrendCharts /></el-icon>
                <span>{{ stat.change }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="hero-actions">
          <el-button type="primary" size="large" class="action-btn" @click="navigateToUpload">
            <el-icon><Upload /></el-icon>
            上传数据
          </el-button>
          <el-button size="large" class="action-btn secondary" @click="navigateToAnalytics">
            <el-icon><TrendCharts /></el-icon>
            查看分析
          </el-button>
        </div>
      </div>
    </div>

    <!-- Real-time Notifications -->
    <div class="notification-container">
      <div v-for="notification in realTimeNotifications" :key="notification.id" 
           class="real-time-notification" :class="notification.type">
        <div class="notification-icon">
          <el-icon>
            <component :is="notification.icon" />
          </el-icon>
        </div>
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
        </div>
        <div class="notification-close" @click="removeNotification(notification.id)">
          <el-icon><Close /></el-icon>
        </div>
      </div>
    </div>

    <!-- Real-time Monitoring Dashboard -->
    <div v-if="currentView === 'realtime-monitoring'" class="realtime-monitoring-section">
      <div class="section-header">
        <h2 class="section-title">实时监控仪表板</h2>
        <div class="section-actions">
          <el-button @click="toggleRealtimeUpdates" :type="realtimeUpdatesEnabled ? 'primary' : ''">
            <el-icon><Timer /></el-icon>
            {{ realtimeUpdatesEnabled ? '实时更新中' : '启动实时更新' }}
          </el-button>
          <el-button @click="exportMonitoringData">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
        </div>
      </div>
      
      <div class="monitoring-dashboard">
        <!-- Live Blood Inventory -->
        <div class="monitoring-card blood-inventory">
          <div class="card-header">
            <h3>实时血液库存</h3>
            <div class="live-indicator">
              <div class="live-dot"></div>
              <span>实时</span>
            </div>
          </div>
          <div class="inventory-grid">
            <div v-for="bloodType in bloodInventoryData" :key="bloodType.type" 
                 class="blood-type-card" :class="bloodType.status">
              <div class="blood-type">{{ bloodType.type }}</div>
              <div class="blood-amount">{{ bloodType.amount }}ml</div>
              <div class="blood-status">{{ bloodType.statusText }}</div>
              <div class="blood-trend" :class="bloodType.trend">
                <el-icon v-if="bloodType.trend === 'up'"><TrendCharts /></el-icon>
                <el-icon v-else-if="bloodType.trend === 'down'"><TrendCharts /></el-icon>
                <el-icon v-else><Minus /></el-icon>
                <span>{{ bloodType.change }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Donation Centers Status -->
        <div class="monitoring-card centers-status">
          <div class="card-header">
            <h3>捐赠中心状态</h3>
            <el-select v-model="selectedRegion" size="small" placeholder="选择地区">
              <el-option label="全部地区" value="all" />
              <el-option label="北京" value="beijing" />
              <el-option label="上海" value="shanghai" />
              <el-option label="广州" value="guangzhou" />
            </el-select>
          </div>
          <div class="centers-grid">
            <div v-for="center in donationCentersData" :key="center.id" 
                 class="center-card" :class="center.status">
              <div class="center-info">
                <div class="center-name">{{ center.name }}</div>
                <div class="center-address">{{ center.address }}</div>
              </div>
              <div class="center-metrics">
                <div class="metric">
                  <span class="metric-label">等待时间</span>
                  <span class="metric-value">{{ center.waitTime }}分钟</span>
                </div>
                <div class="metric">
                  <span class="metric-label">当前容量</span>
                  <span class="metric-value">{{ center.capacity }}%</span>
                </div>
                <div class="metric">
                  <span class="metric-label">今日捐赠</span>
                  <span class="metric-value">{{ center.todayDonations }}</span>
                </div>
              </div>
              <div class="center-status-indicator" :class="center.status">
                <div class="status-dot"></div>
                <span>{{ center.statusText }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Emergency Alerts -->
        <div class="monitoring-card emergency-alerts">
          <div class="card-header">
            <h3>紧急警报</h3>
            <el-badge :value="emergencyAlerts.length" :max="99" class="alert-badge">
              <el-button @click="refreshAlerts" size="small">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </el-badge>
          </div>
          <div class="alerts-container">
            <div v-for="alert in emergencyAlerts" :key="alert.id" 
                 class="alert-item" :class="alert.severity">
              <div class="alert-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="alert-content">
                <div class="alert-title">{{ alert.title }}</div>
                <div class="alert-message">{{ alert.message }}</div>
                <div class="alert-time">{{ alert.time }}</div>
              </div>
              <div class="alert-actions">
                <el-button size="small" @click="handleAlert(alert)">处理</el-button>
                <el-button size="small" @click="dismissAlert(alert.id)">忽略</el-button>
              </div>
            </div>
            <div v-if="emergencyAlerts.length === 0" class="no-alerts">
              <el-icon><Check /></el-icon>
              <span>当前无紧急警报</span>
            </div>
          </div>
        </div>

        <!-- Geographic Distribution Map -->
        <div class="monitoring-card geographic-map">
          <div class="card-header">
            <h3>地理分布图</h3>
            <div class="map-controls">
              <el-button-group size="small">
                <el-button @click="setMapView('inventory')">库存</el-button>
                <el-button @click="setMapView('demand')">需求</el-button>
                <el-button @click="setMapView('centers')">中心</el-button>
              </el-button-group>
            </div>
          </div>
          <div class="map-container">
            <div class="map-placeholder">
              <el-icon><Location /></el-icon>
              <h4>实时地理分布</h4>
              <p>显示各区域血液库存和需求分布</p>
              <div class="map-legend">
                <div class="legend-item">
                  <div class="legend-color high"></div>
                  <span>高需求</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color medium"></div>
                  <span>中等需求</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color low"></div>
                  <span>低需求</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI-Powered Features Section -->
    <div class="ai-features-section">
      <div class="section-header">
        <h2 class="section-title">AI智能功能</h2>
        <div class="section-actions">
          <el-button @click="toggleAIMode" :type="aiMode ? 'primary' : ''">
            <el-icon><Star /></el-icon>
            AI模式
          </el-button>
        </div>
      </div>
      
      <div class="ai-features-grid">
        <div class="ai-feature-card clickable" @click="showAIDetails('blood-match')">
          <div class="feature-icon blood-match">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <div class="feature-content">
            <h3>血液匹配AI</h3>
            <p>智能预测最佳供血者-受血者匹配，超越基础血型考虑</p>
            <div class="feature-stats">
              <span class="stat">匹配准确率: 98.7%</span>
            </div>
          </div>
        </div>
        
        <div class="ai-feature-card clickable" @click="showAIDetails('scarcity-alert')">
          <div class="feature-icon scarcity-alert">
            <el-icon><Warning /></el-icon>
          </div>
          <div class="feature-content">
            <h3>稀缺预警系统</h3>
            <p>AI预测2-3周前区域血液短缺，基于天气、假期、活动数据</p>
            <div class="feature-stats">
              <span class="stat">预警准确率: 94.2%</span>
            </div>
          </div>
        </div>
        
        <div class="ai-feature-card clickable" @click="showAIDetails('inventory-opt')">
          <div class="feature-icon inventory-opt">
            <el-icon><Box /></el-icon>
          </div>
          <div class="feature-content">
            <h3>智能库存优化</h3>
            <p>机器学习建议最佳血液成分生产比例，基于预测需求</p>
            <div class="feature-stats">
              <span class="stat">效率提升: 23%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Emergency Response Dashboard -->
    <div class="emergency-section">
      <div class="section-header">
        <h2 class="section-title">应急响应中心</h2>
        <div class="section-actions">
          <el-button @click="toggleEmergencyMode" :type="emergencyMode ? 'danger' : ''">
            <el-icon><Warning /></el-icon>
            {{ emergencyMode ? '应急模式激活' : '激活应急模式' }}
          </el-button>
        </div>
      </div>
      
      <div class="emergency-dashboard" :class="{ 'active': emergencyMode }">
        <div class="emergency-stats">
          <div class="emergency-stat">
            <div class="stat-value">{{ emergencyStats.activeEmergencies }}</div>
            <div class="stat-label">活跃紧急事件</div>
          </div>
          <div class="emergency-stat">
            <div class="stat-value">{{ emergencyStats.bloodNeeded }}</div>
            <div class="stat-label">急需血液单位</div>
          </div>
          <div class="emergency-stat">
            <div class="stat-value">{{ emergencyStats.donorsAlerted }}</div>
            <div class="stat-label">已通知捐赠者</div>
          </div>
        </div>
        
        <div class="emergency-map">
          <div class="map-placeholder">
            <div class="emergency-pulse"></div>
            <span>实时应急地图</span>
          </div>
        </div>
        
        <div class="emergency-actions">
          <el-button type="danger" size="large" @click="activateMassCasualty">
            <el-icon><Warning /></el-icon>
            大规模伤亡模式
          </el-button>
          <el-button type="primary" size="large" @click="mobilizeDonors">
            <el-icon><Promotion /></el-icon>
            动员捐赠者
          </el-button>
        </div>
      </div>
    </div>

    <!-- Enhanced KPI Section -->
    <div class="kpi-section">
      <div class="section-header">
        <h2 class="section-title">实时分析</h2>
        <div class="section-actions">
          <el-button-group>
            <el-button :type="timeRange === 'day' ? 'primary' : ''" @click="setTimeRange('day')">日</el-button>
            <el-button :type="timeRange === 'week' ? 'primary' : ''" @click="setTimeRange('week')">周</el-button>
            <el-button :type="timeRange === 'month' ? 'primary' : ''" @click="setTimeRange('month')">月</el-button>
            <el-button :type="timeRange === 'year' ? 'primary' : ''" @click="setTimeRange('year')">年</el-button>
          </el-button-group>
          <el-button @click="toggleMainAutoRefresh" :type="autoRefresh ? 'success' : ''">
            <el-icon><Timer /></el-icon>
            自动刷新
          </el-button>
        </div>
      </div>
      
      <div class="kpi-grid">
        <div v-for="kpi in enhancedKpis" :key="kpi.id" class="kpi-card advanced" :class="kpi.trend">
          <div class="kpi-header">
            <div class="kpi-icon-wrapper">
              <div class="kpi-icon" :style="{ background: kpi.gradient }">
                <el-icon>
                  <component :is="kpi.icon" />
                </el-icon>
              </div>
              <div class="kpi-badge" :class="kpi.status.toLowerCase()">
                {{ kpi.status }}
              </div>
              <div class="kpi-live-indicator" v-if="kpi.live">
                <div class="live-dot"></div>
                <span>实时</span>
              </div>
            </div>
            <div class="kpi-menu">
              <el-dropdown trigger="click">
                <el-button text>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="viewDetails(kpi)">查看详情</el-dropdown-item>
                    <el-dropdown-item @click="exportKpi(kpi)">导出数据</el-dropdown-item>
                    <el-dropdown-item @click="setAlert(kpi)">设置警报</el-dropdown-item>
                    <el-dropdown-item @click="viewHistory(kpi)">查看历史</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          
          <div class="kpi-content">
            <div class="kpi-value-wrapper">
              <div class="kpi-value" :class="{ 'updating': kpi.updating }">{{ kpi.value }}</div>
              <div class="kpi-change" :class="kpi.trend">
                <el-icon v-if="kpi.trend === 'up'"><TrendCharts /></el-icon>
                <el-icon v-else><TrendCharts /></el-icon>
                <span>{{ kpi.change }}</span>
              </div>
            </div>
            <div class="kpi-label">{{ kpi.label }}</div>
            <div class="kpi-sparkline">
              <div class="sparkline-chart" :style="{ background: kpi.sparklineGradient }"></div>
            </div>
            <div class="kpi-progress">
              <el-progress :percentage="kpi.progress" :color="kpi.progressColor" :show-text="false" />
              <span class="progress-text">{{ kpi.progress }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Donor Engagement Revolution -->
    <div class="donor-engagement-section">
      <div class="section-header">
        <h2 class="section-title">捐赠者参与革命</h2>
        <div class="section-actions">
          <el-button @click="showGamification">
            <el-icon><Star /></el-icon>
            游戏化系统
          </el-button>
        </div>
      </div>
      
      <div class="engagement-features">
        <div class="engagement-card health-passport">
          <div class="card-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="card-content">
            <h3>健康护照</h3>
            <p>追踪捐赠者健康指标，展示献血健康益处</p>
            <div class="passport-stats">
              <div class="mini-stat">
                <span class="value">12</span>
                <span class="label">捐赠次数</span>
              </div>
              <div class="mini-stat">
                <span class="value">3.6L</span>
                <span class="label">总献血量</span>
              </div>
              <div class="mini-stat">
                <span class="value">36</span>
                <span class="label">拯救生命</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="engagement-card vr-education">
          <div class="card-icon">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="card-content">
            <h3>VR教育体验</h3>
            <p>3D可视化血液成分使用：血小板抗癌、血浆救烧伤</p>
            <el-button type="primary" size="small" @click="startVRExperience">
              开始VR体验
            </el-button>
          </div>
        </div>
        
        <div class="engagement-card gamification">
          <div class="card-icon">
            <el-icon><Star /></el-icon>
          </div>
          <div class="card-content">
            <h3>游戏化系统</h3>
            <p>里程碑徽章、排行榜、影响力可视化</p>
            <div class="badges">
              <div class="badge gold" title="首次捐赠">🏆</div>
              <div class="badge silver" title="加仑俱乐部">💎</div>
              <div class="badge bronze" title="应急响应者">🚨</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Impact Visualization -->
    <div class="impact-section">
      <div class="section-header">
        <h2 class="section-title">影响力可视化</h2>
        <div class="section-actions">
          <el-button @click="generateImpactStory">
            <el-icon><Document /></el-icon>
            生成影响力故事
          </el-button>
        </div>
      </div>
      
      <div class="impact-dashboard">
        <div class="blood-flow-visualization">
          <div class="flow-title">血液流动实时地图</div>
          <div class="flow-map">
            <div class="flow-node donor">供血者</div>
            <div class="flow-arrow">→</div>
            <div class="flow-node center">血液中心</div>
            <div class="flow-arrow">→</div>
            <div class="flow-node hospital">医院</div>
            <div class="flow-arrow">→</div>
            <div class="flow-node recipient">受血者</div>
          </div>
        </div>
        
        <div class="impact-stories">
          <div class="story-card">
            <div class="story-icon">❤️</div>
            <div class="story-content">
              <h4>您的血液拯救了3条生命</h4>
              <p>包括一名癌症患者、一名车祸伤者和一名早产儿</p>
            </div>
          </div>
          <div class="story-card">
            <div class="story-icon">🏥</div>
            <div class="story-content">
              <h4>社区医院血库充足</h4>
              <p>感谢您的定期捐赠，本地医院血库保持安全水平</p>
            </div>
          </div>
        </div>
        
        <div class="sustainability-metrics">
          <h3>可持续性指标</h3>
          <div class="metric">
            <span class="metric-label">环境足迹减少:</span>
            <span class="metric-value">-45%</span>
          </div>
          <div class="metric">
            <span class="metric-label">vs合成替代品:</span>
            <span class="metric-value">100%天然</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Advanced Analytics Suite -->
    <div class="charts-section">
      <el-row :gutter="24">
        <el-col :span="16">
          <div class="chart-card advanced">
            <div class="chart-header">
              <h3>捐赠趋势分析</h3>
              <div class="chart-controls">
                <el-select v-model="chartPeriod" size="small">
                  <el-option label="最近7天" value="7d" />
                  <el-option label="最近30天" value="30d" />
                  <el-option label="最近90天" value="90d" />
                </el-select>
                <el-button size="small" @click="refreshChart">
                  <el-icon><Refresh /></el-icon>
                </el-button>
                <el-button size="small" @click="toggleChartType">
                  <el-icon><Switch /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="chart-container">
              <div class="chart-placeholder advanced" :class="{ 'chart-3d': chartType === '3d' }">
                <div class="chart-animation">
                  <div class="chart-bar" style="height: 60%; animation-delay: 0s;"></div>
                  <div class="chart-bar" style="height: 80%; animation-delay: 0.2s;"></div>
                  <div class="chart-bar" style="height: 45%; animation-delay: 0.4s;"></div>
                  <div class="chart-bar" style="height: 90%; animation-delay: 0.6s;"></div>
                  <div class="chart-bar" style="height: 70%; animation-delay: 0.8s;"></div>
                  <div class="chart-bar" style="height: 85%; animation-delay: 1s;"></div>
                  <div class="chart-bar" style="height: 65%; animation-delay: 1.2s;"></div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="chart-card advanced">
            <div class="chart-header">
              <h3>血型分布</h3>
              <el-button size="small" @click="refreshBloodChart">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
            <div class="chart-container">
              <div class="blood-type-wheel">
                <div class="wheel-segment" v-for="type in bloodTypes" :key="type.type" 
                     :style="{ transform: `rotate(${type.angle}deg)`, background: type.color }">
                  <div class="segment-label">{{ type.type }}</div>
                </div>
                <div class="wheel-center">
                  <div class="center-value">{{ totalBloodUnits }}</div>
                  <div class="center-label">总单位数</div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- Quantum Analytics Dashboard -->
    <div class="quantum-analytics-section">
      <div class="section-header">
        <h2 class="section-title">量子分析仪表板</h2>
        <div class="section-actions">
          <el-button @click="activateQuantumMode" :type="quantumMode ? 'primary' : ''">
            <el-icon><MagicStick /></el-icon>
            量子模式
          </el-button>
          <el-button @click="toggleNeuralNetwork" :type="neuralNetworkActive ? 'success' : ''">
            <el-icon><Connection /></el-icon>
            神经网络
          </el-button>
        </div>
      </div>
      
      <div class="quantum-dashboard" :class="{ 'quantum-active': quantumMode }">
        <!-- Quantum Blood Prediction -->
        <div class="quantum-card prediction">
          <div class="quantum-header">
            <div class="quantum-icon">
              <div class="quantum-orb"></div>
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="quantum-title">
              <h3>量子血液预测</h3>
              <p>基于量子计算的血液需求预测</p>
            </div>
            <div class="quantum-status">
              <div class="quantum-indicator active"></div>
              <span>量子计算中</span>
            </div>
          </div>
          <div class="quantum-content">
            <div class="prediction-grid">
              <div v-for="prediction in quantumPredictions" :key="prediction.id" class="prediction-item">
                <div class="prediction-time">{{ prediction.time }}</div>
                <div class="prediction-blood-type">{{ prediction.type }}</div>
                <div class="prediction-amount" :class="prediction.severity">{{ prediction.amount }}ml</div>
                <div class="prediction-confidence" :style="{ width: prediction.confidence + '%' }"></div>
                <div class="prediction-label">{{ prediction.confidence }}% 置信度</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Neural Network Analysis -->
        <div class="quantum-card neural">
          <div class="neural-header">
            <div class="neural-icon">
              <div class="neural-network">
                <div class="neural-node" v-for="n in 12" :key="n" :style="{ animationDelay: (n * 0.1) + 's' }"></div>
                <div class="neural-connection" v-for="c in 8" :key="'c-' + c" :style="{ animationDelay: (c * 0.15) + 's' }"></div>
              </div>
            </div>
            <div class="neural-title">
              <h3>神经网络分析</h3>
              <p>深度学习血液模式识别</p>
            </div>
          </div>
          <div class="neural-content">
            <div class="neural-metrics">
              <div class="neural-metric">
                <div class="metric-value">99.7%</div>
                <div class="metric-label">预测准确率</div>
              </div>
              <div class="neural-metric">
                <div class="metric-value">0.3s</div>
                <div class="metric-label">响应时间</div>
              </div>
              <div class="neural-metric">
                <div class="metric-value">1.2M</div>
                <div class="metric-label">数据点处理</div>
              </div>
            </div>
            <div class="neural-patterns">
              <div class="pattern-item">
                <div class="pattern-icon">🧬</div>
                <div class="pattern-text">DNA匹配优化</div>
              </div>
              <div class="pattern-item">
                <div class="pattern-icon">🧠</div>
                <div class="pattern-text">认知决策支持</div>
              </div>
              <div class="pattern-item">
                <div class="pattern-icon">⚡</div>
                <div class="pattern-text">实时学习适应</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Holographic Blood Flow -->
        <div class="quantum-card holographic">
          <div class="holo-header">
            <div class="holo-icon">
              <div class="hologram">
                <div class="holo-layer layer-1"></div>
                <div class="holo-layer layer-2"></div>
                <div class="holo-layer layer-3"></div>
              </div>
            </div>
            <div class="holo-title">
              <h3>全息血液流动</h3>
              <p>3D实时血液分布可视化</p>
            </div>
          </div>
          <div class="holo-content">
            <div class="blood-stream">
              <div class="stream-particle" v-for="particle in bloodParticles" :key="particle.id"
                   :style="{ 
                     left: particle.x + '%', 
                     top: particle.y + '%', 
                     animationDelay: particle.delay + 's',
                     '--blood-color': particle.color 
                   }">
                <div class="particle-core"></div>
              </div>
            </div>
            <div class="stream-controls">
              <el-button-group size="small">
                <el-button @click="setStreamView('arterial')">动脉</el-button>
                <el-button @click="setStreamView('venous')">静脉</el-button>
                <el-button @click="setStreamView('capillary')">毛细血管</el-button>
              </el-button-group>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Blockchain Blood Tracking -->
    <div class="blockchain-section">
      <div class="section-header">
        <h2 class="section-title">区块链血液追踪</h2>
        <div class="section-actions">
          <el-button @click="verifyBlockchain" :loading="verifyingBlockchain">
            <el-icon><Key /></el-icon>
            验证区块链
          </el-button>
          <el-button @click="mintNFT" type="primary">
            <el-icon><Coin /></el-icon>
            铸造NFT证书
          </el-button>
        </div>
      </div>
      
      <div class="blockchain-dashboard">
        <!-- Blood Chain Explorer -->
        <div class="blockchain-card explorer">
          <div class="chain-header">
            <div class="chain-icon">
              <div class="blockchain-visual">
                <div class="block" v-for="block in blockchainBlocks" :key="block.id" 
                     :style="{ animationDelay: block.delay + 's' }">
                  <div class="block-hash">{{ block.hash }}</div>
                </div>
                <div class="chain-link" v-for="link in blockchainLinks" :key="link.id"></div>
              </div>
            </div>
            <div class="chain-title">
              <h3>血液链浏览器</h3>
              <p>不可篡改的血液追踪记录</p>
            </div>
          </div>
          <div class="chain-content">
            <div class="chain-stats">
              <div class="chain-stat">
                <div class="stat-value">{{ blockchainStats.totalBlocks }}</div>
                <div class="stat-label">区块总数</div>
              </div>
              <div class="chain-stat">
                <div class="stat-value">{{ blockchainStats.transactions }}</div>
                <div class="stat-label">交易记录</div>
              </div>
              <div class="chain-stat">
                <div class="stat-value">{{ blockchainStats.verified }}</div>
                <div class="stat-label">已验证</div>
              </div>
            </div>
            <div class="recent-transactions">
              <div v-for="tx in recentTransactions" :key="tx.id" class="transaction-item">
                <div class="tx-hash">{{ tx.hash }}</div>
                <div class="tx-type">{{ tx.type }}</div>
                <div class="tx-amount">{{ tx.amount }}ml</div>
                <div class="tx-status" :class="tx.status">{{ tx.statusText }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Smart Contracts -->
        <div class="blockchain-card contracts">
          <div class="contract-header">
            <div class="contract-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="contract-title">
              <h3>智能合约</h3>
              <p>自动化血液管理协议</p>
            </div>
          </div>
          <div class="contract-content">
            <div class="contract-list">
              <div v-for="contract in smartContracts" :key="contract.id" class="contract-item">
                <div class="contract-name">{{ contract.name }}</div>
                <div class="contract-desc">{{ contract.description }}</div>
                <div class="contract-status">
                  <div class="status-dot" :class="contract.status"></div>
                  <span>{{ contract.statusText }}</span>
                </div>
                <el-button size="small" @click="executeContract(contract)">执行</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- NFT Certificates -->
        <div class="blockchain-card nft">
          <div class="nft-header">
            <div class="nft-icon">
              <div class="nft-badge">
                <div class="badge-shine"></div>
                <el-icon><Medal /></el-icon>
              </div>
            </div>
            <div class="nft-title">
              <h3>NFT数字证书</h3>
              <p>血液捐赠者数字身份认证</p>
            </div>
          </div>
          <div class="nft-content">
            <div class="nft-gallery">
              <div v-for="nft in nftCertificates" :key="nft.id" class="nft-item">
                <div class="nft-image" :style="{ backgroundImage: `url(${nft.image})` }">
                  <div class="nft-overlay">
                    <div class="nft-rarity" :class="nft.rarity">{{ nft.rarityText }}</div>
                  </div>
                </div>
                <div class="nft-info">
                  <div class="nft-name">{{ nft.name }}</div>
                  <div class="nft-donor">{{ nft.donor }}</div>
                  <div class="nft-value">{{ nft.value }} ETH</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Metaverse Blood Center -->
    <div class="metaverse-section">
      <div class="section-header">
        <h2 class="section-title">元宇宙血液中心</h2>
        <div class="section-actions">
          <el-button @click="enterMetaverse" type="primary" size="large">
            <el-icon><VideoCamera /></el-icon>
            进入元宇宙
          </el-button>
          <el-button @click="toggleARMode" :type="arMode ? 'success' : ''">
            <el-icon><Iphone /></el-icon>
            AR模式
          </el-button>
        </div>
      </div>
      
      <div class="metaverse-dashboard">
        <!-- Virtual Blood Center -->
        <div class="metaverse-card virtual-center">
          <div class="vr-header">
            <div class="vr-icon">
              <div class="vr-preview">
                <div class="vr-room">
                  <div class="vr-equipment" v-for="item in vrEquipment" :key="item.id"
                       :style="{ left: item.x + '%', top: item.y + '%' }">
                    <el-icon><component :is="item.icon" /></el-icon>
                  </div>
                </div>
              </div>
            </div>
            <div class="vr-title">
              <h3>虚拟血液中心</h3>
              <p>沉浸式3D血液管理体验</p>
            </div>
          </div>
          <div class="vr-content">
            <div class="vr-features">
              <div class="vr-feature">
                <div class="feature-icon">🥽</div>
                <div class="feature-text">VR设备支持</div>
              </div>
              <div class="vr-feature">
                <div class="feature-icon">🎮</div>
                <div class="feature-text">交互式培训</div>
              </div>
              <div class="vr-feature">
                <div class="feature-icon">🌐</div>
                <div class="feature-text">全球协作</div>
              </div>
            </div>
            <div class="vr-stats">
              <div class="vr-stat">
                <div class="stat-value">{{ vrStats.activeUsers }}</div>
                <div class="stat-label">在线用户</div>
              </div>
              <div class="vr-stat">
                <div class="stat-value">{{ vrStats.sessions }}</div>
                <div class="stat-label">今日会话</div>
              </div>
              <div class="vr-stat">
                <div class="stat-value">{{ vrStats.satisfaction }}%</div>
                <div class="stat-label">满意度</div>
              </div>
            </div>
          </div>
        </div>

        <!-- AR Blood Scanner -->
        <div class="metaverse-card ar-scanner">
          <div class="ar-header">
            <div class="ar-icon">
              <div class="ar-viewfinder">
                <div class="viewfinder-frame"></div>
                <div class="scan-line"></div>
                <div class="scan-points">
                  <div class="scan-point" v-for="point in 8" :key="point"></div>
                </div>
              </div>
            </div>
            <div class="ar-title">
              <h3>AR血液扫描仪</h3>
              <p>增强现实血液分析技术</p>
            </div>
          </div>
          <div class="ar-content">
            <div class="ar-capabilities">
              <div class="ar-capability">
                <div class="cap-icon">📱</div>
                <div class="cap-text">移动AR支持</div>
              </div>
              <div class="ar-capability">
                <div class="cap-icon">🔍</div>
                <div class="cap-text">实时血管识别</div>
              </div>
              <div class="ar-capability">
                <div class="cap-icon">📊</div>
                <div class="cap-text">3D数据可视化</div>
              </div>
            </div>
            <el-button type="primary" @click="startARScan" size="large">
              <el-icon><Camera /></el-icon>
              开始AR扫描
            </el-button>
          </div>
        </div>

        <!-- Digital Twin Simulation -->
        <div class="metaverse-card digital-twin">
          <div class="twin-header">
            <div class="twin-icon">
              <div class="twin-visualization">
                <div class="twin-body">
                  <div class="twin-organ heart" @click="simulateOrgan('heart')">
                    <el-icon><CaretBottom /></el-icon>
                  </div>
                  <div class="twin-organ lungs" @click="simulateOrgan('lungs')">
                    <el-icon><Operation /></el-icon>
                  </div>
                  <div class="twin-organ liver" @click="simulateOrgan('liver')">
                    <el-icon><Tools /></el-icon>
                  </div>
                  <div class="blood-flow" v-for="flow in bloodFlows" :key="flow.id"
                       :style="{ animationDelay: flow.delay + 's' }"></div>
                </div>
              </div>
            </div>
            <div class="twin-title">
              <h3>数字孪生仿真</h3>
              <p>患者血液系统数字模型</p>
            </div>
          </div>
          <div class="twin-content">
            <div class="twin-controls">
              <el-button-group>
                <el-button @click="runSimulation('normal')">正常</el-button>
                <el-button @click="runSimulation('emergency')">紧急</el-button>
                <el-button @click="runSimulation('surgery')">手术</el-button>
              </el-button-group>
            </div>
            <div class="twin-results">
              <div class="result-item">
                <span class="result-label">血氧饱和度:</span>
                <span class="result-value">98.2%</span>
              </div>
              <div class="result-item">
                <span class="result-label">循环效率:</span>
                <span class="result-value">94.7%</span>
              </div>
              <div class="result-item">
                <span class="result-label">预测风险:</span>
                <span class="result-value low">低风险</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Professional Profile Sidebar -->
    <aside class="professional-sidebar" :class="{ active: showProfile }">
      <div class="sidebar-header">
        <div class="sidebar-title">
          <el-icon><User /></el-icon>
          <h3>个人中心</h3>
        </div>
        <el-button @click="toggleProfile" class="close-btn" text>
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      
      <div class="sidebar-content">
        <!-- User Profile Section -->
        <div class="profile-section">
          <div class="user-avatar">
            <img src="https://picsum.photos/seed/user-avatar/100/100.jpg" alt="用户头像" />
            <div class="status-indicator online"></div>
          </div>
          <div class="user-info">
            <h4>张医生</h4>
            <p class="user-title">高级血液分析师</p>
            <p class="user-id">ID: BDA-2024-0892</p>
            <div class="user-badges">
              <span class="badge premium">高级会员</span>
              <span class="badge verified">已认证</span>
              <span class="badge expert">专家</span>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-section">
          <h5>快速统计</h5>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon">
                <el-icon><Star /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">156</div>
                <div class="stat-label">捐赠次数</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">
                <el-icon><DataAnalysis /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">A+</div>
                <div class="stat-label">血型</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">
                <el-icon><Box /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">4.8L</div>
                <div class="stat-label">总献血量</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Settings Menu -->
        <div class="settings-menu">
          <h5>账户设置</h5>
          <div class="menu-items">
            <div class="menu-item" @click="viewFullProfile">
              <el-icon><User /></el-icon>
              <span>个人资料</span>
              <el-icon class="arrow"><Right /></el-icon>
            </div>
            <div class="menu-item" @click="shareProfile">
              <el-icon><Share /></el-icon>
              <span>分享资料</span>
              <el-icon class="arrow"><Right /></el-icon>
            </div>
            <div class="menu-item" @click="exportHealthData">
              <el-icon><Document /></el-icon>
              <span>导出数据</span>
              <el-icon class="arrow"><Right /></el-icon>
            </div>
            <div class="menu-item" @click="securityAudit">
              <el-icon><Warning /></el-icon>
              <span>安全审计</span>
              <el-icon class="arrow"><Right /></el-icon>
            </div>
          </div>
        </div>

        <!-- Notification Settings -->
        <div class="notification-settings">
          <h5>通知设置</h5>
          <div class="setting-toggles">
            <div class="toggle-item">
              <div class="toggle-info">
                <span>捐赠提醒</span>
                <small>定期捐赠提醒通知</small>
              </div>
              <el-switch v-model="settings.donationReminders" />
            </div>
            <div class="toggle-item">
              <div class="toggle-info">
                <span>紧急通知</span>
                <small>紧急情况血液需求</small>
              </div>
              <el-switch v-model="settings.emergencyAlerts" />
            </div>
            <div class="toggle-item">
              <div class="toggle-info">
                <span>健康报告</span>
                <small>定期健康指标报告</small>
              </div>
              <el-switch v-model="settings.healthReports" />
            </div>
          </div>
        </div>

        <!-- Privacy Settings -->
        <div class="privacy-settings">
          <h5>隐私设置</h5>
          <div class="setting-toggles">
            <div class="toggle-item">
              <div class="toggle-info">
                <span>公开资料</span>
                <small>其他用户可查看我的资料</small>
              </div>
              <el-switch v-model="settings.publicProfile" />
            </div>
            <div class="toggle-item">
              <div class="toggle-info">
                <span>数据分享</span>
                <small>参与医学研究数据共享</small>
              </div>
              <el-switch v-model="settings.dataSharing" />
            </div>
            <div class="toggle-item">
              <div class="toggle-info">
                <span>位置信息</span>
                <small>显示大致位置信息</small>
              </div>
              <el-switch v-model="settings.locationSharing" />
            </div>
          </div>
        </div>

        <!-- Security Actions -->
        <div class="security-actions">
          <h5>安全操作</h5>
          <div class="action-buttons">
            <el-button @click="changePassword" class="security-btn warning">
              <el-icon><Setting /></el-icon>
              修改密码
            </el-button>
            <el-button @click="logoutAll" class="security-btn danger">
              <el-icon><Close /></el-icon>
              退出所有设备
            </el-button>
          </div>
        </div>
      </div>
    </aside>

    <!-- Drag-and-Drop Dashboard Builder -->
    <div class="dashboard-builder-section" v-show="currentView === 'dashboard-builder'">
      <div class="section-header">
        <h2 class="section-title">仪表板构建器</h2>
        <div class="section-actions">
          <el-button @click="saveDashboard" type="primary">
            <el-icon><Document /></el-icon>
            保存仪表板
          </el-button>
          <el-button @click="loadDashboard">
            <el-icon><Upload /></el-icon>
            加载仪表板
          </el-button>
          <el-button @click="exportDashboard">
            <el-icon><Share /></el-icon>
            导出配置
          </el-button>
          <el-button @click="resetDashboard">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
      </div>

      <!-- Dashboard Settings Panel -->
      <div class="dashboard-settings">
        <div class="settings-tabs">
          <el-tabs v-model="activeSettingsTab" type="card">
            <el-tab-pane label="基本设置" name="basic">
              <div class="settings-content">
                <div class="setting-item">
                  <label>仪表板名称</label>
                  <el-input v-model="currentDashboardName" placeholder="输入仪表板名称" />
                </div>
                <div class="setting-item">
                  <label>主题选择</label>
                  <div class="theme-selector">
                    <div 
                      v-for="theme in availableThemes" 
                      :key="theme.id"
                      class="theme-option"
                      :class="{ active: currentTheme === theme.id }"
                      @click="changeTheme(theme)"
                    >
                      <div class="theme-preview" :style="{ background: `linear-gradient(135deg, ${theme.colors[0]} 0%, ${theme.colors[1]} 100%)` }"></div>
                      <span>{{ theme.name }}</span>
                    </div>
                  </div>
                </div>
                <div class="setting-item">
                  <label>自动刷新</label>
                  <div class="refresh-controls">
                    <el-switch v-model="autoRefreshEnabled" @change="toggleAutoRefresh" />
                    <el-input-number 
                      v-model="refreshInterval" 
                      :min="5" 
                      :max="300" 
                      :disabled="!autoRefreshEnabled"
                      @change="updateRefreshInterval"
                    />
                    <span>秒</span>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="模板" name="templates">
              <div class="settings-content">
                <div class="template-grid">
                  <div 
                    v-for="template in dashboardTemplates" 
                    :key="template.id"
                    class="template-card"
                    @click="applyTemplate(template)"
                  >
                    <div class="template-preview">
                      <div class="mini-layout">
                        <div v-for="(item, index) in template.items.slice(0, 3)" :key="index" 
                             class="mini-component" 
                             :style="getMiniComponentStyle(item, index)">
                        </div>
                      </div>
                    </div>
                    <div class="template-info">
                      <h4>{{ template.name }}</h4>
                      <p>{{ template.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="导入/导出" name="import-export">
              <div class="settings-content">
                <div class="setting-item">
                  <label>导入仪表板配置</label>
                  <el-upload
                    class="upload-demo"
                    :auto-upload="false"
                    :on-change="importDashboard"
                    accept=".json"
                  >
                    <el-button type="primary">
                      <el-icon><Upload /></el-icon>
                      选择文件
                    </el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持 JSON 格式的仪表板配置文件
                      </div>
                    </template>
                  </el-upload>
                </div>
                <div class="setting-item">
                  <label>导出当前配置</label>
                  <el-button @click="exportDashboard" type="success">
                    <el-icon><Share /></el-icon>
                    导出配置文件
                  </el-button>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <!-- Component Palette -->
      <div class="component-palette">
        <h3>组件库</h3>
        <div class="palette-grid">
          <div 
            v-for="component in componentPalette" 
            :key="component.id"
            class="palette-item"
            draggable="true"
            @dragstart="handleDragStart($event, component)"
          >
            <div class="palette-icon" :style="{ background: component.gradient }">
              <el-icon>
                <component :is="component.icon" />
              </el-icon>
            </div>
            <span>{{ component.name }}</span>
          </div>
        </div>
      </div>

      <!-- Drop Zone -->
      <div class="dashboard-canvas">
        <div 
          class="drop-zone"
          @drop="handleDrop($event)"
          @dragover="handleDragOver($event)"
          @dragleave="handleDragLeave($event)"
          :class="{ 'drag-over': isDragOver }"
        >
          <div class="canvas-header">
            <h3>仪表板画布</h3>
            <div class="layout-controls">
              <el-button-group>
                <el-button size="small" @click="setLayout('grid')">网格</el-button>
                <el-button size="small" @click="setLayout('free')">自由</el-button>
                <el-button size="small" @click="setLayout('masonry')">瀑布</el-button>
              </el-button-group>
            </div>
          </div>
          
          <div class="canvas-content" :class="`layout-${currentLayout}`">
            <div 
              v-for="(item, index) in dashboardItems" 
              :key="item.id"
              class="dashboard-component"
              :class="`component-${item.type}`"
              :style="getItemStyle(item, index)"
              draggable="true"
              @dragstart="handleComponentDragStart($event, index)"
              @drop="handleComponentDrop($event, index)"
              @dragover="handleComponentDragOver($event)"
            >
              <div class="component-header">
                <h4>{{ item.title }}</h4>
                <div class="component-actions">
                  <el-button size="small" text @click="editComponent(index)">
                    <el-icon><Setting /></el-icon>
                  </el-button>
                  <el-button size="small" text @click="removeComponent(index)">
                    <el-icon><Close /></el-icon>
                  </el-button>
                </div>
              </div>
              
              <div class="component-content">
                <!-- Chart Component -->
                <div v-if="item.type === 'chart'" class="chart-placeholder">
                  <div class="chart-icon">
                    <el-icon><DataAnalysis /></el-icon>
                  </div>
                  <p>{{ item.description || '数据图表' }}</p>
                </div>
                
                <!-- Stats Component -->
                <div v-else-if="item.type === 'stats'" class="stats-grid">
                  <div v-for="stat in item.data || [1,2,3,4]" :key="stat" class="stat-item">
                    <div class="stat-value">{{ Math.floor(Math.random() * 1000) }}</div>
                    <div class="stat-label">指标 {{ stat }}</div>
                  </div>
                </div>
                
                <!-- Table Component -->
                <div v-else-if="item.type === 'table'" class="table-placeholder">
                  <el-table :data="mockTableData" size="small" style="width: 100%">
                    <el-table-column prop="name" label="名称" />
                    <el-table-column prop="value" label="数值" />
                    <el-table-column prop="status" label="状态" />
                  </el-table>
                </div>
                
                <!-- Alert Component -->
                <div v-else-if="item.type === 'alert'" class="alert-placeholder">
                  <el-alert
                    title="系统警报"
                    type="warning"
                    description="这是一个示例警报组件"
                    show-icon
                    :closable="false"
                  />
                </div>
                
                <!-- Progress Component -->
                <div v-else-if="item.type === 'progress'" class="progress-list">
                  <div v-for="progress in item.data || [1,2,3]" :key="progress" class="progress-item">
                    <span>任务 {{ progress }}</span>
                    <el-progress :percentage="Math.floor(Math.random() * 100)" />
                  </div>
                </div>
                
                <!-- Default Component -->
                <div v-else class="default-placeholder">
                  <el-icon><Box /></el-icon>
                  <p>{{ item.description || '组件内容' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Status Monitoring -->
    <div class="system-status-section" v-show="currentView === 'system-status'">
      <div class="section-header">
        <h2 class="section-title">系统状态监控</h2>
        <div class="section-actions">
          <el-button @click="refreshSystemStatus" type="primary">
            <el-icon><Refresh /></el-icon>
            刷新状态
          </el-button>
          <el-button @click="exportStatusReport">
            <el-icon><Share /></el-icon>
            导出报告
          </el-button>
        </div>
      </div>

      <!-- System Overview -->
      <div class="system-overview">
        <div class="overview-cards">
          <div class="status-card" :class="systemHealth.status">
            <div class="status-header">
              <div class="status-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="status-info">
                <h3>系统健康状态</h3>
                <span class="status-value">{{ systemHealth.status }}</span>
              </div>
            </div>
            <div class="status-metrics">
              <div class="metric">
                <span class="metric-label">正常运行时间</span>
                <span class="metric-value">{{ systemHealth.uptime }}%</span>
              </div>
              <div class="metric">
                <span class="metric-label">响应时间</span>
                <span class="metric-value">{{ systemHealth.responseTime }}ms</span>
              </div>
            </div>
          </div>

          <div class="status-card" :class="serverStatus.status">
            <div class="status-header">
              <div class="status-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="status-info">
                <h3>服务器状态</h3>
                <span class="status-value">{{ serverStatus.status }}</span>
              </div>
            </div>
            <div class="status-metrics">
              <div class="metric">
                <span class="metric-label">CPU使用率</span>
                <span class="metric-value">{{ serverStatus.cpuUsage }}%</span>
              </div>
              <div class="metric">
                <span class="metric-label">内存使用率</span>
                <span class="metric-value">{{ serverStatus.memoryUsage }}%</span>
              </div>
            </div>
          </div>

          <div class="status-card" :class="databaseStatus.status">
            <div class="status-header">
              <div class="status-icon">
                <el-icon><Box /></el-icon>
              </div>
              <div class="status-info">
                <h3>数据库状态</h3>
                <span class="status-value">{{ databaseStatus.status }}</span>
              </div>
            </div>
            <div class="status-metrics">
              <div class="metric">
                <span class="metric-label">连接数</span>
                <span class="metric-value">{{ databaseStatus.connections }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">查询时间</span>
                <span class="metric-value">{{ databaseStatus.queryTime }}ms</span>
              </div>
            </div>
          </div>

          <div class="status-card" :class="networkStatus.status">
            <div class="status-header">
              <div class="status-icon">
                <el-icon><Link /></el-icon>
              </div>
              <div class="status-info">
                <h3>网络状态</h3>
                <span class="status-value">{{ networkStatus.status }}</span>
              </div>
            </div>
            <div class="status-metrics">
              <div class="metric">
                <span class="metric-label">带宽使用</span>
                <span class="metric-value">{{ networkStatus.bandwidth }}Mbps</span>
              </div>
              <div class="metric">
                <span class="metric-label">延迟</span>
                <span class="metric-value">{{ networkStatus.latency }}ms</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Service Health Details -->
      <div class="service-health">
        <h3>服务健康详情</h3>
        <div class="service-grid">
          <div 
            v-for="service in services" 
            :key="service.id"
            class="service-card"
            :class="service.status"
          >
            <div class="service-header">
              <div class="service-icon">
                <el-icon>
                  <component :is="service.icon" />
                </el-icon>
              </div>
              <div class="service-info">
                <h4>{{ service.name }}</h4>
                <span class="service-status">{{ service.status }}</span>
              </div>
              <div class="service-actions">
                <el-button size="small" text @click="restartService(service.id)">
                  <el-icon><Refresh /></el-icon>
                </el-button>
                <el-button size="small" text @click="viewServiceLogs(service.id)">
                  <el-icon><Document /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="service-metrics">
              <div class="service-metric">
                <span class="metric-label">CPU</span>
                <div class="metric-bar">
                  <div class="metric-fill" :style="{ width: service.cpu + '%' }"></div>
                </div>
                <span class="metric-value">{{ service.cpu }}%</span>
              </div>
              <div class="service-metric">
                <span class="metric-label">内存</span>
                <div class="metric-bar">
                  <div class="metric-fill" :style="{ width: service.memory + '%' }"></div>
                </div>
                <span class="metric-value">{{ service.memory }}%</span>
              </div>
              <div class="service-metric">
                <span class="metric-label">请求/秒</span>
                <span class="metric-value">{{ service.requests }}</span>
              </div>
            </div>
            <div class="service-alerts" v-if="service.alerts && service.alerts.length > 0">
              <div v-for="alert in service.alerts.slice(0, 2)" :key="alert.id" class="service-alert" :class="alert.type">
                <el-icon><Warning /></el-icon>
                <span>{{ alert.message }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Metrics -->
      <div class="performance-metrics">
        <h3>性能指标</h3>
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-header">
              <h4>响应时间分布</h4>
              <el-button size="small" text @click="viewDetailedMetrics">
                <el-icon><MoreFilled /></el-icon>
              </el-button>
            </div>
            <div class="metric-chart">
              <div class="response-time-bars">
                <div v-for="time in responseTimeDistribution" :key="time.range" class="time-bar">
                  <div class="time-label">{{ time.range }}</div>
                  <div class="time-bar-container">
                    <div class="time-bar-fill" :style="{ width: time.percentage + '%' }"></div>
                  </div>
                  <span class="time-percentage">{{ time.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-header">
              <h4>错误率趋势</h4>
              <el-button size="small" text @click="viewErrorDetails">
                <el-icon><MoreFilled /></el-icon>
              </el-button>
            </div>
            <div class="metric-chart">
              <div class="error-trend">
                <div class="trend-line">
                  <div v-for="(point, index) in errorTrend" :key="index" class="trend-point" :style="{ left: (index * 20) + '%', bottom: point.value + '%' }">
                    <div class="trend-dot"></div>
                    <span class="trend-value">{{ point.value }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-header">
              <h4>吞吐量</h4>
              <el-button size="small" text @click="viewThroughputDetails">
                <el-icon><MoreFilled /></el-icon>
              </el-button>
            </div>
            <div class="metric-chart">
              <div class="throughput-stats">
                <div class="throughput-item">
                  <span class="throughput-label">当前</span>
                  <span class="throughput-value">{{ throughput.current }}</span>
                </div>
                <div class="throughput-item">
                  <span class="throughput-label">平均</span>
                  <span class="throughput-value">{{ throughput.average }}</span>
                </div>
                <div class="throughput-item">
                  <span class="throughput-label">峰值</span>
                  <span class="throughput-value">{{ throughput.peak }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Task Management Section -->
    <div class="task-management-section" v-show="currentView === 'task-management'">
      <div class="section-header">
        <h2 class="section-title">任务管理</h2>
        <div class="section-actions">
          <el-button @click="createNewTask" type="primary">
            <el-icon><Plus /></el-icon>
            新建任务
          </el-button>
          <el-button @click="filterTasks">
            <el-icon><Filter /></el-icon>
            筛选
          </el-button>
          <el-button @click="exportTaskReport">
            <el-icon><Share /></el-icon>
            导出报告
          </el-button>
        </div>
      </div>

      <!-- Task Statistics -->
      <div class="task-statistics">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><List /></el-icon>
            </div>
            <div class="stat-content">
              <h3>总任务数</h3>
              <div class="stat-value">{{ taskStats.total }}</div>
              <div class="stat-change" :class="taskStats.totalChange > 0 ? 'positive' : 'negative'">
                <el-icon><TrendCharts /></el-icon>
                {{ taskStats.totalChange > 0 ? '+' : '' }}{{ taskStats.totalChange }}%
              </div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <h3>进行中</h3>
              <div class="stat-value">{{ taskStats.inProgress }}</div>
              <div class="stat-change positive">
                <el-icon><TrendCharts /></el-icon>
                +{{ taskStats.inProgressChange }}%
              </div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <h3>已完成</h3>
              <div class="stat-value">{{ taskStats.completed }}</div>
              <div class="stat-change positive">
                <el-icon><TrendCharts /></el-icon>
                +{{ taskStats.completedChange }}%
              </div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <h3>待处理</h3>
              <div class="stat-value">{{ taskStats.pending }}</div>
              <div class="stat-change negative">
                <el-icon><TrendCharts /></el-icon>
                {{ taskStats.pendingChange }}%
              </div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Timer /></el-icon>
            </div>
            <div class="stat-content">
              <h3>平均完成时间</h3>
              <div class="stat-value">{{ taskStats.avgCompletionTime }}h</div>
              <div class="stat-change">
                <el-icon><TrendCharts /></el-icon>
                {{ taskStats.avgCompletionTimeChange }}%
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Task Filters -->
      <div class="task-filters">
        <div class="filter-group">
          <label>状态筛选:</label>
          <el-radio-group v-model="taskFilter.status" size="small">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="pending">待处理</el-radio-button>
            <el-radio-button label="in-progress">进行中</el-radio-button>
            <el-radio-button label="completed">已完成</el-radio-button>
            <el-radio-button label="cancelled">已取消</el-radio-button>
          </el-radio-group>
        </div>
        <div class="filter-group">
          <label>优先级:</label>
          <el-select v-model="taskFilter.priority" placeholder="选择优先级" size="small">
            <el-option label="全部" value="all"></el-option>
            <el-option label="高" value="high"></el-option>
            <el-option label="中" value="medium"></el-option>
            <el-option label="低" value="low"></el-option>
          </el-select>
        </div>
        <div class="filter-group">
          <label>负责人:</label>
          <el-select v-model="taskFilter.assignee" placeholder="选择负责人" size="small">
            <el-option label="全部" value="all"></el-option>
            <el-option label="张医生" value="张医生"></el-option>
            <el-option label="李护士" value="李护士"></el-option>
            <el-option label="王技术员" value="王技术员"></el-option>
            <el-option label="陈管理员" value="陈管理员"></el-option>
          </el-select>
        </div>
        <div class="filter-group">
          <label>截止日期:</label>
          <el-date-picker
            v-model="taskFilter.dueDate"
            type="daterange"
            size="small"
            placeholder="选择日期范围"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </div>
      </div>

      <!-- Task List -->
      <div class="task-list">
        <div class="task-table">
          <el-table :data="filteredTasks" style="width: 100%" @selection-change="handleTaskSelection">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="title" label="任务标题" min-width="200">
              <template #default="scope">
                <div class="task-title">
                  <span class="task-title-text">{{ scope.row.title }}</span>
                  <div class="task-tags">
                    <el-tag 
                      v-for="tag in scope.row.tags" 
                      :key="tag" 
                      :type="tag.type"
                      size="small"
                    >
                      {{ tag.label }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag 
                  :type="getPriorityType(scope.row.priority)" 
                  size="small"
                >
                  {{ getPriorityLabel(scope.row.priority) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag 
                  :type="getStatusType(scope.row.status)" 
                  size="small"
                >
                  {{ getStatusLabel(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="assignee" label="负责人" width="120">
              <template #default="scope">
                <div class="assignee-info">
                  <el-avatar :size="20" :src="scope.row.assignee.avatar">
                    {{ scope.row.assignee.name.charAt(0) }}
                  </el-avatar>
                  <span>{{ scope.row.assignee.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="dueDate" label="截止日期" width="120">
              <template #default="scope">
                <span :class="getDueDateClass(scope.row.dueDate)">
                  {{ new Date(scope.row.dueDate).toLocaleDateString('zh-CN') }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="progress" label="进度" width="120">
              <template #default="scope">
                <el-progress 
                  :percentage="scope.row.progress" 
                  :status="getProgressStatus(scope.row.progress)"
                  :stroke-width="6"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <div class="task-actions">
                  <el-button size="small" text @click="editTask(scope.row)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" text @click="viewTaskDetails(scope.row)">
                    <el-icon><View /></el-icon>
                  </el-button>
                  <el-button size="small" text @click="deleteTask(scope.row)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Task Details Modal -->
      <el-dialog v-model="taskDetailsVisible" title="任务详情" width="600px">
        <div v-if="selectedTask" class="task-details">
          <div class="task-detail-header">
            <h3>{{ selectedTask.title }}</h3>
            <div class="task-detail-meta">
              <span class="detail-item">
                <el-icon><User /></el-icon>
                {{ selectedTask.assignee.name }}
              </span>
              <span class="detail-item">
                <el-icon><Calendar /></el-icon>
                {{ new Date(selectedTask.dueDate).toLocaleDateString('zh-CN') }}
              </span>
              <span class="detail-item">
                <el-icon><StarFilled /></el-icon>
                {{ getPriorityLabel(selectedTask.priority) }}
              </span>
            </div>
          </div>
          
          <div class="task-detail-content">
            <div class="detail-section">
              <h4>任务描述</h4>
              <p>{{ selectedTask.description }}</p>
            </div>
            
            <div class="detail-section">
              <h4>任务要求</h4>
              <ul>
                <li v-for="requirement in selectedTask.requirements" :key="requirement">{{ requirement }}</li>
              </ul>
            </div>
            
            <div class="detail-section">
              <h4>附件</h4>
              <div class="attachment-list">
                <div v-for="attachment in selectedTask.attachments" :key="attachment.id" class="attachment-item">
                  <el-icon><Document /></el-icon>
                  <span>{{ attachment.name }}</span>
                  <el-button size="small" text @click="downloadAttachment(attachment)">
                    <el-icon><Download /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
            
            <div class="detail-section">
              <h4>进度记录</h4>
              <div class="progress-history">
                <div v-for="record in selectedTask.progressHistory" :key="record.id" class="progress-record">
                  <div class="record-time">{{ new Date(record.timestamp).toLocaleDateString('zh-CN') }}</div>
                  <div class="record-info">
                    <span>{{ record.user.name }}</span>
                    <span class="record-action">{{ record.action }}</span>
                    <span class="record-value">{{ record.value }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="task-detail-actions">
            <el-button @click="editTask(selectedTask)" type="primary">
              <el-icon><Edit /></el-icon>
              编辑任务
            </el-button>
            <el-button @click="viewTaskComments(selectedTask)">
              <el-icon><ChatDotRound /></el-icon>
              查看评论
            </el-button>
            <el-button @click="shareTask(selectedTask)">
              <el-icon><Share /></el-icon>
              分享任务
            </el-button>
          </div>
        </div>
      </el-dialog>

      <!-- Task Comments Modal -->
      <el-dialog v-model="taskCommentsVisible" title="任务评论" width="600px">
        <div v-if="selectedTask" class="task-comments">
          <div class="comments-header">
            <h4>{{ selectedTask.title }} - 评论</h4>
          </div>
          <div class="comments-list">
            <div v-for="comment in selectedTask.comments" :key="comment.id" class="comment-item">
              <div class="comment-avatar">
                <el-avatar :size="32" :src="comment.user.avatar">
                  {{ comment.user.name.charAt(0) }}
                </el-avatar>
              </div>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.user.name }}</span>
                  <span class="comment-time">{{ new Date(comment.timestamp).toLocaleDateString('zh-CN') }}</span>
                </div>
                <div class="comment-text">{{ comment.content }}</div>
              </div>
            </div>
          </div>
          <div class="comment-input">
            <el-input
              v-model="newComment"
              type="textarea"
              placeholder="添加评论..."
              :rows="3"
            />
            <el-button @click="addComment" type="primary" style="margin-top: 12px;">
              <el-icon><ChatDotRound /></el-icon>
              发送评论
            </el-button>
          </div>
        </div>
      </el-dialog>
    </div>

    <!-- Enhanced Quick Actions -->
    <div class="quick-actions-section">
      <div class="section-header">
        <h2 class="section-title">快速操作</h2>
        <el-button @click="customizeActions">
          <el-icon><Setting /></el-icon>
          自定义
        </el-button>
      </div>
      
      <div class="actions-grid">
        <div v-for="action in quickActions" :key="action.id" class="action-card" @click="executeAction(action)">
          <div class="action-icon" :style="{ background: action.gradient }">
            <el-icon>
              <component :is="action.icon" />
            </el-icon>
          </div>
          <div class="action-content">
            <div class="action-title">{{ action.title }}</div>
            <div class="action-description">{{ action.description }}</div>
          </div>
          <div class="action-shortcut">{{ action.shortcut }}</div>
        </div>
      </div>
    </div>

    <!-- Comprehensive Footer -->
    <footer class="comprehensive-footer">
      <!-- Main Footer Content -->
      <div class="footer-main">
        <div class="footer-container">
          <div class="footer-grid">
            <!-- Blood Domain Platform -->
            <div class="footer-section">
              <div class="footer-logo">
                <h3>血液领域分析平台</h3>
                <p>先进的血液管理和分析系统</p>
              </div>
              <div class="footer-description">
                <p>致力于通过AI技术和数据分析，革新血液管理行业，拯救更多生命。</p>
              </div>
              <div class="social-links">
                <a href="#" class="social-link">
                  <el-icon><Share /></el-icon>
                </a>
                <a href="#" class="social-link">
                  <el-icon><Star /></el-icon>
                </a>
                <a href="#" class="social-link">
                  <el-icon><Document /></el-icon>
                </a>
              </div>
            </div>

            <!-- Quick Links -->
            <div class="footer-section">
              <h4>快速链接</h4>
              <ul class="footer-links">
                <li><a href="#dashboard">仪表板</a></li>
                <li><a href="#analytics">数据分析</a></li>
                <li><a href="#donors">捐赠者管理</a></li>
                <li><a href="#inventory">库存管理</a></li>
                <li><a href="#campaigns">活动管理</a></li>
                <li><a href="#reports">报告中心</a></li>
              </ul>
            </div>

            <!-- AI Features -->
            <div class="footer-section">
              <h4>AI功能</h4>
              <ul class="footer-links">
                <li><a href="#blood-match">血液匹配AI</a></li>
                <li><a href="#scarcity-alert">稀缺预警</a></li>
                <li><a href="#inventory-opt">库存优化</a></li>
                <li><a href="#predictive">预测分析</a></li>
                <li><a href="#emergency">应急响应</a></li>
                <li><a href="#impact">影响力分析</a></li>
              </ul>
            </div>

            <!-- Support -->
            <div class="footer-section">
              <h4>支持与帮助</h4>
              <ul class="footer-links">
                <li><a href="#help">帮助中心</a></li>
                <li><a href="#docs">文档</a></li>
                <li><a href="#api">API文档</a></li>
                <li><a href="#training">培训资源</a></li>
                <li><a href="#community">社区论坛</a></li>
                <li><a href="#contact">联系我们</a></li>
              </ul>
            </div>

            <!-- Contact Info -->
            <div class="footer-section">
              <h4>联系信息</h4>
              <div class="contact-info">
                <div class="contact-item">
                  <el-icon><Phone /></el-icon>
                  <span>紧急热线: 400-123-4567</span>
                </div>
                <div class="contact-item">
                  <el-icon><Message /></el-icon>
                  <span>邮箱: info@blooddomain.cn</span>
                </div>
                <div class="contact-item">
                  <el-icon><Location /></el-icon>
                  <span>地址: 北京市朝阳区生命科学园</span>
                </div>
                <div class="contact-item">
                  <el-icon><Clock /></el-icon>
                  <span>24/7 应急响应</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Impact Statistics -->
      <div class="footer-impact">
        <div class="footer-container">
          <div class="impact-stats">
            <div class="impact-stat">
              <div class="stat-number">2.5M+</div>
              <div class="stat-label">拯救生命</div>
            </div>
            <div class="impact-stat">
              <div class="stat-number">850K+</div>
              <div class="stat-label">注册捐赠者</div>
            </div>
            <div class="impact-stat">
              <div class="stat-number">1,200+</div>
              <div class="stat-label">合作医院</div>
            </div>
            <div class="impact-stat">
              <div class="stat-number">98.7%</div>
              <div class="stat-label">AI匹配准确率</div>
            </div>
            <div class="impact-stat">
              <div class="stat-number">24/7</div>
              <div class="stat-label">全天候服务</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Technology Partners -->
      <div class="footer-partners">
        <div class="footer-container">
          <h4>技术合作伙伴</h4>
          <div class="partners-grid">
            <div class="partner-item">
              <span>🏥 中华医学会</span>
            </div>
            <div class="partner-item">
              <span>🔬 国家血液中心</span>
            </div>
            <div class="partner-item">
              <span>🎓 清华大学医学院</span>
            </div>
            <div class="partner-item">
              <span>🏢 卫健委信息中心</span>
            </div>
            <div class="partner-item">
              <span>🤖 AI医疗联盟</span>
            </div>
            <div class="partner-item">
              <span>📊 大数据健康平台</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Legal & Compliance -->
      <div class="footer-legal">
        <div class="footer-container">
          <div class="legal-content">
            <div class="legal-links">
              <a href="#privacy">隐私政策</a>
              <a href="#terms">使用条款</a>
              <a href="#compliance">合规声明</a>
              <a href="#gdpr">GDPR合规</a>
              <a href="#hipaa">HIPAA合规</a>
              <a href="#accessibility">无障碍访问</a>
            </div>
            <div class="certifications">
              <span class="cert-badge">ISO 27001</span>
              <span class="cert-badge">GDPR</span>
              <span class="cert-badge">HIPAA</span>
              <span class="cert-badge">SOC 2</span>
            </div>
          </div>
          <div class="copyright">
            <p>&copy; 2026 血液领域分析平台. 保留所有权利. | 用❤️和AI构建</p>
          </div>
        </div>
      </div>
    </footer>

    <!-- Floating Action Button -->
    <div class="floating-action-button" :class="{ active: fabOpen }">
      <div class="fab-main" @click="toggleFab">
        <el-icon>
          <Plus />
        </el-icon>
      </div>
      <div class="fab-options">
        <div class="fab-option" @click="navigateToUpload" title="上传数据">
          <el-icon><Upload /></el-icon>
        </div>
        <div class="fab-option" @click="navigateToAnalytics" title="数据分析">
          <el-icon><DataAnalysis /></el-icon>
        </div>
        <div class="fab-option" @click="toggleEmergencyMode" title="应急模式">
          <el-icon><Warning /></el-icon>
        </div>
        <div class="fab-option" @click="toggleAIMode" title="AI助手">
          <el-icon><Star /></el-icon>
        </div>
      </div>
    </div>

    <!-- AI Details Dialog -->
    <el-dialog
      v-model="aiDetailsVisible"
      :title="aiDetails.title"
      width="70%"
      :before-close="closeAIDetails"
      class="ai-details-dialog"
    >
      <div class="ai-details-content">
        <div class="ai-overview">
          <div class="ai-icon-large" :class="aiDetails.iconClass">
            <el-icon><component :is="aiDetails.icon" /></el-icon>
          </div>
          <div class="ai-info">
            <h3>{{ aiDetails.title }}</h3>
            <p>{{ aiDetails.description }}</p>
            <div class="ai-metrics">
              <div class="metric" v-for="metric in aiDetails.metrics" :key="metric.label">
                <span class="metric-value">{{ metric.value }}</span>
                <span class="metric-label">{{ metric.label }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="ai-features">
          <h4>核心功能</h4>
          <ul>
            <li v-for="feature in aiDetails.features" :key="feature">{{ feature }}</li>
          </ul>
        </div>
        
        <div class="ai-benefits">
          <h4>系统优势</h4>
          <div class="benefits-grid">
            <div class="benefit-item" v-for="benefit in aiDetails.benefits" :key="benefit.title">
              <div class="benefit-icon">✓</div>
              <div class="benefit-content">
                <h5>{{ benefit.title }}</h5>
                <p>{{ benefit.description }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="ai-stats">
          <h4>性能统计</h4>
          <div class="stats-grid">
            <div class="stat-item" v-for="stat in aiDetails.stats" :key="stat.label">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeAIDetails">关闭</el-button>
          <el-button type="primary" @click="configureAI">配置设置</el-button>
          <el-button type="success" @click="viewAIReports">查看报告</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Upload, 
  TrendCharts, 
  MoreFilled, 
  Refresh, 
  Document, 
  User, 
  DataAnalysis,
  Warning,
  Star,
  Box,
  Calendar,
  Moon,
  Sunny,
  ChatDotRound,
  Close,
  Promotion,
  Timer,
  Switch,
  VideoPlay,
  Setting,
  Share,
  Phone,
  Message,
  Location,
  Clock,
  Right,
  Plus,
  Monitor,
  Link,
  List,
  Check,
  Filter,
  Edit,
  Delete,
  View,
  StarFilled,
  Download,
  Notification,
  MagicStick,
  Connection,
  Key,
  Coin,
  Medal,
  VideoCamera,
  Iphone,
  Camera,
  CaretBottom,
  Operation,
  Grid,
  Tools
} from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const router = useRouter()
const notificationStore = useNotificationStore()

// Advanced State Management
const isDarkMode = ref(false)
const showAIAssistant = ref(false)
const showProfile = ref(false)
const fabOpen = ref(false)
const currentView = ref('dashboard')
const autoRefresh = ref(false)
const liveFeed = ref(false)
const chartType = ref('2d')
const aiInput = ref('')
const totalBloodUnits = ref('2,456')

// Quantum Analytics State
const quantumMode = ref(false)
const neuralNetworkActive = ref(false)
const quantumPredictions = ref([
  { id: 1, time: '14:30', type: 'A+', amount: 450, confidence: 87, severity: 'medium' },
  { id: 2, time: '15:45', type: 'O-', amount: 320, confidence: 92, severity: 'high' },
  { id: 3, time: '16:20', type: 'B+', amount: 280, confidence: 78, severity: 'low' }
])
const bloodParticles = ref([
  { id: 1, x: 10, y: 20, delay: 0, color: '#ef4444' },
  { id: 2, x: 30, y: 40, delay: 0.5, color: '#3b82f6' },
  { id: 3, x: 50, y: 60, delay: 1, color: '#10b981' },
  { id: 4, x: 70, y: 30, delay: 1.5, color: '#f59e0b' },
  { id: 5, x: 90, y: 50, delay: 2, color: '#8b5cf6' }
])

// Blockchain State
const verifyingBlockchain = ref(false)
const blockchainStats = ref({
  totalBlocks: 1247,
  transactions: 8934,
  verified: 8891
})
const blockchainBlocks = ref([
  { id: 1, hash: '0x7a9f...', delay: 0 },
  { id: 2, hash: '0x2b4c...', delay: 0.2 },
  { id: 3, hash: '0x8d1e...', delay: 0.4 },
  { id: 4, hash: '0x5f6a...', delay: 0.6 }
])
const blockchainLinks = ref([
  { id: 1 }, { id: 2 }, { id: 3 }
])
const recentTransactions = ref([
  { id: 1, hash: '0x3f2a...', type: '捐赠', amount: 450, status: 'confirmed', statusText: '已确认' },
  { id: 2, hash: '0x8b7c...', type: '输血', amount: 320, status: 'pending', statusText: '待处理' },
  { id: 3, hash: '0x1d9e...', type: '检测', amount: 180, status: 'confirmed', statusText: '已确认' }
])
const smartContracts = ref([
  { id: 1, name: '血液质量验证', description: '自动验证血液质量标准', status: 'active', statusText: '活跃' },
  { id: 2, name: '紧急分配协议', description: '紧急情况下自动分配血液', status: 'standby', statusText: '待命' },
  { id: 3, name: '捐赠者奖励', description: '基于区块链的捐赠奖励系统', status: 'active', statusText: '活跃' }
])
const nftCertificates = ref([
  { id: 1, name: '英雄捐赠者', donor: '李明', value: 0.05, rarity: 'legendary', rarityText: '传奇', image: 'https://picsum.photos/seed/nft1/200/200.jpg' },
  { id: 2, name: '生命守护者', donor: '王芳', value: 0.03, rarity: 'epic', rarityText: '史诗', image: 'https://picsum.photos/seed/nft2/200/200.jpg' },
  { id: 3, name: '血液天使', donor: '张伟', value: 0.02, rarity: 'rare', rarityText: '稀有', image: 'https://picsum.photos/seed/nft3/200/200.jpg' }
])

// Metaverse State
const arMode = ref(false)
const vrStats = ref({
  activeUsers: 342,
  sessions: 1289,
  satisfaction: 96
})
const vrEquipment = ref([
  { id: 1, x: 20, y: 30, icon: 'Monitor' },
  { id: 2, x: 50, y: 20, icon: 'DataAnalysis' },
  { id: 3, x: 70, y: 40, icon: 'Heart' },
  { id: 4, x: 30, y: 60, icon: 'Wind' }
])
const bloodFlows = ref([
  { id: 1, delay: 0 },
  { id: 2, delay: 0.3 },
  { id: 3, delay: 0.6 },
  { id: 4, delay: 0.9 }
])

// AI and Emergency Features State
const aiMode = ref(false)
const emergencyMode = ref(false)
const emergencyStats = ref({
  activeEmergencies: 3,
  bloodNeeded: '450',
  donorsAlerted: '1,234'
})

// AI Details Dialog State
const aiDetailsVisible = ref(false)
const aiDetails = ref({
  title: '',
  description: '',
  icon: '',
  iconClass: '',
  metrics: [],
  features: [],
  benefits: [],
  stats: []
})

// Donor Engagement State
const gamificationEnabled = ref(false)
const vrExperienceActive = ref(false)

// Account Settings State
const settings = ref({
  donationReminders: true,
  emergencyAlerts: true,
  healthReports: false,
  publicProfile: false,
  dataSharing: true,
  locationSharing: false
})

const userProfile = ref({
  name: '张医生',
  title: '高级血液分析师',
  id: 'BDA-2024-0892',
  donations: 156,
  bloodType: 'A+',
  totalVolume: '4.8L',
  avatar: 'https://picsum.photos/seed/user-avatar/100/100.jpg'
})

// Hero Statistics with Enhanced Data
const heroStats = ref([
  {
    id: 'donations',
    label: '总捐赠数',
    value: '12,456',
    change: '+12.3%',
    trend: 'up',
    animated: true
  },
  {
    id: 'donors',
    label: '活跃捐赠者',
    value: '3,892',
    change: '+8.7%',
    trend: 'up',
    animated: true
  },
  {
    id: 'success',
    label: '成功率',
    value: '98.5%',
    change: '+0.3%',
    trend: 'up',
    animated: true
  }
])

// Enhanced KPI Data with Live Indicators
const enhancedKpis = ref([
  {
    id: 'total-donations',
    label: '总捐赠数',
    value: '12,456',
    change: '+12.3%',
    trend: 'up',
    icon: 'Document',
    status: '优秀',
    live: true,
    updating: false,
    progress: 85,
    progressColor: '#67c23a',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    sparklineGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 'active-donors',
    label: '活跃捐赠者',
    value: '3,892',
    change: '+8.7%',
    trend: 'up',
    icon: 'User',
    status: '良好',
    live: true,
    updating: false,
    progress: 72,
    progressColor: '#409eff',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    sparklineGradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    id: 'processing-rate',
    label: '处理率',
    value: '98.5%',
    change: '+0.3%',
    trend: 'up',
    icon: 'DataAnalysis',
    status: '最佳',
    live: true,
    updating: false,
    progress: 95,
    progressColor: '#e6a23c',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    sparklineGradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    id: 'inventory-level',
    label: '库存水平',
    value: '87%',
    change: '-2.1%',
    trend: 'down',
    icon: 'Box',
    status: '警告',
    live: true,
    updating: false,
    progress: 87,
    progressColor: '#f56c6c',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    sparklineGradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  }
])

// Particle System for Background
const particles = ref([
  { id: 1, x: 10, y: 20, delay: 0 },
  { id: 2, x: 80, y: 30, delay: 1 },
  { id: 3, x: 25, y: 70, delay: 2 },
  { id: 4, x: 60, y: 50, delay: 3 },
  { id: 5, x: 90, y: 80, delay: 4 },
  { id: 6, x: 40, y: 10, delay: 5 }
])

// AI Assistant Messages
const aiMessages = ref([
  {
    id: 1,
    type: 'ai',
    text: '你好！我是你的AI助手。我可以帮助你分析血液捐赠数据并提供洞察。',
    time: '刚刚'
  }
])

// Real-time Notifications
const realTimeNotifications = ref([
  {
    id: 1,
    type: 'success',
    title: '新捐赠记录',
    message: '收到来自捐赠者#1234的O+血型捐赠',
    icon: 'Document'
  },
  {
    id: 2,
    type: 'warning',
    title: '低库存警报',
    message: 'B-血型库存低于20%',
    icon: 'Warning'
  }
])

// Enhanced Blood Type Data
const bloodTypes = ref([
  { type: 'O+', percentage: 38, color: '#e74c3c', angle: 0 },
  { type: 'A+', percentage: 34, color: '#3498db', angle: 45 },
  { type: 'B+', percentage: 9, color: '#2ecc71', angle: 90 },
  { type: 'AB+', percentage: 3, color: '#9b59b6', angle: 135 },
  { type: 'O-', percentage: 7, color: '#c0392b', angle: 180 },
  { type: 'A-', percentage: 6, color: '#2980b9', angle: 225 },
  { type: 'B-', percentage: 2, color: '#27ae60', angle: 270 },
  { type: 'AB-', percentage: 1, color: '#8e44ad', angle: 315 }
])

// Enhanced Recent Activity
const recentActivities = ref([
  {
    id: 1,
    title: 'New Donation Campaign Started',
    description: 'Summer Blood Drive 2024 has been launched',
    time: '2 hours ago',
    icon: 'Star',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    isNew: true
  },
  {
    id: 2,
    title: 'Inventory Alert',
    description: 'B- blood type is running low',
    time: '4 hours ago',
    icon: 'Warning',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    isNew: true
  },
  {
    id: 3,
    title: 'System Update Completed',
    description: 'Quality control module updated successfully',
    time: '6 hours ago',
    icon: 'Refresh',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    isNew: false
  }
])

// Enhanced Quick Actions with Shortcuts
const quickActions = ref([
  {
    id: 1,
    title: 'Upload Data',
    description: 'Import new donation records',
    icon: 'Upload',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    shortcut: 'Ctrl+U'
  },
  {
    id: 2,
    title: 'View Analytics',
    description: 'Access detailed analytics',
    icon: 'TrendCharts',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    shortcut: 'Ctrl+A'
  },
  {
    id: 3,
    title: 'Manage Donors',
    description: 'Update donor information',
    icon: 'User',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    shortcut: 'Ctrl+D'
  },
  {
    id: 4,
    title: 'Schedule Campaign',
    description: 'Create new donation campaign',
    icon: 'Calendar',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    shortcut: 'Ctrl+C'
  }
])

// Auto-refresh interval
let refreshTimer = null

// Advanced Methods
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  window.document.body.classList.toggle('dark-mode')
  const mode = isDarkMode.value ? '深色模式' : '浅色模式'
  notificationStore.info(`${mode}已激活 - 优化${isDarkMode.value ? '夜间' : '日间'}使用体验`)
}

const toggleAIAssistant = () => {
  showAIAssistant.value = !showAIAssistant.value
  const status = showAIAssistant.value ? '开启' : '关闭'
  notificationStore.info(`AI助手已${status} - 智能血液数据分析助手`)
}

const toggleProfile = () => {
  showProfile.value = !showProfile.value
  const status = showProfile.value ? '打开' : '关闭'
  notificationStore.info(`个人中心已${status} - 管理血液分析师档案`)
}

// Quantum Analytics Functions
const activateQuantumMode = () => {
  quantumMode.value = !quantumMode.value
  const status = quantumMode.value ? '激活' : '关闭'
  notificationStore.success(`量子计算模式已${status} - 启用超高性能血液预测`)
}

const toggleNeuralNetwork = () => {
  neuralNetworkActive.value = !neuralNetworkActive.value
  const status = neuralNetworkActive.value ? '激活' : '关闭'
  notificationStore.success(`神经网络分析已${status} - 深度学习血液模式识别`)
}

const setStreamView = (view) => {
  notificationStore.info(`血液流动视图切换到${view === 'arterial' ? '动脉' : view === 'venous' ? '静脉' : '毛细血管'}模式`)
}

// Blockchain Functions
const verifyBlockchain = async () => {
  verifyingBlockchain.value = true
  notificationStore.info('正在验证区块链完整性...')
  
  setTimeout(() => {
    verifyingBlockchain.value = false
    notificationStore.success('区块链验证完成 - 所有血液追踪记录有效')
  }, 2000)
}

const mintNFT = () => {
  notificationStore.success('正在铸造NFT数字证书 - 血液捐赠者数字身份认证')
}

const executeContract = (contract) => {
  notificationStore.success(`执行智能合约: ${contract.name} - ${contract.description}`)
}

// Metaverse Functions
const enterMetaverse = () => {
  notificationStore.success('正在进入元宇宙血液中心 - 沉浸式3D血液管理体验')
}

const toggleARMode = () => {
  arMode.value = !arMode.value
  const status = arMode.value ? '激活' : '关闭'
  notificationStore.success(`AR模式已${status} - 增强现实血液分析技术`)
}

const startARScan = () => {
  notificationStore.info('启动AR血液扫描 - 实时血管识别和3D数据可视化')
}

const simulateOrgan = (organ) => {
  const organNames = {
    heart: '心脏',
    lungs: '肺部',
    liver: '肝脏'
  }
  notificationStore.info(`正在模拟${organNames[organ]}血液流动 - 数字孪生仿真分析`)
}

const runSimulation = (mode) => {
  const modeNames = {
    normal: '正常',
    emergency: '紧急',
    surgery: '手术'
  }
  notificationStore.success(`启动${modeNames[mode]}模式仿真 - 患者血液系统数字模型`)
}

// Professional Navigation Methods
const navigateToDashboard = () => {
  currentView.value = 'dashboard'
  notificationStore.info('已切换到仪表板视图 - 显示血液系统概览')
  router.push('/dashboard')
}

const navigateToAnalytics = () => {
  currentView.value = 'analytics'
  notificationStore.info('已切换到数据分析视图 - 深度分析血液数据趋势')
  router.push('/analytics/donations')
}

const navigateToRealtimeMonitoring = () => {
  currentView.value = 'realtime-monitoring'
  notificationStore.info('已切换到实时监控视图 - 监控血液库存和捐赠活动')
  router.push('/realtime-monitoring')
}

// Real-time Monitoring Methods
const toggleRealtimeUpdates = () => {
  realtimeUpdatesEnabled.value = !realtimeUpdatesEnabled.value
  if (realtimeUpdatesEnabled.value) {
    notificationStore.success('实时更新已启用')
    startRealtimeUpdates()
  } else {
    notificationStore.info('实时更新已禁用')
    stopRealtimeUpdates()
  }
}

const startRealtimeUpdates = () => {
  // Simulate real-time updates
  setInterval(() => {
    updateBloodInventory()
    updateDonationCenters()
    updateEmergencyAlerts()
  }, 5000)
}

const stopRealtimeUpdates = () => {
  // Clear real-time update intervals
}

const updateBloodInventory = () => {
  bloodInventoryData.value.forEach(bloodType => {
    // Simulate small random changes
    const change = Math.floor(Math.random() * 20) - 10
    bloodType.amount = Math.max(0, bloodType.amount + change)
    
    // Update trend
    if (change > 0) {
      bloodType.trend = 'up'
      bloodType.change = `+${(Math.random() * 5).toFixed(1)}%`
    } else if (change < 0) {
      bloodType.trend = 'down'
      bloodType.change = `-${(Math.random() * 3).toFixed(1)}%`
    } else {
      bloodType.trend = 'stable'
      bloodType.change = '0%'
    }
    
    // Update status based on amount
    if (bloodType.amount < 200) {
      bloodType.status = 'critical'
      bloodType.statusText = '紧急'
    } else if (bloodType.amount < 500) {
      bloodType.status = 'low'
      bloodType.statusText = '偏低'
    } else {
      bloodType.status = 'normal'
      bloodType.statusText = '正常'
    }
  })
}

const updateDonationCenters = () => {
  donationCentersData.value.forEach(center => {
    // Simulate small changes in metrics
    center.waitTime = Math.max(5, center.waitTime + Math.floor(Math.random() * 10) - 5)
    center.capacity = Math.min(100, Math.max(0, center.capacity + Math.floor(Math.random() * 20) - 10))
    center.todayDonations += Math.floor(Math.random() * 3)
  })
}

const updateEmergencyAlerts = () => {
  // Simulate new alerts occasionally
  if (Math.random() > 0.8) {
    const newAlert = {
      id: Date.now(),
      title: '实时警报',
      message: '系统检测到新的异常情况',
      severity: ['critical', 'warning', 'info'][Math.floor(Math.random() * 3)],
      time: '刚刚'
    }
    emergencyAlerts.value.unshift(newAlert)
    
    // Keep only last 10 alerts
    if (emergencyAlerts.value.length > 10) {
      emergencyAlerts.value = emergencyAlerts.value.slice(0, 10)
    }
  }
}

const exportMonitoringData = () => {
  notificationStore.success('正在导出监控数据...')
  // Simulate data export
  setTimeout(() => {
    notificationStore.success('监控数据导出完成')
  }, 2000)
}

const refreshAlerts = () => {
  notificationStore.info('正在刷新警报...')
  // Simulate refreshing alerts
  setTimeout(() => {
    notificationStore.success('警报已刷新')
  }, 1000)
}

const handleAlert = (alert) => {
  notificationStore.info(`正在处理警报: ${alert.title}`)
  // Remove alert after handling
  const index = emergencyAlerts.value.findIndex(a => a.id === alert.id)
  if (index > -1) {
    emergencyAlerts.value.splice(index, 1)
  }
}

const dismissAlert = (alertId) => {
  const index = emergencyAlerts.value.findIndex(a => a.id === alertId)
  if (index > -1) {
    emergencyAlerts.value.splice(index, 1)
    notificationStore.info('警报已忽略')
  }
}

const setMapView = (view) => {
  currentMapView.value = view
  notificationStore.info(`地图视图已切换到: ${view}`)
}

const navigateToDonors = () => {
  currentView.value = 'donors'
  notificationStore.info('已切换到捐赠者管理视图 - 管理捐赠者信息和资格')
  router.push('/donors')
}

const navigateToEmergency = () => {
  currentView.value = 'emergency'
  notificationStore.info('已切换到应急响应视图 - 管理紧急血液需求')
  router.push('/emergency-response')
}

const sendAIMessage = () => {
  if (!aiInput.value.trim()) return
  
  aiMessages.value.push({
    id: Date.now(),
    type: 'user',
    text: aiInput.value,
    time: 'Just now'
  })
  
  // Simulate AI response
  setTimeout(() => {
    aiMessages.value.push({
      id: Date.now() + 1,
      type: 'ai',
      text: 'I\'m analyzing your request. Based on current data trends, I recommend focusing on increasing O- blood type donations as they\'re currently at critical levels.',
      time: 'Just now'
    })
  }, 1000)
  
  aiInput.value = ''
}

const toggleMainAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  if (autoRefresh.value) {
    refreshTimer = setInterval(() => {
      updateKPIs()
    }, 5000)
    notificationStore.success('Auto-refresh enabled')
  } else {
    clearInterval(refreshTimer)
    notificationStore.info('Auto-refresh disabled')
  }
}

const toggleLiveFeed = () => {
  liveFeed.value = !liveFeed.value
  if (liveFeed.value) {
    simulateLiveUpdates()
    notificationStore.success('实时动态已启用')
  } else {
    notificationStore.info('实时动态已禁用')
  }
}

const toggleChartType = () => {
  chartType.value = chartType.value === '2d' ? '3d' : '2d'
  notificationStore.info(`切换到${chartType.value}图表模式`)
}

// AI and Emergency Features Methods
const toggleAIMode = () => {
  aiMode.value = !aiMode.value
  if (aiMode.value) {
    notificationStore.success('AI模式已激活 - 智能预测功能启用')
    // Enable AI predictions
    enableAIPredictions()
  } else {
    notificationStore.info('AI模式已关闭')
  }
}

const toggleEmergencyMode = () => {
  emergencyMode.value = !emergencyMode.value
  if (emergencyMode.value) {
    notificationStore.error('应急模式已激活 - 所有系统重新配置为紧急响应')
    // Update emergency stats
    emergencyStats.value.activeEmergencies = Math.floor(Math.random() * 5) + 1
    emergencyStats.value.bloodNeeded = Math.floor(Math.random() * 500) + 200
    emergencyStats.value.donorsAlerted = Math.floor(Math.random() * 2000) + 500
  } else {
    notificationStore.success('应急模式已关闭 - 系统恢复正常运行')
  }
}

const activateMassCasualty = () => {
  notificationStore.error('大规模伤亡模式已激活 - 自动资源重新分配')
  emergencyStats.value.activeEmergencies = 10
  emergencyStats.value.bloodNeeded = '2000'
  emergencyStats.value.donorsAlerted = '5000'
}

const mobilizeDonors = () => {
  notificationStore.success('正在动员理想捐赠者 - 基于位置和血型定向通知')
  emergencyStats.value.donorsAlerted = (parseInt(emergencyStats.value.donorsAlerted) + 500).toString()
}

// AI Details Methods
const showAIDetails = (aiType) => {
  const aiConfigs = {
    'blood-match': {
      title: '血液匹配AI',
      description: '先进的人工智能系统，通过深度学习算法分析供血者和受血者的基因标记、抗体模式和临床历史，实现超越传统ABO血型匹配的精准配对。',
      icon: 'DataAnalysis',
      iconClass: 'blood-match',
      metrics: [
        { label: '匹配准确率', value: '98.7%' },
        { label: '处理时间', value: '< 2秒' },
        { label: '成功率提升', value: '35%' }
      ],
      features: [
        'HLA分型匹配算法',
        '抗体交叉反应预测',
        '基因标记分析',
        '临床风险评估',
        '紧急快速匹配模式',
        '历史匹配记录追踪'
      ],
      benefits: [
        {
          title: '提高输血安全性',
          description: '通过精准匹配减少输血反应风险，提升患者安全'
        },
        {
          title: '优化库存利用',
          description: '智能分配血液资源，减少浪费，提高使用效率'
        },
        {
          title: '快速应急响应',
          description: '紧急情况下快速找到最佳匹配，拯救生命'
        }
      ],
      stats: [
        { label: '日均匹配次数', value: '1,245' },
        { label: '成功匹配', value: '1,229' },
        { label: '患者满意度', value: '96.8%' },
        { label: '医生信任度', value: '94.2%' }
      ]
    },
    'scarcity-alert': {
      title: '稀缺预警系统',
      description: '基于机器学习的预测系统，分析天气模式、节假日效应、社区活动和历史数据，提前2-3周预测血液短缺风险。',
      icon: 'Warning',
      iconClass: 'scarcity-alert',
      metrics: [
        { label: '预警准确率', value: '94.2%' },
        { label: '提前预警时间', value: '2-3周' },
        { label: '误报率', value: '< 5%' }
      ],
      features: [
        '多维度数据分析',
        '实时天气集成',
        '节假日模式识别',
        '社区活动监控',
        '历史趋势分析',
        '自动预警推送'
      ],
      benefits: [
        {
          title: '主动预防管理',
          description: '提前预警让血库有充足时间准备应对措施'
        },
        {
          title: '减少紧急情况',
          description: '预测性管理避免血液短缺紧急状况'
        },
        {
          title: '优化捐赠活动',
          description: '基于预测数据精准安排血液捐赠活动'
        }
      ],
      stats: [
        { label: '预测准确事件', value: '156' },
        { label: '成功预警', value: '147' },
        { label: '避免短缺', value: '89%' },
        { label: '成本节约', value: '¥2.3M' }
      ]
    },
    'inventory-opt': {
      title: '智能库存优化',
      description: '利用机器学习算法分析历史需求模式、季节性变化和临床需求，自动推荐最佳血液成分生产比例和库存分配策略。',
      icon: 'Box',
      iconClass: 'inventory-opt',
      metrics: [
        { label: '效率提升', value: '23%' },
        { label: '浪费减少', value: '18%' },
        { label: '成本节约', value: '¥1.8M/年' }
      ],
      features: [
        '需求预测算法',
        '自动补货提醒',
        '过期预警系统',
        '库存分配优化',
        '成分制备建议',
        '跨库调配协调'
      ],
      benefits: [
        {
          title: '减少血液浪费',
          description: '智能预测减少过期血液，提高资源利用率'
        },
        {
          title: '优化库存结构',
          description: '根据临床需求动态调整血液成分比例'
        },
        {
          title: '降低运营成本',
          description: '自动化管理减少人工成本和库存持有成本'
        }
      ],
      stats: [
        { label: '日均处理量', value: '8,450单位' },
        { label: '库存周转率', value: '12.3天' },
        { label: '浪费率降低', value: '18%' },
        { label: '运营效率', value: '89.7%' }
      ]
    }
  }
  
  aiDetails.value = aiConfigs[aiType] || aiConfigs['blood-match']
  aiDetailsVisible.value = true
  notificationStore.info(`正在查看 ${aiDetails.value.title} 详情`)
}

const closeAIDetails = () => {
  aiDetailsVisible.value = false
}

const configureAI = () => {
  notificationStore.info(`正在配置 ${aiDetails.value.title} 设置`)
  // Navigate to AI configuration page
  router.push('/ai-configuration')
}

const viewAIReports = () => {
  notificationStore.info(`正在生成 ${aiDetails.value.title} 报告`)
  // Navigate to AI reports page
  router.push('/ai-reports')
}

// Donor Engagement Methods
const showGamification = () => {
  gamificationEnabled.value = !gamificationEnabled.value
  notificationStore.success(gamificationEnabled.value ? '游戏化系统已启用' : '游戏化系统已关闭')
}

const startVRExperience = () => {
  vrExperienceActive.value = true
  notificationStore.success('VR教育体验已启动 - 正在加载3D可视化')
}

const generateImpactStory = () => {
  const stories = [
    '您的血液拯救了3条生命，包括一名癌症患者、一名车祸伤者和一名早产儿',
    '您的定期捐赠帮助社区医院血库保持安全水平',
    '您的O型阴性血液成为紧急情况下的救命血'
  ]
  const randomStory = stories[Math.floor(Math.random() * stories.length)]
  notificationStore.success(`影响力故事生成: ${randomStory}`)
}

const enableAIPredictions = () => {
  // Simulate AI predictions
  setTimeout(() => {
    notificationStore.info('AI预测: 未来2周内A型血液需求可能增加15%')
  }, 2000)
  setTimeout(() => {
    notificationStore.warning('AI预警: 下周假期可能导致血液短缺')
  }, 4000)
}

const toggleFab = () => {
  fabOpen.value = !fabOpen.value
}

// Dashboard Builder State
const dashboardItems = ref([])
const componentPalette = ref([
  {
    id: 'chart',
    name: '数据图表',
    type: 'chart',
    icon: 'DataAnalysis',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    description: '可视化数据图表组件'
  },
  {
    id: 'stats',
    name: '统计卡片',
    type: 'stats',
    icon: 'TrendCharts',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    description: '关键指标统计展示'
  },
  {
    id: 'table',
    name: '数据表格',
    type: 'table',
    icon: 'Document',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    description: '结构化数据表格'
  },
  {
    id: 'alert',
    name: '警报组件',
    type: 'alert',
    icon: 'Warning',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    description: '系统警报和通知'
  },
  {
    id: 'progress',
    name: '进度条',
    type: 'progress',
    icon: 'Timer',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    description: '任务进度展示'
  },
  {
    id: 'map',
    name: '地图组件',
    type: 'map',
    icon: 'Location',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    description: '地理位置可视化'
  }
])

const currentLayout = ref('grid')
const isDragOver = ref(false)
const draggedComponent = ref(null)
const draggedIndex = ref(null)
const activeSettingsTab = ref('basic')

const mockTableData = ref([
  { name: '项目A', value: 1234, status: '正常' },
  { name: '项目B', value: 5678, status: '警告' },
  { name: '项目C', value: 9012, status: '正常' }
])

// Dashboard Builder Methods
const navigateToDashboardBuilder = () => {
  currentView.value = 'dashboard-builder'
  notificationStore.info('已切换到仪表板构建器 - 自定义血液数据仪表板')
  router.push('/dashboard-builder')
}

const navigateToSystemStatus = () => {
  currentView.value = 'system-status'
  notificationStore.info('已切换到系统状态监控 - 监控血液系统健康状态')
  router.push('/system-status')
}

const navigateToTaskManagement = () => {
  currentView.value = 'task-management'
  notificationStore.info('已切换到任务管理 - 管理血液相关任务和流程')
  router.push('/task-management')
}

// Task Management State
const taskStats = ref({
  total: 156,
  totalChange: 12.5,
  inProgress: 45,
  inProgressChange: 8.3,
  completed: 89,
  completedChange: 15.7,
  pending: 22,
  pendingChange: -5.2,
  avgCompletionTime: 24.5,
  avgCompletionTimeChange: -3.1
})

const taskFilter = ref({
  status: 'all',
  priority: 'all',
  assignee: 'all',
  dueDate: null
})

const tasks = ref([
  {
    id: 1,
    title: '血液库存数据分析报告',
    description: '分析本月血液库存数据，生成详细的分析报告',
    priority: 'high',
    status: 'in-progress',
    assignee: { name: '张医生', avatar: 'https://picsum.photos/seed/zhang/100/100.jpg' },
    dueDate: '2024-01-15',
    progress: 65,
    tags: [{ label: '数据分析', type: 'primary' }, { label: '报告', type: 'success' }],
    requirements: ['完成数据收集', '进行统计分析', '生成可视化图表', '撰写分析报告'],
    attachments: [
      { id: 1, name: '血液库存数据.xlsx' },
      { id: 2, name: '分析模板.docx' }
    ],
    progressHistory: [
      { id: 1, timestamp: '2024-01-10', user: { name: '张医生' }, action: '开始任务', value: 0 },
      { id: 2, timestamp: '2024-01-12', user: { name: '张医生' }, action: '数据收集完成', value: 30 },
      { id: 3, timestamp: '2024-01-13', user: { name: '张医生' }, action: '分析进行中', value: 65 }
    ],
    comments: [
      { id: 1, timestamp: '2024-01-10', user: { name: '李护士', avatar: 'https://picsum.photos/seed/li/100/100.jpg' }, content: '请确保包含最近一周的数据' },
      { id: 2, timestamp: '2024-01-12', user: { name: '王技术员', avatar: 'https://picsum.photos/seed/wang/100/100.jpg' }, content: '数据已经准备好，可以开始分析' }
    ]
  },
  {
    id: 2,
    title: '紧急血液调配协调',
    description: '协调医院间的紧急血液调配，确保及时供应',
    priority: 'high',
    status: 'pending',
    assignee: { name: '李护士', avatar: 'https://picsum.photos/seed/li/100/100.jpg' },
    dueDate: '2024-01-14',
    progress: 0,
    tags: [{ label: '紧急', type: 'danger' }, { label: '协调', type: 'warning' }],
    requirements: ['联系供血医院', '确认血液类型', '安排运输', '更新库存记录'],
    attachments: [],
    progressHistory: [],
    comments: []
  },
  {
    id: 3,
    title: '捐赠者信息管理系统升级',
    description: '升级捐赠者信息管理系统，提高数据处理效率',
    priority: 'medium',
    status: 'completed',
    assignee: { name: '王技术员', avatar: 'https://picsum.photos/seed/wang/100/100.jpg' },
    dueDate: '2024-01-12',
    progress: 100,
    tags: [{ label: '系统升级', type: 'info' }, { label: 'IT', type: 'primary' }],
    requirements: ['系统备份', '代码更新', '测试验证', '数据迁移'],
    attachments: [
      { id: 3, name: '升级方案.pdf' },
      { id: 4, name: '测试报告.docx' }
    ],
    progressHistory: [
      { id: 4, timestamp: '2024-01-08', user: { name: '王技术员' }, action: '开始升级', value: 0 },
      { id: 5, timestamp: '2024-01-10', user: { name: '王技术员' }, action: '系统备份完成', value: 25 },
      { id: 6, timestamp: '2024-01-11', user: { name: '王技术员' }, action: '代码更新完成', value: 75 },
      { id: 7, timestamp: '2024-01-12', user: { name: '王技术员' }, action: '升级完成', value: 100 }
    ],
    comments: [
      { id: 3, timestamp: '2024-01-09', user: { name: '陈管理员', avatar: 'https://picsum.photos/seed/chen/100/100.jpg' }, content: '升级过程中请确保数据安全' },
      { id: 4, timestamp: '2024-01-12', user: { name: '王技术员' }, content: '升级已完成，系统运行正常' }
    ]
  },
  {
    id: 4,
    title: '月度血液质量检测',
    description: '进行月度血液质量检测，确保血液安全',
    priority: 'medium',
    status: 'in-progress',
    assignee: { name: '陈管理员', avatar: 'https://picsum.photos/seed/chen/100/100.jpg' },
    dueDate: '2024-01-20',
    progress: 35,
    tags: [{ label: '质量检测', type: 'success' }, { label: '月度', type: 'info' }],
    requirements: ['样本采集', '实验室检测', '数据分析', '报告生成'],
    attachments: [
      { id: 5, name: '检测标准.pdf' }
    ],
    progressHistory: [
      { id: 8, timestamp: '2024-01-13', user: { name: '陈管理员' }, action: '开始检测', value: 0 },
      { id: 9, timestamp: '2024-01-14', user: { name: '陈管理员' }, action: '样本采集完成', value: 35 }
    ],
    comments: []
  },
  {
    id: 5,
    title: '新员工培训计划制定',
    description: '制定新员工培训计划，包括血液管理知识和操作技能',
    priority: 'low',
    status: 'pending',
    assignee: { name: '张医生', avatar: 'https://picsum.photos/seed/zhang/100/100.jpg' },
    dueDate: '2024-01-25',
    progress: 0,
    tags: [{ label: '培训', type: 'warning' }, { label: 'HR', type: 'info' }],
    requirements: ['需求调研', '课程设计', '材料准备', '培训安排'],
    attachments: [],
    progressHistory: [],
    comments: []
  }
])

const selectedTask = ref(null)
const taskDetailsVisible = ref(false)
const taskCommentsVisible = ref(false)
const newComment = ref('')
const selectedTasks = ref([])

// Computed property for filtered tasks
const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    let matches = true
    
    if (taskFilter.value.status !== 'all') {
      matches = matches && task.status === taskFilter.value.status
    }
    
    if (taskFilter.value.priority !== 'all') {
      matches = matches && task.priority === taskFilter.value.priority
    }
    
    if (taskFilter.value.assignee !== 'all') {
      matches = matches && task.assignee.name === taskFilter.value.assignee
    }
    
    if (taskFilter.value.dueDate && taskFilter.value.dueDate.length === 2) {
      const taskDate = new Date(task.dueDate)
      const startDate = new Date(taskFilter.value.dueDate[0])
      const endDate = new Date(taskFilter.value.dueDate[1])
      matches = matches && taskDate >= startDate && taskDate <= endDate
    }
    
    return matches
  })
})

// Task Management Methods
const createNewTask = () => {
  notificationStore.info('正在打开新建任务对话框')
}

const filterTasks = () => {
  notificationStore.info('任务筛选已应用')
}

const exportTaskReport = () => {
  const reportData = {
    timestamp: new Date().toISOString(),
    statistics: taskStats.value,
    tasks: tasks.value,
    filters: taskFilter.value
  }
  
  const dataStr = JSON.stringify(reportData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = window.document.createElement('a')
  link.href = url
  link.download = `task-report-${Date.now()}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  notificationStore.success('任务报告已导出')
}

const handleTaskSelection = (selection) => {
  selectedTasks.value = selection
}

const editTask = (task) => {
  notificationStore.info(`正在编辑任务: ${task.title}`)
}

const viewTaskDetails = (task) => {
  selectedTask.value = task
  taskDetailsVisible.value = true
}

const deleteTask = (task) => {
  notificationStore.warning(`正在删除任务: ${task.title}`)
}

const getPriorityType = (priority) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

const getPriorityLabel = (priority) => {
  const labels = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return labels[priority] || '中'
}

const getStatusType = (status) => {
  const types = {
    'pending': 'info',
    'in-progress': 'warning',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status) => {
  const labels = {
    'pending': '待处理',
    'in-progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return labels[status] || '未知'
}

const getDueDateClass = (dueDate) => {
  const today = new Date()
  const due = new Date(dueDate)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 3) return 'due-soon'
  return 'normal'
}

const getProgressStatus = (progress) => {
  if (progress === 100) return 'success'
  if (progress >= 70) return ''
  return 'exception'
}

const downloadAttachment = (attachment) => {
  notificationStore.info(`正在下载: ${attachment.name}`)
}

const viewTaskComments = (task) => {
  selectedTask.value = task
  taskCommentsVisible.value = true
}

const addComment = () => {
  if (newComment.value.trim()) {
    if (selectedTask.value) {
      selectedTask.value.comments.push({
        id: Date.now(),
        timestamp: new Date().toISOString(),
        user: { name: '当前用户', avatar: 'https://picsum.photos/seed/current/100/100.jpg' },
        content: newComment.value
      })
      newComment.value = ''
      notificationStore.success('评论已添加')
    }
  }
}

const shareTask = (task) => {
  notificationStore.info(`正在分享任务: ${task.title}`)
}

// System Status State
const systemHealth = ref({
  status: 'healthy',
  uptime: 99.9,
  responseTime: 120
})

const serverStatus = ref({
  status: 'optimal',
  cpuUsage: 45,
  memoryUsage: 62
})

const databaseStatus = ref({
  status: 'connected',
  connections: 127,
  queryTime: 85
})

const networkStatus = ref({
  status: 'stable',
  bandwidth: 850,
  latency: 25
})

const services = ref([
  {
    id: 'api-gateway',
    name: 'API网关',
    status: 'healthy',
    icon: 'Link',
    cpu: 35,
    memory: 48,
    requests: 1250,
    alerts: []
  },
  {
    id: 'auth-service',
    name: '认证服务',
    status: 'healthy',
    icon: 'User',
    cpu: 22,
    memory: 31,
    requests: 890,
    alerts: []
  },
  {
    id: 'data-service',
    name: '数据服务',
    status: 'warning',
    icon: 'DataAnalysis',
    cpu: 78,
    memory: 85,
    requests: 2100,
    alerts: [
      { id: 1, type: 'warning', message: 'CPU使用率超过阈值' },
      { id: 2, type: 'info', message: '请求量增加20%' }
    ]
  },
  {
    id: 'notification-service',
    name: '通知服务',
    status: 'healthy',
    icon: 'Notification',
    cpu: 15,
    memory: 28,
    requests: 450,
    alerts: []
  },
  {
    id: 'backup-service',
    name: '备份服务',
    status: 'healthy',
    icon: 'Document',
    cpu: 8,
    memory: 12,
    requests: 120,
    alerts: []
  },
  {
    id: 'monitoring-service',
    name: '监控服务',
    status: 'healthy',
    icon: 'Monitor',
    cpu: 25,
    memory: 35,
    requests: 680,
    alerts: []
  }
])

const responseTimeDistribution = ref([
  { range: '< 100ms', percentage: 45 },
  { range: '100-500ms', percentage: 35 },
  { range: '500ms-1s', percentage: 15 },
  { range: '> 1s', percentage: 5 }
])

const errorTrend = ref([
  { value: 2.1 },
  { value: 1.8 },
  { value: 2.3 },
  { value: 1.9 },
  { value: 2.5 }
])

const throughput = ref({
  current: '12,450 req/s',
  average: '11,200 req/s',
  peak: '18,900 req/s'
})

// Real-time Monitoring State
const realtimeUpdatesEnabled = ref(false)
const selectedRegion = ref('all')
const currentMapView = ref('inventory')

const bloodInventoryData = ref([
  {
    type: 'A+',
    amount: 1250,
    status: 'normal',
    statusText: '正常',
    trend: 'up',
    change: '+5.2%'
  },
  {
    type: 'A-',
    amount: 680,
    status: 'low',
    statusText: '偏低',
    trend: 'down',
    change: '-2.1%'
  },
  {
    type: 'B+',
    amount: 920,
    status: 'normal',
    statusText: '正常',
    trend: 'stable',
    change: '0%'
  },
  {
    type: 'B-',
    amount: 340,
    status: 'critical',
    statusText: '紧急',
    trend: 'down',
    change: '-8.5%'
  },
  {
    type: 'O+',
    amount: 2100,
    status: 'normal',
    statusText: '正常',
    trend: 'up',
    change: '+3.7%'
  },
  {
    type: 'O-',
    amount: 180,
    status: 'low',
    statusText: '偏低',
    trend: 'down',
    change: '-1.2%'
  },
  {
    type: 'AB+',
    amount: 450,
    status: 'normal',
    statusText: '正常',
    trend: 'stable',
    change: '0%'
  },
  {
    type: 'AB-',
    amount: 120,
    status: 'critical',
    statusText: '紧急',
    trend: 'down',
    change: '-4.3%'
  }
])

const donationCentersData = ref([
  {
    id: 1,
    name: '北京血液中心',
    address: '朝阳区建国路88号',
    status: 'open',
    statusText: '开放',
    waitTime: 15,
    capacity: 75,
    todayDonations: 42
  },
  {
    id: 2,
    name: '上海血液中心',
    address: '浦东新区世纪大道200号',
    status: 'busy',
    statusText: '繁忙',
    waitTime: 35,
    capacity: 90,
    todayDonations: 68
  },
  {
    id: 3,
    name: '广州血液中心',
    address: '天河区珠江新城',
    status: 'open',
    statusText: '开放',
    waitTime: 20,
    capacity: 60,
    todayDonations: 35
  },
  {
    id: 4,
    name: '深圳血液中心',
    address: '福田区深南大道',
    status: 'closed',
    statusText: '关闭',
    waitTime: 0,
    capacity: 0,
    todayDonations: 28
  }
])

const emergencyAlerts = ref([
  {
    id: 1,
    title: 'B型血紧急短缺',
    message: '深圳市人民医院急需B型血，库存仅够维持2小时',
    severity: 'critical',
    time: '5分钟前'
  },
  {
    id: 2,
    title: '设备维护通知',
    message: '广州血液中心检测设备将于今晚22:00-23:00维护',
    severity: 'warning',
    time: '15分钟前'
  },
  {
    id: 3,
    title: '捐赠者激增',
    message: '北京血液中心当前捐赠者数量超出预期30%',
    severity: 'info',
    time: '30分钟前'
  }
])

// System Status Methods
const refreshSystemStatus = () => {
  // Simulate refreshing system status
  notificationStore.info('正在刷新系统状态...')
  
  setTimeout(() => {
    // Update random values
    systemHealth.value.uptime = 99.5 + Math.random() * 0.4
    systemHealth.value.responseTime = 100 + Math.floor(Math.random() * 50)
    
    serverStatus.value.cpuUsage = 40 + Math.floor(Math.random() * 30)
    serverStatus.value.memoryUsage = 55 + Math.floor(Math.random() * 25)
    
    databaseStatus.value.connections = 120 + Math.floor(Math.random() * 20)
    databaseStatus.value.queryTime = 80 + Math.floor(Math.random() * 30)
    
    networkStatus.value.bandwidth = 800 + Math.floor(Math.random() * 200)
    networkStatus.value.latency = 20 + Math.floor(Math.random() * 15)
    
    // Update service metrics
    services.value.forEach(service => {
      service.cpu = 20 + Math.floor(Math.random() * 60)
      service.memory = 20 + Math.floor(Math.random() * 60)
      service.requests = 800 + Math.floor(Math.random() * 1500)
      
      // Randomly add alerts
      if (Math.random() > 0.8 && service.cpu > 70) {
        if (!service.alerts) service.alerts = []
        service.alerts.push({
          id: Date.now(),
          type: 'warning',
          message: `CPU使用率: ${service.cpu}%`
        })
      }
    })
    
    notificationStore.success('系统状态已刷新')
  }, 1000)
}

const exportStatusReport = () => {
  const reportData = {
    timestamp: new Date().toISOString(),
    systemHealth: systemHealth.value,
    serverStatus: serverStatus.value,
    databaseStatus: databaseStatus.value,
    networkStatus: networkStatus.value,
    services: services.value,
    performance: {
      responseTimeDistribution: responseTimeDistribution.value,
      errorTrend: errorTrend.value,
      throughput: throughput.value
    }
  }
  
  const dataStr = JSON.stringify(reportData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = window.document.createElement('a')
  link.href = url
  link.download = `system-status-${Date.now()}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  notificationStore.success('系统状态报告已导出')
}

const restartService = (serviceId) => {
  const service = services.value.find(s => s.id === serviceId)
  if (service) {
    notificationStore.warning(`正在重启服务: ${service.name}`)
    
    setTimeout(() => {
      service.status = 'healthy'
      service.cpu = 20 + Math.floor(Math.random() * 30)
      service.memory = 20 + Math.floor(Math.random() * 30)
      service.alerts = []
      notificationStore.success(`服务 ${service.name} 重启成功`)
    }, 2000)
  }
}

const viewServiceLogs = (serviceId) => {
  const service = services.value.find(s => s.id === serviceId)
  if (service) {
    notificationStore.info(`正在查看 ${service.name} 日志`)
  }
}

const viewDetailedMetrics = () => {
  notificationStore.info('正在打开详细指标面板')
}

const viewErrorDetails = () => {
  notificationStore.info('正在打开错误详情面板')
}

const viewThroughputDetails = () => {
  notificationStore.info('正在打开吞吐量详情面板')
}

const getMiniComponentStyle = (item, index) => {
  const scale = 0.3
  return {
    position: 'absolute',
    left: (item.position.x * scale) + 'px',
    top: (item.position.y * scale) + 'px',
    width: (item.size.width * scale) + 'px',
    height: (item.size.height * scale) + 'px',
    background: 'rgba(102, 126, 234, 0.2)',
    border: '1px solid rgba(102, 126, 234, 0.4)',
    borderRadius: '4px'
  }
}

const handleDragStart = (event, component) => {
  draggedComponent.value = component
  event.dataTransfer.effectAllowed = 'copy'
}

const handleDragOver = (event) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'copy'
  isDragOver.value = true
}

const handleDragLeave = (event) => {
  isDragOver.value = false
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  
  if (draggedComponent.value) {
    const newItem = {
      id: Date.now(),
      type: draggedComponent.value.type,
      title: draggedComponent.value.name,
      description: draggedComponent.value.description,
      icon: draggedComponent.value.icon,
      gradient: draggedComponent.value.gradient,
      position: { x: 0, y: 0 },
      size: { width: 300, height: 200 }
    }
    dashboardItems.value.push(newItem)
    notificationStore.success(`已添加 ${draggedComponent.value.name} 组件`)
    draggedComponent.value = null
  }
}

const handleComponentDragStart = (event, index) => {
  draggedIndex.value = index
  event.dataTransfer.effectAllowed = 'move'
}

const handleComponentDragOver = (event) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
}

const handleComponentDrop = (event, targetIndex) => {
  event.preventDefault()
  
  if (draggedIndex.value !== null && draggedIndex.value !== targetIndex) {
    const draggedItem = dashboardItems.value[draggedIndex.value]
    dashboardItems.value.splice(draggedIndex.value, 1)
    dashboardItems.value.splice(targetIndex, 0, draggedItem)
    notificationStore.info('组件位置已更新')
  }
  draggedIndex.value = null
}

const getItemStyle = (item, index) => {
  if (currentLayout.value === 'free') {
    return {
      position: 'absolute',
      left: item.position.x + 'px',
      top: item.position.y + 'px',
      width: item.size.width + 'px',
      height: item.size.height + 'px'
    }
  }
  return {}
}

const setLayout = (layout) => {
  currentLayout.value = layout
  notificationStore.info(`布局已切换为${layout === 'grid' ? '网格' : layout === 'free' ? '自由' : '瀑布'}布局`)
}

const editComponent = (index) => {
  notificationStore.info(`编辑组件: ${dashboardItems.value[index].title}`)
}

const removeComponent = (index) => {
  const component = dashboardItems.value[index]
  dashboardItems.value.splice(index, 1)
  notificationStore.warning(`已移除 ${component.title} 组件`)
}

const saveDashboard = () => {
  const dashboardData = {
    items: dashboardItems.value,
    layout: currentLayout.value,
    timestamp: new Date().toISOString(),
    name: currentDashboardName.value || '自定义仪表板',
    theme: currentTheme.value,
    autoRefresh: autoRefreshEnabled.value,
    refreshInterval: refreshInterval.value
  }
  localStorage.setItem('customDashboard', JSON.stringify(dashboardData))
  notificationStore.success('仪表板已保存')
}

const loadDashboard = () => {
  const savedDashboard = localStorage.getItem('customDashboard')
  if (savedDashboard) {
    const dashboardData = JSON.parse(savedDashboard)
    dashboardItems.value = dashboardData.items || []
    currentLayout.value = dashboardData.layout || 'grid'
    currentDashboardName.value = dashboardData.name || '自定义仪表板'
    currentTheme.value = dashboardData.theme || 'default'
    autoRefreshEnabled.value = dashboardData.autoRefresh || false
    refreshInterval.value = dashboardData.refreshInterval || 30
    notificationStore.success('仪表板已加载')
  } else {
    notificationStore.info('没有找到保存的仪表板')
  }
}

const exportDashboard = () => {
  const dashboardData = {
    items: dashboardItems.value,
    layout: currentLayout.value,
    timestamp: new Date().toISOString(),
    name: currentDashboardName.value || '自定义仪表板',
    theme: currentTheme.value,
    autoRefresh: autoRefreshEnabled.value,
    refreshInterval: refreshInterval.value
  }
  
  const dataStr = JSON.stringify(dashboardData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = window.document.createElement('a')
  link.href = url
  link.download = `dashboard-${Date.now()}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  notificationStore.success('仪表板配置已导出')
}

const importDashboard = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const dashboardData = JSON.parse(e.target.result)
        dashboardItems.value = dashboardData.items || []
        currentLayout.value = dashboardData.layout || 'grid'
        currentDashboardName.value = dashboardData.name || '导入的仪表板'
        currentTheme.value = dashboardData.theme || 'default'
        autoRefreshEnabled.value = dashboardData.autoRefresh || false
        refreshInterval.value = dashboardData.refreshInterval || 30
        notificationStore.success('仪表板配置已导入')
      } catch (error) {
        notificationStore.error('导入失败：文件格式错误')
      }
    }
    reader.readAsText(file)
  }
}

// Dashboard Customization State
const currentDashboardName = ref('自定义仪表板')
const currentTheme = ref('default')
const autoRefreshEnabled = ref(false)
const refreshInterval = ref(30)
const availableThemes = ref([
  { id: 'default', name: '默认主题', colors: ['#667eea', '#764ba2'] },
  { id: 'ocean', name: '海洋主题', colors: ['#30cfd0', '#330867'] },
  { id: 'sunset', name: '日落主题', colors: ['#fa709a', '#fee140'] },
  { id: 'forest', name: '森林主题', colors: ['#43e97b', '#38f9d7'] },
  { id: 'fire', name: '火焰主题', colors: ['#f093fb', '#f5576c'] }
])

const dashboardTemplates = ref([
  {
    id: 'analytics',
    name: '分析仪表板',
    description: '数据分析和可视化',
    items: [
      { type: 'chart', title: '趋势分析', position: { x: 0, y: 0 }, size: { width: 400, height: 300 } },
      { type: 'stats', title: '关键指标', position: { x: 420, y: 0 }, size: { width: 350, height: 300 } },
      { type: 'table', title: '数据表格', position: { x: 0, y: 320 }, size: { width: 770, height: 250 } }
    ]
  },
  {
    id: 'monitoring',
    name: '监控仪表板',
    description: '系统监控和状态',
    items: [
      { type: 'alert', title: '系统警报', position: { x: 0, y: 0 }, size: { width: 350, height: 200 } },
      { type: 'progress', title: '任务进度', position: { x: 370, y: 0 }, size: { width: 400, height: 200 } },
      { type: 'stats', title: '性能指标', position: { x: 0, y: 220 }, size: { width: 770, height: 180 } }
    ]
  },
  {
    id: 'operations',
    name: '运营仪表板',
    description: '运营数据和管理',
    items: [
      { type: 'chart', title: '运营趋势', position: { x: 0, y: 0 }, size: { width: 380, height: 280 } },
      { type: 'stats', title: '运营指标', position: { x: 400, y: 0 }, size: { width: 370, height: 280 } },
      { type: 'table', title: '运营数据', position: { x: 0, y: 300 }, size: { width: 770, height: 220 } }
    ]
  }
])

// Dashboard Customization Methods
const applyTemplate = (template) => {
  dashboardItems.value = template.items.map(item => ({
    ...item,
    id: Date.now() + Math.random(),
    title: item.title,
    type: item.type,
    position: item.position,
    size: item.size
  }))
  currentLayout.value = 'free'
  notificationStore.success(`已应用模板: ${template.name}`)
}

const changeTheme = (theme) => {
  currentTheme.value = theme.id
  notificationStore.info(`主题已切换为: ${theme.name}`)
}

const toggleAutoRefresh = () => {
  autoRefreshEnabled.value = !autoRefreshEnabled.value
  if (autoRefreshEnabled.value) {
    startAutoRefresh()
    notificationStore.success('自动刷新已启用')
  } else {
    stopAutoRefresh()
    notificationStore.info('自动刷新已禁用')
  }
}

const startAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  refreshTimer = setInterval(() => {
    // Refresh dashboard data
    notificationStore.info('仪表板数据已刷新')
  }, refreshInterval.value * 1000)
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

const updateRefreshInterval = (interval) => {
  refreshInterval.value = interval
  if (autoRefreshEnabled.value) {
    startAutoRefresh()
    notificationStore.info(`刷新间隔已更新为 ${interval} 秒`)
  }
}

const resetDashboard = () => {
  dashboardItems.value = []
  currentLayout.value = 'grid'
  currentDashboardName.value = '自定义仪表板'
  currentTheme.value = 'default'
  autoRefreshEnabled.value = false
  refreshInterval.value = 30
  stopAutoRefresh()
  notificationStore.info('仪表板已重置')
}

// Account Settings Methods
const editProfile = () => {
  notificationStore.info('正在打开个人资料编辑器')
}

const viewFullProfile = () => {
  notificationStore.success('正在加载完整个人资料')
}

const shareProfile = () => {
  notificationStore.success('个人资料分享链接已复制到剪贴板')
}

const resetSettings = () => {
  settings.value = {
    donationReminders: true,
    emergencyAlerts: true,
    healthReports: false,
    publicProfile: false,
    dataSharing: true,
    locationSharing: false
  }
  notificationStore.success('设置已重置为默认值')
}

const exportHealthData = () => {
  notificationStore.success('正在导出健康数据，将发送到您的邮箱')
}

const securityAudit = () => {
  notificationStore.info('正在进行安全审计，请稍候...')
  setTimeout(() => {
    notificationStore.success('安全审计完成 - 未发现异常')
  }, 2000)
}

const changePassword = () => {
  notificationStore.warning('正在跳转到密码修改页面')
}

const logoutAll = () => {
  notificationStore.error('正在退出所有已登录设备...')
  setTimeout(() => {
    notificationStore.success('已成功退出所有设备')
  }, 1500)
}

const manageDevices = () => {
  notificationStore.info('正在加载设备管理界面')
}

const removeNotification = (id) => {
  const index = realTimeNotifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    realTimeNotifications.value.splice(index, 1)
  }
}

const updateKPIs = () => {
  enhancedKpis.value.forEach(kpi => {
    kpi.updating = true
    setTimeout(() => {
      // Simulate data update
      kpi.updating = false
    }, 1000)
  })
}

const simulateLiveUpdates = () => {
  // Simulate real-time activity updates
  const activities = [
    { title: '新捐赠', description: '收到A+血型捐赠', icon: 'Document' },
    { title: '捐赠者注册', description: '新捐赠者#5678已注册', icon: 'User' },
    { title: '活动更新', description: '夏季活动进度: 75%', icon: 'Star' }
  ]
  
  setInterval(() => {
    if (liveFeed.value && Math.random() > 0.7) {
      const activity = activities[Math.floor(Math.random() * activities.length)]
      recentActivities.value.unshift({
        id: Date.now(),
        ...activity,
        time: '刚刚',
        color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        isNew: true
      })
      
      // Keep only last 10 activities
      if (recentActivities.value.length > 10) {
        recentActivities.value = recentActivities.value.slice(0, 10)
      }
    }
  }, 8000)
}

const customizeActions = () => {
  notificationStore.info('操作自定义即将推出！')
}

// Existing Methods
const timeRange = ref('month')
const chartPeriod = ref('30d')

const setTimeRange = (range) => {
  timeRange.value = range
  notificationStore.info(`时间范围已更改为${range}`)
}

const navigateToUpload = () => {
  router.push('/upload')
}

// Other Methods

const viewDetails = (kpi) => {
  notificationStore.info(`查看${kpi.label}的详情`)
}

const exportKpi = (kpi) => {
  notificationStore.success(`正在导出${kpi.label}数据`)
}

const setAlert = (kpi) => {
  notificationStore.info(`为${kpi.label}设置警报`)
}

const viewHistory = (kpi) => {
  notificationStore.info(`查看${kpi.label}的历史`)
}

const refreshChart = () => {
  notificationStore.success('图表已刷新')
}

const refreshBloodChart = () => {
  notificationStore.success('血型图表已刷新')
}

const viewAllActivity = () => {
  notificationStore.info('查看所有活动')
}

const viewActivity = (activity) => {
  notificationStore.info(`查看: ${activity.title}`)
}

const executeAction = (action) => {
  notificationStore.info(`执行: ${action.title}`)
}

// Keyboard shortcuts
const handleKeyboardShortcuts = (event) => {
  if (event.ctrlKey) {
    switch (event.key) {
      case 'u':
        event.preventDefault()
        navigateToUpload()
        break
      case 'a':
        event.preventDefault()
        navigateToAnalytics()
        break
      case 'd':
        event.preventDefault()
        router.push('/analytics/donors')
        break
      case 'c':
        event.preventDefault()
        router.push('/analytics/campaigns')
        break
    }
  }
}

onMounted(() => {
  // Initialize dashboard
  notificationStore.success('Advanced dashboard loaded successfully')
  
  // Add keyboard shortcuts
  document.addEventListener('keydown', handleKeyboardShortcuts)
  
  // Check system theme preference
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDarkMode.value = true
    window.document.body.classList.add('dark-mode')
  }
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  document.removeEventListener('keydown', handleKeyboardShortcuts)
})
</script>

<style scoped>
.advanced-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 0;
  position: relative;
  overflow-x: hidden;
}

/* Animated background pattern */
.advanced-dashboard::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(239, 68, 68, 0.05) 0%, transparent 50%);
  z-index: -1;
  animation: backgroundFloat 20s ease-in-out infinite;
}

@keyframes backgroundFloat {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(-20px, -20px) rotate(1deg); }
  66% { transform: translate(20px, -10px) rotate(-1deg); }
}

/* Professional Navigation Header */
.professional-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 1000;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.professional-nav:hover {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-right: 40px;
  min-width: 300px;
  flex-shrink: 0;
}

.brand-logo {
  width: 40px;
  height: 40px;
  background: rgba(248, 250, 252, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.brand-logo:hover {
  background: rgba(248, 250, 252, 0.95);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.brand-logo .el-icon {
  font-size: 20px;
  color: #64748b;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-left: 10px;
  flex-shrink: 0;
  min-width: 200px;
}

.brand-text h1 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
}

.brand-text span {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.nav-menu {
  display: flex;
  gap: 12px;
  align-items: center;
}

.nav-dropdown {
  position: relative;
}

.nav-dropdown .el-button {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #475569;
  border-radius: 12px;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

.nav-dropdown .el-button:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #475569;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.6);
  color: #475569;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.nav-item:hover::before {
  left: 100%;
}

.nav-item.active {
  background: rgba(100, 116, 139, 0.15);
  color: #334155;
  border-color: rgba(100, 116, 139, 0.3);
  box-shadow: 0 4px 16px rgba(100, 116, 139, 0.15);
}

.nav-item .el-icon {
  font-size: 16px;
}

.nav-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  color: #64748b;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.action-btn:hover {
  background: rgba(248, 250, 252, 0.8);
  border-color: rgba(255, 255, 255, 0.4);
  color: #475569;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.action-btn:hover::before {
  left: 100%;
}

.action-btn.active {
  background: rgba(100, 116, 139, 0.2);
  border-color: rgba(100, 116, 139, 0.3);
  color: #334155;
  box-shadow: 0 4px 16px rgba(100, 116, 139, 0.2);
}

.ai-btn.active {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
}

.theme-btn.active {
  background: rgba(168, 85, 247, 0.2);
  border-color: rgba(168, 85, 247, 0.3);
  color: #a855f7;
  box-shadow: 0 4px 16px rgba(168, 85, 247, 0.2);
}

.profile-btn.active {
  background: rgba(34, 197, 94, 0.2);
  border-color: rgba(34, 197, 94, 0.3);
  color: #22c55e;
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.2);
}

/* Dark Mode Navigation */
.dark-mode .professional-nav {
  background: rgba(30, 41, 59, 0.98);
  border-bottom-color: rgba(255, 255, 255, 0.06);
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.04);
}

.dark-mode .brand-text h1 {
  color: #f8fafc;
}

.dark-mode .brand-text span {
  color: #94a3b8;
}

.dark-mode .nav-item {
  color: #94a3b8;
}

.dark-mode .nav-item:hover {
  background: rgba(148, 163, 184, 0.08);
  color: #cbd5e1;
}

.dark-mode .nav-item.active {
  background: rgba(148, 163, 184, 0.12);
  color: #e2e8f0;
  border-color: rgba(148, 163, 184, 0.2);
}

.dark-mode .action-btn {
  border-color: rgba(255, 255, 255, 0.08);
  color: #94a3b8;
}

.dark-mode .action-btn:hover {
  background: rgba(148, 163, 184, 0.08);
  border-color: rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
}

.dark-mode .action-btn.active {
  background: rgba(148, 163, 184, 0.12);
  border-color: rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
}

.dark-mode .ai-btn.active {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.25);
  color: #60a5fa;
}

.dark-mode .theme-btn.active {
  background: rgba(168, 85, 247, 0.15);
  border-color: rgba(168, 85, 247, 0.25);
  color: #c084fc;
}

.dark-mode .profile-btn.active {
  background: rgba(34, 197, 94, 0.15);
  border-color: rgba(34, 197, 94, 0.25);
  color: #4ade80;
}

/* Dropdown menu styling */
.el-dropdown-menu {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.el-dropdown-menu__item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  color: #475569;
  transition: all 0.3s ease;
}

.el-dropdown-menu__item:hover {
  background: rgba(100, 116, 139, 0.1);
  color: #334155;
}

.el-dropdown-menu__item .el-icon {
  font-size: 16px;
}

/* Adjust main content for fixed navigation */
.advanced-dashboard {
  padding-top: 70px;
}

/* Remove old floating controls styles */

/* Hero Section */
.hero-section {
  position: relative;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.animated-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
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
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 20%;
  left: 30%;
  animation-delay: 4s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 30%;
  right: 30%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: white;
  max-width: 800px;
  padding: 0 20px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.2;
}

.gradient-text {
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.highlight {
  display: block;
  font-size: 3rem;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 60px;
  margin-bottom: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.action-btn {
  padding: 12px 32px;
  font-size: 1rem;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* KPI Section */
.kpi-section {
  padding: 60px 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.kpi-card.advanced {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.kpi-card.advanced:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.kpi-icon-wrapper {
  position: relative;
}

.kpi-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.kpi-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  background: #e8f5e8;
  color: #27ae60;
}

.kpi-badge.warning {
  background: #fff3cd;
  color: #856404;
}

.kpi-content {
  text-align: center;
}

.kpi-value-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.kpi-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.kpi-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.9rem;
  font-weight: 600;
}

.kpi-change.up {
  color: #27ae60;
}

.kpi-change.down {
  color: #e74c3c;
}

.kpi-label {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 16px;
}

.kpi-sparkline {
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
}

.sparkline-chart {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

/* Charts Section */
.charts-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.chart-card.advanced {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  height: 400px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-header h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.chart-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.chart-placeholder.advanced {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-animation {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 200px;
}

.chart-bar {
  width: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  animation: growBar 2s ease-out infinite;
}

.chart-bar:nth-child(2) { animation-delay: 0.2s; }
.chart-bar:nth-child(3) { animation-delay: 0.4s; }
.chart-bar:nth-child(4) { animation-delay: 0.6s; }
.chart-bar:nth-child(5) { animation-delay: 0.8s; }
.chart-bar:nth-child(6) { animation-delay: 1s; }
.chart-bar:nth-child(7) { animation-delay: 1.2s; }

@keyframes growBar {
  0% { height: 0; }
  50% { height: var(--height); }
  100% { height: var(--height); }
}

.blood-type-wheel {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  position: relative;
  margin: 0 auto;
  background: conic-gradient(
    from 0deg,
    #e74c3c 0deg 45deg,
    #3498db 45deg 90deg,
    #2ecc71 90deg 135deg,
    #9b59b6 135deg 180deg,
    #c0392b 180deg 225deg,
    #2980b9 225deg 270deg,
    #27ae60 270deg 315deg,
    #8e44ad 315deg 360deg
  );
}

/* Activity Section */
.activity-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.activity-feed {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #ecf0f1;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.activity-description {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.activity-time {
  color: #95a5a6;
  font-size: 0.8rem;
}

/* Quick Actions Section */
.quick-actions-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.action-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  flex-shrink: 0;
}

.action-content {
  flex: 1;
}

.action-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.action-description {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* AI Features Section */
.ai-features-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Responsive AI Features Section */
@media (max-width: 1024px) {
  .ai-features-section {
    padding: 0 16px 50px;
  }
}

@media (max-width: 768px) {
  .ai-features-section {
    padding: 0 12px 40px;
  }
}

@media (max-width: 480px) {
  .ai-features-section {
    padding: 0 8px 30px;
  }
}

.ai-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.ai-feature-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px;
  color: white;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.ai-feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
}

/* Responsive AI Features */
@media (max-width: 1024px) {
  .ai-features-section {
    padding: 0 16px 50px;
  }
  
  .ai-features-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .ai-feature-card {
    padding: 20px;
    gap: 16px;
  }
  
  .feature-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .feature-content h3 {
    font-size: 1.1rem;
  }
  
  .feature-content p {
    font-size: 0.9rem;
  }
  
  /* Enhanced navbar tooltips for tablet */
  .nav-menu .el-tooltip {
    display: block;
  }
  
  .nav-actions .el-tooltip {
    display: block;
  }
}

@media (max-width: 768px) {
  .ai-features-section {
    padding: 0 12px 40px;
  }
  
  .ai-features-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .ai-feature-card {
    padding: 16px;
    gap: 12px;
    flex-direction: column;
    text-align: center;
  }
  
  .feature-icon {
    width: 48px;
    height: 48px;
    font-size: 18px;
    margin: 0 auto;
  }
  
  .feature-content h3 {
    font-size: 1rem;
    text-align: center;
  }
  
  .feature-content p {
    font-size: 0.85rem;
    text-align: center;
    margin-bottom: 8px;
  }
  
  .feature-stats .stat {
    font-size: 0.8rem;
    text-align: center;
  }
  
  /* Mobile navbar improvements */
  .nav-menu .el-tooltip {
    display: none;
  }
  
  .nav-actions .el-tooltip {
    display: none;
  }
  
  /* Show tooltips on hover for mobile */
  .nav-item[data-tooltip]:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    white-space: nowrap;
    z-index: 1000;
    pointer-events: none;
    max-width: 200px;
    word-wrap: break-word;
  }
  
  .action-btn[data-tooltip]:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    white-space: nowrap;
    z-index: 1000;
    pointer-events: none;
    max-width: 200px;
    word-wrap: break-word;
  }
}

@media (max-width: 480px) {
  .ai-features-grid {
    gap: 12px;
  }
  
  .ai-feature-card {
    padding: 12px;
    gap: 8px;
  }
  
  .feature-icon {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
  
  .feature-content h3 {
    font-size: 0.95rem;
  }
  
  .feature-content p {
    font-size: 0.8rem;
    line-height: 1.4;
  }
  
  .feature-stats .stat {
    font-size: 0.75rem;
  }
  
  /* Ultra-mobile navbar tooltips */
  .nav-item[data-tooltip]:hover::after {
    font-size: 0.7rem;
    bottom: -25px;
    max-width: 150px;
  }
  
  .action-btn[data-tooltip]:hover::after {
    font-size: 0.7rem;
    bottom: -25px;
    max-width: 150px;
  }
}

.feature-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.feature-content h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.feature-content p {
  margin: 0 0 12px 0;
  opacity: 0.9;
  line-height: 1.5;
}

.feature-stats .stat {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Emergency Section */
.emergency-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.emergency-dashboard {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px;
  color: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.emergency-dashboard:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.25);
}

.emergency-dashboard.active {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.emergency-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.emergency-stat {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.emergency-stat .stat-value {
  font-size: 2rem;
  font-weight: 600;
  color: white;
  margin-bottom: 4px;
}

.emergency-stat .stat-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.emergency-map {
  margin-bottom: 24px;
}

.map-placeholder {
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  color: white;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.emergency-pulse {
  width: 20px;
  height: 20px;
  background: #fbbf24;
  border-radius: 50%;
  position: absolute;
  animation: emergencyPulse 2s infinite;
}

.emergency-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

/* Donor Engagement Section */
.donor-engagement-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.engagement-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.engagement-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.engagement-card:hover {
  transform: translateY(-4px);
}

.engagement-card .card-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  margin-bottom: 16px;
}

.engagement-card h3 {
  margin: 0 0 8px 0;
  color: #1f2937;
  font-size: 1.1rem;
}

.engagement-card p {
  margin: 0 0 16px 0;
  color: #6b7280;
  line-height: 1.5;
}

.passport-stats {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.mini-stat {
  text-align: center;
  flex: 1;
}

.mini-stat .value {
  display: block;
  font-size: 1.2rem;
  font-weight: bold;
  color: #10b981;
}

.mini-stat .label {
  font-size: 0.8rem;
  color: #6b7280;
}

.badges {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.badge {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.badge:hover {
  transform: scale(1.1);
}

.badge.gold {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.badge.silver {
  background: linear-gradient(135deg, #e5e7eb 0%, #9ca3af 100%);
}

.badge.bronze {
  background: linear-gradient(135deg, #d97706 0%, #92400e 100%);
}

/* Impact Visualization Section */
.impact-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.impact-dashboard {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #bbf7d0;
}

.blood-flow-visualization {
  margin-bottom: 32px;
}

.flow-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #16a34a;
  margin-bottom: 16px;
}

.flow-map {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.flow-node {
  padding: 12px 20px;
  background: white;
  border-radius: 8px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.flow-node.donor {
  background: #dbeafe;
  color: #1e40af;
}

.flow-node.center {
  background: #fef3c7;
  color: #92400e;
}

.flow-node.hospital {
  background: #fce7f3;
  color: #9f1239;
}

.flow-node.recipient {
  background: #dcfce7;
  color: #16a34a;
}

.flow-arrow {
  font-size: 1.5rem;
  color: #6b7280;
}

.impact-stories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.story-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.story-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.story-content h4 {
  margin: 0 0 8px 0;
  color: #1f2937;
}

.story-content p {
  margin: 0;
  color: #6b7280;
  line-height: 1.5;
}

.sustainability-metrics h3 {
  margin: 0 0 16px 0;
  color: #16a34a;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #d1d5db;
}

.metric:last-child {
  border-bottom: none;
}

.metric-label {
  color: #6b7280;
}

.metric-value {
  font-weight: bold;
  color: #16a34a;
}

/* Animations */
@keyframes emergencyPulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0.5;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

/* Comprehensive Footer Styles */
.comprehensive-footer {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  color: white;
  margin-top: 80px;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Main Footer Content */
.footer-main {
  padding: 60px 0 40px;
  border-bottom: 1px solid #374151;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr;
  gap: 40px;
}

.footer-section h3 {
  color: #ef4444;
  font-size: 1.5rem;
  margin-bottom: 8px;
  font-weight: 700;
}

.footer-section h4 {
  color: #f3f4f6;
  font-size: 1.1rem;
  margin-bottom: 20px;
  font-weight: 600;
  border-bottom: 2px solid #ef4444;
  padding-bottom: 8px;
}

.footer-logo p {
  color: #9ca3af;
  margin: 0 0 16px 0;
  font-size: 0.9rem;
}

.footer-description p {
  color: #d1d5db;
  line-height: 1.6;
  margin-bottom: 20px;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-link {
  width: 40px;
  height: 40px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: #ef4444;
  color: white;
  transform: translateY(-2px);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.3s ease;
  display: flex;
  align-items: center;
}

.footer-links a:hover {
  color: #ef4444;
}

.footer-links a::before {
  content: '→';
  margin-right: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.footer-links a:hover::before {
  opacity: 1;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #d1d5db;
}

.contact-item .el-icon {
  color: #ef4444;
  font-size: 18px;
}

/* Impact Statistics */
.footer-impact {
  padding: 40px 0;
  background: rgba(239, 68, 68, 0.1);
  border-bottom: 1px solid #374151;
}

.impact-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 30px;
  text-align: center;
}

.impact-stat {
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.impact-stat:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(239, 68, 68, 0.2);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #ef4444;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  color: #f3f4f6;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Technology Partners */
.footer-partners {
  padding: 40px 0;
  background: rgba(31, 41, 55, 0.5);
  border-bottom: 1px solid #374151;
}

.footer-partners h4 {
  text-align: center;
  color: #f3f4f6;
  margin-bottom: 30px;
  font-size: 1.3rem;
}

.partners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.partner-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: all 0.3s ease;
  font-weight: 500;
}

.partner-item:hover {
  background: rgba(239, 68, 68, 0.1);
  transform: translateY(-2px);
}

/* Legal & Compliance */
.footer-legal {
  padding: 30px 0;
  background: #111827;
}

.legal-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 20px;
}

.legal-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.legal-links a {
  color: #9ca3af;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.legal-links a:hover {
  color: #ef4444;
}

.certifications {
  display: flex;
  gap: 12px;
}

.cert-badge {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #374151;
  color: #6b7280;
  font-size: 0.9rem;
}

.copyright p {
  margin: 0;
}

/* Footer Responsive Design */
@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }
  
  .impact-stats {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 20px;
  }
  
  .legal-content {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .footer-main {
    padding: 40px 0 30px;
  }
  
  .impact-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .partners-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .legal-links {
    flex-direction: column;
    gap: 12px;
  }
  
  .certifications {
    justify-content: center;
  }
}

/* Footer Animations */
.footer-section {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

.footer-section:nth-child(1) { animation-delay: 0.1s; }
.footer-section:nth-child(2) { animation-delay: 0.2s; }
.footer-section:nth-child(3) { animation-delay: 0.3s; }
.footer-section:nth-child(4) { animation-delay: 0.4s; }
.footer-section:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.impact-stat {
  opacity: 0;
  animation: scaleIn 0.5s ease-out forwards;
}

.impact-stat:nth-child(1) { animation-delay: 0.1s; }
.impact-stat:nth-child(2) { animation-delay: 0.2s; }
.impact-stat:nth-child(3) { animation-delay: 0.3s; }
.impact-stat:nth-child(4) { animation-delay: 0.4s; }
.impact-stat:nth-child(5) { animation-delay: 0.5s; }

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Dark Mode Footer Enhancements */
.dark-mode .comprehensive-footer {
  background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
}

.dark-mode .footer-section h3,
.dark-mode .footer-section h4 {
  color: #f87171;
}

/* Professional Sidebar Styles */
.professional-sidebar {
  position: fixed;
  top: 70px;
  right: -380px;
  width: 380px;
  height: calc(100vh - 70px);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  box-shadow: -8px 0 32px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 999;
  overflow-y: auto;
  border-left: 1px solid rgba(255, 255, 255, 0.2);
}

.professional-sidebar.active {
  right: 0;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(248, 250, 252, 0.6);
  backdrop-filter: blur(10px);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-title h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.2rem;
  font-weight: 600;
}

.sidebar-title .el-icon {
  color: #64748b;
  font-size: 20px;
}

.close-btn {
  color: #94a3b8 !important;
}

.close-btn:hover {
  color: #475569 !important;
}

.sidebar-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-height: calc(100vh - 70px - 80px);
  overflow-y: auto;
}

/* Profile Section */
.profile-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(254, 252, 232, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(251, 191, 36, 0.3);
  margin-bottom: 24px;
  box-shadow: 0 4px 16px rgba(251, 191, 36, 0.1);
}

.user-avatar {
  position: relative;
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(251, 191, 36, 0.3);
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid white;
}

.status-indicator.online {
  background: #84cc16;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-info h4 {
  margin: 0 0 4px 0;
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-title {
  color: #64748b;
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-id {
  color: #94a3b8;
  margin: 0 0 8px 0;
  font-size: 0.8rem;
  font-family: monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.badge {
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 500;
}

.badge.premium {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
}

.badge.verified {
  background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%);
  color: white;
}

.badge.expert {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

/* Stats Section */
.stats-section {
  margin-bottom: 24px;
}

.stats-section h5 {
  margin: 0 0 16px 0;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background: rgba(248, 250, 252, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 32px;
  height: 32px;
  margin: 0 auto 8px;
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #1e293b;
  margin-bottom: 2px;
}

.stat-label {
  color: #64748b;
  font-size: 0.75rem;
}

/* Settings Menu */
.settings-menu {
  margin-bottom: 24px;
}

.settings-menu h5 {
  margin: 0 0 16px 0;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748b;
  background: rgba(248, 250, 252, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.menu-item:hover {
  background: rgba(248, 250, 252, 0.8);
  color: #475569;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.menu-item .el-icon:first-child {
  font-size: 16px;
}

.menu-item .arrow {
  margin-left: auto;
  font-size: 12px;
  opacity: 0.5;
}

/* Settings Toggles */
.notification-settings,
.privacy-settings {
  margin-bottom: 24px;
}

.notification-settings h5,
.privacy-settings h5 {
  margin: 0 0 16px 0;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.setting-toggles {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(248, 250, 252, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.toggle-info {
  flex: 1;
  min-width: 0;
}

.toggle-info span {
  display: block;
  color: #1e293b;
  font-weight: 500;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.toggle-info small {
  color: #64748b;
  font-size: 0.75rem;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Security Actions */
.security-actions {
  margin-bottom: 24px;
}

.security-actions h5 {
  margin: 0 0 16px 0;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.security-btn {
  justify-content: flex-start !important;
  padding: 12px 16px !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  border: 1px solid rgba(0, 0, 0, 0.06) !important;
}

.security-btn.warning {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
  border-color: rgba(251, 191, 36, 0.3) !important;
  color: white !important;
}

.security-btn.danger {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
  border-color: rgba(248, 113, 113, 0.3) !important;
  color: white !important;
}

/* Dark Mode Sidebar */
.dark-mode .professional-sidebar {
  background: rgba(30, 41, 59, 0.98);
  border-left-color: rgba(255, 255, 255, 0.06);
  box-shadow: -2px 0 12px rgba(0, 0, 0, 0.08);
}

.dark-mode .sidebar-header {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border-bottom-color: rgba(255, 255, 255, 0.06);
}

.dark-mode .sidebar-title h3 {
  color: #f8fafc;
}

.dark-mode .sidebar-title .el-icon {
  color: #94a3b8;
}

.dark-mode .close-btn {
  color: #64748b !important;
}

.dark-mode .close-btn:hover {
  color: #cbd5e1 !important;
}

.dark-mode .profile-section {
  background: linear-gradient(135deg, #334155 0%, #475569 100%);
  border-color: rgba(251, 191, 36, 0.3);
}

.dark-mode .user-info h4 {
  color: #f8fafc;
}

.dark-mode .user-title {
  color: #94a3b8;
}

.dark-mode .user-id {
  color: #64748b;
}

.dark-mode .stats-section h5,
.dark-mode .settings-menu h5,
.dark-mode .notification-settings h5,
.dark-mode .privacy-settings h5,
.dark-mode .security-actions h5 {
  color: #cbd5e1;
}

.dark-mode .stat-item {
  background: #334155;
  border-color: rgba(255, 255, 255, 0.06);
}

.dark-mode .stat-value {
  color: #f8fafc;
}

.dark-mode .stat-label {
  color: #94a3b8;
}

.dark-mode .menu-item {
  color: #94a3b8;
}

.dark-mode .menu-item:hover {
  background: rgba(148, 163, 184, 0.12);
  color: #cbd5e1;
}

.dark-mode .toggle-item {
  background: #334155;
  border-color: rgba(255, 255, 255, 0.06);
}

.dark-mode .toggle-info span {
  color: #f8fafc;
}

.dark-mode .toggle-info small {
  color: #94a3b8;
}

.dark-mode .security-btn {
  border-color: rgba(255, 255, 255, 0.06) !important;
}

.dark-mode .security-btn.warning {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
  border-color: rgba(251, 191, 36, 0.3) !important;
  color: white !important;
}

.dark-mode .security-btn.danger {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
  border-color: rgba(248, 113, 113, 0.3) !important;
  color: white !important;
}

/* Dark Mode Emergency Section */
.dark-mode .emergency-dashboard {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.dark-mode .emergency-dashboard.active {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.dark-mode .emergency-stat {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.dark-mode .emergency-stat .stat-value {
  color: white;
}

.dark-mode .emergency-stat .stat-label {
  color: rgba(255, 255, 255, 0.9);
}

.dark-mode .map-placeholder {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Floating Action Button */
.floating-action-button {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
}

.fab-main {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.fab-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.fab-main:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
}

.fab-main:hover::before {
  left: 100%;
}

.fab-main .el-icon {
  font-size: 24px;
  color: white;
  transition: transform 0.3s ease;
}

.floating-action-button.active .fab-main .el-icon {
  transform: rotate(45deg);
}

.fab-options {
  position: absolute;
  bottom: 70px;
  right: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);
  transition: all 0.3s ease;
}

.floating-action-button.active .fab-options {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.fab-option {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  transform: scale(0);
  position: relative;
  overflow: hidden;
}

.fab-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.floating-action-button.active .fab-option {
  transform: scale(1);
}

.floating-action-button.active .fab-option:nth-child(1) {
  transition-delay: 0.1s;
}

.floating-action-button.active .fab-option:nth-child(2) {
  transition-delay: 0.2s;
}

.floating-action-button.active .fab-option:nth-child(3) {
  transition-delay: 0.3s;
}

.floating-action-button.active .fab-option:nth-child(4) {
  transition-delay: 0.4s;
}

.fab-option:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.fab-option:hover::before {
  left: 100%;
}

.fab-option .el-icon {
  font-size: 20px;
  color: #64748b;
  transition: color 0.3s ease;
}

.fab-option:hover .el-icon {
  color: #334155;
}

/* Dashboard Builder Section */
.dashboard-builder-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Dashboard Builder Section */
.dashboard-builder-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.dashboard-settings {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.settings-tabs {
  width: 100%;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-item label {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9rem;
}

.theme-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(248, 250, 252, 0.8);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.theme-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.theme-option.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.theme-preview {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.theme-option span {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 500;
}

.refresh-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.template-card {
  background: rgba(248, 250, 252, 0.8);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background: rgba(248, 250, 252, 0.95);
}

.template-preview {
  height: 80px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}

.mini-layout {
  position: relative;
  width: 100%;
  height: 100%;
}

.mini-component {
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.4);
  border-radius: 4px;
}

.template-info h4 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.template-info p {
  margin: 0;
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.4;
}

.upload-demo {
  width: 100%;
}

/* Dark Mode Dashboard Settings */
.dark-mode .dashboard-settings {
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .setting-item label {
  color: #f8fafc;
}

.dark-mode .theme-option {
  background: rgba(51, 65, 85, 0.8);
}

.dark-mode .theme-option:hover {
  background: rgba(51, 65, 85, 0.95);
}

.dark-mode .theme-option span {
  color: #cbd5e1;
}

.dark-mode .template-card {
  background: rgba(51, 65, 85, 0.8);
}

.dark-mode .template-card:hover {
  background: rgba(51, 65, 85, 0.95);
}

.dark-mode .template-preview {
  background: rgba(255, 255, 255, 0.1);
}

.dark-mode .template-info h4 {
  color: #f8fafc;
}

.dark-mode .template-info p {
  color: #94a3b8;
}

.component-palette {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.component-palette h3 {
  margin: 0 0 20px 0;
  color: #1e293b;
  font-size: 1.2rem;
  font-weight: 600;
}

.palette-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.palette-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: rgba(248, 250, 252, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: grab;
  transition: all 0.3s ease;
  text-align: center;
}

.palette-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background: rgba(248, 250, 252, 0.95);
}

.palette-item:active {
  cursor: grabbing;
  transform: scale(0.95);
}

.palette-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.palette-item span {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.dashboard-canvas {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.drop-zone {
  min-height: 600px;
  border: 2px dashed rgba(100, 116, 139, 0.3);
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
}

.drop-zone.drag-over {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.canvas-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.canvas-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.2rem;
  font-weight: 600;
}

.canvas-content {
  min-height: 500px;
  position: relative;
}

.canvas-content.layout-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.canvas-content.layout-free {
  position: relative;
  min-height: 500px;
}

.canvas-content.layout-masonry {
  column-count: 3;
  column-gap: 20px;
}

.dashboard-component {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: move;
}

.dashboard-component:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.component-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: rgba(248, 250, 252, 0.8);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.component-header h4 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.component-actions {
  display: flex;
  gap: 4px;
}

.component-content {
  padding: 20px;
  min-height: 150px;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 150px;
}

.chart-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background: rgba(248, 250, 252, 0.6);
  border-radius: 8px;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
}

.table-placeholder {
  width: 100%;
}

.alert-placeholder {
  width: 100%;
}

.progress-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.progress-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-item span {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.default-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 150px;
  color: #94a3b8;
}

.default-placeholder .el-icon {
  font-size: 32px;
}

/* Dark Mode Dashboard Builder */
.dark-mode .component-palette,
.dark-mode .dashboard-canvas {
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .component-palette h3,
.dark-mode .canvas-header h3 {
  color: #f8fafc;
}

.dark-mode .palette-item {
  background: rgba(51, 65, 85, 0.8);
}

.dark-mode .palette-item:hover {
  background: rgba(51, 65, 85, 0.95);
}

.dark-mode .palette-item span {
  color: #cbd5e1;
}

.dark-mode .drop-zone {
  border-color: rgba(148, 163, 184, 0.3);
}

.dark-mode .drop-zone.drag-over {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.dark-mode .dashboard-component {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .component-header {
  background: rgba(51, 65, 85, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .component-header h4 {
  color: #f8fafc;
}

.dark-mode .stat-item {
  background: rgba(51, 65, 85, 0.6);
}

.dark-mode .stat-value {
  color: #f8fafc;
}

.dark-mode .stat-label {
  color: #94a3b8;
}

.dark-mode .progress-item span {
  color: #94a3b8;
}

.dark-mode .default-placeholder {
  color: #64748b;
}

/* Task Management Section */
.task-management-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.task-statistics {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.stat-card:nth-child(1) .stat-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card:nth-child(2) .stat-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-card:nth-child(3) .stat-icon {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
}

.stat-card:nth-child(4) .stat-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.stat-card:nth-child(5) .stat-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.stat-change.positive {
  color: #22c55e;
}

.stat-change.negative {
  color: #ef4444;
}

.task-filters {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9rem;
  white-space: nowrap;
}

.task-list {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.task-table {
  width: 100%;
}

.task-title {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-title-text {
  font-weight: 600;
  color: #1e293b;
}

.task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.task-actions {
  display: flex;
  gap: 4px;
}

.assignee-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.overdue {
  color: #ef4444;
  font-weight: 600;
}

.due-soon {
  color: #f59e0b;
  font-weight: 600;
}

.normal {
  color: #64748b;
}

.task-details {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.task-detail-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  padding-bottom: 16px;
}

.task-detail-header h3 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 1.2rem;
  font-weight: 600;
}

.task-detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.9rem;
  color: #64748b;
}

.detail-item .el-icon {
  font-size: 16px;
}

.task-detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.detail-section p {
  margin: 0;
  color: #64748b;
  line-height: 1.6;
}

.detail-section ul {
  margin: 0;
  padding-left: 20px;
  color: #64748b;
}

.detail-section li {
  margin-bottom: 4px;
}

.attachment-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(248, 250, 252, 0.8);
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1e293b;
}

.progress-history {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.progress-record {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: rgba(248, 250, 252, 0.8);
  border-radius: 6px;
}

.record-time {
  min-width: 100px;
  font-size: 0.8rem;
  color: #64748b;
}

.record-info {
  flex: 1;
  display: flex;
  gap: 8px;
  align-items: center;
}

.record-action {
  color: #64748b;
  font-size: 0.8rem;
}

.record-value {
  font-weight: 600;
  color: #1e293b;
}

.task-detail-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.task-comments {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comments-header h4 {
  margin: 0 0 16px 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(248, 250, 252, 0.8);
  border-radius: 8px;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.comment-author {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9rem;
}

.comment-time {
  font-size: 0.8rem;
  color: #64748b;
}

.comment-text {
  color: #64748b;
  line-height: 1.5;
}

.comment-input {
  display: flex;
  flex-direction: column;
}

/* Dark Mode Task Management */
.dark-mode .task-statistics,
.dark-mode .task-filters,
.dark-mode .task-list {
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .stat-card {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .stat-content h3 {
  color: #f8fafc;
}

.dark-mode .stat-value {
  color: #f8fafc;
}

.dark-mode .stat-change {
  color: #94a3b8;
}

.dark-mode .stat-change.positive {
  color: #86efac;
}

.dark-mode .stat-change.negative {
  color: #f87171;
}

.dark-mode .filter-group label {
  color: #f8fafc;
}

.dark-mode .task-title-text {
  color: #f8fafc;
}

.dark-mode .detail-item {
  color: #cbd5e1;
}

.dark-mode .detail-section h4 {
  color: #f8fafc;
}

.dark-mode .detail-section p,
.dark-mode .detail-section ul,
.dark-mode .detail-section li {
  color: #94a3b8;
}

.dark-mode .attachment-item {
  background: rgba(51, 65, 85, 0.8);
  color: #f8fafc;
}

.dark-mode .progress-record {
  background: rgba(51, 65, 85, 0.8);
}

.dark-mode .record-time,
.dark-mode .record-action {
  color: #94a3b8;
}

.dark-mode .record-value {
  color: #f8fafc;
}

.dark-mode .comment-item {
  background: rgba(51, 65, 85, 0.8);
}

.dark-mode .comment-author {
  color: #f8fafc;
}

.dark-mode .comment-time {
  color: #94a3b8;
}

.dark-mode .comment-text {
  color: #94a3b8;
}

/* Responsive Sidebar */
@media (max-width: 768px) {
  .professional-sidebar {
    width: 100%;
    right: -100%;
  }
  
  .professional-sidebar.active {
    right: 0;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }
  
  .stat-item {
    padding: 8px;
  }
  
  .stat-icon {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  
  .stat-value {
    font-size: 1rem;
  }
}

/* Account Section Styles */
.account-section {
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.account-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.account-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.account-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* Profile Card */
.profile-header {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
}

.profile-avatar {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ef4444;
}

.avatar-status {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
}

.avatar-status.online {
  background: #10b981;
}

.profile-info h3 {
  margin: 0 0 4px 0;
  color: #1f2937;
  font-size: 1.3rem;
  font-weight: 600;
}

.profile-title {
  color: #6b7280;
  margin: 0 0 4px 0;
  font-size: 0.9rem;
}

.profile-id {
  color: #9ca3af;
  margin: 0 0 12px 0;
  font-size: 0.8rem;
  font-family: monospace;
}

.profile-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.premium {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
}

.badge.verified {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.badge.expert {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.profile-stat {
  text-align: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.profile-stat .stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ef4444;
  margin-bottom: 4px;
}

.profile-stat .stat-label {
  color: #6b7280;
  font-size: 0.8rem;
}

.profile-actions {
  display: flex;
  gap: 12px;
}

/* Settings Card */
.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.settings-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.1rem;
  font-weight: 600;
}

.settings-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-group h4 {
  margin: 0 0 16px 0;
  color: #374151;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
}

.setting-label {
  display: block;
  color: #1f2937;
  font-weight: 500;
  margin-bottom: 2px;
}

.setting-desc {
  color: #6b7280;
  font-size: 0.85rem;
}

/* Health Card */
.health-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.health-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.1rem;
  font-weight: 600;
}

.health-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.metric-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  flex-shrink: 0;
}

.metric-icon.hemoglobin {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.metric-icon.pressure {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.metric-icon.weight {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.metric-icon.bmi {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 1.1rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 2px;
}

.metric-label {
  color: #6b7280;
  font-size: 0.8rem;
  margin-bottom: 2px;
}

.metric-status {
  font-size: 0.75rem;
  font-weight: 500;
}

.metric-status.good {
  color: #10b981;
}

.health-chart {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
}

.chart-title {
  color: #374151;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 12px;
}

.mini-chart {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 40px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 2px;
  min-height: 8px;
}

/* Security Card */
.security-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.security-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.1rem;
  font-weight: 600;
}

.security-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.security-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.security-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  flex-shrink: 0;
}

.security-icon.two-factor {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.security-icon.last-login {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.security-icon.devices {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.security-content {
  flex: 1;
}

.security-title {
  color: #1f2937;
  font-weight: 500;
  margin-bottom: 2px;
}

.security-desc {
  color: #6b7280;
  font-size: 0.85rem;
  margin-bottom: 4px;
}

.security-status {
  font-size: 0.8rem;
  font-weight: 500;
}

.security-status.enabled {
  color: #10b981;
}

.security-status.normal {
  color: #3b82f6;
}

.security-actions {
  display: flex;
  gap: 12px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .highlight {
    font-size: 2rem;
  }
  
  .hero-stats {
    flex-direction: column;
    gap: 20px;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}

/* Real-time Monitoring Dashboard Styles */
.realtime-monitoring-section {
  padding: 40px 0;
}

.monitoring-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.monitoring-card {
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.monitoring-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: #10b981;
  font-weight: 500;
}

.live-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Blood Inventory Styles */
.inventory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.blood-type-card {
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.blood-type-card.normal {
  border-color: rgba(16, 185, 129, 0.3);
  background: rgba(16, 185, 129, 0.05);
}

.blood-type-card.low {
  border-color: rgba(251, 146, 60, 0.3);
  background: rgba(251, 146, 60, 0.05);
}

.blood-type-card.critical {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
}

.blood-type {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.blood-amount {
  font-size: 1.3rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.blood-status {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.blood-trend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.blood-trend.up {
  color: #10b981;
}

.blood-trend.down {
  color: #ef4444;
}

.blood-trend.stable {
  color: #6b7280;
}

/* Donation Centers Styles */
.centers-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.center-card {
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.center-card.open {
  border-color: rgba(16, 185, 129, 0.3);
  background: rgba(16, 185, 129, 0.05);
}

.center-card.busy {
  border-color: rgba(251, 146, 60, 0.3);
  background: rgba(251, 146, 60, 0.05);
}

.center-card.closed {
  border-color: rgba(107, 114, 128, 0.3);
  background: rgba(107, 114, 128, 0.05);
}

.center-info {
  flex: 1;
}

.center-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.center-address {
  font-size: 0.85rem;
  color: #6b7280;
}

.center-metrics {
  display: flex;
  gap: 16px;
  margin: 12px 0;
}

.metric {
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 2px;
}

.metric-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.center-status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.center-status-indicator.open .status-dot {
  background: #10b981;
}

.center-status-indicator.busy .status-dot {
  background: #f59e0b;
}

.center-status-indicator.closed .status-dot {
  background: #6b7280;
}

/* Emergency Alerts Styles */
.alerts-container {
  max-height: 300px;
  overflow-y: auto;
}

.alert-item {
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.alert-item.critical {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
}

.alert-item.warning {
  border-color: rgba(251, 146, 60, 0.3);
  background: rgba(251, 146, 60, 0.05);
}

.alert-item.info {
  border-color: rgba(59, 130, 246, 0.3);
  background: rgba(59, 130, 246, 0.05);
}

.alert-icon {
  color: #374151;
  margin-top: 2px;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.alert-message {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.alert-time {
  font-size: 0.75rem;
  color: #9ca3af;
}

.alert-actions {
  display: flex;
  gap: 8px;
}

.no-alerts {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

/* Geographic Map Styles */
.map-container {
  height: 300px;
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.map-placeholder {
  text-align: center;
  color: #6b7280;
}

.map-placeholder h4 {
  margin: 16px 0 8px 0;
  color: #374151;
}

.map-placeholder p {
  margin: 0 0 16px 0;
  font-size: 0.85rem;
}

.map-legend {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.high {
  background: #ef4444;
}

.legend-color.medium {
  background: #f59e0b;
}

.legend-color.low {
  background: #10b981;
}

/* Dark Mode for Real-time Monitoring */
.dark-mode .monitoring-card {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .card-header h3 {
  color: #f8fafc;
}

.dark-mode .blood-type-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .blood-type {
  color: #f8fafc;
}

.dark-mode .blood-amount {
  color: #e2e8f0;
}

.dark-mode .blood-status {
  color: #94a3b8;
}

.dark-mode .center-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .center-name {
  color: #f8fafc;
}

.dark-mode .center-address {
  color: #94a3b8;
}

.dark-mode .metric-value {
  color: #e2e8f0;
}

.dark-mode .alert-item {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .alert-title {
  color: #f8fafc;
}

.dark-mode .alert-message {
  color: #94a3b8;
}

.dark-mode .map-container {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .map-placeholder {
  color: #94a3b8;
}

.dark-mode .map-placeholder h4 {
  color: #e2e8f0;
}

/* Responsive Navigation */
@media (max-width: 1200px) {
  .nav-brand {
    margin-right: 20px;
    min-width: 250px;
  }
  
  .nav-menu {
    gap: 8px;
  }
  
  .nav-item {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
  
  .nav-item .el-icon {
    font-size: 14px;
  }
}

@media (max-width: 1024px) {
  .nav-container {
    padding: 0 16px;
  }
  
  .nav-brand {
    margin-right: 16px;
    min-width: 200px;
  }
  
  .brand-text h1 {
    font-size: 1.1rem;
  }
  
  .brand-text span {
    font-size: 0.75rem;
  }
  
  .nav-menu {
    gap: 6px;
  }
  
  .nav-item {
    padding: 6px 10px;
    font-size: 0.85rem;
  }
  
  .nav-item .el-icon {
    font-size: 13px;
  }
  
  .nav-actions {
    gap: 8px;
  }
  
  .action-btn {
    padding: 6px 10px;
    font-size: 0.85rem;
  }
  
  .action-btn .el-icon {
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .professional-nav {
    height: 60px;
  }
  
  .nav-container {
    padding: 0 12px;
  }
  
  .nav-brand {
    margin-right: 12px;
    min-width: 150px;
    gap: 12px;
  }
  
  .brand-logo {
    width: 32px;
    height: 32px;
  }
  
  .brand-logo .el-icon {
    font-size: 16px;
  }
  
  .brand-text {
    margin-left: 8px;
    min-width: 120px;
  }
  
  .brand-text h1 {
    font-size: 1rem;
  }
  
  .brand-text span {
    font-size: 0.7rem;
  }
  
  .nav-menu {
    gap: 4px;
  }
  
  .nav-item {
    padding: 6px 8px;
    font-size: 0.8rem;
    border-radius: 8px;
  }
  
  .nav-item .el-icon {
    font-size: 12px;
  }
  
  .nav-item span {
    display: none;
  }
  
  .nav-dropdown .el-button span {
    display: none;
  }
  
  .nav-actions {
    gap: 6px;
  }
  
  .action-btn {
    padding: 6px 8px;
    font-size: 0.8rem;
    border-radius: 8px;
  }
  
  .action-btn .el-icon {
    font-size: 12px;
  }
  
  .action-btn span {
    display: none;
  }
}

@media (max-width: 480px) {
  .professional-nav {
    height: 56px;
  }
  
  .nav-container {
    padding: 0 8px;
  }
  
  .nav-brand {
    margin-right: 8px;
    min-width: 120px;
    gap: 8px;
  }
  
  .brand-logo {
    width: 28px;
    height: 28px;
  }
  
  .brand-logo .el-icon {
    font-size: 14px;
  }
  
  .brand-text {
    margin-left: 6px;
    min-width: 80px;
  }
  
  .brand-text h1 {
    font-size: 0.9rem;
  }
  
  .brand-text span {
    display: none;
  }
  
  .nav-menu {
    gap: 2px;
  }
  
  .nav-item {
    padding: 4px 6px;
    font-size: 0.75rem;
    border-radius: 6px;
  }
  
  .nav-item .el-icon {
    font-size: 11px;
  }
  
  .nav-actions {
    gap: 4px;
  }
  
  .action-btn {
    padding: 4px 6px;
    font-size: 0.75rem;
    border-radius: 6px;
  }
  
  .action-btn .el-icon {
    font-size: 11px;
  }
}

/* AI Details Dialog Styles */
.ai-details-dialog {
  backdrop-filter: blur(10px);
}

.ai-details-dialog .el-dialog {
  border-radius: 16px;
  overflow: hidden;
}

.ai-details-dialog .el-dialog__header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px;
  margin: 0;
}

.ai-details-dialog .el-dialog__title {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

.ai-details-dialog .el-dialog__headerbtn .el-dialog__close {
  color: white;
  font-size: 20px;
}

.ai-details-content {
  padding: 24px;
  max-height: 70vh;
  overflow-y: auto;
}

.ai-overview {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  align-items: flex-start;
}

.ai-icon-large {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
  flex-shrink: 0;
}

.ai-icon-large.blood-match {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
}

.ai-icon-large.scarcity-alert {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
}

.ai-icon-large.inventory-opt {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
}

.ai-info {
  flex: 1;
}

.ai-info h3 {
  margin: 0 0 12px 0;
  color: #1e293b;
  font-size: 1.4rem;
  font-weight: 600;
}

.ai-info p {
  margin: 0 0 20px 0;
  color: #64748b;
  line-height: 1.6;
  font-size: 1rem;
}

.ai-metrics {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.metric {
  text-align: center;
  padding: 12px 16px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  min-width: 100px;
}

.metric-value {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 0.85rem;
  color: #64748b;
}

.ai-features,
.ai-benefits,
.ai-stats {
  margin-bottom: 32px;
}

.ai-features h4,
.ai-benefits h4,
.ai-stats h4 {
  margin: 0 0 16px 0;
  color: #1e293b;
  font-size: 1.2rem;
  font-weight: 600;
}

.ai-features ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.ai-features li {
  padding: 12px 16px;
  background: rgba(52, 211, 153, 0.1);
  border-radius: 8px;
  border-left: 4px solid #34d399;
  font-size: 0.95rem;
  color: #374151;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.benefit-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(16, 185, 129, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.benefit-icon {
  width: 32px;
  height: 32px;
  background: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 4px;
}

.benefit-content h5 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
}

.benefit-content p {
  margin: 0;
  color: #64748b;
  line-height: 1.5;
  font-size: 0.95rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border-radius: 12px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #6366f1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

/* Responsive AI Details Dialog */
@media (max-width: 1024px) {
  .ai-details-dialog {
    width: 85% !important;
  }
  
  .ai-overview {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .ai-metrics {
    justify-content: center;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .ai-details-dialog {
    width: 95% !important;
    margin: 20px;
  }
  
  .ai-details-content {
    padding: 16px;
  }
  
  .ai-icon-large {
    width: 60px;
    height: 60px;
    font-size: 24px;
  }
  
  .ai-info h3 {
    font-size: 1.2rem;
  }
  
  .ai-metrics {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .ai-features ul {
    grid-template-columns: 1fr;
  }
  
  .benefit-item {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dialog-footer {
    flex-direction: column;
    gap: 8px;
  }
  
  .dialog-footer .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .ai-details-dialog .el-dialog__header {
    padding: 16px;
  }
  
  .ai-details-dialog .el-dialog__title {
    font-size: 1.2rem;
  }
  
  .ai-details-content {
    padding: 12px;
  }
  
  .ai-overview {
    gap: 16px;
    margin-bottom: 24px;
  }
  
  .ai-icon-large {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .metric {
    padding: 8px 12px;
    min-width: 80px;
  }
  
  .metric-value {
    font-size: 1rem;
  }
  
  .ai-features,
  .ai-benefits,
  .ai-stats {
    margin-bottom: 20px;
  }
  
  .ai-features h4,
  .ai-benefits h4,
  .ai-stats h4 {
    font-size: 1.1rem;
    margin-bottom: 12px;
  }
  
  .benefit-item {
    flex-direction: column;
    text-align: center;
    padding: 12px;
  }
  
  .stat-item {
    padding: 16px;
  }
  
  .stat-value {
    font-size: 1.2rem;
  }
}

/* Quantum Analytics Styles */
.quantum-analytics-section {
  margin-bottom: 48px;
  padding: 32px;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  border-radius: 24px;
  border: 2px solid rgba(139, 92, 246, 0.3);
  position: relative;
  overflow: hidden;
}

.quantum-analytics-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(167, 139, 250, 0.2) 0%, transparent 50%);
  animation: quantumPulse 4s ease-in-out infinite;
}

@keyframes quantumPulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.quantum-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  position: relative;
  z-index: 1;
}

.quantum-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.quantum-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
}

.quantum-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.quantum-icon {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.quantum-orb {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  animation: orbRotate 3s linear infinite;
}

@keyframes orbRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.quantum-title h3 {
  color: white;
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 700;
}

.quantum-title p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 14px;
}

.quantum-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #10b981;
  font-size: 12px;
  font-weight: 600;
}

.quantum-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: indicatorPulse 2s infinite;
}

@keyframes indicatorPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.prediction-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.prediction-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  position: relative;
}

.prediction-time {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  margin-bottom: 4px;
}

.prediction-blood-type {
  color: white;
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 4px;
}

.prediction-amount {
  color: white;
  font-size: 14px;
  margin-bottom: 8px;
}

.prediction-amount.high {
  color: #ef4444;
}

.prediction-amount.medium {
  color: #f59e0b;
}

.prediction-amount.low {
  color: #10b981;
}

.prediction-confidence {
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin-bottom: 4px;
}

.prediction-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 11px;
}

/* Neural Network Styles */
.neural-network {
  position: relative;
  width: 60px;
  height: 60px;
}

.neural-node {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: nodePulse 2s infinite;
}

@keyframes nodePulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.5; }
}

.neural-connection {
  position: absolute;
  width: 2px;
  height: 20px;
  background: linear-gradient(180deg, transparent, #10b981, transparent);
  animation: connectionFlow 1.5s infinite;
}

@keyframes connectionFlow {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

.neural-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.neural-metric {
  text-align: center;
}

.neural-metric .metric-value {
  color: #10b981;
  font-size: 20px;
  font-weight: 800;
  display: block;
  margin-bottom: 4px;
}

.neural-metric .metric-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.neural-patterns {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pattern-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.pattern-icon {
  font-size: 16px;
}

.pattern-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
}

/* Holographic Styles */
.hologram {
  position: relative;
  width: 60px;
  height: 60px;
  transform-style: preserve-3d;
  animation: holoRotate 4s linear infinite;
}

@keyframes holoRotate {
  from { transform: rotateY(0deg); }
  to { transform: rotateY(360deg); }
}

.holo-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid;
  border-radius: 50%;
  opacity: 0.6;
}

.layer-1 {
  border-color: #3b82f6;
  transform: rotateX(0deg);
}

.layer-2 {
  border-color: #8b5cf6;
  transform: rotateX(60deg);
}

.layer-3 {
  border-color: #ec4899;
  transform: rotateX(120deg);
}

.blood-stream {
  position: relative;
  height: 120px;
  margin-bottom: 16px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.02);
  overflow: hidden;
}

.stream-particle {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--blood-color);
  animation: streamFlow 3s linear infinite;
}

@keyframes streamFlow {
  from { transform: translateX(-10px); }
  to { transform: translateX(100%); }
}

.particle-core {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: inherit;
  box-shadow: 0 0 10px var(--blood-color);
}

/* Blockchain Styles */
.blockchain-section {
  margin-bottom: 48px;
  padding: 32px;
  background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
  border-radius: 24px;
  border: 2px solid rgba(16, 185, 129, 0.3);
}

.blockchain-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.blockchain-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.blockchain-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);
}

.blockchain-visual {
  display: flex;
  align-items: center;
  gap: 8px;
}

.block {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 10px;
  font-weight: 700;
  animation: blockAppear 0.5s ease-out;
}

@keyframes blockAppear {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.chain-link {
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.5);
  position: relative;
}

.chain-link::after {
  content: '';
  position: absolute;
  right: -4px;
  top: -3px;
  width: 0;
  height: 0;
  border-left: 6px solid rgba(255, 255, 255, 0.5);
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
}

.chain-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.chain-stat {
  text-align: center;
}

.chain-stat .stat-value {
  color: #10b981;
  font-size: 20px;
  font-weight: 800;
  display: block;
  margin-bottom: 4px;
}

.chain-stat .stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.recent-transactions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.transaction-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-size: 12px;
}

.tx-hash {
  color: #10b981;
  font-family: monospace;
}

.tx-type {
  color: rgba(255, 255, 255, 0.9);
}

.tx-amount {
  color: white;
  font-weight: 600;
}

.tx-status {
  text-align: right;
}

.tx-status.confirmed {
  color: #10b981;
}

.tx-status.pending {
  color: #f59e0b;
}

/* NFT Styles */
.nft-badge {
  position: relative;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.badge-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
  animation: badgeShine 3s infinite;
}

@keyframes badgeShine {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.nft-gallery {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.nft-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.nft-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
}

.nft-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 50%, rgba(0,0,0,0.7) 100%);
  display: flex;
  align-items: flex-end;
  padding: 4px;
}

.nft-rarity {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.nft-rarity.legendary {
  background: #f59e0b;
  color: white;
}

.nft-rarity.epic {
  background: #8b5cf6;
  color: white;
}

.nft-rarity.rare {
  background: #3b82f6;
  color: white;
}

.nft-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.nft-name {
  color: white;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 2px;
}

.nft-donor {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  margin-bottom: 2px;
}

.nft-value {
  color: #10b981;
  font-size: 12px;
  font-weight: 600;
}

/* Metaverse Styles */
.metaverse-section {
  margin-bottom: 48px;
  padding: 32px;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border-radius: 24px;
  border: 2px solid rgba(59, 130, 246, 0.3);
}

.metaverse-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.metaverse-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.metaverse-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
}

/* VR Styles */
.vr-preview {
  position: relative;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 12px;
  overflow: hidden;
}

.vr-room {
  position: relative;
  width: 100%;
  height: 100%;
}

.vr-equipment {
  position: absolute;
  color: white;
  font-size: 12px;
  animation: vrFloat 3s ease-in-out infinite;
}

@keyframes vrFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}

.vr-features {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.vr-feature {
  text-align: center;
}

.feature-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.feature-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 11px;
}

.vr-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.vr-stat {
  text-align: center;
}

.vr-stat .stat-value {
  color: #3b82f6;
  font-size: 18px;
  font-weight: 800;
  display: block;
  margin-bottom: 4px;
}

.vr-stat .stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 11px;
}

/* AR Styles */
.ar-viewfinder {
  position: relative;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
  border-radius: 12px;
  overflow: hidden;
}

.viewfinder-frame {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 4px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 10px;
  right: 10px;
  height: 2px;
  background: #10b981;
  animation: scanMove 2s linear infinite;
}

@keyframes scanMove {
  0% { top: 10px; }
  50% { top: 48px; }
  100% { top: 10px; }
}

.scan-points {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.scan-point {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #10b981;
  border-radius: 50%;
}

.scan-point:nth-child(1) { top: 10px; left: 10px; }
.scan-point:nth-child(2) { top: 10px; right: 10px; }
.scan-point:nth-child(3) { bottom: 10px; left: 10px; }
.scan-point:nth-child(4) { bottom: 10px; right: 10px; }

.ar-capabilities {
  display: flex;
  justify-content: space-around;
  margin-bottom: 16px;
}

.cap-icon {
  font-size: 18px;
  margin-bottom: 4px;
}

.cap-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 11px;
  text-align: center;
}

/* Digital Twin Styles */
.twin-visualization {
  position: relative;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 12px;
  overflow: hidden;
}

.twin-body {
  position: relative;
  width: 100%;
  height: 100%;
}

.twin-organ {
  position: absolute;
  width: 16px;
  height: 16px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.twin-organ:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.2);
}

.twin-organ.heart {
  top: 20px;
  left: 22px;
}

.twin-organ.lungs {
  top: 10px;
  left: 10px;
}

.twin-organ.liver {
  top: 35px;
  left: 35px;
}

.blood-flow {
  position: absolute;
  width: 2px;
  height: 8px;
  background: #ef4444;
  border-radius: 1px;
  animation: bloodFlow 1s linear infinite;
}

@keyframes bloodFlow {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

.twin-controls {
  margin-bottom: 16px;
}

.twin-results {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.result-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.result-value {
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.result-value.low {
  color: #10b981;
}
</style>
