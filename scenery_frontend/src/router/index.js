import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  { path: '/', component: () => import('../views/Welcome.vue') },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register', component: () => import('../views/Register.vue') },
  {
    path: '/tourist',
    component: () => import('../layouts/TouristLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: 'home', component: () => import('../views/tourist/Home.vue') },
      { path: 'spots', component: () => import('../views/tourist/Spots.vue') },
      { path: 'routes', component: () => import('../views/tourist/Routes.vue') },
      { path: 'favorites', component: () => import('../views/tourist/Favorites.vue') },
      { path: 'feedback', component: () => import('../views/tourist/Feedback.vue') },
      { path: 'faqs', component: () => import('../views/tourist/FAQs.vue') },
      { path: 'chat', component: () => import('../views/tourist/Chat.vue') },
      { path: 'mine', component: () => import('../views/tourist/Mine.vue') }
    ]
  },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: 'dashboard', component: () => import('../views/admin/Dashboard.vue') },
      { path: 'users', component: () => import('../views/admin/Users.vue') },
      { path: 'spots', component: () => import('../views/admin/Spots.vue') },
      { path: 'routes', component: () => import('../views/admin/Routes.vue') },
      { path: 'faqs', component: () => import('../views/admin/FAQs.vue') },
      { path: 'feedbacks', component: () => import('../views/admin/Feedbacks.vue') },
      { path: 'chats', component: () => import('../views/admin/Chats.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const store = useUserStore()
  if (to.meta.requiresAuth && !store.isLogin) return '/login'
  if (to.meta.requiresAdmin && !store.isAdmin) return '/tourist/home'
  if ((to.path === '/login' || to.path === '/register') && store.isLogin) {
    return store.isAdmin ? '/admin/dashboard' : '/tourist/home'
  }
})

export default router
