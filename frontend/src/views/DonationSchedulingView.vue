<template>
  <div class="donation-scheduling">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="section-header">
              <span>Donation Scheduling</span>
              <div class="header-actions">
                <el-button type="primary" @click="addAppointment">
                  <el-icon><Plus /></el-icon>
                  Schedule Appointment
                </el-button>
                <el-button @click="refreshSchedule">
                  <el-icon><Refresh /></el-icon>
                  Refresh
                </el-button>
              </div>
            </div>
          </template>

          <!-- Calendar View -->
          <el-row :gutter="16">
            <el-col :span="18">
              <el-card>
                <template #header>
                  <div class="calendar-header">
                    <span>Appointment Calendar</span>
                    <div class="calendar-controls">
                      <el-button @click="previousMonth">
                        <el-icon><ArrowLeft /></el-icon>
                      </el-button>
                      <span class="current-month">{{ currentMonth }}</span>
                      <el-button @click="nextMonth">
                        <el-icon><ArrowRight /></el-icon>
                      </el-button>
                    </div>
                  </div>
                </template>
                <div class="calendar-grid">
                  <div class="calendar-weekdays">
                    <div v-for="day in weekdays" :key="day" class="weekday">
                      {{ day }}
                    </div>
                  </div>
                  <div class="calendar-days">
                    <div 
                      v-for="day in calendarDays" 
                      :key="day.date"
                      class="calendar-day"
                      :class="getDayClass(day)"
                      @click="selectDate(day)"
                    >
                      <div class="day-number">{{ day.day }}</div>
                      <div v-if="day.appointments" class="appointment-dots">
                        <div 
                          v-for="i in Math.min(day.appointments, 3)" 
                          :key="i"
                          class="dot"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card>
                <template #header>
                  <span>Selected Date</span>
                </template>
                <div class="selected-date-info">
                  <div class="date-display">{{ selectedDateDisplay }}</div>
                  <div class="appointment-count">
                    {{ selectedDateAppointments.length }} appointments
                  </div>
                </div>
                <el-divider />
                <div class="date-appointments">
                  <div 
                    v-for="appointment in selectedDateAppointments" 
                    :key="appointment.id"
                    class="appointment-item"
                  >
                    <div class="appointment-time">{{ appointment.time }}</div>
                    <div class="appointment-details">
                      <div class="appointment-name">{{ appointment.donorName }}</div>
                      <div class="appointment-type">{{ appointment.type }}</div>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- Appointments Table -->
          <el-divider>All Appointments</el-divider>
          <el-table :data="appointments" style="width: 100%">
            <el-table-column prop="date" label="Date" width="120" />
            <el-table-column prop="time" label="Time" width="100" />
            <el-table-column prop="donorName" label="Donor Name" />
            <el-table-column prop="donorType" label="Blood Type" width="100" />
            <el-table-column prop="type" label="Donation Type" width="120" />
            <el-table-column prop="location" label="Location" />
            <el-table-column prop="status" label="Status" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="150">
              <template #default="{ row }">
                <el-button size="small" @click="editAppointment(row)">Edit</el-button>
                <el-button size="small" type="danger" @click="cancelAppointment(row)">Cancel</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Refresh, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { useNotificationStore } from '../stores/notificationStore'

const notificationStore = useNotificationStore()

const currentDate = ref(new Date())
const selectedDate = ref(new Date())

const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const appointments = ref([
  {
    id: 1,
    date: '2024-01-15',
    time: '09:00',
    donorName: 'John Smith',
    donorType: 'O+',
    type: 'Whole Blood',
    location: 'Main Center',
    status: 'Scheduled'
  },
  {
    id: 2,
    date: '2024-01-15',
    time: '10:30',
    donorName: 'Sarah Johnson',
    donorType: 'A+',
    type: 'Plasma',
    location: 'Mobile Unit A',
    status: 'Scheduled'
  },
  {
    id: 3,
    date: '2024-01-16',
    time: '14:00',
    donorName: 'Michael Brown',
    donorType: 'B+',
    type: 'Platelets',
    location: 'Main Center',
    status: 'Confirmed'
  }
])

const currentMonth = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const selectedDateDisplay = computed(() => {
  return selectedDate.value.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

const selectedDateAppointments = computed(() => {
  const dateStr = selectedDate.value.toISOString().split('T')[0]
  return appointments.value.filter(apt => apt.date === dateStr)
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  
  const days = []
  
  // Add empty cells for days before month starts
  for (let i = 0; i < firstDay; i++) {
    days.push({ day: '', date: null })
  }
  
  // Add days of the month
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month, day)
    const dateStr = date.toISOString().split('T')[0]
    const dayAppointments = appointments.value.filter(apt => apt.date === dateStr)
    
    days.push({
      day,
      date: dateStr,
      appointments: dayAppointments.length,
      isToday: date.toDateString() === new Date().toDateString()
    })
  }
  
  return days
})

const getDayClass = (day) => {
  if (!day.date) return 'empty'
  if (day.isToday) return 'today'
  if (day.appointments > 0) return 'has-appointments'
  return 'normal'
}

const getStatusType = (status) => {
  switch (status) {
    case 'Scheduled': return 'info'
    case 'Confirmed': return 'success'
    case 'Completed': return 'success'
    case 'Cancelled': return 'danger'
    default: return 'warning'
  }
}

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1)
}

const selectDate = (day) => {
  if (day.date) {
    selectedDate.value = new Date(day.date)
  }
}

const addAppointment = () => {
  notificationStore.info('Schedule new appointment')
}

const refreshSchedule = () => {
  notificationStore.success('Schedule refreshed')
}

const editAppointment = (appointment) => {
  notificationStore.info(`Edit appointment: ${appointment.donorName}`)
}

const cancelAppointment = (appointment) => {
  notificationStore.warning(`Cancel appointment: ${appointment.donorName}`)
}
</script>

<style scoped>
.donation-scheduling {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.current-month {
  font-weight: 600;
  min-width: 150px;
  text-align: center;
}

.calendar-grid {
  padding: 16px;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 8px;
}

.weekday {
  text-align: center;
  font-weight: 600;
  color: #606266;
  padding: 8px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  aspect-ratio: 1;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.calendar-day:hover {
  border-color: #409eff;
  background: #ecf5ff;
}

.calendar-day.today {
  border-color: #409eff;
  background: #409eff;
  color: white;
}

.calendar-day.has-appointments {
  border-color: #67c23a;
  background: #f0f9ff;
}

.calendar-day.empty {
  border: none;
  cursor: default;
}

.day-number {
  font-weight: 500;
  margin-bottom: 4px;
}

.appointment-dots {
  display: flex;
  gap: 2px;
}

.dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #409eff;
}

.selected-date-info {
  text-align: center;
  margin-bottom: 16px;
}

.date-display {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.appointment-count {
  color: #606266;
  font-size: 14px;
}

.date-appointments {
  max-height: 300px;
  overflow-y: auto;
}

.appointment-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.appointment-item:last-child {
  border-bottom: none;
}

.appointment-time {
  font-weight: 600;
  color: #409eff;
  min-width: 50px;
}

.appointment-details {
  flex: 1;
}

.appointment-name {
  font-weight: 500;
  margin-bottom: 2px;
}

.appointment-type {
  font-size: 12px;
  color: #606266;
}
</style>
