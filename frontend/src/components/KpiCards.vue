<template>
  <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
    <el-card v-for="k in items" :key="k.label" shadow="never">
      <div style="display:flex;flex-direction:column;gap:6px">
        <div style="opacity:0.75;font-size:12px">{{ k.label }}</div>
        <div style="font-size:22px;font-weight:800">{{ k.value }}</div>
        <div v-if="k.sub" style="opacity:0.75;font-size:12px">{{ k.sub }}</div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] }
})
</script>
