// store/modules/user.js
import apiClient from '@/apiClient';

const state = {
  user: null,
};

const mutations = {
  SET_USER(state, user) {
    state.user = user;
  },
  CLEAR_USER(state) {
    state.user = null;
  },
};

const actions = {
  async fetchUser({ commit }) {
    try {
      const response = await apiClient.get('/users/me');
      commit('SET_USER', response.data);
    } catch (error) {
      commit('CLEAR_USER');
      throw error;
    }
  },
};

const getters = {
  getUser: (state) => state.user,
  userIconUrl: (state) => {
    if (state.user && state.user.icon) {
      return `${process.env.VUE_APP_API_BASE_URL}/icons/${state.user.icon}`;
    }
    return null;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
