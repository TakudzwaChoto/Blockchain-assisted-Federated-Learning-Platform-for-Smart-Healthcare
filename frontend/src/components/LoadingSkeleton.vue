<template>
  <div class="skeleton-wrapper">
    <!-- KPI Cards Skeleton -->
    <el-row :gutter="16" v-if="type === 'kpi'">
      <el-col :span="6" v-for="i in 4" :key="i">
        <el-skeleton animated>
          <template #template>
            <el-skeleton-item variant="rect" style="height: 80px; border-radius: 8px;" />
          </template>
        </el-skeleton>
      </el-col>
    </el-row>

    <!-- Chart Skeleton -->
    <el-skeleton animated v-else-if="type === 'chart'">
      <template #template>
        <el-skeleton-item variant="rect" style="height: 400px; border-radius: 8px;" />
      </template>
    </el-skeleton>

    <!-- Table Skeleton -->
    <el-skeleton animated v-else-if="type === 'table'">
      <template #template>
        <div style="padding: 16px;">
          <el-skeleton-item variant="text" style="height: 20px; margin-bottom: 12px;" />
          <el-skeleton-item variant="text" style="height: 20px; margin-bottom: 12px;" v-for="i in 5" :key="i" />
        </div>
      </template>
    </el-skeleton>

    <!-- Card Skeleton -->
    <el-skeleton animated v-else>
      <template #template>
        <el-skeleton-item variant="rect" style="height: 120px; border-radius: 8px;" />
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'card',
    validator: (value) => ['kpi', 'chart', 'table', 'card'].includes(value)
  }
})
</script>

<style scoped>
.skeleton-wrapper {
  width: 100%;
}
</style>
