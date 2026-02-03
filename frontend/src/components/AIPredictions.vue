<template>
  <div class="ai-predictions">
    <div class="ai-header">
      <div class="ai-title">
        <div class="ai-icon-container">
          <el-icon size="28" color="#667eea"><TrendCharts /></el-icon>
        </div>
        <div>
          <h3>AI Predictions</h3>
          <p class="ai-subtitle">Intelligent predictions based on machine learning</p>
        </div>
      </div>
      <div class="ai-status">
        <el-tag type="success" size="small" effect="dark">
          <el-icon size="12"><CircleCheck /></el-icon>
          AI Active
        </el-tag>
      </div>
    </div>
    
    <div class="predictions-grid">
      <div class="prediction-card blood-shortage">
        <div class="prediction-header">
          <div class="prediction-icon">
            <el-icon size="20"><Warning /></el-icon>
          </div>
          <div class="prediction-title">Blood Shortage Alert</div>
        </div>
        <div class="prediction-content">
          <div class="prediction-risk high">
            Risk: High
          </div>
          <div class="prediction-details">
            A-type blood shortage expected in 3-5 days, immediate emergency procurement recommended
          </div>
          <div class="prediction-actions">
            <el-button type="danger" size="small">
              Take Action
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="prediction-card demand-surge">
        <div class="prediction-header">
          <div class="prediction-icon">
            <el-icon size="20"><TrendCharts /></el-icon>
          </div>
          <div class="prediction-title">Demand Surge Prediction</div>
        </div>
        <div class="prediction-content">
          <div class="prediction-risk medium">
            Risk: Medium
          </div>
          <div class="prediction-details">
            35% increase in surgical demand expected in 1-2 weeks, advance preparation recommended
          </div>
          <div class="prediction-actions">
            <el-button type="warning" size="small">
              Prepare
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="prediction-card optimal-supply">
        <div class="prediction-header">
          <div class="prediction-icon">
            <el-icon size="20"><CircleCheck /></el-icon>
          </div>
          <div class="prediction-title">Optimal Supply Status</div>
        </div>
        <div class="prediction-content">
          <div class="prediction-risk low">
            Risk: Low
          </div>
          <div class="prediction-details">
            Current inventory status is good, maintain existing levels
          </div>
          <div class="prediction-actions">
            <el-button type="success" size="small">
              Maintain
            </el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="ai-insights">
      <h4>AI Insights</h4>
      <div class="insights-list">
        <div class="insight-item">
          <div class="insight-icon">
            <el-icon size="16"><InfoFilled /></el-icon>
          </div>
          <div class="insight-text">Recommend increasing A-type blood inventory to avoid shortage risk</div>
        </div>
        <div class="insight-item">
          <div class="insight-icon">
            <el-icon size="16"><TrendCharts /></el-icon>
          </div>
          <div class="insight-text">Surgical peak expected next Tuesday, prepare in advance</div>
        </div>
        <div class="insight-item">
          <div class="insight-icon">
            <el-icon size="16"><CircleCheck /></el-icon>
          </div>
          <div class="insight-text">Current inventory turnover rate is good, continue to maintain</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Warning, TrendCharts, CircleCheck, InfoFilled } from '@element-plus/icons-vue'

// AI prediction data
const predictions = ref({
  bloodShortage: {
    risk: 'high',
    probability: 87,
    timeframe: '3-5 days'
  },
  demandSurge: {
    risk: 'medium',
    probability: 65,
    timeframe: '1-2 weeks'
  },
  optimalSupply: {
    risk: 'low',
    probability: 92,
    timeframe: '2-3 weeks'
  }
})

onMounted(() => {
  // Simulate AI predictions loading
  console.log('AI Predictions loaded:', predictions.value)
})
</script>

<style scoped>
.ai-predictions {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
}

.ai-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.ai-icon-container {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.ai-title h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.ai-subtitle {
  margin: 4px 0 0 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
}

.ai-status {
  display: flex;
  align-items: center;
}

.predictions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.prediction-card {
  border-radius: 12px;
  padding: 24px;
  background: white;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.prediction-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

.prediction-card.blood-shortage::before {
  background: linear-gradient(180deg, #ff4757 0%, #ff6b7a 100%);
}

.prediction-card.demand-surge::before {
  background: linear-gradient(180deg, #ffa502 0%, #ffb142 100%);
}

.prediction-card.optimal-supply::before {
  background: linear-gradient(180deg, #26de81 0%, #4cd97b 100%);
}

.prediction-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.prediction-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.prediction-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 600;
  font-size: 18px;
  color: white;
  position: relative;
  overflow: hidden;
}

.prediction-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  border-radius: 10px;
}

.prediction-card.blood-shortage .prediction-icon {
  background: linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%);
  box-shadow: 0 4px 12px rgba(255, 71, 87, 0.3);
}

.prediction-card.demand-surge .prediction-icon {
  background: linear-gradient(135deg, #ffa502 0%, #ffb142 100%);
  box-shadow: 0 4px 12px rgba(255, 165, 2, 0.3);
}

.prediction-card.optimal-supply .prediction-icon {
  background: linear-gradient(135deg, #26de81 0%, #4cd97b 100%);
  box-shadow: 0 4px 12px rgba(38, 222, 129, 0.3);
}

.prediction-title {
  font-weight: 600;
  font-size: 16px;
}

.prediction-risk {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.prediction-risk.high {
  background: linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%);
  color: white;
}

.prediction-risk.medium {
  background: linear-gradient(135deg, #ffa502 0%, #ffb142 100%);
  color: white;
}

.prediction-risk.low {
  background: linear-gradient(135deg, #26de81 0%, #4cd97b 100%);
  color: white;
}

.prediction-details {
  color: #4b5563;
  font-size: 14px;
  margin-bottom: 20px;
  line-height: 1.6;
  background: #f9fafb;
  padding: 12px;
  border-radius: 8px;
  border-left: 3px solid #e5e7eb;
}

.ai-insights {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  position: relative;
}

.ai-insights h4 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-insights h4::before {
  content: '💡';
  font-size: 20px;
}

.insights-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.insight-item:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.insight-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.insight-text {
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
}

@media (max-width: 768px) {
  .predictions-grid {
    grid-template-columns: 1fr;
  }
  
  .ai-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
