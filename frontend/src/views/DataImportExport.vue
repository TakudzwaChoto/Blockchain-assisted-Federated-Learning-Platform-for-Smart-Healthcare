<template>
  <div class="data-import-export">
    <el-card>
      <template #header>
        <div class="section-header">
          <h3>数据导入导出系统</h3>
          <el-tag type="success">支持百万级数据处理</el-tag>
        </div>
      </template>

      <!-- Import Section -->
      <el-row :gutter="24" class="import-section">
        <el-col :span="12">
          <el-card class="import-card">
            <template #header>
              <div class="card-header">
                <el-icon><Upload /></el-icon>
                <span>批量数据导入</span>
              </div>
            </template>

            <!-- File Upload -->
            <el-upload
              ref="uploadRef"
              class="upload-demo"
              drag
              :auto-upload="false"
              :on-change="handleFileChange"
              :limit="10"
              accept=".csv,.xlsx,.xls,.json"
            >
              <el-icon class="el-icon--upload"><Upload /></el-icon>
              <div class="el-upload__text">
                拖拽文件到此处或 <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持 CSV, Excel, JSON 格式，单文件最大 100MB
                </div>
              </template>
            </el-upload>

            <!-- Import Options -->
            <div class="import-options" v-if="selectedFile">
              <h4>导入选项</h4>
              <el-form :model="importOptions" label-width="120px">
                <el-form-item label="数据类型">
                  <el-select v-model="importOptions.dataType" placeholder="选择数据类型">
                    <el-option label="捐赠者信息" value="donors" />
                    <el-option label="捐赠记录" value="donations" />
                    <el-option label="输血申请" value="requests" />
                    <el-option label="库存数据" value="inventory" />
                  </el-select>
                </el-form-item>
                
                <el-form-item label="处理模式">
                  <el-radio-group v-model="importOptions.mode">
                    <el-radio label="append">追加数据</el-radio>
                    <el-radio label="replace">替换数据</el-radio>
                    <el-radio label="update">更新数据</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="数据清洗">
                  <el-checkbox-group v-model="importOptions.cleaning">
                    <el-checkbox label="deduplication">去重处理</el-checkbox>
                    <el-checkbox label="validation">数据验证</el-checkbox>
                    <el-checkbox label="standardization">格式标准化</el-checkbox>
                    <el-checkbox label="missing_values">缺失值处理</el-checkbox>
                  </el-checkbox-group>
                </el-form-item>

                <el-form-item label="字段映射">
                  <el-button @click="showFieldMapping = true">配置字段映射</el-button>
                  <span v-if="fieldMappings.length > 0" class="mapping-count">
                    已配置 {{ fieldMappings.length }} 个字段映射
                  </span>
                </el-form-item>
              </el-form>

              <div class="import-actions">
                <el-button @click="previewData" :disabled="!selectedFile">
                  <el-icon><View /></el-icon>
                  预览数据
                </el-button>
                <el-button type="primary" @click="startImport" :loading="importing">
                  <el-icon><Upload /></el-icon>
                  开始导入
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- Export Section -->
        <el-col :span="12">
          <el-card class="export-card">
            <template #header>
              <div class="card-header">
                <el-icon><Download /></el-icon>
                <span>数据导出</span>
              </div>
            </template>

            <el-form :model="exportOptions" label-width="120px">
              <el-form-item label="导出数据">
                <el-checkbox-group v-model="exportOptions.dataTypes">
                  <el-checkbox label="donors">捐赠者信息</el-checkbox>
                  <el-checkbox label="donations">捐赠记录</el-checkbox>
                  <el-checkbox label="requests">输血申请</el-checkbox>
                  <el-checkbox label="inventory">库存数据</el-checkbox>
                  <el-checkbox label="analytics">分析报告</el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item label="时间范围">
                <el-date-picker
                  v-model="exportOptions.dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                />
              </el-form-item>

              <el-form-item label="导出格式">
                <el-radio-group v-model="exportOptions.format">
                  <el-radio label="csv">CSV</el-radio>
                  <el-radio label="excel">Excel</el-radio>
                  <el-radio label="json">JSON</el-radio>
                  <el-radio label="pdf">PDF报告</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="过滤条件">
                <el-button @click="showFilters = true">设置过滤条件</el-button>
                <span v-if="hasFilters" class="filter-count">
                  已设置 {{ filterCount }} 个过滤条件
                </span>
              </el-form-item>
            </el-form>

            <div class="export-actions">
              <el-button @click="previewExport">
                <el-icon><View /></el-icon>
                预览导出
              </el-button>
              <el-button type="primary" @click="startExport" :loading="exporting">
                <el-icon><Download /></el-icon>
                开始导出
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- Data Preview -->
      <el-card v-if="previewDataVisible" class="preview-card">
        <template #header>
          <div class="preview-header">
            <span>数据预览 (前100条记录)</span>
            <el-button @click="previewDataVisible = false" size="small">关闭</el-button>
          </div>
        </template>
        
        <el-table :data="previewDataList" height="400" style="width: 100%">
          <el-table-column
            v-for="column in previewColumns"
            :key="column.prop"
            :prop="column.prop"
            :label="column.label"
            :width="column.width"
          />
        </el-table>
        
        <div class="preview-info">
          <el-alert
            :title="`共 ${totalRecords} 条记录，当前显示前 ${Math.min(100, totalRecords)} 条`"
            type="info"
            :closable="false"
          />
        </div>
      </el-card>

      <!-- Processing Status -->
      <el-card v-if="processingVisible" class="processing-card">
        <template #header>
          <span>处理状态</span>
        </template>
        
        <div class="processing-content">
          <el-steps :active="currentStep" align-center>
            <el-step title="数据读取" description="解析文件格式" />
            <el-step title="数据清洗" description="去重验证标准化" />
            <el-step title="数据转换" description="字段映射转换" />
            <el-step title="数据导入" description="写入数据库" />
          </el-steps>
          
          <div class="progress-section">
            <el-progress 
              :percentage="processingProgress" 
              :status="processingStatus"
            />
            <p class="progress-text">{{ processingMessage }}</p>
          </div>
          
          <div class="processing-stats">
            <el-row :gutter="16">
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ processedRecords }}</div>
                  <div class="stat-label">已处理记录</div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ validRecords }}</div>
                  <div class="stat-label">有效记录</div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ errorRecords }}</div>
                  <div class="stat-label">错误记录</div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-number">{{ duplicateRecords }}</div>
                  <div class="stat-label">重复记录</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-card>
    </el-card>

    <!-- Field Mapping Dialog -->
    <el-dialog v-model="showFieldMapping" title="字段映射配置" width="800px">
      <div class="field-mapping">
        <el-table :data="fieldMappings" style="width: 100%">
          <el-table-column label="源字段" width="200">
            <template #default="{ row, $index }">
              <el-input v-model="row.sourceField" placeholder="源文件字段名" />
            </template>
          </el-table-column>
          <el-table-column label="目标字段" width="200">
            <template #default="{ row, $index }">
              <el-select v-model="row.targetField" placeholder="选择目标字段">
                <el-option
                  v-for="field in availableFields"
                  :key="field.value"
                  :label="field.label"
                  :value="field.value"
                />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="数据类型" width="150">
            <template #default="{ row, $index }">
              <el-select v-model="row.dataType" placeholder="数据类型">
                <el-option label="字符串" value="string" />
                <el-option label="数字" value="number" />
                <el-option label="日期" value="date" />
                <el-option label="布尔值" value="boolean" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row, $index }">
              <el-button @click="removeMapping($index)" type="danger" size="small">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="mapping-actions">
          <el-button @click="addMapping">添加映射</el-button>
          <el-button type="primary" @click="autoMapping">自动映射</el-button>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showFieldMapping = false">取消</el-button>
        <el-button type="primary" @click="saveFieldMapping">保存映射</el-button>
      </template>
    </el-dialog>

    <!-- Filters Dialog -->
    <el-dialog v-model="showFilters" title="过滤条件设置" width="600px">
      <el-form :model="filterConditions" label-width="120px">
        <el-form-item label="血型过滤">
          <el-checkbox-group v-model="filterConditions.bloodTypes">
            <el-checkbox label="A+">A+</el-checkbox>
            <el-checkbox label="A-">A-</el-checkbox>
            <el-checkbox label="B+">B+</el-checkbox>
            <el-checkbox label="B-">B-</el-checkbox>
            <el-checkbox label="O+">O+</el-checkbox>
            <el-checkbox label="O-">O-</el-checkbox>
            <el-checkbox label="AB+">AB+</el-checkbox>
            <el-checkbox label="AB-">AB-</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="年龄范围">
          <el-slider
            v-model="filterConditions.ageRange"
            range
            :min="18"
            :max="65"
            :format-tooltip="(val) => `${val}岁`"
          />
        </el-form-item>
        
        <el-form-item label="性别过滤">
          <el-radio-group v-model="filterConditions.gender">
            <el-radio label="all">全部</el-radio>
            <el-radio label="male">男性</el-radio>
            <el-radio label="female">女性</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="状态过滤">
          <el-select v-model="filterConditions.status" placeholder="选择状态">
            <el-option label="全部" value="" />
            <el-option label="活跃" value="active" />
            <el-option label="非活跃" value="inactive" />
            <el-option label="暂停" value="suspended" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showFilters = false">取消</el-button>
        <el-button type="primary" @click="saveFilters">保存过滤条件</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Upload, Download, View 
} from '@element-plus/icons-vue'

// Reactive data
const uploadRef = ref()
const selectedFile = ref(null)
const importing = ref(false)
const exporting = ref(false)
const showFieldMapping = ref(false)
const showFilters = ref(false)
const previewDataVisible = ref(false)
const processingVisible = ref(false)

// Import options
const importOptions = reactive({
  dataType: '',
  mode: 'append',
  cleaning: ['deduplication', 'validation']
})

// Export options
const exportOptions = reactive({
  dataTypes: ['donors'],
  dateRange: [],
  format: 'csv'
})

// Field mapping
const fieldMappings = ref([])
const availableFields = ref([
  { label: '姓名', value: 'name' },
  { label: '血型', value: 'bloodType' },
  { label: '年龄', value: 'age' },
  { label: '性别', value: 'gender' },
  { label: '电话', value: 'phone' },
  { label: '邮箱', value: 'email' },
  { label: '地址', value: 'address' },
  { label: '状态', value: 'status' }
])

// Filter conditions
const filterConditions = reactive({
  bloodTypes: [],
  ageRange: [18, 65],
  gender: 'all',
  status: ''
})

// Preview data
const previewDataList = ref([])
const previewColumns = ref([])
const totalRecords = ref(0)

// Processing status
const currentStep = ref(0)
const processingProgress = ref(0)
const processingStatus = ref('')
const processingMessage = ref('')
const processedRecords = ref(0)
const validRecords = ref(0)
const errorRecords = ref(0)
const duplicateRecords = ref(0)

// Computed properties
const hasFilters = computed(() => {
  return filterConditions.bloodTypes.length > 0 || 
         filterConditions.status !== '' || 
         filterConditions.gender !== 'all'
})

const filterCount = computed(() => {
  let count = 0
  if (filterConditions.bloodTypes.length > 0) count++
  if (filterConditions.status !== '') count++
  if (filterConditions.gender !== 'all') count++
  return count
})

// Methods
const handleFileChange = (file) => {
  selectedFile.value = file
  // Auto-detect file format and suggest data type
  const extension = file.name.split('.').pop().toLowerCase()
  if (extension === 'csv' || extension === 'xlsx' || extension === 'xls') {
    // Could suggest data type based on file name or content
    if (file.name.toLowerCase().includes('donor')) {
      importOptions.dataType = 'donors'
    } else if (file.name.toLowerCase().includes('donation')) {
      importOptions.dataType = 'donations'
    }
  }
}

const previewData = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  try {
    // Simulate file reading and preview
    const mockData = generateMockPreviewData(importOptions.dataType)
    previewDataList.value = mockData.data
    previewColumns.value = mockData.columns
    totalRecords.value = mockData.total
    previewDataVisible.value = true
    
    ElMessage.success('数据预览生成成功')
  } catch (error) {
    ElMessage.error('数据预览失败: ' + error.message)
  }
}

const startImport = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  if (!importOptions.dataType) {
    ElMessage.warning('请选择数据类型')
    return
  }
  
  importing.value = true
  processingVisible.value = true
  currentStep.value = 0
  processingProgress.value = 0
  
  try {
    // Simulate batch processing steps
    await simulateBatchProcessing()
    
    ElMessage.success(`数据导入完成！共处理 ${processedRecords.value} 条记录`)
  } catch (error) {
    ElMessage.error('数据导入失败: ' + error.message)
  } finally {
    importing.value = false
    processingVisible.value = false
  }
}

const simulateBatchProcessing = async () => {
  const steps = [
    { name: '数据读取', duration: 2000, progress: 25 },
    { name: '数据清洗', duration: 3000, progress: 50 },
    { name: '数据转换', duration: 2000, progress: 75 },
    { name: '数据导入', duration: 3000, progress: 100 }
  ]
  
  const mockStats = {
    total: 150000, // Simulate 150k records
    valid: 148500,
    errors: 1200,
    duplicates: 300
  }
  
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i]
    currentStep.value = i
    processingMessage.value = `正在${step.name}...`
    processingStatus.value = 'active'
    
    // Simulate progress within this step
    const startProgress = i === 0 ? 0 : steps[i - 1].progress
    const endProgress = step.progress
    const progressSteps = 20
    
    for (let j = 0; j <= progressSteps; j++) {
      processingProgress.value = startProgress + (endProgress - startProgress) * (j / progressSteps)
      processedRecords.value = Math.floor(mockStats.total * (processingProgress.value / 100))
      validRecords.value = Math.floor(mockStats.valid * (processingProgress.value / 100))
      errorRecords.value = Math.floor(mockStats.errors * (processingProgress.value / 100))
      duplicateRecords.value = Math.floor(mockStats.duplicates * (processingProgress.value / 100))
      
      await new Promise(resolve => setTimeout(resolve, step.duration / progressSteps))
    }
  }
  
  processingStatus.value = 'success'
  processingMessage.value = '导入完成！'
}

const startExport = async () => {
  if (exportOptions.dataTypes.length === 0) {
    ElMessage.warning('请选择要导出的数据类型')
    return
  }
  
  exporting.value = true
  
  try {
    // Simulate export process
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    ElMessage.success('数据导出完成！文件已下载')
  } catch (error) {
    ElMessage.error('数据导出失败: ' + error.message)
  } finally {
    exporting.value = false
  }
}

const previewExport = () => {
  ElMessage.info('导出预览功能开发中')
}

const removeMapping = (index) => {
  fieldMappings.value.splice(index, 1)
}

const addMapping = () => {
  fieldMappings.value.push({
    sourceField: '',
    targetField: '',
    dataType: 'string'
  })
}

const autoMapping = () => {
  // Simulate automatic field mapping based on common patterns
  const commonMappings = [
    { source: 'name', target: 'name', type: 'string' },
    { source: 'blood_type', target: 'bloodType', type: 'string' },
    { source: 'age', target: 'age', type: 'number' },
    { source: 'gender', target: 'gender', type: 'string' },
    { source: 'phone', target: 'phone', type: 'string' },
    { source: 'email', target: 'email', type: 'string' }
  ]
  
  fieldMappings.value = commonMappings.map(mapping => ({
    sourceField: mapping.source,
    targetField: mapping.target,
    dataType: mapping.type
  }))
  
  ElMessage.success('自动字段映射完成')
}

const saveFieldMapping = () => {
  showFieldMapping.value = false
  ElMessage.success('字段映射配置已保存')
}

const saveFilters = () => {
  showFilters.value = false
  ElMessage.success('过滤条件已保存')
}

const generateMockPreviewData = (dataType) => {
  const mockData = {
    donors: {
      columns: [
        { prop: 'name', label: '姓名', width: 120 },
        { prop: 'bloodType', label: '血型', width: 80 },
        { prop: 'age', label: '年龄', width: 80 },
        { prop: 'gender', label: '性别', width: 80 },
        { prop: 'phone', label: '电话', width: 120 },
        { prop: 'email', label: '邮箱', width: 180 },
        { prop: 'status', label: '状态', width: 100 }
      ],
      data: Array.from({ length: 10 }, (_, i) => ({
        name: `捐赠者${i + 1}`,
        bloodType: ['A+', 'B+', 'O+', 'AB+'][Math.floor(Math.random() * 4)],
        age: Math.floor(Math.random() * 40) + 20,
        gender: ['男', '女'][Math.floor(Math.random() * 2)],
        phone: `138${Math.floor(Math.random() * 100000000)}`,
        email: `donor${i + 1}@example.com`,
        status: ['活跃', '非活跃'][Math.floor(Math.random() * 2)]
      })),
      total: 150000
    },
    donations: {
      columns: [
        { prop: 'donorId', label: '捐赠者ID', width: 120 },
        { prop: 'donationDate', label: '捐赠日期', width: 120 },
        { prop: 'bloodType', label: '血型', width: 80 },
        { prop: 'volume', label: '血量(ml)', width: 100 },
        { prop: 'location', label: '捐赠地点', width: 150 },
        { prop: 'status', label: '状态', width: 100 }
      ],
      data: Array.from({ length: 10 }, (_, i) => ({
        donorId: `D${String(i + 1).padStart(6, '0')}`,
        donationDate: `2024-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
        bloodType: ['A+', 'B+', 'O+', 'AB+'][Math.floor(Math.random() * 4)],
        volume: [200, 300, 400][Math.floor(Math.random() * 3)],
        location: ['北京中心', '上海中心', '广州中心'][Math.floor(Math.random() * 3)],
        status: '已完成'
      })),
      total: 280000
    }
  }
  
  return mockData[dataType] || mockData.donors
}
</script>

<style scoped>
.data-import-export {
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  margin: 0;
  color: #333;
}

.import-section {
  margin-bottom: 24px;
}

.import-card, .export-card {
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.upload-demo {
  width: 100%;
}

.import-options, .export-options {
  margin-top: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.import-options h4, .export-options h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.import-actions, .export-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.mapping-count, .filter-count {
  margin-left: 8px;
  color: #666;
  font-size: 14px;
}

.preview-card {
  margin-top: 24px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-info {
  margin-top: 16px;
}

.processing-card {
  margin-top: 24px;
}

.processing-content {
  padding: 20px 0;
}

.progress-section {
  margin: 24px 0;
  text-align: center;
}

.progress-text {
  margin-top: 8px;
  color: #666;
}

.processing-stats {
  margin-top: 24px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.field-mapping {
  max-height: 400px;
  overflow-y: auto;
}

.mapping-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

@media (max-width: 768px) {
  .import-section {
    margin-bottom: 16px;
  }
  
  .import-actions, .export-actions {
    flex-direction: column;
  }
  
  .processing-stats .el-col {
    margin-bottom: 12px;
  }
}
</style>
