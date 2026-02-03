<template>
  <el-dropdown @command="handleExport" trigger="click">
    <el-button type="primary" :loading="exporting">
      <el-icon><Download /></el-icon>
      Export
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="png">
          <el-icon><Picture /></el-icon>
          Export as PNG
        </el-dropdown-item>
        <el-dropdown-item command="pdf">
          <el-icon><Document /></el-icon>
          Export as PDF
        </el-dropdown-item>
        <el-dropdown-item command="excel">
          <el-icon><Grid /></el-icon>
          Export as Excel
        </el-dropdown-item>
        <el-dropdown-item command="csv">
          <el-icon><Tickets /></el-icon>
          Export as CSV
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { ref } from 'vue'
import { Download, Picture, Document, Grid, Tickets } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'
import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

const props = defineProps({
  data: { type: [Array, Object], required: true },
  filename: { type: String, default: 'export' },
  title: { type: String, default: 'Export' }
})

const emit = defineEmits(['export-start', 'export-complete'])

const notificationStore = useNotificationStore()
const exporting = ref(false)

const handleExport = async (format) => {
  exporting.value = true
  emit('export-start', format)

  try {
    switch (format) {
      case 'png':
        await exportAsPNG()
        break
      case 'pdf':
        await exportAsPDF()
        break
      case 'excel':
        await exportAsExcel()
        break
      case 'csv':
        await exportAsCSV()
        break
    }
    
    notificationStore.success(`Exported as ${format.toUpperCase()} successfully`)
    emit('export-complete', format)
  } catch (error) {
    console.error('Export error:', error)
    notificationStore.error(`Failed to export as ${format.toUpperCase()}`)
  } finally {
    exporting.value = false
  }
}

const exportAsPNG = async () => {
  // Find the nearest chart container or use the whole component
  const element = window.document.querySelector('.chart-container') || 
                  window.document.querySelector('.el-card__body') ||
                  window.document.body
  
  const canvas = await html2canvas(element, {
    backgroundColor: '#ffffff',
    scale: 2
  })
  
  const link = window.document.createElement('a')
  link.download = `${props.filename}.png`
  link.href = canvas.toDataURL()
  link.click()
}

const exportAsPDF = async () => {
  const element = window.document.querySelector('.chart-container') || 
                  window.document.querySelector('.el-card__body') ||
                  window.document.body
  
  const canvas = await html2canvas(element, {
    backgroundColor: '#ffffff',
    scale: 2
  })
  
  const imgData = canvas.toDataURL('image/png')
  const pdf = new jsPDF('landscape', 'mm', 'a4')
  
  const imgWidth = 280
  const pageHeight = 190
  const imgHeight = (canvas.height * imgWidth) / canvas.width
  let heightLeft = imgHeight
  let position = 10

  pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight)
  heightLeft -= pageHeight

  while (heightLeft >= 0) {
    position = heightLeft - imgHeight + 10
    pdf.addPage()
    pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight)
    heightLeft -= pageHeight
  }

  pdf.save(`${props.filename}.pdf`)
}

const exportAsExcel = () => {
  let data = props.data
  
  // Convert object to array if needed
  if (Array.isArray(data)) {
    if (data.length === 0) return
    
    // If array of objects, convert to worksheet
    if (typeof data[0] === 'object') {
      const ws = XLSX.utils.json_to_sheet(data)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, props.title)
      XLSX.writeFile(wb, `${props.filename}.xlsx`)
    } else {
      // Simple array
      const ws = XLSX.utils.aoa_to_sheet([data])
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, props.title)
      XLSX.writeFile(wb, `${props.filename}.xlsx`)
    }
  } else if (typeof data === 'object') {
    // Convert object to array of key-value pairs
    const ws = XLSX.utils.json_to_sheet([data])
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, props.title)
    XLSX.writeFile(wb, `${props.filename}.xlsx`)
  }
}

const exportAsCSV = () => {
  let data = props.data
  
  if (Array.isArray(data)) {
    if (data.length === 0) return
    
    let csvContent = ''
    
    if (typeof data[0] === 'object') {
      // Array of objects - include headers
      const headers = Object.keys(data[0])
      csvContent += headers.join(',') + '\n'
      
      data.forEach(item => {
        const values = headers.map(header => {
          const value = item[header]
          return typeof value === 'string' && value.includes(',') 
            ? `"${value}"` 
            : value
        })
        csvContent += values.join(',') + '\n'
      })
    } else {
      // Simple array
      csvContent = data.join('\n')
    }
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const link = window.document.createElement('a')
    link.download = `${props.filename}.csv`
    link.href = URL.createObjectURL(blob)
    link.click()
  } else if (typeof data === 'object') {
    // Convert object to CSV
    const headers = Object.keys(data)
    const values = headers.map(header => data[header])
    const csvContent = headers.join(',') + '\n' + values.join(',')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const link = window.document.createElement('a')
    link.download = `${props.filename}.csv`
    link.href = URL.createObjectURL(blob)
    link.click()
  }
}
</script>

<style scoped>
.el-dropdown {
  display: inline-block;
}
</style>
