import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

// Layout Components
import AppLayout from '../components/AppLayout.vue'
import LoginView from '../components/LoginView.vue'
import LandingPage from '../views/LandingPage.vue'
import AdvancedHomeView from '../views/AdvancedHomeView.vue'

// Admin Views
import AdminDashboard from '../views/AdminDashboard.vue'
import DataImportExport from '../views/DataImportExport.vue'
import AdvancedAnalytics from '../views/AdvancedAnalytics.vue'

// User Views
import UserDashboard from '../views/UserDashboard.vue'

// Doctor Views
import DoctorDashboard from '../views/DoctorDashboard.vue'
import DoctorDonorManagement from '../views/DoctorDonorManagement.vue'
import DoctorTransfusionRequests from '../views/DoctorTransfusionRequests.vue'
import DoctorPersonalAnalytics from '../views/DoctorPersonalAnalytics.vue'

// Simple test component
const TestComponent = {
  template: '<div><h1>Test Component Works!</h1><p>This is a simple test component.</p></div>'
}

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'AdvancedHome',
    component: AdvancedHomeView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/admin',
    component: AppLayout,
    meta: { requiresAuth: true, roles: ['admin'] },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'data-import-export',
        name: 'DataImportExport',
        component: DataImportExport,
        meta: { requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'advanced-analytics',
        name: 'AdvancedAnalytics',
        component: AdvancedAnalytics,
        meta: { requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'dashboard-builder',
        name: 'DashboardBuilder',
        component: () => import('../views/DashboardBuilder.vue'),
        meta: { requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../views/AdminUserManagement.vue'),
        meta: { requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'analytics',
        name: 'AdminAnalytics',
        component: () => import('../views/AdminAnalytics.vue'),
        meta: { requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'system',
        name: 'AdminSystem',
        component: () => import('../views/AdminSystemSettings.vue'),
        meta: { requiresAuth: true, roles: ['admin'] }
      }
    ]
  },
  {
    path: '/user',
    component: AppLayout,
    meta: { requiresAuth: true, roles: ['user'] },
    children: [
      {
        path: '',
        redirect: '/user/dashboard'
      },
      {
        path: 'dashboard',
        name: 'UserDashboard',
        component: UserDashboard,
        meta: { requiresAuth: true, roles: ['user'] }
      },
      {
        path: 'donors',
        name: 'UserDonors',
        component: () => import('../views/UserDonorManagement.vue'),
        meta: { requiresAuth: true, roles: ['user'] }
      },
      {
        path: 'requests',
        name: 'UserRequests',
        component: () => import('../views/UserRequestManagement.vue'),
        meta: { requiresAuth: true, roles: ['user'] }
      },
      {
        path: 'analytics',
        name: 'UserAnalytics',
        component: () => import('../views/UserPersonalAnalytics.vue'),
        meta: { requiresAuth: true, roles: ['user'] }
      }
    ]
  },
  {
    path: '/doctor',
    component: AppLayout,
    meta: { requiresAuth: true, roles: ['doctor'] },
    children: [
      {
        path: '',
        redirect: '/doctor/dashboard'
      },
      {
        path: 'dashboard',
        name: 'DoctorDashboard',
        component: DoctorDashboard,
        meta: { requiresAuth: true, roles: ['doctor'] }
      },
      {
        path: 'donors',
        name: 'DoctorDonors',
        component: DoctorDonorManagement,
        meta: { requiresAuth: true, roles: ['doctor'] }
      },
      {
        path: 'requests',
        name: 'DoctorRequests',
        component: DoctorTransfusionRequests,
        meta: { requiresAuth: true, roles: ['doctor'] }
      },
      {
        path: 'analytics',
        name: 'DoctorAnalytics',
        component: DoctorPersonalAnalytics,
        meta: { requiresAuth: true, roles: ['doctor'] }
      }
    ]
  },
  {
    path: '/government',
    component: AppLayout,
    meta: { requiresAuth: true, roles: ['government'] },
    children: [
      {
        path: '',
        redirect: '/government/dashboard'
      },
      {
        path: 'dashboard',
        name: 'GovernmentDashboard',
        component: () => import('../views/GovernmentDashboard.vue'),
        meta: { requiresAuth: true, roles: ['government'] }
      },
      {
        path: 'oversight',
        name: 'GovernmentOversight',
        component: () => import('../views/GovernmentOversight.vue'),
        meta: { requiresAuth: true, roles: ['government'] }
      },
      {
        path: 'policy',
        name: 'GovernmentPolicy',
        component: () => import('../views/GovernmentPolicy.vue'),
        meta: { requiresAuth: true, roles: ['government'] }
      },
      {
        path: 'emergency',
        name: 'GovernmentEmergency',
        component: () => import('../views/GovernmentEmergency.vue'),
        meta: { requiresAuth: true, roles: ['government'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Load auth state
  authStore.load()
  
  // Allow access to landing page and login without authentication
  if (to.path === '/' || to.path === '/login') {
    // If authenticated and trying to access login, redirect to appropriate dashboard
    if (to.path === '/login' && authStore.isAuthenticated) {
      if (authStore.isAdmin) {
        next('/admin/dashboard')
      } else if (authStore.isDoctor) {
        next('/doctor/dashboard')
      } else if (authStore.isUser) {
        next('/user/dashboard')
      } else if (authStore.isGovernment) {
        next('/government/dashboard')
      } else {
        next('/login')
      }
      return
    }
    next()
    return
  }
  
  // Check if authentication is required
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // Check role-based access
  if (to.meta.roles && to.meta.roles.length > 0) {
    const hasRequiredRole = to.meta.roles.some(role => {
      if (role === 'admin') return authStore.isAdmin
      if (role === 'doctor') return authStore.isDoctor
      if (role === 'user') return authStore.isUser
      if (role === 'government') return authStore.isGovernment
      return false
    })
    
    if (!hasRequiredRole) {
      // Redirect to appropriate dashboard based on user role
      if (authStore.isAdmin) {
        next('/admin/dashboard')
      } else if (authStore.isDoctor) {
        next('/doctor/dashboard')
      } else if (authStore.isUser) {
        next('/user/dashboard')
      } else if (authStore.isGovernment) {
        next('/government/dashboard')
      } else {
        next('/login')
      }
      return
    }
  }
  
  next()
})

export default router
