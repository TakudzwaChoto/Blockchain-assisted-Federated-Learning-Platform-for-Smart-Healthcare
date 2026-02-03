<template>
  <div style="display:flex;flex-direction:column;gap:12px">
    <global-filters />

    <el-card>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:space-between">
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
          <div style="font-weight:800">仪表板构建器</div>
          <el-select v-model="activeId" style="width:220px" @change="onSelect">
            <el-option v-for="d in dashboards" :key="d.id" :label="d.name" :value="d.id" />
          </el-select>
          <el-button @click="newDashboard">新建</el-button>
        </div>

        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <el-button type="primary" @click="addWidget('trend')">添加趋势</el-button>
          <el-button type="primary" @click="addWidget('forecast')">添加预测</el-button>
          <el-button type="primary" @click="addWidget('associations')">添加关联</el-button>
          <el-button type="success" @click="save">保存</el-button>
        </div>
      </div>
    </el-card>

    <!-- Simple widget display instead of grid layout -->
    <el-card>
      <div style="display:flex;flex-direction:column;gap:16px">
        <div v-for="item in layout" :key="item.i" style="border:1px solid #e0e0e0;border-radius:8px;padding:16px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
            <div style="font-weight:700">{{ widgets[item.i]?.type || item.i }}</div>
            <el-button size="small" type="danger" @click="remove(item.i)">删除</el-button>
          </div>
          <widget-renderer :widget="widgets[item.i]" :dataset-id="datasetId" />
        </div>
        
        <div v-if="layout.length === 0" style="text-align:center;padding:40px;color:#666">
          <div>暂无组件</div>
          <div style="margin-top:8px">点击上方按钮添加分析组件</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GlobalFilters from '../components/GlobalFilters.vue'
import WidgetRenderer from '../components/WidgetRenderer.vue'

// Fixed dataset to prevent store issues
const datasetId = ref('blood-domain-dataset')

// Simple dashboard data
const dashboards = ref([
  { id: 'default', name: 'Default Dashboard', layout: [], widgets: {} }
])
const activeId = ref('default')

const layout = ref([])
const widgets = ref({})

// Simplified functions to prevent hanging
function onSelect() {
  console.log('Dashboard selected:', activeId.value)
}

function save() {
  console.log('Dashboard saved')
}

function newDashboard() {
  const id = `dash_${Date.now()}`
  dashboards.value.push({
    id,
    name: `Dashboard ${dashboards.value.length + 1}`,
    layout: [],
    widgets: {}
  })
  activeId.value = id
  layout.value = []
  widgets.value = {}
}

function addWidget(type) {
  const id = `${type}_${Date.now()}`
  widgets.value[id] = { type }
  layout.value.push({ i: id, x: 0, y: 0, w: 6, h: 8 })
}

function remove(id) {
  layout.value = layout.value.filter((x) => x.i !== id)
  const next = { ...widgets.value }
  delete next[id]
  widgets.value = next
}
</script>
