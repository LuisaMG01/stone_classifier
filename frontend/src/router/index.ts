import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/classify',
    name: 'classify',
    component: () => import('../views/Predict.vue')
  },
  {
    path: '/classify-rocks',
    name: 'classify-rocks',
    component: () => import('../views/RockPredict.vue')
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('../views/History.vue')
  },
  {
    path: '/rock-history',
    name: 'rock-history',
    component: () => import('../views/RockHistory.vue')
  },
  {
    path: '/model-analysis',
    name: 'model-analysis',
    component: () => import('../views/ModelAnalysis.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 