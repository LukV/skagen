import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import DesignView from '@/views/DesignView.vue';
import LoginView from '@/views/LoginView.vue';
import SignUpView from '@/views/SignUpView.vue';
import ForgotPasswordView from '@/views/ForgotPasswordView.vue';
import MobileMenu from '@/views/MobileMenu.vue';
import ClaimView from '@/views/ClaimView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    components: {
      main: HomeView
    },
    meta: { 
      showShare: false, 
      showSearch: false, 
      showMore: false 
    },
    alias: '/home'
  },
  {
    path: '/claim',
    name: 'claim',
    components: {
      main: ClaimView
    },
    meta: { 
      showShare: true, 
      showSearch: true, 
      showMore: true 
    }
  },
  {
    path: '/design',
    name: 'design',
    components: {
      main: DesignView
    }
  },
  // Modal-specific routes
  {
    path: '/auth/login',
    name: 'login',
    components: {
      modal: LoginView
    },
    meta: { universalModal: true }
  },
  {
    path: '/auth/signup',
    name: 'signUp',
    components: {
      modal: SignUpView
    },
    meta: { universalModal: true }
  },
  {
    path: '/auth/forget-password',
    name: 'forgotPassword',
    components: {
      modal: ForgotPasswordView
    },
    meta: { universalModal: true }
  },
  {
    path: '/menu',
    name: 'mobileMenu',
    components: {
      modal: MobileMenu
    },
    meta: { universalModal: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;