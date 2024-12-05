// store/modules/notifications.js

const state = {
    notifications: [],
  };
  
  const mutations = {
    ADD_NOTIFICATION(state, notification) {
      state.notifications.push({ id: Date.now(), ...notification });
    },
    REMOVE_NOTIFICATION(state, notificationId) {
      state.notifications = state.notifications.filter(
        (n) => n.id !== notificationId
      );
    },
  };
  
  const actions = {
    addNotification({ commit }, notification) {
      const id = Date.now();
      const autoDismissTimeout = 12000;
  
      commit('ADD_NOTIFICATION', { id, ...notification });
  
      setTimeout(() => {
        commit('REMOVE_NOTIFICATION', id);
      }, autoDismissTimeout);
    },
    removeNotification({ commit }, notificationId) {
      commit('REMOVE_NOTIFICATION', notificationId);
    },
  };
  
  const getters = {
    allNotifications: (state) => state.notifications,
  };
  
  export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
  };
  