<template>
  <el-card>
    <div style="display:flex;flex-direction:column;gap:12px">
      <div style="font-size:18px;font-weight:700">工作区</div>
      <div style="opacity:0.8">通过粘贴数据集ID打开数据集仪表板。</div>

      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
        <el-input v-model="datasetId" placeholder="数据集ID" style="width:360px" />
        <el-button type="primary" :disabled="!datasetId" @click="go">打开仪表板</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const datasetId = ref('')
const router = useRouter()

function go() {
  router.push(`/dashboard/${datasetId.value}`)
}
</script>
