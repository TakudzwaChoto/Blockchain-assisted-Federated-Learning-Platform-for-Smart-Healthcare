<template>
  <div style="display:grid;grid-template-columns:1fr;gap:12px">
    <time-series-chart
      v-if="volumeChart.x.length"
      title="Trend: Donation volume"
      :x="volumeChart.x"
      :series="volumeChart.series"
      kind="line"
    />
    <time-series-chart
      v-if="donorChart.x.length"
      title="Trend: Unique donors"
      :x="donorChart.x"
      :series="donorChart.series"
      kind="line"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import TimeSeriesChart from './TimeSeriesChart.vue'

const props = defineProps({
  trends: { type: Object, default: null }
})

function groupByDimension(values) {
  const map = new Map()
  for (const v of values) {
    const dim = v.dimension || 'all'
    const p = v.period
    if (!map.has(dim)) map.set(dim, new Map())
    map.get(dim).set(p, v)
  }
  return map
}

function buildChart(values, field) {
  if (!Array.isArray(values) || !values.length) return { x: [], series: [] }

  const periods = Array.from(new Set(values.map((v) => v.period))).sort()
  const byDim = groupByDimension(values)

  const series = []
  for (const [dim, m] of byDim.entries()) {
    series.push({
      name: dim,
      data: periods.map((p) => (m.get(p)?.[field] ?? 0))
    })
  }

  return { x: periods, series }
}

const timeTrendValues = computed(() => {
  // Backend returns: { dataset_id, trends: { time: BloodTrend, ... } }
  const t = props.trends?.trends
  if (!t) return []
  const time = t.time || t.Time || null
  return time?.values || []
})

const volumeChart = computed(() => buildChart(timeTrendValues.value, 'volume'))
const donorChart = computed(() => buildChart(timeTrendValues.value, 'donors'))
</script>
