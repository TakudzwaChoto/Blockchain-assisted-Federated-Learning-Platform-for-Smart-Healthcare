import mockDB from './mockDatabase'

// Helper function to get current user ID
const getCurrentUser = () => {
  try {
    const authData = localStorage.getItem('bde.auth')
    if (authData) {
      const parsed = JSON.parse(authData)
      return parsed.user
    }
  } catch (error) {
    console.error('Failed to get current user:', error)
  }
  return null
}

class DataService {
  // Get data for admin dashboard
  getAdminDashboardData() {
    const data = mockDB.getData()
    const analytics = mockDB.getAnalytics(null, 'admin')
    
    return {
      stats: {
        totalUsers: analytics.totalUsers,
        totalDonors: analytics.totalDonors,
        totalRequests: analytics.totalRequests,
        totalDonations: analytics.totalDonations,
        pendingRequests: analytics.pendingRequests,
        activeUsers: data.users.filter(u => u.status === 'active').length,
        newThisMonth: data.users.filter(u => {
          const thisMonth = new Date().getMonth()
          return u.createdAt && new Date(u.createdAt).getMonth() === thisMonth
        }).length
      },
      recentUsers: data.users.slice(-5).map(u => ({
        id: u.id,
        name: u.name,
        email: u.email,
        role: u.role,
        department: u.department,
        status: u.status,
        lastLogin: u.lastLogin
      })),
      recentActivities: [
        ...data.users.slice(-3).map(u => ({
          id: u.id,
          type: 'user',
          description: `新用户 ${u.name} 注册`,
          timestamp: u.createdAt,
          user: u.name
        })),
        ...data.requests.slice(-3).map(r => ({
          id: r.id,
          type: 'request',
          description: `输血申请 ${r.id} 创建`,
          timestamp: r.createdAt,
          user: r.doctorName
        }))
      ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 5)
    }
  }

  // Get data for user dashboard
  getUserDashboardData(userId) {
    const data = mockDB.getData()
    const user = data.users.find(u => u.id === userId)
    
    if (!user) return null

    const myDonors = data.donors.filter(d => d.createdBy === userId)
    const myRequests = data.requests.filter(r => r.createdBy === userId)
    const myDonations = data.donations.filter(d => d.recordedBy === userId)

    return {
      user: user,
      stats: {
        totalDonors: myDonors.length,
        activeDonors: myDonors.filter(d => d.status === 'active').length,
        totalRequests: myRequests.length,
        pendingRequests: myRequests.filter(r => r.status === 'pending').length,
        totalDonations: myDonations.length,
        recentDonations: myDonations.filter(d => {
          const thisMonth = new Date().getMonth()
          return d.donationDate && new Date(d.donationDate).getMonth() === thisMonth
        }).length
      },
      recentDonors: myDonors.slice(-5),
      recentRequests: myRequests.slice(-5),
      recentDonations: myDonations.slice(-5),
      recentActivities: [
        ...myDonors.slice(-3).map(d => ({
          id: d.id,
          type: 'donor',
          description: `添加捐赠者 ${d.name}`,
          timestamp: d.createdAt,
          user: user.name
        })),
        ...myRequests.slice(-3).map(r => ({
          id: r.id,
          type: 'request',
          description: `创建输血申请 ${r.id}`,
          timestamp: r.createdAt,
          user: user.name
        })),
        ...myDonations.slice(-3).map(d => ({
          id: d.id,
          type: 'donation',
          description: `记录 ${d.donorName} 的捐赠`,
          timestamp: d.donationDate,
          user: user.name
        }))
      ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 5)
    }
  }

  // Get data for doctor dashboard
  getDoctorDashboardData() {
    const data = mockDB.getData()
    const currentUser = getCurrentUser()
    
    // Generate doctor-specific data
    const doctorPatients = data.donors.slice(0, 8).map((donor, index) => ({
      id: donor.id,
      name: donor.name,
      bloodType: donor.bloodType,
      condition: ['稳定', '恢复中', '需要观察', '危重'][index % 4],
      lastTransfusion: index % 3 === 0 ? new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000) : null,
      status: ['stable', 'recovering', 'observation', 'critical'][index % 4],
      assignedDoctor: currentUser?.id
    }))
    
    const doctorRequests = data.requests.slice(0, 6).map((request, index) => ({
      ...request,
      requestedBy: currentUser?.id,
      urgency: ['常规', '紧急', '非常紧急'][index % 3]
    }))
    
    return {
      stats: {
        totalPatients: doctorPatients.length,
        pendingRequests: doctorRequests.filter(r => r.status === 'pending').length,
        todayTransfusions: Math.floor(Math.random() * 5) + 1,
        criticalAlerts: doctorPatients.filter(p => p.status === 'critical').length
      },
      recentPatients: doctorPatients.slice(0, 5),
      recentRequests: doctorRequests.slice(0, 5)
    }
  }

  // Get donors for user management
  getUserDonors(userId) {
    return mockDB.getDonorsByUser(userId)
  }

  // Get requests for user management
  getUserRequests(userId) {
    return mockDB.getRequestsByUser(userId)
  }

  // Add new donor
  addDonor(donorData, userId) {
    return mockDB.addDonor({
      ...donorData,
      createdBy: userId
    })
  }

  // Add new request
  addRequest(requestData, userId) {
    return mockDB.addRequest({
      ...requestData,
      createdBy: userId,
      doctorName: mockDB.getData().users.find(u => u.id === userId)?.name || '未知医生'
    })
  }

  // Add new donation
  addDonation(donationData, userId) {
    const donor = mockDB.getData().donors.find(d => d.id === donationData.donorId)
    return mockDB.addDonation({
      ...donationData,
      donorName: donor?.name || '未知捐赠者',
      bloodType: donor?.bloodType || '未知',
      recordedBy: userId
    })
  }

  // Get all users for admin
  getAllUsers() {
    return mockDB.getAllUsers()
  }

  // Get inventory status
  getInventoryStatus() {
    return mockDB.getInventory()
  }

  // Update user status
  updateUserStatus(userId, status) {
    const data = mockDB.getData()
    const userIndex = data.users.findIndex(u => u.id === userId)
    if (userIndex > -1) {
      data.users[userIndex].status = status
      mockDB.saveData(data)
      return data.users[userIndex]
    }
    return null
  }

  // Delete user
  deleteUser(userId) {
    const data = mockDB.getData()
    const userIndex = data.users.findIndex(u => u.id === userId)
    if (userIndex > -1) {
      data.users.splice(userIndex, 1)
      mockDB.saveData(data)
      return true
    }
    return false
  }
}

export default new DataService()
