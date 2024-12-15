import { createStore } from 'vuex';

export default createStore({
  state: {
    isLoggedIn: false,
    userName: null,
    claim: localStorage.getItem('latestClaim') || ''
  },
  mutations: {
    LOGIN(state, payload) {
      state.isLoggedIn = true;
      state.userName = payload?.userName || 'John Doe';
      state.universalModalView = null;
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.userName = null;
    },
    SET_CLAIM(state, payload) {
      state.claim = payload;
      localStorage.setItem('latestClaim', payload);
    },
  },
  actions: {
    login({ commit }, userName) {
      commit('LOGIN', { userName });
    },
    logout({ commit }) {
      commit('LOGOUT');
    },
    setClaim({ commit }, claim) {
      commit('SET_CLAIM', claim); // Save the claim to the store
    },
  },
});