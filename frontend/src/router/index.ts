import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('@/pages/LandingPage.vue'), meta: { guest: true } },
    { path: '/login', component: () => import('@/pages/LoginPage.vue'), meta: { guest: true } },
    {
      path: '/app',
      component: () => import('@/layouts/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/app/match' },
        { path: 'match', component: () => import('@/pages/MatchPage.vue') },
        { path: 'chat', component: () => import('@/pages/ChatListPage.vue') },
        { path: 'chat/:id', component: () => import('@/pages/ChatDetailPage.vue') },
        { path: 'posts', component: () => import('@/pages/PostsPage.vue') },
        { path: 'profile', component: () => import('@/pages/ProfilePage.vue') },
        { path: 'questionnaire', component: () => import('@/pages/QuestionnairePage.vue') },
        { path: 'history', component: () => import('@/pages/HistoryPage.vue') },
      ],
    },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) return '/login'
  if (to.meta.guest && auth.isLoggedIn && to.path !== '/') return '/app/match'
})

export default router
