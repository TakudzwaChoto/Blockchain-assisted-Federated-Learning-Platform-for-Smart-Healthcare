<template>
  <el-card shadow="never">
    <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
      <div style="font-weight:700">Filters</div>

      <el-select v-model="datasetId" placeholder="选择数据集" style="width:320px" @change="onDatasetChange">
        <el-option label="血液领域数据集" value="blood-domain-dataset" />
        <el-option label="测试数据集" value="test-dataset" />
      </el-select>

      <el-select v-model="dimension" style="width:200px" @change="onDimensionChange">
        <el-option label="时间" value="time" />
        <el-option label="血型" value="blood_type" />
        <el-option label="捐赠类型" value="donation_type" />
        <el-option label="性别" value="gender" />
        <el-option label="年龄组" value="age_group" />
        <el-option label="地区" value="region" />
      </el-select>

      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="to"
        start-placeholder="开始"
        end-placeholder="结束"
        @change="onDateRangeChange"
      />

      <el-button @click="reset">重置</el-button>
    </div>
  </el-card>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useWorkspaceStore } from '../stores/workspaceStore'

const store = useWorkspaceStore()
store.load()

const datasetId = ref(store.datasetId)
const dimension = ref(store.filters.dimension)
const dateRange = ref(store.filters.dateRange)

watch(
  () => store.datasetId,
  (v) => {
    datasetId.value = v
  }
)

function onDatasetChange() {
  store.setDataset(datasetId.value)
}

function onDimensionChange() {
  store.setFilters({ dimension: dimension.value })
}

function onDateRangeChange() {
  store.setFilters({ dateRange: dateRange.value })
}

function reset() {
  datasetId.value = 'blood-domain-dataset'
  dateRange.value = null
  dimension.value = 'time'
  store.setDataset('blood-domain-dataset')
  store.setFilters({ dateRange: null, dimension: 'time' })
}
</script>
