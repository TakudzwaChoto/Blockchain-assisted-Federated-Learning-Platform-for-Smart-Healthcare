<template>
  <div>
    <el-empty v-if="!datasetId" description="请先在上方选择数据集" />

    <template v-else>
      <!-- Show loading state -->
      <div v-if="loadingTrends || loadingForecast || loadingAssociations" style="text-align: center; padding: 20px">
        <el-icon class="is-loading" style="font-size: 24px">
          <Loading />
        </el-icon>
        <p style="margin-top: 10px">加载中...</p>
      </div>

      <!-- Error display -->
      <el-alert 
        v-else-if="trends?.error || forecast?.error || associations?.error"
        :title="trends?.error || forecast?.error || associations?.error"
        type="error"
        show-icon
        :closable="false"
        style="margin-bottom: 16px"
      />

      <!-- Show empty state when no data loaded -->
      <el-empty 
        v-else-if="!trends && !forecast && !associations" 
        description="点击刷新按钮加载数据"
      />

      <!-- Show data when available -->
      <template v-else>
        <!-- Simple fallback display to prevent chart rendering issues -->
        <div v-if="widget.type === 'trend' && trends" style="padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
          <h4>趋势分析数据</h4>
          <div v-if="trends.trends" style="margin-top: 10px;">
            <div v-for="(item, index) in trends.trends.slice(0, 5)" :key="index" style="padding: 5px 0; border-bottom: 1px solid #f0f0f0;">
              {{ item.month || item.period }}: {{ item.value }} {{ item.blood_type || '' }}
            </div>
          </div>
          <div v-else style="color: #666;">
            数据格式: {{ JSON.stringify(trends).substring(0, 100) }}...
          </div>
        </div>

        <div v-else-if="widget.type === 'forecast' && forecast" style="padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
          <h4>预测分析数据</h4>
          <div v-if="forecast.forecast" style="margin-top: 10px;">
            <div v-for="(item, index) in forecast.forecast.slice(0, 5)" :key="index" style="padding: 5px 0; border-bottom: 1px solid #f0f0f0;">
              {{ item.date }}: 预测值 {{ item.predicted }} (置信区间: {{ item.confidence_low }}-{{ item.confidence_high }})
            </div>
          </div>
          <div v-else style="color: #666;">
            数据格式: {{ JSON.stringify(forecast).substring(0, 100) }}...
          </div>
        </div>

        <div v-else-if="widget.type === 'associations' && associations" style="padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
          <h4>关联规则数据</h4>
          <div v-if="associations.associations" style="margin-top: 10px;">
            <div v-for="(item, index) in associations.associations.slice(0, 3)" :key="index" style="padding: 5px 0; border-bottom: 1px solid #f0f0f0;">
              <div>{{ item.antecedent.join(' + ') }} → {{ item.consequent.join(' + ') }}</div>
              <div style="font-size: 0.9em; color: #666;">
                置信度: {{ (item.confidence * 100).toFixed(1) }}%, 支持度: {{ (item.support * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
          <div v-else style="color: #666;">
            数据格式: {{ JSON.stringify(associations).substring(0, 100) }}...
          </div>
        </div>

        <el-empty v-else description="未知组件类型" />
      </template>

      <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
        <el-button v-if="widget.type === 'trend'" :loading="loadingTrends" @click="loadTrends">刷新数据</el-button>
        <el-button v-if="widget.type === 'forecast'" :loading="loadingForecast" @click="loadForecast">刷新数据</el-button>
        <el-button v-if="widget.type === 'associations'" :loading="loadingAssociations" @click="loadAssociations">刷新数据</el-button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { runTrends, runForecast, mineAssociations } from '../services/api'

const props = defineProps({
  widget: { type: Object, required: true },
  datasetId: { type: String, default: '' }
})

const trends = ref(null)
const forecast = ref(null)
const associations = ref(null)

const loadingTrends = ref(false)
const loadingForecast = ref(false)
const loadingAssociations = ref(false)

async function loadTrends() {
  if (!props.datasetId) {
    console.warn('No datasetId provided for trends analysis')
    return
  }
  loadingTrends.value = true
  
  // Add timeout to prevent infinite loading
  const timeout = setTimeout(() => {
    loadingTrends.value = false
    trends.value = { error: '加载超时，请重试' }
  }, 8000)
  
  try {
    trends.value = await runTrends(props.datasetId, 'monthly', 365)
  } catch (error) {
    console.error('Failed to load trends:', error)
    trends.value = { error: 'Failed to load trends data' }
  } finally {
    clearTimeout(timeout)
    loadingTrends.value = false
  }
}

async function loadForecast() {
  if (!props.datasetId) {
    console.warn('No datasetId provided for forecast analysis')
    return
  }
  loadingForecast.value = true
  
  // Add timeout to prevent infinite loading
  const timeout = setTimeout(() => {
    loadingForecast.value = false
    forecast.value = { error: '加载超时，请重试' }
  }, 8000)
  
  try {
    forecast.value = await runForecast(props.datasetId, 30, 'daily', 'volume_ml')
  } catch (error) {
    console.error('Failed to load forecast:', error)
    forecast.value = { error: 'Failed to load forecast data' }
  } finally {
    clearTimeout(timeout)
    loadingForecast.value = false
  }
}

async function loadAssociations() {
  if (!props.datasetId) {
    console.warn('No datasetId provided for associations analysis')
    return
  }
  loadingAssociations.value = true
  
  // Add timeout to prevent infinite loading
  const timeout = setTimeout(() => {
    loadingAssociations.value = false
    associations.value = { error: '加载超时，请重试' }
  }, 8000)
  
  try {
    associations.value = await mineAssociations(props.datasetId)
  } catch (error) {
    console.error('Failed to load associations:', error)
    associations.value = { error: 'Failed to load associations data' }
  } finally {
    clearTimeout(timeout)
    loadingAssociations.value = false
  }
}

watch(
  () => props.datasetId,
  () => {
    // Reset data but don't auto-load - let user click refresh
    trends.value = null
    forecast.value = null
    associations.value = null
  },
  { immediate: false }
)
</script>
