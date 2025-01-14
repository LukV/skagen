import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import { registerPlugins } from '@/plugins';

// Configure Axios
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;
axios.defaults.headers.common['Accept'] = 'application/json';

// Restore authentication state before app initialization
store.dispatch('restoreAuth').then(() => {
  const app = createApp(App);

  app.use(store);
  app.use(router);
  registerPlugins(app);

  app.mount('#app');
}).catch((error) => {
  console.error('Failed to restore authentication:', error);
});