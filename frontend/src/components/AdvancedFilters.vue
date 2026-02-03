<template>
  <el-card class="advanced-filters">
    <template #header>
      <div class="filter-header">
        <span>Advanced Filters</span>
        <div class="filter-actions">
          <el-button size="small" @click="resetFilters">Reset</el-button>
          <el-button size="small" type="primary" @click="applyFilters">Apply</el-button>
          <el-dropdown @command="saveFilter" trigger="click">
            <el-button size="small">
              Save Filter
              <el-icon><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="save">Save Current</el-dropdown-item>
                <el-dropdown-item command="manage">Manage Saved</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </template>

    <el-form :model="filters" label-width="120px" label-position="top">
      <!-- Date Range Filter -->
      <el-form-item label="Date Range">
        <el-date-picker
          v-model="filters.dateRange"
          type="daterange"
          range-separator="To"
          start-placeholder="Start date"
          end-placeholder="End date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        />
      </el-form-item>

      <!-- Blood Type Filter -->
      <el-form-item label="Blood Type">
        <el-select
          v-model="filters.bloodTypes"
          multiple
          placeholder="Select blood types"
          style="width: 100%"
        >
          <el-option
            v-for="type in bloodTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>
      </el-form-item>

      <!-- Donation Type Filter -->
      <el-form-item label="Donation Type">
        <el-select
          v-model="filters.donationTypes"
          multiple
          placeholder="Select donation types"
          style="width: 100%"
        >
          <el-option
            v-for="type in donationTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>
      </el-form-item>

      <!-- Age Range Filter -->
      <el-form-item label="Age Range">
        <el-slider
          v-model="filters.ageRange"
          range
          :min="18"
          :max="65"
          :marks="{ 18: '18', 30: '30', 45: '45', 65: '65' }"
          style="width: 100%"
        />
      </el-form-item>

      <!-- Volume Range Filter -->
      <el-form-item label="Volume Range (ml)">
        <el-slider
          v-model="filters.volumeRange"
          range
          :min="200"
          :max="500"
          :marks="{ 200: '200', 300: '300', 400: '400', 500: '500' }"
          style="width: 100%"
        />
      </el-form-item>

      <!-- Gender Filter -->
      <el-form-item label="Gender">
        <el-radio-group v-model="filters.gender">
          <el-radio label="all">All</el-radio>
          <el-radio label="male">Male</el-radio>
          <el-radio label="female">Female</el-radio>
          <el-radio label="other">Other</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- Location Filter -->
      <el-form-item label="Location">
        <el-input
          v-model="filters.location"
          placeholder="Enter location (partial match)"
          clearable
        />
      </el-form-item>

      <!-- Custom Numeric Filters -->
      <el-form-item label="Custom Filters">
        <div class="custom-filters">
          <div
            v-for="(filter, index) in filters.customFilters"
            :key="index"
            class="custom-filter-row"
          >
            <el-input
              v-model="filter.field"
              placeholder="Field name"
              style="width: 150px; margin-right: 8px"
            />
            <el-select
              v-model="filter.operator"
              style="width: 120px; margin-right: 8px"
            >
              <el-option label="Equals" value="eq" />
              <el-option label="Not Equals" value="ne" />
              <el-option label="Greater Than" value="gt" />
              <el-option label="Less Than" value="lt" />
              <el-option label="Contains" value="contains" />
            </el-select>
            <el-input
              v-model="filter.value"
              placeholder="Value"
              style="width: 150px; margin-right: 8px"
            />
            <el-button
              size="small"
              type="danger"
              @click="removeCustomFilter(index)"
            >
              Remove
            </el-button>
          </div>
          <el-button size="small" @click="addCustomFilter">Add Filter</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-card>

  <!-- Saved Filters Dialog -->
  <el-dialog v-model="savedFiltersDialog" title="Manage Saved Filters" width="600px">
    <div class="saved-filters">
      <div
        v-for="(filter, index) in savedFilters"
        :key="index"
        class="saved-filter-item"
      >
        <div class="filter-info">
          <div class="filter-name">{{ filter.name }}</div>
          <div class="filter-description">{{ filter.description }}</div>
          <div class="filter-date">Created: {{ formatDate(filter.createdAt) }}</div>
        </div>
        <div class="filter-actions">
          <el-button size="small" @click="loadSavedFilter(filter)">Load</el-button>
          <el-button size="small" type="danger" @click="deleteSavedFilter(index)">Delete</el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const emit = defineEmits(['filters-changed'])

const notificationStore = useNotificationStore()

const bloodTypes = [
  { label: 'A+', value: 'A+' },
  { label: 'A-', value: 'A-' },
  { label: 'B+', value: 'B+' },
  { label: 'B-', value: 'B-' },
  { label: 'AB+', value: 'AB+' },
  { label: 'AB-', value: 'AB-' },
  { label: 'O+', value: 'O+' },
  { label: 'O-', value: 'O-' }
]

const donationTypes = [
  { label: 'Whole Blood', value: 'whole_blood' },
  { label: 'Platelets', value: 'platelets' },
  { label: 'Plasma', value: 'plasma' },
  { label: 'Red Blood Cells', value: 'red_blood_cells' }
]

const filters = reactive({
  dateRange: null,
  bloodTypes: [],
  donationTypes: [],
  ageRange: [18, 65],
  volumeRange: [200, 500],
  gender: 'all',
  location: '',
  customFilters: []
})

const savedFilters = ref([])
const savedFiltersDialog = ref(false)

const resetFilters = () => {
  filters.dateRange = null
  filters.bloodTypes = []
  filters.donationTypes = []
  filters.ageRange = [18, 65]
  filters.volumeRange = [200, 500]
  filters.gender = 'all'
  filters.location = ''
  filters.customFilters = []
}

const applyFilters = () => {
  emit('filters-changed', { ...filters })
  notificationStore.success('Filters applied successfully')
}

const addCustomFilter = () => {
  filters.customFilters.push({
    field: '',
    operator: 'eq',
    value: ''
  })
}

const removeCustomFilter = (index) => {
  filters.customFilters.splice(index, 1)
}

const saveFilter = (command) => {
  if (command === 'save') {
    const name = prompt('Enter filter name:')
    if (name) {
      const filter = {
        name,
        description: `Custom filter with ${filters.customFilters.length} custom conditions`,
        createdAt: new Date().toISOString(),
        filters: JSON.parse(JSON.stringify(filters))
      }
      savedFilters.value.push(filter)
      localStorage.setItem('savedFilters', JSON.stringify(savedFilters.value))
      notificationStore.success('Filter saved successfully')
    }
  } else if (command === 'manage') {
    savedFiltersDialog.value = true
  }
}

const loadSavedFilter = (savedFilter) => {
  Object.assign(filters, savedFilter.filters)
  savedFiltersDialog.value = false
  notificationStore.success(`Loaded filter: ${savedFilter.name}`)
  applyFilters()
}

const deleteSavedFilter = (index) => {
  const filter = savedFilters.value[index]
  savedFilters.value.splice(index, 1)
  localStorage.setItem('savedFilters', JSON.stringify(savedFilters.value))
  notificationStore.warning(`Deleted filter: ${filter.name}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  const saved = localStorage.getItem('savedFilters')
  if (saved) {
    savedFilters.value = JSON.parse(saved)
  }
})
</script>

<style scoped>
.advanced-filters {
  margin-bottom: 20px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-actions {
  display: flex;
  gap: 8px;
}

.custom-filters {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 12px;
  background-color: #f8f9fa;
}

.custom-filter-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.saved-filters {
  max-height: 400px;
  overflow-y: auto;
}

.saved-filter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e4e7ed;
}

.saved-filter-item:last-child {
  border-bottom: none;
}

.filter-info {
  flex: 1;
}

.filter-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.filter-description {
  color: #909399;
  font-size: 14px;
  margin-bottom: 4px;
}

.filter-date {
  color: #c0c4cc;
  font-size: 12px;
}

.filter-actions {
  display: flex;
  gap: 8px;
}
</style>
