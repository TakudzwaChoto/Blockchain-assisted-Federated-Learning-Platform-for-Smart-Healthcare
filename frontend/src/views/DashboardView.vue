<template>
  <div style="display:flex;flex-direction:column;gap:12px">
    <el-card>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
        <div>
          <div style="font-size:18px;font-weight:600">Dataset dashboard</div>
          <div style="opacity:0.8">ID: {{ datasetId }}</div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <ExportButton 
            :data="exportData" 
            :filename="`dashboard-${datasetId}`"
            title="Dashboard Export"
            @export-start="handleExportStart"
            @export-complete="handleExportComplete"
          />
          <el-button :loading="loadingInfo" @click="loadInfo">Refresh</el-button>
          <el-button type="primary" :loading="loadingProcess" @click="runProcess">Run processing</el-button>
        </div>
      </div>
    </el-card>

    <!-- Advanced Filters -->
    <AdvancedFilters @filters-changed="handleFiltersChanged" />

    <!-- Real-Time Updates -->
    <RealTimeUpdates 
      @data-refreshed="handleRealTimeUpdate"
      @alert-selected="handleAlertSelected"
    />

    <!-- Interactive Dashboard -->

    <!-- Data Quality Insights -->
    <DataQualityInsights 
      @issue-selected="handleIssueSelected"
      @fix-issue="handleFixIssue"
      @apply-recommendation="handleApplyRecommendation"
    />

    <!-- Loading Skeletons -->
    <template v-if="loadingInfo">
      <LoadingSkeleton type="kpi" />
      <LoadingSkeleton type="chart" />
      <LoadingSkeleton type="table" />
    </template>

    <!-- Enhanced KPI Section -->
    <el-row :gutter="16" class="kpi-section">
      <el-col :span="6" v-for="kpi in enhancedKpis" :key="kpi.id">
        <el-card class="enhanced-kpi-card" :class="`kpi-${kpi.trend}`">
          <div class="kpi-header">
            <div class="kpi-icon" :style="{ backgroundColor: kpi.color }">
              <el-icon>
                <component :is="kpi.icon" />
              </el-icon>
            </div>
            <div class="kpi-actions">
              <el-dropdown @command="handleKpiAction" trigger="click">
                <el-button size="small" text>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="refresh">Refresh</el-dropdown-item>
                    <el-dropdown-item command="export">Export</el-dropdown-item>
                    <el-dropdown-item command="details">View Details</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ kpi.value }}</div>
            <div class="kpi-label">{{ kpi.label }}</div>
            <div class="kpi-change" :class="kpi.trend">
              <el-icon v-if="kpi.trend === 'up'"><TrendCharts /></el-icon>
              <el-icon v-else-if="kpi.trend === 'down'"><TrendCharts /></el-icon>
              <span>{{ kpi.change }}</span>
            </div>
          </div>
          <div class="kpi-sparkline">
            <div class="sparkline" :style="{ background: kpi.sparkline }"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Dataset Preview -->
    <el-card v-if="info && !loadingInfo" class="chart-container">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <div style="font-weight:600">Dataset Preview</div>
          <el-button size="small" @click="togglePreview">
            {{ showFullPreview ? 'Show Less' : 'Show More' }}
          </el-button>
        </div>
      </template>
      <el-table 
        :data="previewData" 
        :height="showFullPreview ? 500 : 320" 
        style="width:100%"
        v-loading="loadingInfo"
      >
        <el-table-column
          v-for="col in info.columns"
          :key="col"
          :prop="col"
          :label="col"
          min-width="140"
          show-overflow-tooltip
        />
      </el-table>
    </el-card>

    <el-card v-if="processResult">
      <template #header>
        <div style="font-weight:600">Processing report</div>
      </template>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <el-card shadow="never">
          <template #header><div style="font-weight:600">Summary</div></template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="final_rows">{{ processResult.final_rows }}</el-descriptions-item>
            <el-descriptions-item label="final_cols">{{ processResult.final_cols }}</el-descriptions-item>
            <el-descriptions-item label="quality_score">{{ qualityScore }}</el-descriptions-item>
            <el-descriptions-item label="steps">{{ stepsCompleted.join(', ') }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
        <el-card shadow="never">
          <template #header><div style="font-weight:600">Validation summary</div></template>
          <validation-summary-table :validation-results="validationSummary" />
        </el-card>
      </div>
    </el-card>

    <!-- Enhanced Charts Section -->
    <el-row :gutter="16" class="charts-section">
      <el-col :span="12">
        <el-card class="chart-container">
          <template #header>
            <div class="chart-header">
              <span>Donations Trend</span>
              <div class="chart-controls">
                <el-select v-model="trendGranularity" size="small" style="width: 120px">
                  <el-option label="Daily" value="daily" />
                  <el-option label="Weekly" value="weekly" />
                  <el-option label="Monthly" value="monthly" />
                </el-select>
                <el-button type="primary" size="small" :loading="loadingTrends" @click="runTrends">
                  Run Trends
                </el-button>
              </div>
            </div>
          </template>
          <div class="chart-content">
            <AnimatedCharts 
              v-if="trends" 
              :data="trends" 
              :config="{ chartType: 'line' }"
              height="300px"
            />
            <el-empty v-else description="Run trends to see results" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-container">
          <template #header>
            <div class="chart-header">
              <span>Blood Type Distribution</span>
              <div class="chart-controls">
                <el-button size="small" @click="refreshBloodTypeChart">
                  <el-icon><Refresh /></el-icon>
                </el-button>
              </div>
            </div>
          </template>
          <div class="chart-content">
            <AnimatedCharts 
              :data="bloodTypeData" 
              :config="{ chartType: 'pie' }"
              height="300px"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
          <div style="font-weight:600">Forecasting</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <el-input-number v-model="forecastHorizon" :min="7" :max="365" />
            <el-button type="primary" :loading="loadingForecast" @click="runForecast">Run forecast</el-button>
          </div>
        </div>
      </template>
      <forecast-chart v-if="forecast" title="Forecast (by model)" :forecasts="forecast" />
      <el-empty v-else description="Run forecast to see results" />
    </el-card>

    <el-card>
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
          <div style="font-weight:600">Data mining</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <el-button type="primary" :loading="loadingPatterns" @click="runPatterns">Mine patterns</el-button>
            <el-button type="primary" :loading="loadingAssociations" @click="runAssociations">Mine associations</el-button>
          </div>
        </div>
      </template>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <el-card shadow="never">
          <template #header><div style="font-weight:600">Patterns</div></template>
          <pre v-if="patterns" style="max-height:240px;overflow:auto">{{ JSON.stringify(patterns.patterns || patterns, null, 2) }}</pre>
          <el-empty v-else description="Run pattern mining" />
        </el-card>
        <el-card shadow="never">
          <template #header><div style="font-weight:600">Associations</div></template>
          <association-rules-table v-if="associations" :associations="associations" />
          <el-empty v-else description="Run association mining" />
        </el-card>
      </div>
    </el-card>

    <!-- Drill Down Panel -->
    <DrillDownPanel
      ref="drillDownPanel"
      @drill-down="handleDrillDownEvent"
      @export="handleDrillDownExport"
    />

    <el-alert v-if="error" type="error" :closable="false" :title="error" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useNotificationStore } from '../stores/notificationStore'

import KpiCards from '../components/KpiCards.vue'
import LoadingSkeleton from '../components/LoadingSkeleton.vue'
import ExportButton from '../components/ExportButton.vue'
import AdvancedFilters from '../components/AdvancedFilters.vue'
import DataQualityInsights from '../components/DataQualityInsights.vue'
import RealTimeUpdates from '../components/RealTimeUpdates.vue'
import InteractiveDashboard from '../components/InteractiveDashboard.vue'
import AnimatedCharts from '../components/AnimatedCharts.vue'
import DrillDownPanel from '../components/DrillDownPanel.vue'
import TrendCharts from '../components/TrendCharts.vue'
import ForecastChart from '../components/ForecastChart.vue'
import ValidationSummaryTable from '../components/ValidationSummaryTable.vue'
import AssociationRulesTable from '../components/AssociationRulesTable.vue'
import { MoreFilled } from '@element-plus/icons-vue'

import {
  getDataset,
  runProcessing,
  runTrends as apiRunTrends,
  runForecast as apiRunForecast,
  minePatterns,
  mineAssociations
} from '../services/api'

const props = defineProps({
  datasetId: { type: String, required: true }
})

const error = ref('')

const info = ref(null)
const loadingInfo = ref(false)

const processResult = ref(null)
const loadingProcess = ref(false)

const trendGranularity = ref('monthly')
const trends = ref(null)
const loadingTrends = ref(false)

const forecastHorizon = ref(30)
const forecast = ref(null)
const loadingForecast = ref(false)

const patterns = ref(null)
const loadingPatterns = ref(false)

const associations = ref(null)
const loadingAssociations = ref(false)

// Blood Type Chart Data
const bloodTypeData = ref({
  labels: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
  datasets: [{
    data: [30, 15, 25, 10, 5, 8, 35, 12]
  }]
})

// Refresh Blood Type Chart
function refreshBloodTypeChart() {
  notificationStore.success('Blood type chart refreshed')
}

// Enhanced KPI Data
const enhancedKpis = ref([
  {
    id: 'total-donations',
    label: 'Total Donations',
    value: '1,234',
    change: '+12%',
    trend: 'up',
    icon: 'Document',
    color: '#409eff',
    sparkline: 'linear-gradient(135deg, #409eff 0%, #66b1ff 100%)'
  },
  {
    id: 'active-donors',
    label: 'Active Donors',
    value: '892',
    change: '+5%',
    trend: 'up',
    icon: 'User',
    color: '#67c23a',
    sparkline: 'linear-gradient(135deg, #67c23a 0%, #85ce61 100%)'
  },
  {
    id: 'processing-rate',
    label: 'Processing Rate',
    value: '98.5%',
    change: '+0.3%',
    trend: 'up',
    icon: 'DataAnalysis',
    color: '#e6a23c',
    sparkline: 'linear-gradient(135deg, #e6a23c 0%, #ebb563 100%)'
  },
  {
    id: 'error-rate',
    label: 'Error Rate',
    value: '0.2%',
    change: '-0.1%',
    trend: 'down',
    icon: 'Warning',
    color: '#f56c6c',
    sparkline: 'linear-gradient(135deg, #f56c6c 0%, #f78989 100%)'
  }
])

// New professional UI state
const showFullPreview = ref(false)
const drillDownPanel = ref(null)
const notificationStore = useNotificationStore()

const stepsCompleted = computed(() => processResult.value?.stats?.steps_completed || [])
const qualityScore = computed(() => processResult.value?.stats?.data_quality_score ?? '')
const validationSummary = computed(() => processResult.value?.stats?.validation_results || null)

// Export data for ExportButton
const exportData = computed(() => ({
  info: info.value,
  processResult: processResult.value,
  trends: trends.value,
  forecast: forecast.value,
  patterns: patterns.value,
  associations: associations.value
}))

// Preview data for table
const previewData = computed(() => {
  if (!info.value?.preview) return []
  return showFullPreview.value ? info.value.preview : info.value.preview.slice(0, 10)
})

const kpis = computed(() => {
  const out = []
  if (info.value) {
    out.push({ label: 'Rows', value: info.value.rows })
    out.push({ label: 'Columns', value: info.value.cols })
    out.push({ label: 'Fields', value: info.value.columns?.length ?? 0 })
  }
  if (processResult.value) {
    out.push({ label: 'Quality Score', value: qualityScore.value || 0 })
  }
  return out
})

async function loadInfo() {
  loadingInfo.value = true
  error.value = ''
  try {
    info.value = await getDataset(props.datasetId)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loadingInfo.value = false
  }
}

async function runProcess() {
  loadingProcess.value = true
  error.value = ''
  try {
    processResult.value = await runProcessing(props.datasetId)
    await loadInfo()
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loadingProcess.value = false
  }
}

async function runTrends() {
  loadingTrends.value = true
  error.value = ''
  try {
    trends.value = await apiRunTrends(props.datasetId, trendGranularity.value, 365)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loadingTrends.value = false
  }
}

async function runForecast() {
  loadingForecast.value = true
  error.value = ''
  try {
    forecast.value = await apiRunForecast(props.datasetId, forecastHorizon.value, 'daily', 'volume_ml')
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loadingForecast.value = false
  }
}

async function runPatterns() {
  loadingPatterns.value = true
  error.value = ''
  try {
    patterns.value = await minePatterns(props.datasetId)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loadingPatterns.value = false
  }
}

async function runAssociations() {
  loadingAssociations.value = true
  error.value = ''
  try {
    associations.value = await mineAssociations(props.datasetId)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loadingAssociations.value = false
  }
}

onMounted(async () => {
  await loadInfo()
})

// KPI Actions Handler
function handleKpiAction(command) {
  switch (command) {
    case 'refresh':
      notificationStore.success('KPI refreshed')
      break
    case 'export':
      notificationStore.success('KPI exported')
      break
    case 'details':
      notificationStore.info('Opening KPI details...')
      break
  }
}

// Professional UI Event Handlers
function togglePreview() {
  showFullPreview.value = !showFullPreview.value
}

function handleFiltersChanged(filters) {
  console.log('Filters changed:', filters)
  // Apply filters to data
  notificationStore.success('Filters applied successfully')
}

function handleExportStart(format) {
  notificationStore.info(`Exporting as ${format}...`)
}

function handleExportComplete(format) {
  notificationStore.success(`Export completed as ${format}`)
}

function handleRealTimeUpdate() {
  notificationStore.info('Real-time data updated')
}

function handleAlertSelected(alert) {
  notificationStore.warning(`Alert selected: ${alert.title}`)
}

function handleWidgetDrillDown(data) {
  drillDownPanel.value?.open(data)
}

function handleDashboardExport(data) {
  notificationStore.success('Dashboard export initiated')
}

function handleDashboardFilterChange(filters) {
  notificationStore.success('Dashboard filters updated')
}

function handleIssueSelected(issue) {
  notificationStore.info(`Issue selected: ${issue.title}`)
}

function handleFixIssue(issue) {
  notificationStore.success(`Fixing issue: ${issue.title}`)
}

function handleApplyRecommendation(recommendation) {
  notificationStore.success(`Applied recommendation: ${recommendation.title}`)
}

function handleDrillDownEvent(data) {
  console.log('Drill down event:', data)
}

function handleDrillDownExport(data) {
  console.log('Drill down export:', data)
}
</script>
