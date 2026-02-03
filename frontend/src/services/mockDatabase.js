// Mock Database Service - Simulates backend API calls
class MockDatabase {
  constructor() {
    this.initializeData()
  }

  initializeData() {
    // Initialize mock data if not exists
    if (!localStorage.getItem('mockDatabase')) {
      const initialData = {
        users: [
          {
            id: 'admin-001',
            name: '系统管理员',
            email: 'admin@blooddomain.com',
            username: 'admin',
            password: 'admin123', // In real app, this would be hashed
            role: 'admin',
            department: '系统管理部',
            status: 'active',
            permissions: ['view_all', 'manage_users', 'manage_system', 'view_reports'],
            createdAt: new Date('2024-01-01'),
            lastLogin: new Date(),
            loginCount: 156
          },
          {
            id: 'user-001',
            name: '张医生',
            email: 'zhang@hospital.com',
            username: 'user',
            password: 'user123',
            role: 'user',
            department: '血液科',
            status: 'active',
            permissions: ['view_own', 'view_reports'],
            createdAt: new Date('2024-02-15'),
            lastLogin: new Date(Date.now() - 2 * 60 * 60 * 1000),
            loginCount: 89
          },
          {
            id: 'user-002',
            name: '李医生',
            email: 'li@hospital.com',
            username: 'doctor',
            password: 'doctor123',
            role: 'doctor',
            department: '输血科',
            status: 'active',
            permissions: ['view_own', 'view_reports', 'manage_donors', 'manage_requests'],
            createdAt: new Date('2024-03-10'),
            lastLogin: new Date(Date.now() - 24 * 60 * 60 * 1000),
            loginCount: 67
          },
          {
            id: 'gov-001',
            name: '王主任',
            email: 'wang@health.gov.cn',
            username: 'government',
            password: 'gov123',
            role: 'government',
            department: '卫生健康委员会',
            status: 'active',
            permissions: ['view_all', 'view_reports', 'regulatory_oversight', 'policy_compliance', 'emergency_coordination'],
            createdAt: new Date('2024-01-15'),
            lastLogin: new Date(Date.now() - 4 * 60 * 60 * 1000),
            loginCount: 124
          }
        ],
        donors: [
          {
            id: 'donor-001',
            name: '王小明',
            bloodType: 'A+',
            phone: '13800138001',
            idCard: '110101199001011234',
            address: '北京市朝阳区',
            status: 'active',
            lastDonation: new Date('2024-06-15'),
            totalDonations: 12,
            notes: '定期捐赠者，健康状况良好',
            createdBy: 'user-001'
          },
          {
            id: 'donor-002',
            name: '李小红',
            bloodType: 'O+',
            phone: '13800138002',
            idCard: '110101199002022345',
            address: '北京市海淀区',
            status: 'active',
            lastDonation: new Date('2024-05-20'),
            totalDonations: 8,
            notes: '首次捐赠者',
            createdBy: 'user-001'
          }
        ],
        requests: [
          {
            id: 'REQ-2024-001',
            patientName: '张三',
            patientAge: 45,
            bloodType: 'A+',
            amount: 400,
            urgency: 'urgent',
            status: 'pending',
            diagnosis: '胃出血',
            surgeryType: '急诊手术',
            doctorName: '李医生',
            notes: '患者情况紧急，需要尽快输血',
            createdAt: new Date('2024-06-20T10:30:00'),
            processedAt: null,
            processedBy: null,
            createdBy: 'user-002'
          }
        ],
        donations: [
          {
            id: 'donation-001',
            donorId: 'donor-001',
            donorName: '王小明',
            bloodType: 'A+',
            amount: 200,
            donationType: 'whole',
            healthStatus: 'good',
            donationDate: new Date('2024-06-15'),
            notes: '健康状况良好',
            recordedBy: 'user-001'
          }
        ],
        inventory: [
          {
            id: 'inv-001',
            bloodType: 'A+',
            amount: 1250,
            capacity: 2000,
            unit: 'ml',
            lastUpdated: new Date(),
            status: 'normal'
          },
          {
            id: 'inv-002',
            bloodType: 'O+',
            amount: 1890,
            capacity: 2000,
            unit: 'ml',
            lastUpdated: new Date(),
            status: 'normal'
          }
        ]
      }
      localStorage.setItem('mockDatabase', JSON.stringify(initialData))
    }
  }

  getData() {
    const data = localStorage.getItem('mockDatabase')
    return data ? JSON.parse(data) : { users: [], donors: [], requests: [], donations: [], inventory: [] }
  }

  saveData(data) {
    localStorage.setItem('mockDatabase', JSON.stringify(data))
  }

  // User operations
  addUser(userData) {
    const data = this.getData()
    const newUser = {
      ...userData,
      id: `user-${Date.now()}`,
      createdAt: new Date(),
      lastLogin: null,
      loginCount: 0
    }
    data.users.push(newUser)
    this.saveData(data)
    return newUser
  }

  findUser(username, password) {
    const data = this.getData()
    return data.users.find(user => user.username === username && user.password === password)
  }

  findUserByUsername(username) {
    const data = this.getData()
    return data.users.find(user => user.username === username)
  }

  getAllUsers() {
    const data = this.getData()
    return data.users
  }

  // Donor operations
  addDonor(donorData) {
    const data = this.getData()
    const newDonor = {
      ...donorData,
      id: `donor-${Date.now()}`,
      totalDonations: 0,
      lastDonation: null
    }
    data.donors.push(newDonor)
    this.saveData(data)
    return newDonor
  }

  getDonorsByUser(userId) {
    const data = this.getData()
    return data.donors.filter(donor => donor.createdBy === userId)
  }

  getAllDonors() {
    const data = this.getData()
    return data.donors
  }

  // Request operations
  addRequest(requestData) {
    const data = this.getData()
    const newRequest = {
      ...requestData,
      id: `REQ-${new Date().getFullYear()}-${String(data.requests.length + 1).padStart(3, '0')}`,
      createdAt: new Date(),
      processedAt: null,
      processedBy: null
    }
    data.requests.push(newRequest)
    this.saveData(data)
    return newRequest
  }

  getRequestsByUser(userId) {
    const data = this.getData()
    return data.requests.filter(request => request.createdBy === userId)
  }

  getAllRequests() {
    const data = this.getData()
    return data.requests
  }

  // Donation operations
  addDonation(donationData) {
    const data = this.getData()
    const newDonation = {
      ...donationData,
      id: `donation-${Date.now()}`,
      donationDate: new Date()
    }
    data.donations.push(newDonation)
    this.saveData(data)
    return newDonation
  }

  getDonationsByUser(userId) {
    const data = this.getData()
    return data.donations.filter(donation => donation.recordedBy === userId)
  }

  // Inventory operations
  getInventory() {
    const data = this.getData()
    return data.inventory
  }

  updateInventory(bloodType, amount) {
    const data = this.getData()
    const inventory = data.inventory.find(inv => inv.bloodType === bloodType)
    if (inventory) {
      inventory.amount = Math.max(0, inventory.amount + amount)
      inventory.lastUpdated = new Date()
      this.saveData(data)
    }
    return inventory
  }

  // Analytics operations
  getAnalytics(userId, userRole) {
    const data = this.getData()
    
    if (userRole === 'admin') {
      return {
        totalUsers: data.users.length,
        totalDonors: data.donors.length,
        totalRequests: data.requests.length,
        totalDonations: data.donations.length,
        pendingRequests: data.requests.filter(r => r.status === 'pending').length,
        inventoryStatus: data.inventory
      }
    } else {
      return {
        myDonors: data.donors.filter(d => d.createdBy === userId).length,
        myRequests: data.requests.filter(r => r.createdBy === userId).length,
        myDonations: data.donations.filter(d => d.recordedBy === userId).length,
        recentActivity: [
          ...data.donors.filter(d => d.createdBy === userId).slice(-5),
          ...data.requests.filter(r => r.createdBy === userId).slice(-5)
        ]
      }
    }
  }
}

// Create singleton instance
const mockDB = new MockDatabase()

export default mockDB
