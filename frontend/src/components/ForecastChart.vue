<template>
  <div style="width:100%">
    <v-chart :option="option" autoresize style="height:380px" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent, DataZoomComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent, DataZoomComponent])

const props = defineProps({
  title: { type: String, default: 'Forecast' },
  forecasts: { type: Object, default: null }
})

function buildSeries(forecasts) {
  const out = []
  if (!forecasts) return out

  const models = forecasts.forecasts || {}
  for (const [model, f] of Object.entries(models)) {
    const x = (f.forecast_values || []).map((p) => p.date)
    const y = (f.forecast_values || []).map((p) => p.value)
    out.push({ name: model, x, y, ci: f.confidence_intervals || [] })
  }
  return out
}

const parsed = computed(() => buildSeries(props.forecasts))

const option = computed(() => {
  const allX = parsed.value.length ? parsed.value[0].x : []

  const series = []
  for (const s of parsed.value) {
    // Main line
    series.push({
      name: s.name,
      type: 'line',
      smooth: true,
      showSymbol: false,
      data: s.y
    })

    // Confidence band (if lengths match)
    if (Array.isArray(s.ci) && s.ci.length === s.y.length) {
      const lower = s.ci.map((t) => t[0])
      const upper = s.ci.map((t) => t[1])

      series.push({
        name: `${s.name} (lower)`,
        type: 'line',
        data: lower,
        lineStyle: { opacity: 0 },
        stack: `${s.name}-band`,
        symbol: 'none'
      })

      series.push({
        name: `${s.name} (upper)`,
        type: 'line',
        data: upper,
        lineStyle: { opacity: 0 },
        areaStyle: { opacity: 0.12 },
        stack: `${s.name}-band`,
        symbol: 'none'
      })
    }
  }

  return {
    title: { text: props.title, left: 'center' },
    tooltip: { trigger: 'axis' },
    legend: { top: 28 },
    grid: { left: 40, right: 20, top: 70, bottom: 60 },
    dataZoom: [{ type: 'inside' }, { type: 'slider' }],
    xAxis: { type: 'category', data: allX, axisLabel: { rotate: 35 } },
    yAxis: { type: 'value' },
    series
  }
})
</script>
