import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/portfolio', name: 'portfolio', component: () => import('@/views/PortfolioView.vue') },
  { path: '/portfolio/:slug', name: 'work', component: () => import('@/views/WorkView.vue'), props: true },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
