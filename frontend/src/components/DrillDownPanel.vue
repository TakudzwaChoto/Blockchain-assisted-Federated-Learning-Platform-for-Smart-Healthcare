<template>
  <el-drawer
    v-model="visible"
    :title="panelTitle"
    size="60%"
    direction="rtl"
    class="drill-down-panel"
  >
    <!-- Panel Header -->
    <div class="panel-header">
      <div class="breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item
            v-for="(crumb, index) in breadcrumbs"
            :key="index"
            @click="navigateToBreadcrumb(index)"
            class="breadcrumb-item"
          >
            {{ crumb.label }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <div class="panel-actions">
        <el-button size="small" @click="exportCurrentView">
          <el-icon><Download /></el-icon>
          Export
        </el-button>
        <el-button size="small" @click="resetDrillDown">
          <el-icon><RefreshLeft /></el-icon>
          Reset
        </el-button>
      </div>
    </div>

    <!-- Data Summary -->
    <div class="data-summary">
      <el-row :gutter="16">
        <el-col :span="6" v-for="summary in dataSummary" :key="summary.label">
          <div class="summary-card">
            <div class="summary-value">{{ summary.value }}</div>
            <div class="summary-label">{{ summary.label }}</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- Drill Down Content -->
    <div class="drill-down-content">
      <!-- Chart View -->
      <el-card v-if="viewType === 'chart'" class="chart-container">
        <template #header>
          <div class="view-header">
            <span>Chart View</span>
            <el-select v-model="chartType" size="small" style="width: 120px">
              <el-option label="Bar" value="bar" />
              <el-option label="Line" value="line" />
              <el-option label="Pie" value="pie" />
              <el-option label="Scatter" value="scatter" />
            </el-select>
          </div>
        </template>
        <div class="chart-wrapper">
          <v-chart
            :option="chartOption"
            :style="{ height: '400px' }"
            autoresize
          />
        </div>
      </el-card>

      <!-- Table View -->
      <el-card v-if="viewType === 'table'" class="table-container">
        <template #header>
          <div class="view-header">
            <span>Table View</span>
            <div class="table-controls">
              <el-input
                v-model="tableSearch"
                placeholder="Search..."
                size="small"
                style="width: 200px"
                clearable
              />
              <el-button size="small" @click="toggleColumnSelector">
                <el-icon><Setting /></el-icon>
                Columns
              </el-button>
            </div>
          </div>
        </template>
        <el-table
          :data="filteredTableData"
          height="400"
          v-loading="loading"
          @row-click="handleRowClick"
          stripe
        >
          <el-table-column
            v-for="col in visibleColumns"
            :key="col.prop"
            :prop="col.prop"
            :label="col.label"
            :width="col.width"
            :sortable="col.sortable"
            show-overflow-tooltip
          >
            <template #default="{ row }">
              <span v-if="col.formatter">{{ col.formatter(row[col.prop]) }}</span>
              <span v-else>{{ row[col.prop] }}</span>
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="120" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="drillDown(row)">
                <el-icon><ArrowRight /></el-icon>
                Drill Down
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- Pivot View -->
      <el-card v-if="viewType === 'pivot'" class="pivot-container">
        <template #header>
          <div class="view-header">
            <span>Pivot View</span>
            <div class="pivot-controls">
              <el-select v-model="pivotRow" placeholder="Row" size="small" style="width: 120px">
                <el-option
                  v-for="col in availableColumns"
                  :key="col"
                  :label="col"
                  :value="col"
                />
              </el-select>
              <el-select v-model="pivotCol" placeholder="Column" size="small" style="width: 120px">
                <el-option
                  v-for="col in availableColumns"
                  :key="col"
                  :label="col"
                  :value="col"
                />
              </el-select>
              <el-select v-model="pivotAgg" placeholder="Aggregation" size="small" style="width: 120px">
                <el-option label="Count" value="count" />
                <el-option label="Sum" value="sum" />
                <el-option label="Average" value="avg" />
                <el-option label="Min" value="min" />
                <el-option label="Max" value="max" />
              </el-select>
            </div>
          </div>
        </template>
        <div class="pivot-table">
          <el-table :data="pivotData" height="400" v-loading="loading">
            <el-table-column
              v-for="col in pivotColumns"
              :key="col"
              :prop="col"
              :label="col"
              sortable
            />
          </el-table>
        </div>
      </el-card>
    </div>

    <!-- View Toggle -->
    <div class="view-toggle">
      <el-radio-group v-model="viewType" size="small">
        <el-radio-button label="chart">Chart</el-radio-button>
        <el-radio-button label="table">Table</el-radio-button>
        <el-radio-button label="pivot">Pivot</el-radio-button>
      </el-radio-group>
    </div>

    <!-- Column Selector Dialog -->
    <el-dialog v-model="columnSelectorVisible" title="Select Columns" width="400px">
      <el-checkbox-group v-model="selectedColumns">
        <el-checkbox
          v-for="col in availableColumns"
          :key="col"
          :label="col"
          style="display: block; margin-bottom: 8px"
        >
          {{ col }}
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <el-button @click="columnSelectorVisible = false">Cancel</el-button>
        <el-button type="primary" @click="applyColumnSelection">Apply</el-button>
      </template>
    </el-dialog>
  </el-drawer>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, ScatterChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import {
  Download,
  RefreshLeft,
  Setting,
  ArrowRight
} from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

// Register ECharts components
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const emit = defineEmits(['drill-down', 'export'])

const notificationStore = useNotificationStore()

const visible = ref(false)
const loading = ref(false)
const viewType = ref('table')
const chartType = ref('bar')
const tableSearch = ref('')
const columnSelectorVisible = ref(false)

// Drill down state
const breadcrumbs = ref([
  { label: 'All Data', level: 0 }
])
const currentData = ref([])
const currentFilters = ref({})

// Data summary
const dataSummary = computed(() => [
  { label: 'Total Records', value: currentData.value.length.toLocaleString() },
  { label: 'Filtered Records', value: filteredTableData.value.length.toLocaleString() },
  { label: 'Unique Donors', value: getUniqueCount('donor_id') },
  { label: 'Date Range', value: getDateRange() }
])

// Table data
const availableColumns = ref([
  'donor_id', 'name', 'blood_type', 'donation_date', 'volume_ml', 'location'
])

const selectedColumns = ref([...availableColumns.value])
const visibleColumns = computed(() => {
  return selectedColumns.value.map(col => ({
    prop: col,
    label: col.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    width: getColumnWidth(col),
    sortable: true,
    formatter: getColumnFormatter(col)
  }))
})

const filteredTableData = computed(() => {
  if (!tableSearch.value) return currentData.value
  
  const search = tableSearch.value.toLowerCase()
  return currentData.value.filter(row => {
    return Object.values(row).some(value => 
      String(value).toLowerCase().includes(search)
    )
  })
})

// Chart data
const chartOption = computed(() => {
  if (!currentData.value.length) return {}
  
  const data = currentData.value
  
  if (chartType.value === 'bar') {
    return {
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: data.map(item => item.blood_type || 'Unknown')
      },
      yAxis: { type: 'value' },
      series: [{
        type: 'bar',
        data: data.map(item => item.volume_ml || 0)
      }]
    }
  } else if (chartType.value === 'line') {
    return {
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: data.map(item => item.donation_date || 'Unknown')
      },
      yAxis: { type: 'value' },
      series: [{
        type: 'line',
        data: data.map(item => item.volume_ml || 0)
      }]
    }
  } else if (chartType.value === 'pie') {
    const bloodTypeCount = {}
    data.forEach(item => {
      const type = item.blood_type || 'Unknown'
      bloodTypeCount[type] = (bloodTypeCount[type] || 0) + 1
    })
    
    return {
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: '50%',
        data: Object.entries(bloodTypeCount).map(([name, value]) => ({ name, value }))
      }]
    }
  }
  
  return {}
})

// Pivot data
const pivotRow = ref('blood_type')
const pivotCol = ref('location')
const pivotAgg = ref('count')

const pivotColumns = computed(() => {
  if (!currentData.value.length) return []
  
  const pivotData = {}
  currentData.value.forEach(item => {
    const rowKey = item[pivotRow.value] || 'Unknown'
    const colKey = item[pivotCol.value] || 'Unknown'
    
    if (!pivotData[rowKey]) {
      pivotData[rowKey] = { [pivotCol.value]: rowKey }
    }
    
    if (!pivotData[rowKey][colKey]) {
      pivotData[rowKey][colKey] = 0
    }
    
    if (pivotAgg.value === 'count') {
      pivotData[rowKey][colKey]++
    } else if (pivotAgg.value === 'sum') {
      pivotData[rowKey][colKey] += (item.volume_ml || 0)
    }
  })
  
  return Object.values(pivotData)
})

const pivotData = computed(() => pivotColumns.value)

const panelTitle = computed(() => {
  const current = breadcrumbs.value[breadcrumbs.value.length - 1]
  return `Drill Down: ${current.label}`
})

// Methods
const open = (data, filters = {}) => {
  currentData.value = data || []
  currentFilters.value = filters
  breadcrumbs.value = [{ label: 'All Data', level: 0 }]
  visible.value = true
}

const drillDown = (row) => {
  const newLevel = breadcrumbs.value.length
  const label = `${row.blood_type || 'Unknown'} - ${row.name || 'Unknown'}`
  
  breadcrumbs.value.push({ label, level: newLevel })
  
  // Filter data based on clicked row
  currentData.value = currentData.value.filter(item => 
    item.donor_id === row.donor_id
  )
  
  notificationStore.success(`Drilled down to: ${label}`)
  emit('drill-down', { level: newLevel, data: row, filters: currentFilters.value })
}

const navigateToBreadcrumb = (index) => {
  if (index === breadcrumbs.value.length - 1) return
  
  breadcrumbs.value = breadcrumbs.value.slice(0, index + 1)
  // Reset data to appropriate level
  notificationStore.info(`Navigated to: ${breadcrumbs.value[index].label}`)
}

const resetDrillDown = () => {
  breadcrumbs.value = [{ label: 'All Data', level: 0 }]
  currentFilters.value = {}
  tableSearch.value = ''
  notificationStore.info('Drill down reset')
}

const exportCurrentView = () => {
  const exportData = {
    type: viewType.value,
    data: viewType.value === 'table' ? filteredTableData.value : currentData.value,
    filters: currentFilters.value,
    breadcrumbs: breadcrumbs.value
  }
  
  emit('export', exportData)
  notificationStore.success('Export initiated')
}

const toggleColumnSelector = () => {
  columnSelectorVisible.value = true
}

const applyColumnSelection = () => {
  columnSelectorVisible.value = false
  notificationStore.success('Column selection applied')
}

const handleRowClick = (row) => {
  drillDown(row)
}

const getUniqueCount = (field) => {
  const unique = new Set(currentData.value.map(item => item[field]))
  return unique.size.toLocaleString()
}

const getDateRange = () => {
  if (!currentData.value.length) return 'N/A'
  
  const dates = currentData.value
    .map(item => item.donation_date)
    .filter(Boolean)
    .sort()
  
  if (dates.length === 0) return 'N/A'
  if (dates.length === 1) return dates[0]
  
  return `${dates[0]} - ${dates[dates.length - 1]}`
}

const getColumnWidth = (col) => {
  const widths = {
    donor_id: 100,
    name: 150,
    blood_type: 100,
    donation_date: 120,
    volume_ml: 100,
    location: 120
  }
  return widths[col] || 120
}

const getColumnFormatter = (col) => {
  if (col === 'volume_ml') {
    return (value) => `${value} ml`
  }
  if (col === 'donation_date') {
    return (value) => new Date(value).toLocaleDateString()
  }
  return null
}

// Watch for pivot changes
watch([pivotRow, pivotCol, pivotAgg], () => {
  // Pivot data will recalculate automatically
}, { deep: true })

defineExpose({
  open
})
</script>

<style scoped>
.drill-down-panel :deep(.el-drawer__body) {
  padding: 0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
  background-color: #f8f9fa;
}

.breadcrumb-item {
  cursor: pointer;
}

.breadcrumb-item:hover {
  color: #409eff;
}

.panel-actions {
  display: flex;
  gap: 8px;
}

.data-summary {
  padding: 16px;
  background-color: #ffffff;
  border-bottom: 1px solid #e4e7ed;
}

.summary-card {
  text-align: center;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.summary-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.summary-label {
  font-size: 12px;
  color: #909399;
  text-transform: uppercase;
}

.drill-down-content {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-controls,
.pivot-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.chart-wrapper {
  width: 100%;
}

.view-toggle {
  position: sticky;
  bottom: 0;
  padding: 16px;
  background-color: #ffffff;
  border-top: 1px solid #e4e7ed;
  text-align: center;
}

@media (max-width: 768px) {
  .panel-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .data-summary .el-col {
    margin-bottom: 12px;
  }
  
  .view-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .table-controls,
  .pivot-controls {
    flex-wrap: wrap;
  }
}
</style>
