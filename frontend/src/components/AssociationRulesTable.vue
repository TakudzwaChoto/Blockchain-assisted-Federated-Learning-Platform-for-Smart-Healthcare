<template>
  <el-table :data="rules" style="width:100%" height="360">
    <el-table-column label="Antecedents" min-width="240">
      <template #default="scope">
        <el-tag v-for="a in scope.row.antecedents" :key="a" style="margin:2px">{{ a }}</el-tag>
      </template>
    </el-table-column>

    <el-table-column label="Consequents" min-width="240">
      <template #default="scope">
        <el-tag type="success" v-for="c in scope.row.consequents" :key="c" style="margin:2px">{{ c }}</el-tag>
      </template>
    </el-table-column>

    <el-table-column prop="support" label="Support" width="110" sortable />
    <el-table-column prop="confidence" label="Confidence" width="120" sortable />
    <el-table-column prop="lift" label="Lift" width="90" sortable />
  </el-table>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  associations: { type: Object, default: null }
})

const rules = computed(() => {
  const a = props.associations?.associations
  if (!a) return []
  if (Array.isArray(a.association_rules)) return a.association_rules
  if (Array.isArray(a.rules)) return a.rules
  return []
})
</script>
