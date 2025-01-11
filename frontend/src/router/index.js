import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import ClaimsView from '@/views/ClaimsView.vue';
import LoginView from '@/components/LoginView.vue';
import SignupView from '@/components/SignupView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    alias: '/home',
    component: HomeView,
  },
  {
    path: '/claims/:id?',
    name: 'claims',
    component: ClaimsView,
    props: true,
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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;