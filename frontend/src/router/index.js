import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
import HomeView from '@/views/HomeView.vue';
import ClaimsView from '@/views/ClaimsView.vue';
import LoginView from '@/components/LoginView.vue';
import SignupView from '@/components/SignupView.vue';
import RequestPasswordReset from '@/components/RequestPasswordReset.vue';
import ResetPassword from '@/components/ResetPassword.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    alias: ['/home', '/new'],
    component: HomeView,
  },
  {
    path: '/claims/:id?',
    name: 'claims',
    component: ClaimsView,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/auth/login',
    name: 'login',
    components: {
      default: HomeView,
      modal: LoginView,
    },
    meta: { universalModal: true },
  },
  {
    path: '/auth/signup',
    name: 'signup',
    components: {
      default: HomeView,
      modal: SignupView,
    },
    meta: { universalModal: true },
  },
  {
    path: '/auth/forgot-password',
    name: 'forgotPassword',
    components: {
      default: HomeView,
      modal: RequestPasswordReset,
    },
    meta: { universalModal: true },
  },
  {
    path: '/reset-password',
    name: 'resetPassword',
    components: {
      default: HomeView,
      modal: ResetPassword,
    },
    meta: { universalModal: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard for Protected Routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else {
    next();
  }
});

export default router;