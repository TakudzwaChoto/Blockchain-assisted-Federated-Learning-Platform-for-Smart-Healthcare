import { defineStore } from 'pinia'

// All translations
const translations = {
  zh: {
          // Navigation
          'nav.admin': '管理控制台',
          'nav.dataImportExport': '数据导入导出',
          'nav.advancedAnalytics': '高级分析预测',
          'nav.dashboardBuilder': '仪表板构建器',
          'nav.userManagement': '用户管理',
          'nav.analytics': '数据分析',
          'nav.systemSettings': '系统设置',
          'nav.personalWorkspace': '个人工作台',
          'nav.donorManagement': '捐赠者管理',
          'nav.transfusionRequests': '输血申请',
          'nav.personalAnalytics': '个人分析',
          'nav.profile': '个人资料',
          'nav.settings': '设置',
          'nav.logout': '退出登录',
          'nav.logoutSuccess': '退出成功',
          'nav.developmentInProgress': '功能开发中',
          
          // Common
          'blood': '血液',
          'domain': '领域',
          'analytics': '分析',
          'platform': '平台',
          'hero.subtitle': '基于人工智能的血液管理与输血安全分析系统',
          'hero.description': '全面的血液库存管理、输血安全分析、捐赠者管理和智能决策支持，帮助医疗机构提高输血安全性和效率',
          'hero.viewPricing': '查看定价方案',
          'hero.learnFeatures': '了解功能特性',
          'footer.description': '专业的血液管理与输血安全分析解决方案',
          
          // Landing Page
          'landing.logoText': '血液领域分析平台',
          'landing.realTimeData': '实时数据',
          'landing.activeDonors': '活跃供血者',
          'landing.todayTransfusions': '今日输血',
          'landing.safetyRate': '安全率',
          'landing.coreFeatures': '核心功能特性',
          'landing.featuresDescription': '全面的血液管理解决方案，覆盖从供血者管理到输血安全的完整流程',
          'landing.whyChoosePlatform': '为什么选择我们的平台？',
          'landing.medicalInstitutions': '医疗机构',
          'landing.donorData': '供血者数据',
          'landing.systemStability': '系统稳定性',
          'landing.technicalSupport': '技术支持',
          'landing.choosePlan': '选择适合您的方案',
          'landing.pricingDescription': '灵活的定价方案，满足不同规模医疗机构的需求',
          'landing.perMonth': '/月',
          'landing.startNow': '立即开始',
          'landing.selectPlan': '选择方案',
          'landing.readyToImprove': '准备提升您的血液管理水平？',
          'landing.registerDescription': '立即注册账户，体验智能血液管理系统的强大功能',
          'landing.freeRegister': '免费注册',
          'landing.hasAccount': '已有账户？登录',
          'landing.productFeatures': '产品功能',
          'landing.coreFunctions': '核心功能',
          'landing.pricingPlans': '定价方案',
          'landing.systemLogin': '系统登录',
          'landing.supportServices': '支持服务',
          'landing.technicalSupport': '技术支持',
          'landing.trainingServices': '培训服务',
          'landing.apiDocumentation': 'API文档',
          'landing.contactUs': '联系我们',
          'landing.phone': '电话: 400-123-4567',
          'landing.email': '邮箱: support@blooddomain.com',
          'landing.address': '地址: 北京市朝阳区',
          'landing.allRights': '保留所有权利.',
          'landing.selectPaymentMethod': '选择支付方式',
          'landing.youWillGet': '您将获得以下服务：',
          
          // Features
          'landing.donorManagement': '供血者管理',
          'landing.donorManagementDesc': '全面的供血者信息管理，包括健康档案、捐赠历史、资格审核等',
          'landing.donorProfileManagement': '供血者档案管理',
          'landing.healthStatusTracking': '健康状态跟踪',
          'landing.donationHistory': '捐赠历史记录',
          'landing.eligibilityReview': '资格审核流程',
          'landing.transfusionManagement': '输血申请管理',
          'landing.transfusionManagementDesc': '标准化的输血申请流程，确保输血安全与合规性',
          'landing.onlineApplication': '在线申请提交',
          'landing.bloodTypeMatching': '血型匹配验证',
          'landing.emergencyProcessing': '紧急申请处理',
          'landing.inventoryManagement': '库存管理',
          'landing.inventoryManagementDesc': '实时血液库存监控，智能预警与调配建议',
          'landing.realTimeMonitoring': '实时库存监控',
          'landing.expiryAlerts': '过期预警提醒',
          'landing.smartAllocation': '智能调配建议',
          'landing.dataAnalysis': '数据分析',
          'landing.dataAnalysisDesc': '基于AI的数据分析，提供决策支持与趋势预测',
          'landing.usageAnalysis': '使用趋势分析',
          'landing.demandForecasting': '需求预测模型',
          'landing.safetyRiskAssessment': '安全风险评估',
          
          // Benefits
          'landing.securityBenefit': '数据安全',
          'landing.securityBenefitDesc': '企业级加密保护，确保数据安全与隐私',
          'landing.efficiencyBenefit': '效率提升',
          'landing.efficiencyBenefitDesc': '自动化流程减少人工操作，提高工作效率',
          'landing.complianceBenefit': '合规保障',
          'landing.complianceBenefitDesc': '符合医疗行业标准，确保合规性',
          
          // Pricing
          'landing.basicPlan': '基础版',
          'landing.basicPlanDesc': '适合小型医疗机构',
          'landing.max50Users': '最多50名用户',
          'landing.basicDonorManagement': '基础供血者管理',
          'landing.inventoryMonitoring': '库存监控',
          'landing.professionalPlan': '专业版',
          'landing.professionalPlanDesc': '适合中型医疗机构',
          'landing.max200Users': '最多200名用户',
          'landing.completeDonorManagement': '完整供血者管理',
          'landing.smartInventoryManagement': '智能库存管理',
          'landing.enterprisePlan': '企业版',
          'landing.enterprisePlanDesc': '适合大型医疗集团',
          'landing.unlimitedUsers': '无限用户',
          'landing.allFeatures': '全功能模块',
          'landing.customDevelopment': '定制化开发',
          
          // Payment
          'payment.selectMethod': '请选择支付方式',
          'payment.cancel': '取消',
          'payment.confirmPay': '确认支付',
          'payment.success': '支付成功！',
          'payment.failed': '支付失败，请重试',
          'payment.selectMethodWarning': '请选择支付方式',
          
          // Payment Methods
          'payment.wechatPay': '微信支付',
          'payment.wechatPayDesc': '使用微信扫码支付',
          'payment.alipay': '支付宝',
          'payment.alipayDesc': '使用支付宝扫码支付',
          'payment.bankTransfer': '银行转账',
          'payment.bankTransferDesc': '使用银行卡或网银支付',
          'payment.paypal': 'PayPal',
          'payment.paypalDesc': '使用PayPal国际支付',
          
          // Pricing Features
          'pricing.standardReports': '标准报表',
          'pricing.emailSupport': '邮件支持',
          'pricing.advancedDataAnalysis': '高级数据分析',
          'pricing.apiInterface': 'API接口',
          'pricing.prioritySupport': '优先技术支持',
          'pricing.dedicatedServer': '专属服务器',
          'pricing.onSiteTraining': '现场培训',
          'prioritySupport': '24/7专属支持',
          
          // Navigation
          'nav.login': '登录',
          'nav.createAccount': '创建账户',
        },
        en: {
          // Navigation
          'nav.admin': 'Admin Console',
          'nav.dataImportExport': 'Data Import/Export',
          'nav.advancedAnalytics': 'Advanced Analytics & Prediction',
          'nav.dashboardBuilder': 'Dashboard Builder',
          'nav.userManagement': 'User Management',
          'nav.analytics': 'Data Analytics',
          'nav.systemSettings': 'System Settings',
          'nav.personalWorkspace': 'Personal Workspace',
          'nav.donorManagement': 'Donor Management',
          'nav.transfusionRequests': 'Transfusion Requests',
          'nav.personalAnalytics': 'Personal Analytics',
          'nav.profile': 'Profile',
          'nav.settings': 'Settings',
          'nav.logout': 'Logout',
          'nav.logoutSuccess': 'Logout successful',
          'nav.developmentInProgress': 'Feature in development',
          
          // Common
          'blood': 'Blood',
          'domain': 'Domain',
          'analytics': 'Analytics',
          'platform': 'Platform',
          'hero.subtitle': 'AI-powered blood management and transfusion safety analysis system',
          'hero.description': 'Comprehensive blood inventory management, transfusion safety analysis, donor management and intelligent decision support for medical institutions to improve transfusion safety and efficiency',
          'hero.viewPricing': 'View Pricing Plans',
          'hero.learnFeatures': 'Learn Features',
          'footer.description': 'Professional blood Management and transfusion safety Analysis solution',
          
          // Landing Page
          'landing.logoText': 'Blood Domain Analytics Platform',
          'landing.realTimeData': 'Real-time Data',
          'landing.activeDonors': 'Active Donors',
          'landing.todayTransfusions': 'Today\'s Transfusions',
          'landing.safetyRate': 'Safety Rate',
          'landing.coreFeatures': 'Core Features',
          'landing.featuresDescription': 'Comprehensive blood management solution covering complete process from donor management to transfusion safety',
          'landing.whyChoosePlatform': 'Why Choose Our Platform?',
          'landing.medicalInstitutions': 'Medical Institutions',
          'landing.donorData': 'Donor Data',
          'landing.systemStability': 'System Stability',
          'landing.technicalSupport': 'Technical Support',
          'landing.choosePlan': 'Choose the Right Plan for You',
          'landing.pricingDescription': 'Flexible pricing plans to meet the needs of different scale medical institutions',
          'landing.perMonth': '/month',
          'landing.startNow': 'Start Now',
          'landing.selectPlan': 'Select Plan',
          'landing.readyToImprove': 'Ready to Enhance Your Blood Management Level?',
          'landing.registerDescription': 'Register an account now and experience the powerful features of our intelligent blood Management System',
          'landing.freeRegister': 'Free Registration',
          'landing.hasAccount': 'Already have an account? Login',
          'landing.productFeatures': 'Product Features',
          'landing.coreFunctions': 'Core Functions',
          'landing.pricingPlans': 'Pricing Plans',
          'landing.systemLogin': 'System Login',
          'landing.supportServices': 'Support Services',
          'landing.technicalSupport': 'Technical Support',
          'landing.trainingServices': 'Training Services',
          'landing.apiDocumentation': 'API Documentation',
          'landing.contactUs': 'Contact Us',
          'landing.phone': 'Phone: 400-123-4567',
          'landing.email': 'Email: support@blooddomain.com',
          'landing.address': 'Address: Chaoyang District, Beijing',
          'landing.allRights': 'All rights reserved.',
          'landing.selectPaymentMethod': 'Select Payment Method',
          'landing.youWillGet': 'You will get the following services:',
          
          // Features
          'landing.donorManagement': 'Donor Management',
          'landing.donorManagementDesc': 'Comprehensive donor information Management including health records, donation history, eligibility review, etc.',
          'landing.donorProfileManagement': 'Donor Profile Management',
          'landing.healthStatusTracking': 'Health Status Tracking',
          'landing.donationHistory': 'Donation History Records',
          'landing.eligibilityReview': 'Eligibility Review Process',
          'landing.transfusionManagement': 'Transfusion Request Management',
          'landing.transfusionManagementDesc': 'Standardized transfusion request process ensuring transfusion safety and compliance',
          'landing.onlineApplication': 'Online Application Submission',
          'landing.bloodTypeMatching': 'Blood Type Matching Verification',
          'landing.emergencyProcessing': 'Emergency Request Processing',
          'landing.inventoryManagement': 'Inventory Management',
          'landing.inventoryManagementDesc': 'Real-time blood inventory monitoring with intelligent alerts and allocation recommendations',
          'landing.realTimeMonitoring': 'Real-time Inventory Monitoring',
          'landing.expiryAlerts': 'Expiry Alert Reminders',
          'landing.smartAllocation': 'Smart Allocation Suggestions',
          'landing.dataAnalysis': 'Data Analysis',
          'landing.dataAnalysisDesc': 'AI-based data analysis providing decision support and trend prediction',
          'landing.usageAnalysis': 'Usage Trend Analysis',
          'landing.demandForecasting': 'Demand Forecasting Model',
          'landing.safetyRiskAssessment': 'Safety Risk Assessment',
          
          // Benefits
          'landing.securityBenefit': 'Data Security',
          'landing.securityBenefitDesc': 'Enterprise-level encryption protection ensuring data security and privacy',
          'landing.efficiencyBenefit': 'Efficiency Improvement',
          'landing.efficiencyBenefitDesc': 'Automated processes reduce manual operations and improve work efficiency',
          'landing.complianceBenefit': 'Compliance Assurance',
          'landing.complianceBenefitDesc': 'Compliant with medical industry standards ensuring regulatory compliance',
          
          // Pricing
          'landing.basicPlan': 'Basic Plan',
          'landing.basicPlanDesc': 'Suitable for small medical institutions',
          'landing.max50Users': 'Up to 50 users',
          'landing.basicDonorManagement': 'Basic Donor Management',
          'landing.inventoryMonitoring': 'Inventory Monitoring',
          'landing.professionalPlan': 'Professional Plan',
          'landing.professionalPlanDesc': 'Suitable for medium-sized medical institutions',
          'landing.max200Users': 'Up to 200 users',
          'landing.completeDonorManagement': 'Complete Donor Management',
          'landing.smartInventoryManagement': 'Smart Inventory Management',
          'landing.enterprisePlan': 'Enterprise Plan',
          'landing.enterprisePlanDesc': 'Suitable for large medical groups',
          'landing.unlimitedUsers': 'Unlimited Users',
          'landing.allFeatures': 'All Feature Modules',
          'landing.customDevelopment': 'Custom Development',
          
          // Payment
          'payment.selectMethod': 'Select Payment Method',
          'payment.cancel': 'Cancel',
          'payment.confirmPay': 'Confirm Payment',
          'payment.success': 'Payment Successful!',
          'payment.failed': 'Payment Failed, Please Retry',
          'payment.selectMethodWarning': 'Please select payment method',
          
          // Payment Methods
          'payment.wechatPay': 'WeChat Pay',
          'payment.wechatPayDesc': 'Pay with WeChat QR code',
          'payment.alipay': 'Alipay',
          'payment.alipayDesc': 'Pay with Alipay QR code',
          'payment.bankTransfer': 'Bank Transfer',
          'payment.bankTransferDesc': 'Pay with bank card or online banking',
          'payment.paypal': 'PayPal',
          'payment.paypalDesc': 'Pay with PayPal international payment',
          
          // Pricing Features
          'pricing.standardReports': 'Standard Reports',
          'pricing.emailSupport': 'Email Support',
          'pricing.advancedDataAnalysis': 'Advanced Data Analysis',
          'pricing.apiInterface': 'API Interface',
          'pricing.prioritySupport': 'Priority Technical Support',
          'pricing.dedicatedServer': 'Dedicated Server',
          'pricing.onSiteTraining': 'On-site Training',
          'prioritySupport': '24/7 Dedicated Support',
          
          // Navigation
          'nav.login': 'Login',
          'nav.createAccount': 'Create Account',
        }
      }
}

export const useLanguageStore = defineStore('language', {
  state: () => ({
    currentLanguage: 'zh', // Default: Chinese
    currentTranslations: {}, // Current language translations
    availableLanguages: [
      { code: 'zh', name: '中文', flag: '🇨🇳' },
      { code: 'en', name: 'English', flag: '🇺🇸' },
      { code: 'ru', name: 'Русский', flag: '🇷🇺' },
      { code: 'fr', name: 'Français', flag: '🇫🇷' }
    ]
  }),

  getters: {
    getCurrentLanguage: (state) => state.availableLanguages.find(lang => lang.code === state.currentLanguage),
    translations: (state) => state.currentTranslations
  },

  actions: {
    setLanguage(languageCode) {
      this.currentLanguage = languageCode
      localStorage.setItem('language', languageCode)
      this.loadTranslations(languageCode)
    },

    loadTranslations(languageCode) {
      // Load translations based on language code
      this.currentTranslations = translations[languageCode] || translations.zh
    },

    initializeLanguage() {
      const savedLanguage = localStorage.getItem('language') || 'zh'
      this.currentLanguage = savedLanguage
      this.loadTranslations(savedLanguage)
    }
  }
})
