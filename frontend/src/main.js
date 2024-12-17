import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles/globals.css'
import router from './router'
import store from './store'
import axios from 'axios';

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;

store.dispatch('restoreAuth').then(() => {
  const app = createApp(App);
  app.use(store);
  app.use(router);
  app.mount('#app');
});