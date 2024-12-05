// store/index.js
import { createStore } from 'vuex';
import auth from './modules/auth';
import user from './modules/user';
import notifications from './modules/notifications';

const store = createStore({
  modules: {
    auth,
    user,
    notifications,
  },
});

export default store;
