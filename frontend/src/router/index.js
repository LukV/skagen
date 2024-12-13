import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import DesignView from '@/views/DesignView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/design', name: 'design', component: DesignView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router