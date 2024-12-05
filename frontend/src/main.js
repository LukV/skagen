import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify'
import './assets/styles/variables.css';
import './assets/styles/globals.css';

We zijn tot aan de store geraakt. Next up is App.vue, components en assets

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;

store.dispatch('restoreAuth').then(() => {
    const app = createApp(App);
    app.use(router);
    app.use(store);
    app.use(vuetify);
    app.mount('#app');
  });


