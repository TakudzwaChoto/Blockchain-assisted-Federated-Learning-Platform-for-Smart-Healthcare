// Test Data Service - Easy integration for testing the blood domain system
import { testData, testDataUtils } from './testData.js'

class TestDataService {
  constructor() {
    this.data = testData
    this.utils = testDataUtils
  }

  // Donor Management
  getDonors(limit = 50, offset = 0) {
    return this.data.donors.slice(offset, offset + limit)
  }

  getDonorById(id) {
    return this.data.donors.find(donor => donor.id === id)
  }

  getDonorsByBloodType(bloodType) {
    return this.data.donors.filter(donor => donor.bloodType === bloodType)
  }

  getEligibleDonors() {
    return this.data.donors.filter(donor => donor.eligibilityStatus === 'eligible')
  }

  // Blood Inventory
  getBloodInventory(centerName = null) {
    if (centerName) {
      return this.data.bloodInventory.filter(item => item.centerName === centerName)
    }
    return this.data.bloodInventory
  }

  getInventoryByBloodType(bloodType) {
    return this.data.bloodInventory.filter(item => item.bloodType === bloodType)
  }

  getLowStockItems(threshold = 100) {
    return this.data.bloodInventory.filter(item => item.quantity < threshold)
  }

  getExpiringStock(days = 7) {
    const cutoff = new Date()
    cutoff.setDate(cutoff.getDate() + days)
    return this.data.bloodInventory.filter(item => new Date(item.expiryDate) <= cutoff)
  }

  // Donation Centers
  getDonationCenters(city = null) {
    if (city) {
      return this.data.donationCenters.filter(center => center.location.city === city)
    }
    return this.data.donationCenters
  }

  getActiveCenters() {
    return this.data.donationCenters.filter(center => center.status === 'active')
  }

  getCenterById(id) {
    return this.data.donationCenters.find(center => center.id === id)
  }

  // Blood Requests
  getBloodRequests(status = null) {
    if (status) {
      return this.data.bloodRequests.filter(request => request.status === status)
    }
    return this.data.bloodRequests
  }

  getUrgentRequests() {
    return this.data.bloodRequests.filter(request => 
      request.urgency === 'urgent' || request.urgency === 'emergency' || request.urgency === 'critical'
    )
  }

  getPendingRequests() {
    return this.data.bloodRequests.filter(request => request.status === 'pending')
  }

  // Emergency Alerts
  getEmergencyAlerts(severity = null) {
    if (severity) {
      return this.data.emergencyAlerts.filter(alert => alert.severity === severity)
    }
    return this.data.emergencyAlerts
  }

  getActiveAlerts() {
    return this.data.emergencyAlerts.filter(alert => alert.status === 'active')
  }

  getCriticalAlerts() {
    return this.data.emergencyAlerts.filter(alert => alert.severity === 'critical')
  }

  // Staff Management
  getStaffMembers(centerId = null) {
    if (centerId) {
      return this.data.staffRecords.filter(staff => staff.centerId === centerId)
    }
    return this.data.staffRecords
  }

  getStaffByPosition(position) {
    return this.data.staffRecords.filter(staff => staff.position === position)
  }

  getActiveStaff() {
    return this.data.staffRecords.filter(staff => staff.status === 'active')
  }

  // Campaigns
  getCampaigns(status = null) {
    if (status) {
      return this.data.campaigns.filter(campaign => campaign.status === status)
    }
    return this.data.campaigns
  }

  getActiveCampaigns() {
    return this.data.campaigns.filter(campaign => campaign.status === 'active')
  }

  getCompletedCampaigns() {
    return this.data.campaigns.filter(campaign => campaign.status === 'completed')
  }

  // Quality Control
  getQualityControlRecords(status = null) {
    if (status) {
      return this.data.qualityControl.filter(record => record.results.overall === status)
    }
    return this.data.qualityControl
  }

  getFailedQCRecords() {
    return this.data.qualityControl.filter(record => record.results.overall === 'fail')
  }

  getQCRecordsByDateRange(startDate, endDate) {
    return this.data.qualityControl.filter(record => {
      const testDate = new Date(record.testDate)
      return testDate >= new Date(startDate) && testDate <= new Date(endDate)
    })
  }

  // Analytics and Statistics
  getDashboardStats() {
    const totalDonors = this.data.donors.length
    const eligibleDonors = this.data.donors.filter(d => d.eligibilityStatus === 'eligible').length
    const totalInventory = this.data.bloodInventory.reduce((sum, item) => sum + item.quantity, 0)
    const activeCenters = this.data.donationCenters.filter(c => c.status === 'active').length
    const pendingRequests = this.data.bloodRequests.filter(r => r.status === 'pending').length
    const activeAlerts = this.data.emergencyAlerts.filter(a => a.status === 'active').length

    return {
      totalDonors,
      eligibleDonors,
      totalInventory,
      activeCenters,
      pendingRequests,
      activeAlerts,
      eligibilityRate: ((eligibleDonors / totalDonors) * 100).toFixed(1)
    }
  }

  getBloodTypeDistribution() {
    const distribution = {}
    this.data.donors.forEach(donor => {
      distribution[donor.bloodType] = (distribution[donor.bloodType] || 0) + 1
    })
    return distribution
  }

  getMonthlyDonations() {
    const monthlyData = {}
    this.data.donationRecords.forEach(record => {
      const month = new Date(record.donationDate).toISOString().slice(0, 7)
      monthlyData[month] = (monthlyData[month] || 0) + 1
    })
    return monthlyData
  }

  getCenterPerformance() {
    const performance = {}
    this.data.donationCenters.forEach(center => {
      const donations = this.data.donationRecords.filter(r => r.centerId === center.id)
      performance[center.name] = {
        totalDonations: donations.length,
        averageVolume: donations.length > 0 ? 
          (donations.reduce((sum, d) => sum + d.volume, 0) / donations.length).toFixed(0) : 0,
        totalVolume: donations.reduce((sum, d) => sum + d.volume, 0)
      }
    })
    return performance
  }

  // Search and Filter
  searchDonors(query) {
    const lowerQuery = query.toLowerCase()
    return this.data.donors.filter(donor => 
      donor.name.toLowerCase().includes(lowerQuery) ||
      donor.bloodType.toLowerCase().includes(lowerQuery) ||
      donor.phone.includes(query) ||
      donor.email.toLowerCase().includes(lowerQuery)
    )
  }

  searchBloodRequests(query) {
    const lowerQuery = query.toLowerCase()
    return this.data.bloodRequests.filter(request =>
      request.requestingHospital.toLowerCase().includes(lowerQuery) ||
      request.bloodType.toLowerCase().includes(lowerQuery) ||
      request.patientName.toLowerCase().includes(lowerQuery) ||
      request.requestId.toLowerCase().includes(lowerQuery)
    )
  }

  // Data Export
  exportDonors(format = 'json') {
    const data = this.getDonors()
    if (format === 'csv') {
      return this.convertToCSV(data)
    }
    return JSON.stringify(data, null, 2)
  }

  exportInventory(format = 'json') {
    const data = this.getBloodInventory()
    if (format === 'csv') {
      return this.convertToCSV(data)
    }
    return JSON.stringify(data, null, 2)
  }

  // Utility Methods
  convertToCSV(data) {
    if (!data || data.length === 0) return ''
    
    const headers = Object.keys(data[0])
    const csvHeaders = headers.join(',')
    
    const csvRows = data.map(row => {
      return headers.map(header => {
        const value = row[header]
        return typeof value === 'string' && value.includes(',') ? 
          `"${value}"` : value
      }).join(',')
    })
    
    return [csvHeaders, ...csvRows].join('\n')
  }

  // Real-time simulation methods
  simulateNewDonation() {
    const newDonation = {
      id: `DONATION_${Date.now()}`,
      donorId: this.utils.getRandomDonor().id,
      centerId: this.utils.getRandomBloodUnit().centerId,
      donationDate: new Date().toISOString(),
      bloodType: this.utils.getRandomDonor().bloodType,
      volume: Math.floor(Math.random() * 300) + 200,
      status: 'completed'
    }
    this.data.donationRecords.unshift(newDonation)
    return newDonation
  }

  simulateNewRequest() {
    const newRequest = {
      id: `REQ_${Date.now()}`,
      requestId: `BR-${Math.floor(Math.random() * 900000) + 100000}`,
      bloodType: this.utils.getRandomDonor().bloodType,
      urgency: ['routine', 'urgent', 'emergency', 'critical'][Math.floor(Math.random() * 4)],
      status: 'pending',
      requestDate: new Date().toISOString()
    }
    this.data.bloodRequests.unshift(newRequest)
    return newRequest
  }

  simulateNewAlert() {
    const severities = ['low', 'medium', 'high', 'critical']
    const newAlert = {
      id: `ALERT_${Date.now()}`,
      severity: severities[Math.floor(Math.random() * severities.length)],
      title: 'System Alert',
      description: 'Simulated alert for testing',
      status: 'active',
      reportedDate: new Date().toISOString()
    }
    this.data.emergencyAlerts.unshift(newAlert)
    return newAlert
  }

  // Initialize and seed data
  initializeData() {
    console.log('Initializing test data service...')
    console.log('Data Summary:', {
      donors: this.data.donors.length,
      inventory: this.data.bloodInventory.length,
      centers: this.data.donationCenters.length,
      requests: this.data.bloodRequests.length,
      alerts: this.data.emergencyAlerts.length,
      staff: this.data.staffRecords.length,
      campaigns: this.data.campaigns.length,
      qualityControl: this.data.qualityControl.length,
      logs: this.data.systemLogs.length
    })
    return true
  }
}

// Create singleton instance
export const testDataService = new TestDataService()

// Export for easy access
export default testDataService
