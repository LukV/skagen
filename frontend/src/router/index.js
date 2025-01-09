import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../components/LoginView.vue';
import SignupView from '../components/SignupView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
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