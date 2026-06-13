import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/host-records',
      name: 'host-records',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/HostRecords.vue'),
    },
    {
      path: '/dhcp-ranges',
      name: 'dhcp-ranges',
      component: () => import('../views/DhcpRanges.vue'),
    },
  ],
})



export default router
