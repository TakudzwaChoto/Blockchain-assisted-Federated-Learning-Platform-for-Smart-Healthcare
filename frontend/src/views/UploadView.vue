<template>
  <el-card>
    <div style="display:flex;flex-direction:column;gap:12px">
      <div style="font-size:18px;font-weight:600">上传数据集</div>
      <el-upload
        drag
        :auto-upload="false"
        :on-change="onFileChange"
        :limit="1"
        accept=".csv,.xlsx,.xls,.json,.jsonl,.ndjson"
      >
        <div style="padding:20px">拖放文件到此处或点击选择</div>
      </el-upload>

      <div style="display:flex;gap:8px">
        <el-button type="primary" :disabled="!file" :loading="loading" @click="upload">上传</el-button>
      </div>

      <el-alert v-if="error" type="error" :closable="false" :title="error" />

      <el-descriptions v-if="result" title="已上传" :column="2" border>
        <el-descriptions-item label="数据集ID">{{ result.dataset_id }}</el-descriptions-item>
        <el-descriptions-item label="文件名">{{ result.filename }}</el-descriptions-item>
        <el-descriptions-item label="行数">{{ result.rows }}</el-descriptions-item>
        <el-descriptions-item label="列数">{{ result.cols }}</el-descriptions-item>
      </el-descriptions>

      <el-button v-if="result" type="success" @click="goDashboard">前往仪表板</el-button>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadDataset } from '../services/api'

const router = useRouter()
const file = ref(null)
const loading = ref(false)
const error = ref('')
const result = ref(null)

function onFileChange(uploadFile) {
  error.value = ''
  result.value = null
  file.value = uploadFile.raw
}

async function upload() {
  if (!file.value) return
  loading.value = true
  error.value = ''

  try {
    result.value = await uploadDataset(file.value)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loading.value = false
  }
}

function goDashboard() {
  router.push(`/dashboard/${result.value.dataset_id}`)
}
</script>
