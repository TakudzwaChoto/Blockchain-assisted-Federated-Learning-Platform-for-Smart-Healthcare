<template>
  <div class="animated-charts">
    <v-chart
      :option="animatedOption"
      :style="{ height: height }"
      autoresize
      :loading="loading"
      @click="handleChartClick"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
])

const props = defineProps({
  data: { type: Object, required: true },
  config: { type: Object, default: () => ({}) },
  height: { type: String, default: '400px' },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['chart-click'])

const animatedOption = computed(() => ({
  ...baseOption,
  ...props.config,
  animation: true,
  animationDuration: 1500,
  animationEasing: 'cubicOut',
  animationDelay: (idx) => idx * 100
}))

const baseOption = computed(() => {
  if (!props.data) return {}
  
  const chartType = props.config.chartType || 'bar'
  
  if (chartType === 'bar') {
    return {
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: props.data.labels || [] },
      yAxis: { type: 'value' },
      series: [{
        type: 'bar',
        data: props.data.datasets?.[0]?.data || [],
        itemStyle: {
          color: new Proxy({}, {
            get(_, key) {
              const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']
              return colors[key % colors.length]
            }
          })
        }
      }]
    }
  } else if (chartType === 'line') {
    return {
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: props.data.labels || [] },
      yAxis: { type: 'value' },
      series: [{
        type: 'line',
        data: props.data.datasets?.[0]?.data || [],
        smooth: true,
        lineStyle: { width: 3 },
        areaStyle: { opacity: 0.3 }
      }]
    }
  } else if (chartType === 'pie') {
    return {
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: props.data.labels?.map((label, i) => ({
          name: label,
          value: props.data.datasets?.[0]?.data?.[i] || 0
        })) || []
      }]
    }
  }
  
  return {}
})

const handleChartClick = (params) => {
  emit('chart-click', params)
}
</script>

<style scoped>
.animated-charts {
  width: 100%;
  height: 100%;
}
</style>
