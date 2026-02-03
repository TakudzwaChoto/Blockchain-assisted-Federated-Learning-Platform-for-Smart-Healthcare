<template>
  <div style="width:100%">
    <v-chart :option="option" autoresize style="height:360px" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  LineChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent
])

const props = defineProps({
  title: { type: String, default: '' },
  x: { type: Array, default: () => [] },
  series: { type: Array, default: () => [] },
  kind: { type: String, default: 'line' }
})

const option = computed(() => {
  return {
    title: props.title ? { text: props.title, left: 'center' } : undefined,
    tooltip: { trigger: 'axis' },
    legend: { top: 28 },
    grid: { left: 40, right: 20, top: 70, bottom: 50 },
    dataZoom: [{ type: 'inside' }, { type: 'slider' }],
    xAxis: { type: 'category', data: props.x, axisLabel: { rotate: 35 } },
    yAxis: { type: 'value' },
    series: props.series.map((s) => ({
      name: s.name,
      type: props.kind,
      smooth: props.kind === 'line',
      data: s.data
    }))
  }
})
</script>
