<template>
  <div class="forecasting">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>预测分析</span>
              <div class="header-actions">
                <el-button type="primary" @click="runForecast">
                  <el-icon><TrendCharts /></el-icon>
                  生成预测
                </el-button>
                <el-button @click="exportForecast">
                  <el-icon><Download /></el-icon>
                  导出
                </el-button>
              </div>
            </div>
          </template>

          <!-- Forecast Configuration -->
          <div class="forecast-config">
            <el-row :gutter="16">
              <el-col :span="6">
                <el-form-item label="预测周期">
                  <el-select v-model="forecastConfig.period" placeholder="选择周期">
                    <el-option label="7天" value="7" />
                    <el-option label="30天" value="30" />
                    <el-option label="90天" value="90" />
                    <el-option label="180天" value="180" />
                    <el-option label="365天" value="365" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="目标变量">
                  <el-select v-model="forecastConfig.target" placeholder="选择目标">
                    <el-option label="捐赠量" value="volume" />
                    <el-option label="捐赠者数量" value="donors" />
                    <el-option label="血型分布" value="blood_types" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="模型类型">
                  <el-select v-model="forecastConfig.model" placeholder="选择模型">
                    <el-option label="线性回归" value="linear" />
                    <el-option label="ARIMA" value="arima" />
                    <el-option label="Prophet" value="prophet" />
                    <el-option label="神经网络" value="neural" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="置信水平">
                  <el-select v-model="forecastConfig.confidence" placeholder="选择置信度">
                    <el-option label="80%" value="80" />
                    <el-option label="90%" value="90" />
                    <el-option label="95%" value="95" />
                    <el-option label="99%" value="99" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <!-- Forecast Results -->
          <el-divider>Forecast Results</el-divider>
          <el-row :gutter="16">
            <el-col :span="16">
              <el-card>
                <template #header>
                  <span>Forecast Chart</span>
                </template>
                <div class="chart-placeholder">
                  <el-empty description="Forecast chart will be displayed here" />
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <template #header>
                  <span>Key Metrics</span>
                </template>
                <div class="metrics-list">
                  <div class="metric-item">
                    <div class="metric-label">Predicted Volume</div>
                    <div class="metric-value">{{ forecastMetrics.predictedVolume }}</div>
                  </div>
                  <div class="metric-item">
                    <div class="metric-label">Confidence Interval</div>
                    <div class="metric-value">{{ forecastMetrics.confidenceInterval }}</div>
                  </div>
                  <div class="metric-item">
                    <div class="metric-label">Model Accuracy</div>
                    <div class="metric-value">{{ forecastMetrics.accuracy }}</div>
                  </div>
                  <div class="metric-item">
                    <div class="metric-label">Trend Direction</div>
                    <div class="metric-value">
                      <el-tag :type="forecastMetrics.trendType">
                        {{ forecastMetrics.trend }}
                      </el-tag>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- Historical Performance -->
          <el-divider>Model Performance</el-divider>
          <el-table :data="modelPerformance" style="width: 100%">
            <el-table-column prop="model" label="Model" />
            <el-table-column prop="accuracy" label="Accuracy" width="120" />
            <el-table-column prop="mae" label="MAE" width="120" />
            <el-table-column prop="rmse" label="RMSE" width="120" />
            <el-table-column prop="trainingTime" label="Training Time" width="150" />
            <el-table-column label="Actions" width="100">
              <template #default="{ row }">
                <el-button size="small" @click="useModel(row)">Use</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { TrendCharts, Download } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const forecastConfig = ref({
  period: '30',
  target: 'volume',
  model: 'linear',
  confidence: '95'
})

const forecastMetrics = ref({
  predictedVolume: '1,456 units',
  confidenceInterval: '±127 units',
  accuracy: '94.2%',
  trend: 'Increasing',
  trendType: 'success'
})

const modelPerformance = ref([
  {
    model: 'Linear Regression',
    accuracy: '94.2%',
    mae: '45.3',
    rmse: '67.8',
    trainingTime: '2.3s'
  },
  {
    model: 'ARIMA',
    accuracy: '91.7%',
    mae: '52.1',
    rmse: '78.4',
    trainingTime: '5.6s'
  },
  {
    model: 'Prophet',
    accuracy: '93.5%',
    mae: '48.7',
    rmse: '71.2',
    trainingTime: '8.9s'
  }
])

const runForecast = () => {
  notificationStore.success('预测生成成功')
}

const exportForecast = () => {
  notificationStore.success('预测数据导出成功')
}

const useModel = (model) => {
  notificationStore.info(`Using model: ${model.model}`)
}
</script>

<style scoped>
.forecasting {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.forecast-config {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 24px;
}

.chart-placeholder {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.metrics-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.metric-item:last-child {
  border-bottom: none;
}

.metric-label {
  font-weight: 500;
  color: #606266;
}

.metric-value {
  font-weight: 600;
  color: #303133;
}
</style>
