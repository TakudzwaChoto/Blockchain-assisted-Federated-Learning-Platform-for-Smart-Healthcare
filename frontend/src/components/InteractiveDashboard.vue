



<template>
  <div class="interactive-dashboard">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-title">
          <h1>{{ dashboardTitle }}</h1>
          <p class="header-subtitle">Last updated: {{ lastUpdated }}</p>
        </div>
        <div class="header-actions">
          <el-button-group>
            <el-button @click="refreshDashboard" :loading="refreshing">
              <el-icon><Refresh /></el-icon>
              Refresh
            </el-button>
            <el-button @click="toggleFullscreen">
              <el-icon><FullScreen /></el-icon>
              Fullscreen
            </el-button>
            <el-button @click="shareDashboard">
              <el-icon><Share /></el-icon>
              Share
            </el-button>
          </el-button-group>
          <el-dropdown @command="handleLayoutCommand" trigger="click">
            <el-button>
              <el-icon><Grid /></el-icon>
              Layout
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="grid">Grid Layout</el-dropdown-item>
                <el-dropdown-item command="tabs">Tab Layout</el-dropdown-item>
                <el-dropdown-item command="accordion">Accordion Layout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- Global Filters Bar -->
    <div class="global-filters">
      <el-card class="filter-card">
        <div class="filter-content">
          <div class="filter-row">
            <div class="filter-item">
              <label>Date Range:</label>
              <el-date-picker
                v-model="globalFilters.dateRange"
                type="daterange"
                range-separator="To"
                start-placeholder="Start date"
                end-placeholder="End date"
                size="small"
                @change="applyFilters"
              />
            </div>
            <div class="filter-item">
              <label>Blood Type:</label>
              <el-select
                v-model="globalFilters.bloodTypes"
                multiple
                placeholder="All types"
                size="small"
                @change="applyFilters"
              >
                <el-option
                  v-for="type in bloodTypes"
                  :key="type"
                  :label="type"
                  :value="type"
                />
              </el-select>
            </div>
            <div class="filter-item">
              <label>Location:</label>
              <el-input
                v-model="globalFilters.location"
                placeholder="Filter by location"
                size="small"
                clearable
                @change="applyFilters"
              />
            </div>
            <div class="filter-actions">
              <el-button size="small" @click="resetFilters">Reset</el-button>
              <el-button size="small" type="primary" @click="saveFilters">Save</el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- KPI Overview -->
    <div class="kpi-overview">
      <el-row :gutter="16">
        <el-col :span="6" v-for="kpi in kpiData" :key="kpi.id">
          <div class="kpi-card" :class="`kpi-${kpi.trend}`" @click="drillDownToKPI(kpi)">
            <div class="kpi-header">
              <div class="kpi-icon" :style="{ backgroundColor: kpi.color }">
                <el-icon>
                  <component :is="kpi.icon" />
                </el-icon>
              </div>
              <div class="kpi-trend">
                <el-icon v-if="kpi.trend === 'up'"><TrendCharts /></el-icon>
                <el-icon v-else-if="kpi.trend === 'down'"><TrendCharts /></el-icon>
                <span>{{ kpi.change }}</span>
              </div>
            </div>
            <div class="kpi-content">
              <div class="kpi-value">{{ kpi.value }}</div>
              <div class="kpi-label">{{ kpi.label }}</div>
              <div class="kpi-subtitle">{{ kpi.subtitle }}</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- Main Dashboard Content -->
    <div class="dashboard-content" :class="`layout-${layoutType}`">
      <!-- Grid Layout -->
      <template v-if="layoutType === 'grid'">
        <el-row :gutter="16">
          <el-col :span="12" v-for="widget in widgets" :key="widget.id">
            <el-card class="widget-card" :class="`widget-${widget.type}`">
              <template #header>
                <div class="widget-header">
                  <span>{{ widget.title }}</span>
                  <div class="widget-actions">
                    <el-button size="small" @click="refreshWidget(widget)">
                      <el-icon><Refresh /></el-icon>
                    </el-button>
                    <el-button size="small" @click="maximizeWidget(widget)">
                      <el-icon><FullScreen /></el-icon>
                    </el-button>
                    <el-dropdown @command="handleWidgetCommand" trigger="click">
                      <el-button size="small">
                        <el-icon><MoreFilled /></el-icon>
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item :command="{action: 'export', widget}">Export</el-dropdown-item>
                          <el-dropdown-item :command="{action: 'drill', widget}">Drill Down</el-dropdown-item>
                          <el-dropdown-item :command="{action: 'config', widget}">Configure</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </div>
              </template>
              <div class="widget-content">
                <component
                  :is="getWidgetComponent(widget.type)"
                  :data="widget.data"
                  :config="widget.config"
                  @drill-down="handleWidgetDrillDown"
                />
              </div>
            </el-card>
          </el-col>
        </el-row>
      </template>

      <!-- Tab Layout -->
      <template v-else-if="layoutType === 'tabs'">
        <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
          <el-tab-pane
            v-for="tab in tabs"
            :key="tab.id"
            :label="tab.title"
            :name="tab.id"
          >
            <div class="tab-content">
              <el-row :gutter="16">
                <el-col :span="12" v-for="widget in tab.widgets" :key="widget.id">
                  <el-card class="widget-card">
                    <template #header>
                      <div class="widget-header">
                        <span>{{ widget.title }}</span>
                        <el-button size="small" @click="refreshWidget(widget)">
                          <el-icon><Refresh /></el-icon>
                        </el-button>
                      </div>
                    </template>
                    <div class="widget-content">
                      <component
                        :is="getWidgetComponent(widget.type)"
                        :data="widget.data"
                        :config="widget.config"
                      />
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
        </el-tabs>
      </template>

      <!-- Accordion Layout -->
      <template v-else-if="layoutType === 'accordion'">
        <el-collapse v-model="activeAccordion" @change="handleAccordionChange">
          <el-collapse-item
            v-for="section in sections"
            :key="section.id"
            :title="section.title"
            :name="section.id"
          >
            <div class="accordion-content">
              <el-row :gutter="16">
                <el-col :span="12" v-for="widget in section.widgets" :key="widget.id">
                  <el-card class="widget-card">
                    <template #header>
                      <div class="widget-header">
                        <span>{{ widget.title }}</span>
                        <el-button size="small" @click="refreshWidget(widget)">
                          <el-icon><Refresh /></el-icon>
                        </el-button>
                      </div>
                    </template>
                    <div class="widget-content">
                      <component
                        :is="getWidgetComponent(widget.type)"
                        :data="widget.data"
                        :config="widget.config"
                      />
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>
        </el-collapse>
      </template>
    </div>

    <!-- Drill Down Panel -->
    <DrillDownPanel
      ref="drillDownPanel"
      @drill-down="handleDrillDownEvent"
      @export="handleDrillDownExport"
    />

    <!-- Real-time Updates -->
    <RealTimeUpdates
      v-if="showRealTime"
      @data-refreshed="handleRealTimeUpdate"
      @alert-selected="handleAlertSelected"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import {
  Refresh,
  FullScreen,
  Share,
  Grid,
  ArrowDown,
  TrendCharts,
  MoreFilled,
  DataAnalysis,
  User,
  Document,
  Setting
} from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'
import DrillDownPanel from './DrillDownPanel.vue'
import RealTimeUpdates from './RealTimeUpdates.vue'

const emit = defineEmits(['widget-drill-down', 'export', 'filter-change'])

const notificationStore = useNotificationStore()

// Dashboard state
const dashboardTitle = ref('Blood Domain Analytics Dashboard')
const lastUpdated = ref(new Date().toLocaleString())
const refreshing = ref(false)
const layoutType = ref('grid')
const activeTab = ref('overview')
const activeAccordion = ref(['overview'])
const showRealTime = ref(false)

// Global filters
const globalFilters = reactive({
  dateRange: null,
  bloodTypes: [],
  location: ''
})

// Blood types for filter
const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

// KPI Data
const kpiData = ref([
  {
    id: 'total-donations',
    label: 'Total Donations',
    value: '1,234',
    subtitle: 'This month',
    change: '+12%',
    trend: 'up',
    icon: 'Document',
    color: '#409eff'
  },
  {
    id: 'active-donors',
    label: 'Active Donors',
    value: '892',
    subtitle: 'Registered',
    change: '+5%',
    trend: 'up',
    icon: 'User',
    color: '#67c23a'
  },
  {
    id: 'processing-rate',
    label: 'Processing Rate',
    value: '98.5%',
    subtitle: 'Success rate',
    change: '+0.3%',
    trend: 'up',
    icon: 'DataAnalysis',
    color: '#e6a23c'
  },
  {
    id: 'error-rate',
    label: 'Error Rate',
    value: '0.2%',
    subtitle: 'Last 24h',
    change: '-0.1%',
    trend: 'down',
    icon: 'Setting',
    color: '#f56c6c'
  }
])

// Widgets data
const widgets = ref([
  {
    id: 'donations-chart',
    title: 'Donations Trend',
    type: 'chart',
    data: generateChartData(),
    config: { chartType: 'line' }
  },
  {
    id: 'blood-type-distribution',
    title: 'Blood Type Distribution',
    type: 'chart',
    data: generateBloodTypeData(),
    config: { chartType: 'pie' }
  },
  {
    id: 'recent-donations',
    title: 'Recent Donations',
    type: 'table',
    data: generateTableData(),
    config: { pageSize: 10 }
  },
  {
    id: 'quality-metrics',
    title: 'Data Quality',
    type: 'kpi',
    data: generateQualityData(),
    config: {}
  }
])

// Tabs data
const tabs = ref([
  {
    id: 'overview',
    title: 'Overview',
    widgets: widgets.value.slice(0, 2)
  },
  {
    id: 'analytics',
    title: 'Analytics',
    widgets: widgets.value.slice(2, 4)
  }
])

// Sections data
const sections = ref([
  {
    id: 'donations',
    title: 'Donation Analytics',
    widgets: widgets.value.slice(0, 2)
  },
  {
    id: 'quality',
    title: 'Data Quality',
    widgets: widgets.value.slice(2, 4)
  }
])

// Refs
const drillDownPanel = ref(null)

// Methods
const refreshDashboard = async () => {
  refreshing.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    lastUpdated.value = new Date().toLocaleString()
    notificationStore.success('Dashboard refreshed successfully')
  } catch (error) {
    notificationStore.error('Failed to refresh dashboard')
  } finally {
    refreshing.value = false
  }
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

const shareDashboard = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url)
  notificationStore.success('Dashboard URL copied to clipboard')
}

const handleLayoutCommand = (command) => {
  layoutType.value = command
  notificationStore.info(`Switched to ${command} layout`)
}

const applyFilters = () => {
  emit('filter-change', globalFilters)
  notificationStore.success('Filters applied')
}

const resetFilters = () => {
  globalFilters.dateRange = null
  globalFilters.bloodTypes = []
  globalFilters.location = ''
  applyFilters()
}

const saveFilters = () => {
  localStorage.setItem('dashboard-filters', JSON.stringify(globalFilters))
  notificationStore.success('Filters saved')
}

const drillDownToKPI = (kpi) => {
  drillDownPanel.value?.open(generateDrillDownData(kpi.id))
  notificationStore.info(`Drilling down into ${kpi.label}`)
}

const refreshWidget = (widget) => {
  widget.data = generateWidgetData(widget.type)
  notificationStore.success(`${widget.title} refreshed`)
}

const maximizeWidget = (widget) => {
  // Implementation for widget maximization
  notificationStore.info(`Maximizing ${widget.title}`)
}

const handleWidgetCommand = ({ action, widget }) => {
  switch (action) {
    case 'export':
      emit('export', { widget, data: widget.data })
      break
    case 'drill':
      drillDownPanel.value?.open(widget.data)
      break
    case 'config':
      notificationStore.info(`Configure ${widget.title}`)
      break
  }
}

const handleWidgetDrillDown = (data) => {
  drillDownPanel.value?.open(data)
}

const handleTabClick = (tab) => {
  notificationStore.info(`Switched to ${tab.props.label}`)
}

const handleAccordionChange = (activeNames) => {
  notificationStore.info(`Accordion sections changed`)
}

const handleDrillDownEvent = (data) => {
  emit('widget-drill-down', data)
}

const handleDrillDownExport = (data) => {
  emit('export', data)
}

const handleRealTimeUpdate = () => {
  lastUpdated.value = new Date().toLocaleString()
}

const handleAlertSelected = (alert) => {
  notificationStore.warning(`Alert selected: ${alert.title}`)
}

// Helper functions
const getWidgetComponent = (type) => {
  const components = {
    chart: 'TrendCharts',
    table: 'el-table',
    kpi: 'kpi-cards'
  }
  return components[type] || 'div'
}

const generateChartData = () => {
  return {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Donations',
      data: [120, 190, 300, 500, 200, 300]
    }]
  }
}

const generateBloodTypeData = () => {
  return {
    labels: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    datasets: [{
      data: [30, 15, 25, 10, 5, 8, 35, 12]
    }]
  }
}

const generateTableData = () => {
  return Array.from({ length: 10 }, (_, i) => ({
    id: i + 1,
    donor: `Donor ${i + 1}`,
    bloodType: bloodTypes[i % bloodTypes.length],
    date: new Date(Date.now() - i * 86400000).toLocaleDateString(),
    volume: 450 + Math.floor(Math.random() * 100)
  }))
}

const generateQualityData = () => {
  return [
    { label: 'Completeness', value: 95 },
    { label: 'Accuracy', value: 98 },
    { label: 'Consistency', value: 92 }
  ]
}

const generateWidgetData = (type) => {
  switch (type) {
    case 'chart':
      return generateChartData()
    case 'table':
      return generateTableData()
    case 'kpi':
      return generateQualityData()
    default:
      return {}
  }
}

const generateDrillDownData = (kpiId) => {
  return Array.from({ length: 50 }, (_, i) => ({
    id: i + 1,
    donor: `Donor ${i + 1}`,
    bloodType: bloodTypes[i % bloodTypes.length],
    date: new Date(Date.now() - i * 86400000).toLocaleDateString(),
    volume: 450 + Math.floor(Math.random() * 100),
    location: `Location ${i % 5 + 1}`
  }))
}

onMounted(() => {
  // Load saved filters
  const savedFilters = localStorage.getItem('dashboard-filters')
  if (savedFilters) {
    Object.assign(globalFilters, JSON.parse(savedFilters))
  }
})
</script>

<style scoped>
.interactive-dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.dashboard-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-title h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header-subtitle {
  margin: 4px 0 0 0;
  opacity: 0.8;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.global-filters {
  padding: 16px 24px;
  background-color: white;
  border-bottom: 1px solid #e4e7ed;
}

.filter-card {
  margin: 0;
}

.filter-content {
  max-width: 1400px;
  margin: 0 auto;
}

.filter-row {
  display: flex;
  gap: 24px;
  align-items: end;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-item label {
  font-size: 12px;
  font-weight: 500;
  color: #606266;
}

.filter-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.kpi-overview {
  padding: 16px 24px;
}

.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #409eff 0%, #66b1ff 100%);
}

.kpi-up::before {
  background: linear-gradient(90deg, #67c23a 0%, #85ce61 100%);
}

.kpi-down::before {
  background: linear-gradient(90deg, #f56c6c 0%, #f78989 100%);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.kpi-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.kpi-up .kpi-trend {
  color: #67c23a;
}

.kpi-down .kpi-trend {
  color: #f56c6c;
}

.kpi-content {
  text-align: center;
}

.kpi-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.kpi-label {
  font-size: 14px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 4px;
}

.kpi-subtitle {
  font-size: 12px;
  color: #909399;
}

.dashboard-content {
  flex: 1;
  padding: 16px 24px;
  overflow-y: auto;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.widget-card {
  margin-bottom: 16px;
  height: 400px;
}

.widget-card :deep(.el-card__body) {
  height: calc(100% - 57px);
  padding: 16px;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.widget-actions {
  display: flex;
  gap: 4px;
}

.widget-content {
  height: 100%;
}

.layout-tabs .tab-content {
  padding: 16px 0;
}

.layout-accordion .accordion-content {
  padding: 16px 0;
}

@media (max-width: 1200px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .filter-actions {
    margin-left: 0;
  }
  
  .kpi-overview .el-col {
    margin-bottom: 16px;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 12px 16px;
  }
  
  .header-title h1 {
    font-size: 20px;
  }
  
  .global-filters,
  .kpi-overview,
  .dashboard-content {
    padding: 12px 16px;
  }
  
  .kpi-overview .el-col {
    margin-bottom: 12px;
  }
  
  .widget-card {
    height: 350px;
  }
  
  .header-actions {
    flex-wrap: wrap;
  }
}
</style>
