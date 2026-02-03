// Comprehensive Test Data for Blood Domain Analysis System
// Generated synthetic dataset with 4000+ records

// Blood Types and Rh Factors
const BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
const RH_FACTORS = ['positive', 'negative']

// Geographic Locations
const CITIES = [
  '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都', '重庆', '西安',
  '天津', '苏州', '青岛', '厦门', '大连', '宁波', '无锡', '长沙', '郑州', '济南',
  '哈尔滨', '沈阳', '长春', '石家庄', '太原', '合肥', '南昌', '福州', '贵阳', '昆明',
  '兰州', '西宁', '银川', '乌鲁木齐', '呼和浩特', '海口', '三亚', '桂林', '拉萨', '日喀则'
]

// Hospital Names
const HOSPITAL_NAMES = [
  '北京协和医院', '上海瑞金医院', '广州中山医院', '深圳人民医院', '浙江大学医学院附属第一医院',
  '南京鼓楼医院', '武汉同济医院', '成都华西医院', '重庆医科大学附属第一医院', '西安交通大学第一附属医院',
  '天津市肿瘤医院', '苏州大学附属第一医院', '青岛大学附属医院', '厦门大学附属第一医院', '大连医科大学附属第一医院',
  '宁波市医疗中心李惠利医院', '无锡市人民医院', '中南大学湘雅医院', '郑州大学第一附属医院', '山东省立医院',
  '哈尔滨医科大学附属第一医院', '中国医科大学附属第一医院', '吉林大学第一医院', '河北省人民医院', '山西医科大学第一医院',
  '安徽医科大学第一附属医院', '南昌大学第一附属医院', '福建医科大学附属第一医院', '贵州省人民医院', '昆明医科大学第一附属医院',
  '兰州大学第一医院', '青海大学附属医院', '宁夏医科大学总医院', '新疆医科大学第一附属医院', '内蒙古自治区人民医院',
  '海南省人民医院', '三亚市人民医院', '桂林医学院附属医院', '西藏自治区人民医院', '日喀则市人民医院'
]

// Donor Names (Chinese)
const FIRST_NAMES = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '林', '罗', '郑']
const LAST_NAMES = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '洋', '艳', '勇', '军', '杰', '娟', '涛', '明', '超', '秀兰', '霞']

// Random Generator Functions
const randomChoice = (arr) => arr[Math.floor(Math.random() * arr.length)]
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
const randomFloat = (min, max) => parseFloat((Math.random() * (max - min) + min).toFixed(2))
const randomDate = (start, end) => {
  const startDate = new Date(start)
  const endDate = new Date(end)
  return new Date(startDate.getTime() + Math.random() * (endDate.getTime() - startDate.getTime()))
}
const randomId = () => Math.random().toString(36).substr(2, 9)

// Generate Donors (2000 records)
const generateDonors = () => {
  const donors = []
  for (let i = 0; i < 2000; i++) {
    const name = randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES)
    donors.push({
      id: `DONOR_${String(i + 1).padStart(6, '0')}`,
      name: name,
      bloodType: randomChoice(BLOOD_TYPES),
      age: randomInt(18, 65),
      gender: randomChoice(['male', 'female']),
      phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`,
      email: `${name.toLowerCase()}${randomInt(1, 999)}@email.com`,
      address: `${randomChoice(CITIES)}${randomChoice('区', '县', '市')}${randomInt(1, 999)}号`,
      registrationDate: randomDate('2020-01-01', '2024-12-31'),
      lastDonation: randomDate('2023-01-01', '2024-12-31'),
      totalDonations: randomInt(0, 25),
      eligibilityStatus: randomChoice(['eligible', 'ineligible', 'pending']),
      nextEligibleDate: randomDate('2024-01-01', '2025-12-31'),
      healthStatus: randomChoice(['excellent', 'good', 'fair', 'poor']),
      weight: randomFloat(45.0, 95.0),
      height: randomFloat(150.0, 190.0),
      bloodPressure: `${randomInt(90, 140)}/${randomInt(60, 90)}`,
      hemoglobin: randomFloat(11.5, 16.5),
      notes: `Donor ${randomChoice(['regular', 'occasional', 'first-time'])} donor`,
      preferredDonationCenter: randomChoice(HOSPITAL_NAMES),
      consentForResearch: randomChoice([true, false]),
      emergencyContact: {
        name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
        relationship: randomChoice(['spouse', 'parent', 'sibling', 'friend']),
        phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`
      }
    })
  }
  return donors
}

// Generate Blood Inventory (500 records per blood type = 4000 total)
const generateBloodInventory = () => {
  const inventory = []
  const centers = HOSPITAL_NAMES.slice(0, 20) // Use 20 centers
  
  for (const center of centers) {
    for (const bloodType of BLOOD_TYPES) {
      inventory.push({
        id: `INV_${center.substring(0, 3)}_${bloodType.replace('+', 'P').replace('-', 'N')}_${randomId()}`,
        bloodType: bloodType,
        centerName: center,
        centerLocation: randomChoice(CITIES),
        quantity: randomInt(50, 500), // in milliliters
        units: randomInt(1, 10), // number of units
        collectionDate: randomDate('2024-01-01', '2024-12-31'),
        expiryDate: randomDate('2024-12-01', '2025-06-30'),
        storageTemperature: randomFloat(2.0, 6.0),
        storageCondition: randomChoice(['optimal', 'acceptable', 'critical']),
        donorId: `DONOR_${String(randomInt(1, 2000)).padStart(6, '0')}`,
        donationType: randomChoice(['voluntary', 'replacement', 'directed']),
        processingStatus: randomChoice(['processed', 'processing', 'pending']),
        testingStatus: randomChoice(['cleared', 'pending', 'failed']),
        qualityGrade: randomChoice(['A', 'B', 'C']),
        reservedFor: randomChoice(['general', 'emergency', 'surgery', 'research', null]),
        lastUpdated: new Date(),
        notes: `Blood unit ${randomChoice(['fresh', 'regular', 'aged'])} condition`
      })
    }
  }
  return inventory
}

// Generate Donation Centers (100 records)
const generateDonationCenters = () => {
  const centers = []
  for (let i = 0; i < 100; i++) {
    const centerName = HOSPITAL_NAMES[i % HOSPITAL_NAMES.length]
    centers.push({
      id: `CENTER_${String(i + 1).padStart(4, '0')}`,
      name: centerName,
      type: randomChoice(['hospital', 'clinic', 'mobile_unit', 'blood_bank']),
      location: {
        city: randomChoice(CITIES),
        address: `${randomChoice('建设路', '人民路', '解放路', '中山路', '和平路')}${randomInt(1, 999)}号`,
        coordinates: {
          latitude: randomFloat(20.0, 50.0),
          longitude: randomFloat(100.0, 140.0)
        }
      },
      contact: {
        phone: `0${randomInt(10, 99)}-${randomInt(10000000, 99999999)}`,
        email: `contact@${centerName.replace(/[^\w]/g, '').toLowerCase()}.com`,
        website: `https://www.${centerName.replace(/[^\w]/g, '').toLowerCase()}.com`
      },
      operatingHours: {
        monday: { open: '08:00', close: '17:00' },
        tuesday: { open: '08:00', close: '17:00' },
        wednesday: { open: '08:00', close: '17:00' },
        thursday: { open: '08:00', close: '17:00' },
        friday: { open: '08:00', close: '17:00' },
        saturday: { open: '09:00', close: '13:00' },
        sunday: { open: 'closed', close: 'closed' }
      },
      capacity: {
        dailyDonations: randomInt(10, 100),
        storageCapacity: randomInt(100, 1000),
        staffCount: randomInt(5, 50),
        bedsCount: randomInt(2, 20)
      },
      equipment: {
        refrigerators: randomInt(2, 10),
        centrifuges: randomInt(1, 5),
        bloodAnalyzers: randomInt(1, 3),
        computers: randomInt(3, 15),
        mobilePhones: randomInt(5, 20)
      },
      services: randomChoice(['collection', 'testing', 'storage', 'distribution', 'emergency'], randomInt(2, 5)),
      certifications: randomChoice(['ISO', 'WHO', 'National', 'Regional'], randomInt(1, 4)),
      status: randomChoice(['active', 'inactive', 'maintenance', 'emergency_only']),
      rating: randomFloat(3.0, 5.0),
      reviews: randomInt(10, 500),
      establishedYear: randomInt(1950, 2020),
      lastInspection: randomDate('2023-01-01', '2024-12-31'),
      nextInspection: randomDate('2024-01-01', '2025-12-31'),
      manager: {
        name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
        title: randomChoice(['Director', 'Manager', 'Supervisor', 'Coordinator']),
        phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`
      }
    })
  }
  return centers
}

// Generate Donation Records (3000 records)
const generateDonationRecords = () => {
  const records = []
  for (let i = 0; i < 3000; i++) {
    records.push({
      id: `DONATION_${String(i + 1).padStart(7, '0')}`,
      donorId: `DONOR_${String(randomInt(1, 2000)).padStart(6, '0')}`,
      centerId: `CENTER_${String(randomInt(1, 100)).padStart(4, '0')}`,
      donationDate: randomDate('2023-01-01', '2024-12-31'),
      donationTime: `${randomInt(8, 16)}:${String(randomInt(0, 59)).padStart(2, '0')}`,
      bloodType: randomChoice(BLOOD_TYPES),
      volume: randomInt(200, 500), // in milliliters
      donationType: randomChoice(['voluntary', 'replacement', 'directed', 'apheresis']),
      donationMethod: randomChoice(['whole_blood', 'plasma', 'platelets', 'double_red_cells']),
      duration: randomInt(10, 45), // in minutes
      staffId: `STAFF_${String(randomInt(1, 500)).padStart(4, '0')}`,
      staffName: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
      preDonationChecks: {
        hemoglobin: randomFloat(11.5, 16.5),
        bloodPressure: `${randomInt(90, 140)}/${randomInt(60, 90)}`,
        pulse: randomInt(60, 100),
        temperature: randomFloat(36.0, 37.5),
        weight: randomFloat(45.0, 95.0),
        questionsPassed: randomInt(10, 15),
        questionsTotal: 15
      },
      postDonationStatus: randomChoice(['normal', 'dizzy', 'faint', 'bruise', 'other']),
      complications: randomChoice([null, 'dizziness', 'fainting', 'bruising', 'hematoma']),
      followUpRequired: randomChoice([true, false]),
      followUpDate: randomDate('2024-01-01', '2025-01-01'),
      qualityControl: {
        passed: randomChoice([true, false]),
        issues: randomChoice([null, 'clotting', 'contamination', 'volume_issue', 'temperature']),
        retested: randomChoice([true, false]),
        approvedForUse: randomChoice([true, false])
      },
      notes: `Donation ${randomChoice(['routine', 'emergency', 'special', 'research'])} procedure`,
      createdDate: new Date(),
      lastModified: new Date()
    })
  }
  return records
}

// Generate Blood Requests (1500 records)
const generateBloodRequests = () => {
  const requests = []
  for (let i = 0; i < 1500; i++) {
    const urgency = randomChoice(['routine', 'urgent', 'emergency', 'critical'])
    requests.push({
      id: `REQ_${String(i + 1).padStart(6, '0')}`,
      requestId: `BR-${randomInt(100000, 999999)}`,
      requestingHospital: randomChoice(HOSPITAL_NAMES),
      requestingDepartment: randomChoice(['Emergency', 'Surgery', 'ICU', 'Oncology', 'Pediatrics', 'Maternity', 'General']),
      requestingDoctor: `Dr. ${randomChoice(FIRST_NAMES)}${randomChoice(LAST_NAMES)}`,
      patientId: `PAT_${String(randomInt(1, 10000)).padStart(6, '0')}`,
      patientName: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
      patientAge: randomInt(0, 90),
      patientGender: randomChoice(['male', 'female']),
      bloodType: randomChoice(BLOOD_TYPES),
      rhFactor: randomChoice(['positive', 'negative']),
      quantity: randomInt(1, 10), // number of units
      volume: randomInt(200, 2000), // in milliliters
      urgency: urgency,
      requestDate: randomDate('2024-01-01', '2024-12-31'),
      requiredBy: urgency === 'critical' ? 
        new Date(new Date().getTime() + randomInt(1, 4) * 60 * 60 * 1000) : // 1-4 hours
        urgency === 'emergency' ? 
        new Date(new Date().getTime() + randomInt(4, 24) * 60 * 60 * 1000) : // 4-24 hours
        urgency === 'urgent' ? 
        new Date(new Date().getTime() + randomInt(1, 3) * 24 * 60 * 60 * 1000) : // 1-3 days
        new Date(new Date().getTime() + randomInt(3, 7) * 24 * 60 * 60 * 1000), // 3-7 days
      purpose: randomChoice(['surgery', 'transfusion', 'emergency', 'research', 'routine']),
      medicalCondition: randomChoice(['anemia', 'surgery', 'trauma', 'cancer', 'pregnancy', 'cardiac', 'other']),
      specialRequirements: randomChoice([null, 'irradiated', 'washed', 'leukoreduced', 'cmv_negative']),
      status: randomChoice(['pending', 'approved', 'partially_fulfilled', 'fulfilled', 'cancelled', 'expired']),
      assignedCenter: randomChoice(HOSPITAL_NAMES),
      fulfillmentDate: randomDate('2024-01-01', '2024-12-31'),
      fulfillmentNotes: `Request ${randomChoice(['processed', 'delayed', 'expedited', 'partial'])}`,
      cost: randomFloat(500.0, 5000.0),
      insuranceCoverage: randomFloat(0.0, 1.0),
      requestingStaff: {
        name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
        title: randomChoice(['Nurse', 'Doctor', 'Technician', 'Coordinator']),
        phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`
      },
      approvalStaff: {
        name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
        title: randomChoice(['Director', 'Manager', 'Supervisor']),
        approvalDate: randomDate('2024-01-01', '2024-12-31')
      }
    })
  }
  return requests
}

// Generate Emergency Alerts (500 records)
const generateEmergencyAlerts = () => {
  const alerts = []
  for (let i = 0; i < 500; i++) {
    const severity = randomChoice(['low', 'medium', 'high', 'critical'])
    alerts.push({
      id: `ALERT_${String(i + 1).padStart(5, '0')}`,
      alertCode: `ALT-${randomInt(1000, 9999)}`,
      type: randomChoice(['shortage', 'contamination', 'equipment_failure', 'natural_disaster', 'accident', 'outbreak']),
      severity: severity,
      title: `${severity.toUpperCase()}: ${randomChoice(['Blood shortage', 'Equipment failure', 'Contamination risk', 'Emergency situation'])}`,
      description: `Emergency alert regarding ${randomChoice(['blood supply', 'equipment', 'safety', 'capacity'])} at ${randomChoice(HOSPITAL_NAMES)}`,
      location: {
        center: randomChoice(HOSPITAL_NAMES),
        city: randomChoice(CITIES),
        coordinates: {
          latitude: randomFloat(20.0, 50.0),
          longitude: randomFloat(100.0, 140.0)
        }
      },
      affectedBloodTypes: randomChoice(BLOOD_TYPES, randomInt(1, 4)),
      estimatedImpact: randomChoice(['minimal', 'moderate', 'significant', 'severe']),
      reportedBy: {
        name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
        role: randomChoice(['Technician', 'Nurse', 'Manager', 'Director', 'Staff']),
        phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`
      },
      reportedDate: randomDate('2024-01-01', '2024-12-31'),
      status: randomChoice(['active', 'investigating', 'resolved', 'closed']),
      resolutionDate: randomDate('2024-01-01', '2024-12-31'),
      responseTime: randomInt(5, 120), // in minutes
      actionsTaken: randomChoice([
        'Contacted backup suppliers',
        'Activated emergency protocol',
        'Notified all centers',
        'Dispatched emergency team',
        'Implemented contingency plan'
      ], randomInt(1, 3)),
      followUpRequired: randomChoice([true, false]),
      followUpDate: randomDate('2024-01-01', '2025-01-01'),
      affectedPatients: randomInt(0, 50),
      estimatedDuration: randomInt(1, 72), // in hours
      costImpact: randomFloat(0.0, 10000.0),
      lessonsLearned: `Emergency ${randomChoice(['handled well', 'needs improvement', 'critical gaps identified'])}`,
      preventionMeasures: randomChoice([
        'Regular maintenance schedule',
        'Additional training required',
        'Protocol updates needed',
        'Equipment replacement planned'
      ], randomInt(1, 2))
    })
  }
  return alerts
}

// Generate Staff Records (500 records)
const generateStaffRecords = () => {
  const staff = []
  const positions = ['Phlebotomist', 'Nurse', 'Doctor', 'Technician', 'Coordinator', 'Manager', 'Director', 'Administrator', 'Lab Technician', 'Quality Controller']
  
  for (let i = 0; i < 500; i++) {
    staff.push({
      id: `STAFF_${String(i + 1).padStart(4, '0')}`,
      employeeId: `EMP${randomInt(10000, 99999)}`,
      name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
      position: randomChoice(positions),
      department: randomChoice(['Collection', 'Testing', 'Storage', 'Distribution', 'Administration', 'Quality Control']),
      centerId: `CENTER_${String(randomInt(1, 100)).padStart(4, '0')}`,
      centerName: randomChoice(HOSPITAL_NAMES),
      contact: {
        phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`,
        email: `staff${randomInt(1, 999)}@hospital.com`,
        address: `${randomChoice(CITIES)}${randomInt(1, 999)}号`
      },
      hireDate: randomDate('2015-01-01', '2024-01-01'),
      certification: randomChoice(['Phlebotomy', 'Nursing', 'Medical', 'Lab Tech', 'Management']),
      licenseNumber: `LIC${randomInt(100000, 999999)}`,
      experience: randomInt(1, 25), // in years
      specialization: randomChoice(['Blood Collection', 'Donor Screening', 'Blood Testing', 'Quality Control', 'Emergency Response']),
      trainingCompleted: randomChoice(['Basic', 'Advanced', 'Specialized', 'Expert']),
      status: randomChoice(['active', 'on_leave', 'training', 'inactive']),
      availability: randomChoice(['full_time', 'part_time', 'on_call', 'flexible']),
      skills: randomChoice(['Donor Management', 'Blood Collection', 'Emergency Response', 'Quality Assurance', 'Data Management'], randomInt(2, 4)),
      performance: {
        rating: randomFloat(3.0, 5.0),
        collectionsPerMonth: randomInt(10, 200),
        errorRate: randomFloat(0.0, 0.05),
        patientSatisfaction: randomFloat(3.5, 5.0)
      },
      lastTrainingDate: randomDate('2023-01-01', '2024-12-31'),
      nextTrainingDate: randomDate('2024-01-01', '2025-12-31'),
      emergencyContact: {
        name: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
        relationship: randomChoice(['spouse', 'parent', 'sibling', 'friend']),
        phone: `1${randomInt(3, 9)}${randomInt(100000000, 999999999)}`
      }
    })
  }
  return staff
}

// Generate Campaigns (200 records)
const generateCampaigns = () => {
  const campaigns = []
  const campaignTypes = ['blood_drive', 'awareness', 'emergency', 'regular', 'special']
  
  for (let i = 0; i < 200; i++) {
    const startDate = randomDate('2024-01-01', '2024-12-31')
    const endDate = new Date(startDate.getTime() + randomInt(1, 30) * 24 * 60 * 60 * 1000)
    
    campaigns.push({
      id: `CAMPAIGN_${String(i + 1).padStart(4, '0')}`,
      name: `${randomChoice(['春季', '夏季', '秋季', '冬季'])}${randomChoice(['献血', '爱心', '生命', '希望'])}${randomChoice(['活动', '行动', '计划', '运动'])}`,
      type: randomChoice(campaignTypes),
      organizer: randomChoice(HOSPITAL_NAMES),
      location: {
        venue: randomChoice(['医院广场', '社区中心', '学校', '商场', '办公楼']),
        address: `${randomChoice(CITIES)}${randomInt(1, 999)}号`,
        city: randomChoice(CITIES)
      },
      dates: {
        startDate: startDate,
        endDate: endDate,
        duration: Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24))
      },
      target: {
        donors: randomInt(50, 500),
        units: randomInt(100, 1000),
        bloodTypes: randomChoice(BLOOD_TYPES, randomInt(1, 8))
      },
      actual: {
        donors: randomInt(20, 600),
        units: randomInt(50, 1200),
        bloodTypesCollected: randomChoice(BLOOD_TYPES, randomInt(1, 8))
      },
      status: randomChoice(['planned', 'active', 'completed', 'cancelled']),
      budget: randomFloat(1000.0, 50000.0),
      actualCost: randomFloat(800.0, 55000.0),
      marketingChannels: randomChoice(['social_media', 'radio', 'tv', 'newspaper', 'flyers'], randomInt(1, 3)),
      staffAssigned: randomInt(2, 20),
      volunteers: randomInt(5, 50),
      equipment: randomChoice(['mobile_units', 'tents', 'chairs', 'tables', 'signage'], randomInt(2, 5)),
      successMetrics: {
        donorSatisfaction: randomFloat(3.0, 5.0),
        mediaCoverage: randomInt(0, 50),
        socialMediaReach: randomInt(1000, 100000),
        newDonorsAcquired: randomInt(10, 200)
      },
      challenges: randomChoice([
        'Weather conditions',
        'Low turnout',
        'Equipment issues',
        'Staff shortage',
        'Marketing limitations'
      ], randomInt(0, 2)),
      lessons: `Campaign ${randomChoice(['successful', 'moderate', 'needs improvement'])} with ${randomChoice(['good', 'excellent', 'poor'])} planning`,
      recommendations: `${randomChoice(['Increase', 'Maintain', 'Reduce'])} ${randomChoice(['marketing', 'staff', 'budget', 'duration'])} for next campaign`
    })
  }
  return campaigns
}

// Generate Quality Control Records (1000 records)
const generateQualityControl = () => {
  const qc = []
  for (let i = 0; i < 1000; i++) {
    qc.push({
      id: `QC_${String(i + 1).padStart(5, '0')}`,
      batchId: `BATCH_${randomInt(10000, 99999)}`,
      testDate: randomDate('2024-01-01', '2024-12-31'),
      testType: randomChoice(['routine', 'spot', 'investigation', 'validation']),
      testedBy: `STAFF_${String(randomInt(1, 500)).padStart(4, '0')}`,
      bloodType: randomChoice(BLOOD_TYPES),
      unitId: `UNIT_${randomInt(100000, 999999)}`,
      tests: {
        hiv: randomChoice(['negative', 'positive', 'invalid']),
        hepatitis_b: randomChoice(['negative', 'positive', 'invalid']),
        hepatitis_c: randomChoice(['negative', 'positive', 'invalid']),
        syphilis: randomChoice(['negative', 'positive', 'invalid']),
        malaria: randomChoice(['negative', 'positive', 'invalid']),
        htlv: randomChoice(['negative', 'positive', 'invalid']),
        cmv: randomChoice(['negative', 'positive', 'invalid']),
        blood_group: randomChoice(['confirmed', 'discrepancy']),
        rh_factor: randomChoice(['confirmed', 'discrepancy'])
      },
      results: {
        overall: randomChoice(['pass', 'fail', 'repeat']),
        issues: randomChoice([null, 'reactive', 'discrepancy', 'equipment_error', 'sample_issue']),
        action: randomChoice(['release', 'quarantine', 'discard', 'retest']),
        finalDecision: randomChoice(['approved', 'rejected', 'pending'])
      },
      equipment: {
        analyzerId: `EQ_${randomInt(100, 999)}`,
        calibrationDate: randomDate('2024-01-01', '2024-12-31'),
        maintenanceStatus: randomChoice(['current', 'due', 'overdue'])
      },
      reagents: {
        lotNumber: `LOT_${randomInt(10000, 99999)}`,
        expiryDate: randomDate('2024-06-01', '2025-12-31'),
        storageCondition: randomChoice(['optimal', 'acceptable', 'critical'])
      },
      qualityScore: randomFloat(0.0, 100.0),
      comments: `QC ${randomChoice(['passed', 'failed', 'requires attention'])} with ${randomChoice(['no', 'minor', 'major'])} issues`,
      reviewedBy: `STAFF_${String(randomInt(1, 500)).padStart(4, '0')}`,
      reviewDate: randomDate('2024-01-01', '2024-12-31'),
      certification: {
        certified: randomChoice([true, false]),
        certificateNumber: randomChoice([null, `CERT_${randomInt(100000, 999999)}`]),
        expiryDate: randomDate('2024-12-01', '2025-12-31')
      }
    })
  }
  return qc
}

// Generate System Logs (5000 records)
const generateSystemLogs = () => {
  const logs = []
  const actions = ['login', 'logout', 'create', 'update', 'delete', 'view', 'export', 'import', 'backup', 'restore']
  const modules = ['donors', 'inventory', 'requests', 'staff', 'campaigns', 'quality', 'system', 'reports']
  
  for (let i = 0; i < 5000; i++) {
    logs.push({
      id: `LOG_${String(i + 1).padStart(7, '0')}`,
      timestamp: randomDate('2024-01-01', '2024-12-31'),
      userId: `USER_${String(randomInt(1, 1000)).padStart(4, '0')}`,
      username: randomChoice(FIRST_NAMES) + randomChoice(LAST_NAMES),
      action: randomChoice(actions),
      module: randomChoice(modules),
      details: {
        recordId: randomChoice([null, `DONOR_${randomInt(1, 2000)}`, `REQ_${randomInt(1, 1500)}`, `INV_${randomInt(1, 4000)}`]),
        oldValue: randomChoice([null, 'active', 'pending', 'processed']),
        newValue: randomChoice([null, 'inactive', 'completed', 'approved']),
        changes: randomInt(1, 10)
      },
      ipAddress: `${randomInt(1, 255)}.${randomInt(1, 255)}.${randomInt(1, 255)}.${randomInt(1, 255)}`,
      userAgent: randomChoice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Mozilla/5.0 (X11; Linux x86_64)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1)',
        'Mozilla/5.0 (Android 11; Mobile)'
      ]),
      sessionId: `SESSION_${randomId()}`,
      duration: randomInt(100, 30000), // in milliseconds
      success: randomChoice([true, false]),
      errorMessage: randomChoice([null, 'Connection timeout', 'Invalid credentials', 'Permission denied', 'Record not found']),
      severity: randomChoice(['info', 'warning', 'error', 'critical'])
    })
  }
  return logs
}

// Export all datasets
export const testData = {
  donors: generateDonors(),
  bloodInventory: generateBloodInventory(),
  donationCenters: generateDonationCenters(),
  donationRecords: generateDonationRecords(),
  bloodRequests: generateBloodRequests(),
  emergencyAlerts: generateEmergencyAlerts(),
  staffRecords: generateStaffRecords(),
  campaigns: generateCampaigns(),
  qualityControl: generateQualityControl(),
  systemLogs: generateSystemLogs()
}

// Summary statistics
export const dataSummary = {
  totalRecords: Object.values(testData).reduce((sum, dataset) => sum + dataset.length, 0),
  recordCounts: {
    donors: testData.donors.length,
    bloodInventory: testData.bloodInventory.length,
    donationCenters: testData.donationCenters.length,
    donationRecords: testData.donationRecords.length,
    bloodRequests: testData.bloodRequests.length,
    emergencyAlerts: testData.emergencyAlerts.length,
    staffRecords: testData.staffRecords.length,
    campaigns: testData.campaigns.length,
    qualityControl: testData.qualityControl.length,
    systemLogs: testData.systemLogs.length
  },
  dateRange: {
    start: '2020-01-01',
    end: '2025-12-31'
  },
  citiesCovered: CITIES.length,
  hospitalsCovered: HOSPITAL_NAMES.length,
  bloodTypesSupported: BLOOD_TYPES.length
}

// Utility functions for testing
export const testDataUtils = {
  getRandomDonor: () => randomChoice(testData.donors),
  getRandomBloodUnit: () => randomChoice(testData.bloodInventory),
  getRandomRequest: () => randomChoice(testData.bloodRequests),
  getRandomAlert: () => randomChoice(testData.emergencyAlerts),
  getDonorsByBloodType: (bloodType) => testData.donors.filter(d => d.bloodType === bloodType),
  getInventoryByCenter: (centerName) => testData.bloodInventory.filter(i => i.centerName === centerName),
  getCriticalAlerts: () => testData.emergencyAlerts.filter(a => a.severity === 'critical'),
  getEmergencyRequests: () => testData.bloodRequests.filter(r => r.urgency === 'emergency' || r.urgency === 'critical'),
  getRecentDonations: (days = 30) => {
    const cutoff = new Date()
    cutoff.setDate(cutoff.getDate() - days)
    return testData.donationRecords.filter(d => new Date(d.donationDate) >= cutoff)
  },
  getStaffByCenter: (centerId) => testData.staffRecords.filter(s => s.centerId === centerId),
  getActiveCampaigns: () => testData.campaigns.filter(c => c.status === 'active'),
  getFailedQC: () => testData.qualityControl.filter(qc => qc.results.overall === 'fail'),
  getSystemErrors: () => testData.systemLogs.filter(log => log.severity === 'error' || log.severity === 'critical')
}

console.log('Test Data Generated:', dataSummary)
