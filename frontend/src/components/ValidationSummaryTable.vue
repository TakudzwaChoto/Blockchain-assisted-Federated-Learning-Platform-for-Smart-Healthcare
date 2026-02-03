<template>
  <el-table :data="rows" style="width:100%" height="260">
    <el-table-column prop="severity" label="Severity" width="120" />
    <el-table-column prop="count" label="Count" width="120" />
    <el-table-column prop="examples" label="Examples" />
  </el-table>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  validationResults: { type: Object, default: null }
})

const rows = computed(() => {
  const vr = props.validationResults
  if (!vr) return []

  const summary = vr.summary_by_severity || {}
  const examples = vr.examples_by_severity || {}

  return Object.keys(summary).map((severity) => {
    const ex = examples[severity] || []
    const preview = ex
      .slice(0, 3)
      .map((e) => (typeof e === 'string' ? e : e.message || JSON.stringify(e)))
      .join(' | ')

    return {
      severity,
      count: summary[severity],
      examples: preview
    }
  })
})
</script>
