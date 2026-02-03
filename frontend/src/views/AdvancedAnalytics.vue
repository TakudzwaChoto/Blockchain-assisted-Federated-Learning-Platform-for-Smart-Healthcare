<template>
  <div class="advanced-analytics">
    <el-card>
      <template #header>
        <div class="section-header">
          <h3>高级分析与预测引擎</h3>
          <el-tag type="success">AI驱动的智能分析</el-tag>
        </div>
      </template>

      <!-- Analysis Controls -->
      <el-row :gutter="24" class="analysis-controls">
        <el-col :span="8">
          <el-card class="control-card">
            <template #header>
              <div class="card-header">
                <el-icon><TrendCharts /></el-icon>
                <span>分析类型</span>
              </div>
            </template>
            
            <el-form :model="analysisConfig" label-width="100px">
              <el-form-item label="分析维度">
                <el-select v-model="analysisConfig.dimension" placeholder="选择分析维度">
                  <el-option label="时间维度" value="time" />
                  <el-option label="地区维度" value="region" />
                  <el-option label="人群维度" value="demographics" />
                  <el-option label="血型维度" value="bloodType" />
                  <el-option label="综合维度" value="comprehensive" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="分析周期">
                <el-select v-model="analysisConfig.period" placeholder="选择分析周期">
                  <el-option label="日分析" value="daily" />
                  <el-option label="周分析" value="weekly" />
                  <el-option label="月分析" value="monthly" />
                  <el-option label="季度分析" value="quarterly" />
                  <el-option label="年度分析" value="yearly" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="预测模型">
                <el-select v-model="analysisConfig.model" placeholder="选择预测模型">
                  <el-option label="ARIMA模型" value="arima" />
                  <el-option label="Prophet模型" value="prophet" />
                  <el-option label="LSTM神经网络" value="lstm" />
                  <el-option label="线性回归" value="linear" />
                  <el-option label="随机森林" value="randomForest" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="control-card">
            <template #header>
              <div class="card-header">
                <el-icon><Setting /></el-icon>
                <span>参数配置</span>
              </div>
            </template>
            
            <el-form :model="modelParams" label-width="100px">
              <el-form-item label="预测天数">
                <el-input-number 
                  v-model="modelParams.forecastDays" 
                  :min="7" 
                  :max="365" 
                  :step="7"
                />
              </el-form-item>
              
              <el-form-item label="置信区间">
                <el-slider
                  v-model="modelParams.confidenceInterval"
                  :min="80"
                  :max="99"
                  :step="1"
                  :format-tooltip="(val) => `${val}%`"
                />
              </el-form-item>
              
              <el-form-item label="训练周期">
                <el-select v-model="modelParams.trainingPeriod" placeholder="选择训练周期">
                  <el-option label="最近3个月" value="3months" />
                  <el-option label="最近6个月" value="6months" />
                  <el-option label="最近1年" value="1year" />
                  <el-option label="最近2年" value="2years" />
                  <el-option label="全部数据" value="all" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="control-card">
            <template #header>
              <div class="card-header">
                <el-icon><DataAnalysis /></el-icon>
                <span>评估指标</span>
              </div>
            </template>
            
            <div class="metrics-display">
              <div class="metric-item">
                <div class="metric-label">R² 分数</div>
                <div class="metric-value" :class="getMetricClass(modelMetrics.r2)">
                  {{ modelMetrics.r2.toFixed(4) }}
                </div>
                <div class="metric-desc">拟合优度</div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">RMSE</div>
                <div class="metric-value" :class="getMetricClass(modelMetrics.rmse, true)">
                  {{ modelMetrics.rmse.toFixed(2) }}
                </div>
                <div class="metric-desc">均方根误差</div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">MAPE</div>
                <div class="metric-value" :class="getMetricClass(modelMetrics.mape, true)">
                  {{ modelMetrics.mape.toFixed(2) }}%
                </div>
                <div class="metric-desc">平均绝对百分比误差</div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">MAE</div>
                <div class="metric-value" :class="getMetricClass(modelMetrics.mae, true)">
                  {{ modelMetrics.mae.toFixed(2) }}
                </div>
                <div class="metric-desc">平均绝对误差</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- Analysis Actions -->
      <div class="analysis-actions">
        <el-button @click="runAnalysis" :loading="analyzing" type="primary">
          <el-icon><VideoPlay /></el-icon>
          运行分析
        </el-button>
        <el-button @click="trainModel" :loading="training">
          <el-icon><Refresh /></el-icon>
          训练模型
        </el-button>
        <el-button @click="validateModel" :loading="validating">
          <el-icon><Check /></el-icon>
          验证模型
        </el-button>
        <el-button @click="exportResults">
          <el-icon><Download /></el-icon>
          导出结果
        </el-button>
      </div>

      <!-- Forecasting Results -->
      <el-card v-if="forecastResults.length > 0" class="forecast-card">
        <template #header>
          <div class="forecast-header">
            <span>需求预测结果</span>
            <el-tag type="info">{{ analysisConfig.model.toUpperCase() }} 模型</el-tag>
          </div>
        </template>
        
        <div class="forecast-chart">
          <div class="chart-container">
            <div class="chart-title">血液需求预测趋势</div>
            <div class="chart-content">
              <!-- Historical Data -->
              <div class="data-series historical">
                <div 
                  v-for="(point, index) in historicalData" 
                  :key="'hist-' + index"
                  class="data-point"
                  :style="{ 
                    left: (index / historicalData.length * 100) + '%',
                    bottom: (point.value / maxHistoricalValue * 100) + '%'
                  }"
                >
                  <div class="point-value">{{ point.value }}</div>
                </div>
              </div>
              
              <!-- Forecast Data with Confidence Interval -->
              <div class="data-series forecast">
                <div 
                  v-for="(point, index) in forecastResults" 
                  :key="'forecast-' + index"
                  class="forecast-point"
                  :style="{ 
                    left: ((index + historicalData.length) / (historicalData.length + forecastResults.length) * 100) + '%',
                    bottom: (point.predicted / maxForecastValue * 100) + '%'
                  }"
                >
                  <div class="point-value">{{ point.predicted }}</div>
                  <div class="confidence-interval" :style="{
                    height: ((point.upper - point.lower) / maxForecastValue * 100) + '%',
                    bottom: (point.lower / maxForecastValue * 100) + '%'
                  }"></div>
                </div>
              </div>
            </div>
            
            <div class="chart-legend">
              <div class="legend-item">
                <div class="legend-color historical"></div>
                <span>历史数据</span>
              </div>
              <div class="legend-item">
                <div class="legend-color forecast"></div>
                <span>预测值</span>
              </div>
              <div class="legend-item">
                <div class="legend-color confidence"></div>
                <span>置信区间 ({{ modelParams.confidenceInterval }}%)</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Forecast Statistics -->
        <div class="forecast-stats">
          <el-row :gutter="16">
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ forecastStats.averageDemand }}</div>
                  <div class="stat-label">平均需求量</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon><ArrowUp /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ forecastStats.peakDemand }}</div>
                  <div class="stat-label">峰值需求</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon><ArrowDown /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ forecastStats.lowDemand }}</div>
                  <div class="stat-label">最低需求</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ forecastStats.riskDays }}</div>
                  <div class="stat-label">风险天数</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>

      <!-- Trend Analysis -->
      <el-card v-if="trendAnalysis" class="trend-card">
        <template #header>
          <span>趋势分析洞察</span>
        </template>
        
        <div class="trend-insights">
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="insight-section">
                <h4>季节性模式</h4>
                <div class="seasonality-chart">
                  <div 
                    v-for="(month, index) in trendAnalysis.seasonality" 
                    :key="index"
                    class="month-bar"
                    :style="{ 
                      height: month.value + '%',
                      backgroundColor: getSeasonalityColor(month.value)
                    }"
                  >
                    <div class="month-label">{{ month.name }}</div>
                    <div class="month-value">{{ month.value }}</div>
                  </div>
                </div>
              </div>
            </el-col>
            
            <el-col :span="12">
              <div class="insight-section">
                <h4>人群分布分析</h4>
                <div class="demographics-chart">
                  <div 
                    v-for="(group, index) in trendAnalysis.demographics" 
                    :key="index"
                    class="demographic-item"
                  >
                    <div class="group-info">
                      <span class="group-name">{{ group.name }}</span>
                      <span class="group-percentage">{{ group.percentage }}%</span>
                    </div>
                    <el-progress 
                      :percentage="group.percentage" 
                      :color="getDemographicColor(index)"
                      :show-text="false"
                    />
                  </div>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <el-divider />
          
          <div class="ai-insights">
            <h4>AI 智能洞察</h4>
            <div class="insight-cards">
              <div 
                v-for="(insight, index) in trendAnalysis.aiInsights" 
                :key="index"
                class="insight-card"
                :class="insight.type"
              >
                <div class="insight-icon">
                  <el-icon>
                    <component :is="getInsightIcon(insight.type)" />
                  </el-icon>
                </div>
                <div class="insight-content">
                  <div class="insight-title">{{ insight.title }}</div>
                  <div class="insight-description">{{ insight.description }}</div>
                  <div class="insight-confidence">
                    置信度: {{ insight.confidence }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- Model Training Progress -->
      <el-card v-if="trainingVisible" class="training-card">
        <template #header>
          <span>模型训练进度</span>
        </template>
        
        <div class="training-content">
          <el-steps :active="trainingStep" align-center>
            <el-step title="数据预处理" description="清洗和标准化数据" />
            <el-step title="特征工程" description="提取和选择特征" />
            <el-step title="模型训练" description="训练预测模型" />
            <el-step title="模型验证" description="验证模型性能" />
            <el-step title="部署就绪" description="模型部署完成" />
          </el-steps>
          
          <div class="training-progress">
            <el-progress 
              :percentage="trainingProgress" 
              :status="trainingStatus"
            />
            <p class="progress-text">{{ trainingMessage }}</p>
          </div>
          
          <div class="training-metrics">
            <el-row :gutter="16">
              <el-col :span="8">
                <div class="metric-card">
                  <div class="metric-title">训练样本</div>
                  <div class="metric-value-large">{{ trainingMetrics.samples }}</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="metric-card">
                  <div class="metric-title">训练轮次</div>
                  <div class="metric-value-large">{{ trainingMetrics.epochs }}</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="metric-card">
                  <div class="metric-title">训练时长</div>
                  <div class="metric-value-large">{{ trainingMetrics.duration }}s</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  TrendCharts, Setting, DataAnalysis, VideoPlay, Refresh, Check, 
  Download, ArrowUp, ArrowDown, Warning, InfoFilled, SuccessFilled,
  CircleCloseFilled
} from '@element-plus/icons-vue'

// Reactive data
const analyzing = ref(false)
const training = ref(false)
const validating = ref(false)
const trainingVisible = ref(false)
const trainingStep = ref(0)
const trainingProgress = ref(0)
const trainingStatus = ref('')
const trainingMessage = ref('')

// Analysis configuration
const analysisConfig = reactive({
  dimension: 'time',
  period: 'monthly',
  model: 'arima'
})

// Model parameters
const modelParams = reactive({
  forecastDays: 30,
  confidenceInterval: 95,
  trainingPeriod: '6months'
})

// Model metrics
const modelMetrics = reactive({
  r2: 0.8542,
  rmse: 12.34,
  mape: 8.76,
  mae: 9.45
})

// Training metrics
const trainingMetrics = reactive({
  samples: 150000,
  epochs: 100,
  duration: 245
})

// Forecast results
const forecastResults = ref([])
const historicalData = ref([])
const trendAnalysis = ref(null)

// Computed properties
const maxHistoricalValue = computed(() => {
  return Math.max(...historicalData.value.map(d => d.value), 1)
})

const maxForecastValue = computed(() => {
  const allValues = [
    ...historicalData.value.map(d => d.value),
    ...forecastResults.value.map(f => f.upper)
  ]
  return Math.max(...allValues, 1)
})

const forecastStats = computed(() => {
  if (forecastResults.value.length === 0) {
    return {
      averageDemand: 0,
      peakDemand: 0,
      lowDemand: 0,
      riskDays: 0
    }
  }
  
  const values = forecastResults.value.map(f => f.predicted)
  const average = Math.round(values.reduce((a, b) => a + b, 0) / values.length)
  const peak = Math.max(...values)
  const low = Math.min(...values)
  const threshold = average * 0.8
  const riskDays = values.filter(v => v < threshold).length
  
  return {
    averageDemand: average,
    peakDemand: peak,
    lowDemand: low,
    riskDays: riskDays
  }
})

// Methods
const getMetricClass = (value, isError = false) => {
  if (isError) {
    if (value < 5) return 'excellent'
    if (value < 10) return 'good'
    if (value < 20) return 'fair'
    return 'poor'
  } else {
    if (value > 0.9) return 'excellent'
    if (value > 0.8) return 'good'
    if (value > 0.7) return 'fair'
    return 'poor'
  }
}

const getSeasonalityColor = (value) => {
  if (value > 80) return '#f56c6c'
  if (value > 60) return '#e6a23c'
  if (value > 40) return '#409eff'
  return '#67c23a'
}

const getDemographicColor = (index) => {
  const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']
  return colors[index % colors.length]
}

const getInsightIcon = (type) => {
  const icons = {
    'success': SuccessFilled,
    'warning': Warning,
    'info': InfoFilled,
    'error': CircleCloseFilled
  }
  return icons[type] || InfoFilled
}

const runAnalysis = async () => {
  analyzing.value = true
  
  try {
    // Simulate analysis process
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Generate mock historical data
    historicalData.value = Array.from({ length: 90 }, (_, i) => ({
      date: new Date(Date.now() - (89 - i) * 24 * 60 * 60 * 1000),
      value: Math.floor(Math.random() * 100) + 150
    }))
    
    // Generate mock forecast results
    forecastResults.value = Array.from({ length: modelParams.forecastDays }, (_, i) => {
      const baseValue = 180 + Math.sin(i / 7) * 20
      const randomVariation = (Math.random() - 0.5) * 30
      const predicted = Math.round(baseValue + randomVariation)
      const margin = predicted * 0.1 * (modelParams.confidenceInterval / 95)
      
      return {
        date: new Date(Date.now() + (i + 1) * 24 * 60 * 60 * 1000),
        predicted: predicted,
        lower: Math.round(predicted - margin),
        upper: Math.round(predicted + margin)
      }
    })
    
    // Generate trend analysis
    trendAnalysis.value = {
      seasonality: [
        { name: '1月', value: 65 },
        { name: '2月', value: 72 },
        { name: '3月', value: 85 },
        { name: '4月', value: 92 },
        { name: '5月', value: 88 },
        { name: '6月', value: 95 },
        { name: '7月', value: 78 },
        { name: '8月', value: 82 },
        { name: '9月', value: 90 },
        { name: '10月', value: 93 },
        { name: '11月', value: 87 },
        { name: '12月', value: 83 }
      ],
      demographics: [
        { name: '学生群体', percentage: 35 },
        { name: '医护人员', percentage: 25 },
        { name: '公务员', percentage: 20 },
        { name: '企业员工', percentage: 15 },
        { name: '其他群体', percentage: 5 }
      ],
      aiInsights: [
        {
          type: 'success',
          title: '需求趋势稳定',
          description: '未来30天血液需求量预计保持稳定，平均日需求量约' + forecastStats.value.averageDemand + '单位',
          confidence: 92
        },
        {
          type: 'warning',
          title: '季节性波动',
          description: '检测到明显的季节性波动模式，建议在高峰期前增加库存储备',
          confidence: 87
        },
        {
          type: 'info',
          title: '人群偏好分析',
          description: '学生群体是主要捐赠群体，建议在高校开展针对性宣传活动',
          confidence: 78
        }
      ]
    }
    
    ElMessage.success('分析完成！预测模型已生成')
  } catch (error) {
    ElMessage.error('分析失败: ' + error.message)
  } finally {
    analyzing.value = false
  }
}

const trainModel = async () => {
  training.value = true
  trainingVisible.value = true
  trainingStep.value = 0
  trainingProgress.value = 0
  trainingStatus.value = 'active'
  
  try {
    const steps = [
      { name: '数据预处理', duration: 3000 },
      { name: '特征工程', duration: 2000 },
      { name: '模型训练', duration: 5000 },
      { name: '模型验证', duration: 2000 },
      { name: '部署就绪', duration: 1000 }
    ]
    
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i]
      trainingStep.value = i
      trainingMessage.value = `正在${step.name}...`
      
      // Simulate progress
      const progressSteps = 20
      for (let j = 0; j <= progressSteps; j++) {
        trainingProgress.value = (i * 100 / steps.length) + (100 / steps.length) * (j / progressSteps)
        await new Promise(resolve => setTimeout(resolve, step.duration / progressSteps))
      }
    }
    
    trainingStatus.value = 'success'
    trainingMessage.value = '模型训练完成！'
    
    // Update model metrics
    modelMetrics.r2 = 0.8742 + Math.random() * 0.05
    modelMetrics.rmse = 10.34 + Math.random() * 2
    modelMetrics.mape = 7.76 + Math.random() * 2
    modelMetrics.mae = 8.45 + Math.random() * 2
    
    ElMessage.success('模型训练完成！性能已优化')
  } catch (error) {
    trainingStatus.value = 'exception'
    trainingMessage.value = '训练失败'
    ElMessage.error('模型训练失败: ' + error.message)
  } finally {
    training.value = false
  }
}

const validateModel = async () => {
  validating.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Simulate validation results
    const validationScore = 0.85 + Math.random() * 0.1
    
    if (validationScore > 0.9) {
      ElMessage.success(`模型验证通过！准确率: ${(validationScore * 100).toFixed(2)}%`)
    } else if (validationScore > 0.8) {
      ElMessage.warning(`模型验证通过，建议优化。准确率: ${(validationScore * 100).toFixed(2)}%`)
    } else {
      ElMessage.error(`模型验证失败，准确率过低: ${(validationScore * 100).toFixed(2)}%`)
    }
  } catch (error) {
    ElMessage.error('模型验证失败: ' + error.message)
  } finally {
    validating.value = false
  }
}

const exportResults = () => {
  ElMessage.success('分析结果已导出为PDF报告')
}
</script>

<style scoped>
.advanced-analytics {
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  margin: 0;
  color: #333;
}

.analysis-controls {
  margin-bottom: 24px;
}

.control-card {
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.metrics-display {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.metric-item {
  text-align: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.metric-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 4px;
}

.metric-value.excellent {
  color: #67c23a;
}

.metric-value.good {
  color: #409eff;
}

.metric-value.fair {
  color: #e6a23c;
}

.metric-value.poor {
  color: #f56c6c;
}

.metric-desc {
  font-size: 11px;
  color: #999;
}

.analysis-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.forecast-card, .trend-card, .training-card {
  margin-top: 24px;
}

.forecast-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  position: relative;
  height: 400px;
  background: #fafafa;
  border-radius: 8px;
  padding: 20px;
}

.chart-title {
  text-align: center;
  font-weight: 600;
  margin-bottom: 20px;
}

.chart-content {
  position: relative;
  height: 300px;
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.data-series {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
}

.data-point {
  position: absolute;
  width: 4px;
  background: #409eff;
  border-radius: 2px;
}

.data-point .point-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  white-space: nowrap;
}

.forecast-point {
  position: absolute;
  width: 6px;
  background: #67c23a;
  border-radius: 3px;
}

.forecast-point .point-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  white-space: nowrap;
  color: #67c23a;
}

.confidence-interval {
  position: absolute;
  left: -2px;
  width: 10px;
  background: rgba(103, 194, 58, 0.2);
  border: 1px solid rgba(103, 194, 58, 0.3);
  border-radius: 2px;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.historical {
  background: #409eff;
}

.legend-color.forecast {
  background: #67c23a;
}

.legend-color.confidence {
  background: rgba(103, 194, 58, 0.3);
  border: 1px solid #67c23a;
}

.forecast-stats {
  margin-top: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.trend-insights {
  padding: 20px 0;
}

.insight-section h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.seasonality-chart {
  display: flex;
  align-items: flex-end;
  height: 150px;
  gap: 4px;
}

.month-bar {
  flex: 1;
  background: #409eff;
  border-radius: 2px 2px 0 0;
  position: relative;
  min-height: 10px;
}

.month-label {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  white-space: nowrap;
}

.month-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  white-space: nowrap;
}

.demographics-chart {
  space-y: 12px;
}

.demographic-item {
  margin-bottom: 12px;
}

.group-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.group-name {
  font-size: 14px;
  color: #333;
}

.group-percentage {
  font-size: 14px;
  font-weight: 600;
  color: #409eff;
}

.ai-insights h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.insight-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.insight-card {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid;
}

.insight-card.success {
  background: #f0f9ff;
  border-left-color: #67c23a;
}

.insight-card.warning {
  background: #fdf6ec;
  border-left-color: #e6a23c;
}

.insight-card.info {
  background: #f4f4f5;
  border-left-color: #909399;
}

.insight-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.insight-card.success .insight-icon {
  background: #67c23a;
  color: white;
}

.insight-card.warning .insight-icon {
  background: #e6a23c;
  color: white;
}

.insight-card.info .insight-icon {
  background: #909399;
  color: white;
}

.insight-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.insight-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.insight-confidence {
  font-size: 12px;
  color: #999;
}

.training-content {
  padding: 20px 0;
}

.training-progress {
  margin: 24px 0;
  text-align: center;
}

.progress-text {
  margin-top: 8px;
  color: #666;
}

.training-metrics {
  margin-top: 24px;
}

.metric-card {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.metric-title {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}

.metric-value-large {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

@media (max-width: 768px) {
  .analysis-controls {
    margin-bottom: 16px;
  }
  
  .analysis-actions {
    flex-wrap: wrap;
  }
  
  .forecast-stats .el-col {
    margin-bottom: 12px;
  }
  
  .insight-cards {
    grid-template-columns: 1fr;
  }
}
</style>
