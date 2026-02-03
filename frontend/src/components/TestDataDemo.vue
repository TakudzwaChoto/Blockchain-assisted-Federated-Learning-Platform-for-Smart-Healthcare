<template>
  <div class="test-data-demo">
    <div class="demo-header">
      <h2>🧪 Test Data Demo</h2>
      <p>Comprehensive test data for Blood Domain Analysis System</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card clickable" v-for="(value, key) in stats" :key="key" @click="navigateToSection(key)">
        <div class="stat-number">{{ value.toLocaleString() }}</div>
        <div class="stat-label">{{ formatLabel(key) }}</div>
      </div>
    </div>

    <div class="demo-sections">
      <div class="demo-section">
        <h3>📊 Dashboard Statistics</h3>
        <div class="dashboard-stats">
          <div class="dashboard-stat">
            <span class="label">Total Donors:</span>
            <span class="value">{{ dashboardStats.totalDonors.toLocaleString() }}</span>
          </div>
          <div class="dashboard-stat">
            <span class="label">Eligible Donors:</span>
            <span class="value">{{ dashboardStats.eligibleDonors.toLocaleString() }}</span>
          </div>
          <div class="dashboard-stat">
            <span class="label">Total Inventory:</span>
            <span class="value">{{ dashboardStats.totalInventory.toLocaleString() }}ml</span>
          </div>
          <div class="dashboard-stat">
            <span class="label">Active Centers:</span>
            <span class="value">{{ dashboardStats.activeCenters }}</span>
          </div>
          <div class="dashboard-stat">
            <span class="label">Pending Requests:</span>
            <span class="value">{{ dashboardStats.pendingRequests }}</span>
          </div>
          <div class="dashboard-stat">
            <span class="label">Active Alerts:</span>
            <span class="value">{{ dashboardStats.activeAlerts }}</span>
          </div>
        </div>
      </div>

      <div class="demo-section">
        <h3>🩸 Blood Type Distribution</h3>
        <div class="blood-type-grid">
          <div class="blood-type-item clickable" v-for="(count, type) in bloodTypeDistribution" :key="type" @click="navigateToBloodType(type)">
            <div class="blood-type">{{ type }}</div>
            <div class="blood-count">{{ count.toLocaleString() }}</div>
            <div class="blood-percentage">{{ ((count / totalDonors) * 100).toFixed(1) }}%</div>
          </div>
        </div>
      </div>

      <div class="demo-section">
        <h3>🏥 Recent Donations</h3>
        <div class="recent-donations">
          <div class="donation-item clickable" v-for="donation in recentDonations.slice(0, 5)" :key="donation.id" @click="navigateToDonation(donation)">
            <div class="donation-info">
              <span class="donor-id">{{ donation.donorId }}</span>
              <span class="blood-type">{{ donation.bloodType }}</span>
              <span class="volume">{{ donation.volume }}ml</span>
              <span class="date">{{ formatDate(donation.donationDate) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="demo-section">
        <h3>🚨 Active Alerts</h3>
        <div class="alerts-list">
          <div class="alert-item clickable" :class="alert.severity" v-for="alert in activeAlerts.slice(0, 5)" :key="alert.id" @click="navigateToAlert(alert)">
            <div class="alert-severity">{{ alert.severity.toUpperCase() }}</div>
            <div class="alert-title">{{ alert.title }}</div>
            <div class="alert-location">{{ alert.location.center }}</div>
            <div class="alert-date">{{ formatDate(alert.reportedDate) }}</div>
          </div>
        </div>
      </div>

      <div class="demo-section">
        <h3>⚡ Live Simulation</h3>
        <div class="simulation-controls">
          <el-button @click="simulateDonation" type="primary">
            <el-icon><Plus /></el-icon>
            Simulate Donation
          </el-button>
          <el-button @click="simulateRequest" type="warning">
            <el-icon><Bell /></el-icon>
            Simulate Request
          </el-button>
          <el-button @click="simulateAlert" type="danger">
            <el-icon><Warning /></el-icon>
            Simulate Alert
          </el-button>
          <el-button @click="refreshData" type="info">
            <el-icon><Refresh /></el-icon>
            Refresh Data
          </el-button>
        </div>
        <div class="simulation-log">
          <div class="log-item" v-for="log in simulationLog.slice(-5)" :key="log.id">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { testDataService } from '../data/testDataService.js'
import { Plus, Bell, Warning, Refresh } from '@element-plus/icons-vue'

export default {
  name: 'TestDataDemo',
  components: {
    Plus,
    Bell,
    Warning,
    Refresh
  },
  setup() {
    const stats = ref({})
    const dashboardStats = ref({})
    const bloodTypeDistribution = ref({})
    const totalDonors = ref(0)
    const recentDonations = ref([])
    const activeAlerts = ref([])
    const simulationLog = ref([])

    const formatLabel = (key) => {
      const labels = {
        donors: 'Donors',
        bloodInventory: 'Blood Units',
        donationCenters: 'Centers',
        donationRecords: 'Donations',
        bloodRequests: 'Requests',
        emergencyAlerts: 'Alerts',
        staffRecords: 'Staff',
        campaigns: 'Campaigns',
        qualityControl: 'QC Records',
        systemLogs: 'System Logs'
      }
      return labels[key] || key
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const loadStats = () => {
      // Get record counts
      stats.value = {
        donors: testDataService.getDonors().length,
        bloodInventory: testDataService.getBloodInventory().length,
        donationCenters: testDataService.getDonationCenters().length,
        donationRecords: testDataService.data.donationRecords.length,
        bloodRequests: testDataService.getBloodRequests().length,
        emergencyAlerts: testDataService.getEmergencyAlerts().length,
        staffRecords: testDataService.getStaffMembers().length,
        campaigns: testDataService.getCampaigns().length,
        qualityControl: testDataService.getQualityControlRecords().length,
        systemLogs: testDataService.data.systemLogs.length
      }

      // Get dashboard stats
      dashboardStats.value = testDataService.getDashboardStats()

      // Get blood type distribution
      bloodTypeDistribution.value = testDataService.getBloodTypeDistribution()
      totalDonors.value = testDataService.getDonors().length

      // Get recent donations
      recentDonations.value = testDataService.data.donationRecords

      // Get active alerts
      activeAlerts.value = testDataService.getActiveAlerts()
    }

    const simulateDonation = () => {
      const donation = testDataService.simulateNewDonation()
      addLog(`New donation recorded: ${donation.bloodType}, ${donation.volume}ml`)
      loadStats()
    }

    const simulateRequest = () => {
      const request = testDataService.simulateNewRequest()
      addLog(`New blood request: ${request.bloodType}, ${request.urgency}`)
      loadStats()
    }

    const simulateAlert = () => {
      const alert = testDataService.simulateNewAlert()
      addLog(`New alert: ${alert.severity} - ${alert.title}`)
      loadStats()
    }

    const refreshData = () => {
      loadStats()
      addLog('Data refreshed')
    }

    const addLog = (message) => {
      simulationLog.value.push({
        id: Date.now(),
        time: new Date().toLocaleTimeString(),
        message: message
      })
    }

    // Navigation methods
    const navigateToSection = (section) => {
      const routes = {
        donors: '/donors',
        bloodInventory: '/blood-inventory',
        donationCenters: '/donation-centers',
        donationRecords: '/donation-records',
        bloodRequests: '/blood-requests',
        emergencyAlerts: '/emergency-alerts',
        staffRecords: '/staff',
        campaigns: '/campaigns',
        qualityControl: '/quality-control',
        systemLogs: '/system-logs'
      }
      
      const route = routes[section] || '/'
      console.log(`Navigating to: ${route}`)
      
      // Use Vue Router if available, otherwise fallback to window.location
      if (window.router) {
        window.router.push(route)
      } else {
        window.location.href = route
      }
    }

    const navigateToBloodType = (bloodType) => {
      console.log(`Navigating to blood type: ${bloodType}`)
      const route = `/blood-inventory?type=${bloodType}`
      
      if (window.router) {
        window.router.push(route)
      } else {
        window.location.href = route
      }
    }

    const navigateToDonation = (donation) => {
      console.log(`Navigating to donation: ${donation.id}`)
      const route = `/donation-records/${donation.id}`
      
      if (window.router) {
        window.router.push(route)
      } else {
        window.location.href = route
      }
    }

    const navigateToAlert = (alert) => {
      console.log(`Navigating to alert: ${alert.id}`)
      const route = `/emergency-alerts/${alert.id}`
      
      if (window.router) {
        window.router.push(route)
      } else {
        window.location.href = route
      }
    }

    onMounted(() => {
      testDataService.initializeData()
      loadStats()
      addLog('Test data service initialized')
    })

    return {
      stats,
      dashboardStats,
      bloodTypeDistribution,
      totalDonors,
      recentDonations,
      activeAlerts,
      simulationLog,
      formatLabel,
      formatDate,
      simulateDonation,
      simulateRequest,
      simulateAlert,
      refreshData,
      navigateToSection,
      navigateToBloodType,
      navigateToDonation,
      navigateToAlert
    }
  }
}
</script>

<style scoped>
.test-data-demo {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Common clickable styles */
.clickable {
  transition: all 0.3s ease;
  cursor: pointer;
}

.clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.clickable:active {
  transform: translateY(0);
}

.demo-header {
  text-align: center;
  margin-bottom: 32px;
}

.demo-header h2 {
  color: #1e293b;
  margin-bottom: 8px;
}

.demo-header p {
  color: #64748b;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.stat-card:hover {
  border-color: #3b82f6;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.demo-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.demo-section {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 20px;
}

.demo-section h3 {
  color: #1e293b;
  margin-bottom: 16px;
  font-size: 1.2rem;
}

.dashboard-stats {
  display: grid;
  gap: 12px;
}

.dashboard-stat {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.dashboard-stat .label {
  color: #64748b;
}

.dashboard-stat .value {
  font-weight: 600;
  color: #1e293b;
}

.blood-type-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 12px;
}

.blood-type-item {
  text-align: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
}

.blood-type-item:hover {
  background: rgba(255, 255, 255, 0.8);
}

.blood-type {
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.blood-count {
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 2px;
}

.blood-percentage {
  font-size: 0.8rem;
  color: #64748b;
}

.recent-donations {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.donation-item {
  padding: 12px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
}

.donation-item:hover {
  background: rgba(255, 255, 255, 0.8);
}

.donation-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.donor-id {
  color: #64748b;
}

.blood-type {
  font-weight: 600;
  color: #1e293b;
}

.volume {
  color: #374151;
}

.date {
  color: #64748b;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alert-item {
  padding: 12px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.alert-item.low {
  background: rgba(34, 197, 94, 0.1);
  border-left: 4px solid #22c55e;
}

.alert-item.medium {
  background: rgba(251, 146, 60, 0.1);
  border-left: 4px solid #fb923c;
}

.alert-item.high {
  background: rgba(239, 68, 68, 0.1);
  border-left: 4px solid #ef4444;
}

.alert-item.critical {
  background: rgba(127, 29, 29, 0.1);
  border-left: 4px solid #7f1d1d;
}

.alert-severity {
  font-weight: 700;
  font-size: 0.8rem;
}

.alert-title {
  font-weight: 600;
  color: #1e293b;
}

.alert-location {
  color: #64748b;
}

.alert-date {
  color: #64748b;
  font-size: 0.8rem;
}

.simulation-controls {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.simulation-log {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  padding: 12px;
  max-height: 150px;
  overflow-y: auto;
}

.log-item {
  display: flex;
  gap: 12px;
  padding: 4px 0;
  font-size: 0.9rem;
}

.log-time {
  color: #64748b;
  font-family: monospace;
}

.log-message {
  color: #1e293b;
}

@media (max-width: 768px) {
  .demo-sections {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .simulation-controls {
    flex-direction: column;
  }
}
</style>
